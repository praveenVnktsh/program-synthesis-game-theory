
import json
f = open('I:/datasets/naps.trainB.1.0.jsonl','r')
textsFile = open('I:/datasets/trainBInput1.txt', 'w')
codeFile = open('I:/datasets/trainBCode1.txt', 'w')
testsFile = open('I:/datasets/trainBTests1.txt', 'w')

errorFile = open('errorFile.txt','w')
index = 0

def joinFuncText(sequence):
    joined = ''
    i = 0
    while i < len(sequence):
        if sequence[i] == '_' and sequence[i+1] == '_':
            joined += sequence[i]
            i += 1
            if i == len(sequence):
                return joined, "ISSUE"
            joined += sequence[i]
            i += 1
            if i == len(sequence):
                return joined, "ISSUE"
            joined += sequence[i]
            i += 1
            if i == len(sequence):
                return joined, "ISSUE"
            joined += sequence[i]
            i += 1
            if i == len(sequence):
                return joined, "ISSUE"
            joined += sequence[i]
            i += 1
            if i == len(sequence):
                return joined, "ISSUE"

            if sequence[i] == '.':
                joined += sequence[i]
                i+=1
            else: 
                joined += ' '
            continue
        joined += sequence[i] + ' '
        i += 1
    return joined, "OK"

def joinFuncCode(sequence):
    joined = ''
    i = 0
    while i < len(sequence):
        if sequence[i] == '_' and sequence[i+1] == '_':
            joined += sequence[i]
            i += 1
            joined += sequence[i]
            i += 1
            joined += sequence[i]
            i += 1
            joined += sequence[i]
            i += 1
            joined += sequence[i]
            i += 1
            joined += '. '
            # if sequence[i] == '_':
            #     joined += '.' 
            #     continue
            # else: 
            #     joined += ' '
            continue
        joined += sequence[i] + ' '
        i += 1
    return joined

lineCount = 1
while True:
    line = f.readline()
    lineCount += 1
    if len(line) == 0:
        break
    
    dictionary = json.loads(line)
    # print(dictionary.keys())
    sequence = ' '.join(dictionary['code_sequence'])
    
    text, status = joinFuncText(dictionary['text'])
    if status != 'OK':
        errorFile.write(line)
    # solnid = dictionary['solution_id']
    # problemid = dictionary['problem_id']
    # returntype = dictionary['return_type']
    # url = dictionary['url']
    # codetree = dictionary['code_tree']
    tests = dictionary['tests']

    textsFile.write(text + '\n')
    codeFile.write(sequence + '\n')
    testsFile.write(text + '\n')
    # break
    index += 1
    if index%100 == 0:
        print(index)

errorFile.close()
codeFile.close()
testsFile.close()
textsFile.close()
f.close()