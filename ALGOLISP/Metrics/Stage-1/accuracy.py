import importlib
from evaluation import bleu, executor, code_lisp
import json
import numpy as np
import time
from tqdm import tqdm
import argparse
import logging


def flatten(l):
    if(not isinstance(l,list)):
        return [l]
    nl = ['('] + sum((flatten(i) for i in l),[]) + [')']
    return nl

def process(data):
    inpp = []
    sch = []
    outp = []
    args = []
    ios = []

    for i in data:
        take = True
        for j in i['text']:
            if(len(j.split())>1):
                take = True  #It was false mrinal setted it true
                break
        if take:
            inpp.append(i['text'])
            li = []
            for j in i['args']:
                li.append((j,i['args'][j]))
            ios += [i['tests']]
            sch.append(li)
            outp.append(flatten(i['short_tree']))
                        
        else:
            print(i['text'])

    return inpp, sch, outp, args, ios


def is_same_code(res, example):
    correct = res == example
    return correct

def compute_bleu(tar, res):
    try:
        score = bleu.compute_bleu([tar], [res])
        return score.item(0)
    except ZeroDivisionError:
        return 0.0

def get_stats_from_code(res, tar, ios, args, statement, executor_):
    if len(ios) == 0:
        return []
    res1 = res + [")"]*10
    stats = executor.evaluate_code(res1, args, ios, executor_)
    stats['exact-code-match'] = is_same_code(res, tar)
    stats['correct-program'] = int(stats['tests-executed']
                                   == stats['tests-passed'])
    stats['bleu'] = compute_bleu(tar, res)
    stats['example'] = tar
    stats['res'] = res
    stats["statement"] = statement
    return stats

def run_inference(ress, inps, tars, ios, args):
    stats = []
    for i in tqdm(range(len(inps))):
        executor_ = executor.get_executor()
        sstats = get_stats_from_code(
            ress[i], tars[i], ios[i], args[i], inps[i], executor_)
        stats += [sstats]
    return stats

def compute_metrics(all_stats):
    tests_num = 0
    programs_num = 0
    bleu_acc = 0.0
    correct_program_acc = 0
    # Almost correct programs are those that were executed on more than one test and passed at least 50% tests.
    almost_correct_program_acc = 0
    exact_code_match_acc = 0
    syntax_error_acc = 0
    runtime_exception_acc = 0
    other_exception_acc = 0
    for stats in all_stats:
        tests_num += stats['tests-executed']
        programs_num += 1
        bleu_acc += stats['bleu']
        # Almost correct
        # if stats["exact-code-match"]:
        #   almost_correct_program_acc += 1
        if (stats['correct-program'] != 0 or stats['tests-executed'] > 1 and stats['tests-passed']/stats['tests-executed'] >= 0.5):
            almost_correct_program_acc += 1
        # -------------
        # Correct
        # if stats["exact-code-match"]:
        #     correct_program_acc += 1
        # else:
        correct_program_acc += stats['correct-program']
        # ----------------
        exact_code_match_acc += stats['exact-code-match']
        syntax_error_acc += stats['syntax-error']
        runtime_exception_acc += stats['runtime-exception']
        other_exception_acc += len(stats['exceptions'])

    return {'bleu': (bleu_acc/programs_num) if programs_num else 0.0,
            'accuracy': (correct_program_acc/programs_num) if programs_num else 0.0,
            '50p_accuracy': (almost_correct_program_acc/programs_num) if programs_num else 0.0,
            'exact_match_accuracy': (exact_code_match_acc/programs_num) if programs_num else 0.0,
            'syntax_error_freq': (syntax_error_acc/tests_num) if tests_num else 0.0,
            'runtime_exception_freq': (runtime_exception_acc/tests_num) if tests_num else 0.0,
            'other_exception_freq': (other_exception_acc/tests_num) if tests_num else 0.0,
            'programs_num': programs_num,
            'tests_num': tests_num,
            'correct_program_num': correct_program_acc,
            'almost_correct_program_num': almost_correct_program_acc,
            'exact_code_match_num': exact_code_match_acc,
            }


def read(out_file,outp,data):
    results = []
    with open(out_file, "r") as f:
        for line in f.readlines():
            x = line.strip().split()
            for i in range(len(x)):
                if(x[i] =="["):
                    x[i] = "("
                elif(x[i]=="]"):
                    x[i] = ")"
            results.append(x)
            

    node_dict={}
    for i in data:
        if i['nodes'][0] not in node_dict.keys():
            node_dict[i['nodes'][0]]=list()

    for i in range(len(data)):
        node_dict[data[i]['nodes'][0]].append(i)
        
    try:
        for i in node_dict['cf_229_abbreviation']:
            for j in outp[i]:
                if(len(j.split())>1):
                    results[i]=outp[i]
    except KeyError:
        pass

    return results

def read_data(inp_file):
    with open(inp_file,'r') as f:
        data = [json.loads(line) for line in f.readlines()]

    return data


def main():

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--src", required=False,
                        help="Path to the original test(.jsonl file) file.")
    parser.add_argument("--tgt", required=False,
                        help="Path to the model output test(.txt file) file.")
    args = parser.parse_args()

    # args.tgt = "metaset3.test.jsonl"
    # args.src = "t2_algolisp_3_12L.txt"
    
    data=read_data(args.tgt)
    
    inpp, sch, outp, arg, ios=process(data)
    
    results =read(args.src,outp,data)
    ll = len(results)
    
    all_stats = run_inference(results[:ll], inpp[:ll], outp[:ll], ios[:ll], sch[:ll])
    metrics = compute_metrics(all_stats)
    print(metrics)


if __name__ == "__main__":
  main()