
import json
import nltk

def graph(filename, fwritename):
    f = open(filename, "r")
    fwrite = open(fwritename, 'w')

    lineCount = 0
    tokens = []
    while True:
        line = f.readline()
        lineCount += 1
        if lineCount %100 == 0:
            print(lineCount)
        if len(line) == 0:
            break

        dictionary = json.loads(line)
        # print(dictionary.keys())
        # sequence, status = joinFuncText(dictionary['texts'][0])
        # print(type(tokens), type(dictionary['texts'][0]))
        tokens += dictionary['text'][0]
        tokens += dictionary['code_sequence']

    print('Tokenized')
    
    fd = nltk.FreqDist(tokens)
    print('Freq dist computed')

    finalItems=  list(filter(lambda x: x[1]<=10,fd.items()))
    print('Final remaining items = ', len(set(tokens)) - len(finalItems))
    items = []
    for item in finalItems:
        items.append(item[0])
    fwrite.write(json.dumps(items))
  

  # fd.plot(30,cumulative=False)

def getFinalItems(fileName):
  f = open(fileName, 'r')
  l = json.loads(f.read())
  return l


def joinFuncText(sequence):
    joined = ''
    i = 0
    tokensToRemove = getFinalItems('itemsFinal.txt')
    while i < len(sequence):
        if sequence[i] in tokensToRemove:
            joined += '$$CONSTANT$$ '
            i+= 1
            continue
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


def cleanFile(fileName, boolean = False):
    print()
    print(fileName)
    f = open(fileName + '.jsonl','r')

    textsFile = open(fileName + '-text.txt', 'w')
    codeFile = open(fileName + '-code.txt', 'w')
    # testsFile = open('I:/datasets/testBTests.txt', 'w')
    errorFile = open(fileName + 'errorFile.txt','w')
    index = 0
    lineCount = 1
    while True:
        line = f.readline()
        lineCount += 1
        if len(line) == 0:
            break
        
        dictionary = json.loads(line)
        # print(dictionary.keys())
        sequence, status = joinFuncText(dictionary['code_sequence'])
        if status != 'OK':
            errorFile.write(line)
        if boolean:
            text, status = joinFuncText(dictionary['texts'][0])
        else:
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
        # testsFile.write(text + '\n')
        # break
        index += 1
        if index%100 == 0:
            print(index)

    errorFile.close()
    codeFile.close()
    # testsFile.close()
    textsFile.close()
    f.close()

def joinItems():
    f = open('itemstest.txt', 'r')
    l = json.loads(f.read())
    f = open('itemstraina.txt', 'r')
    l += json.loads(f.read())
    f = open('itemstrainb.txt', 'r')
    l += json.loads(f.read())
    f = open('itemsFinal.txt', 'w')
    f.write(json.dumps(l))

def graphAllFiles():
    graph('naps.trainA.1.0.jsonl', 'itemstraina.txt')
    graph('naps.trainB.1.0.jsonl', 'itemstrainb.txt')
    graph('naps.test.1.0.jsonl', 'itemstest.txt')

def cleanAllFiles():
    cleanFile('naps.test.1.0')
    cleanFile('naps.trainA.1.0', True)
    cleanFile('naps.trainB.1.0')

def runAll():
    graphAllFiles()
    cleanAllFiles()

# joinItems()

cleanAllFiles()