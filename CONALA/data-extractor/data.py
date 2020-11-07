
import json


def flattenList(listval):
    flatList = []
    flatList += ['[']
    for item in listval:
        # print(item, type(item))
        if type(item) == list:
            
            flatList += flattenList(item)
            
        else:
            flatList.append(item)
    flatList += [']']
    return flatList



def joinFuncText(sequence):
    
    # print(sequence)
    # print(flattenList(sequence))
    return ' '.join(flattenList(sequence))


def cleanFile(fileName, prefix):
    print()
    print(fileName)
    f = open('data/' + fileName + '.json','r', encoding= 'UTF-8')

    textfile = open(prefix +fileName + '-text.txt', 'w')
    codefile = open(prefix +fileName + '-code.txt', 'w')
    rewrittentextFile = open(prefix +fileName + '-rewrittentext.txt', 'w')
    # testsFile = open('I:/datasets/testBTests.txt', 'w')


    fileStuff = json.load(f)
    index = 0
    for line in fileStuff:
        dictionary = line
        try:
            sequence = dictionary['intent']
            sequence1 = dictionary['rewritten_intent']
            if sequence1 == None:
                continue
            code = dictionary['snippet']
        except Exception as e:
            print(e)
            continue
        textfile.write(json.dumps(sequence)[1:-1] + '\n')
        rewrittentextFile.write(json.dumps(sequence1)[1:-1] + '\n')
        codefile.write(json.dumps(code)[1:-1] + '\n')
        index += 1
        # break
        if index%10 == 0:
            print(index)


    codefile.close()
    # testsFile.close()
    textfile.close()
    f.close()


def cleanAllFiles():
    # cleanFile('metaset3.dev', 'formatted/dev/')
    cleanFile('conala-test', 'formatted/test/')
    # cleanFile('conala-train', 'formatted/train/')

cleanAllFiles()