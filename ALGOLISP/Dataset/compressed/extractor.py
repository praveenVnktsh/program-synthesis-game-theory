import json
f = open('metaset3.test.jsonl','r')
o = open('metadata_problem_type.tsv','w')
index = 1
o.write('index\ttype\n')
while True:

    line = f.readline()
    if len(line) == 0:
        break
    dictionary = json.loads(line)
    ptype = dictionary['nodes'][0]
    o.write(str(index) + '\t' + str(ptype) +'\t\n')