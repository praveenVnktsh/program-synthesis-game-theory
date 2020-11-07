
import json
import nltk

def graph(filename, fwritename, boolean = False):
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
        if boolean:
            tokens += dictionary['texts'][0]
        else:
            tokens += dictionary['text']
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
    # tokensToRemove = getFinalItems('ONMT/REVERSE/itemsFinal.txt')
    while i < len(sequence):
        # if sequence[i] in tokensToRemove:
        #     joined += '$$CONSTANT$$ '
        #     i+= 1
        #     continue
        if sequence[i] == '_' and sequence[i+1] == '_':
            
            joined += sequence[i]
            i += 1
            if i == len(sequence):
                return joined, "ISSUE"
            joined += sequence[i]
            i += 1
            if i == len(sequence):
                return joined, "ISSUE", sequence[i-1]
            joined += sequence[i]
            i += 1
            if i == len(sequence):
                return joined, "ISSUE", sequence[i-1]
            joined += sequence[i]
            i += 1
            if i == len(sequence):
                return joined, "ISSUE", sequence[i-1]
            joined += sequence[i]
            i += 1
            if i == len(sequence):
                return joined, "ISSUE", sequence[i-1]
            print(joined)
            if sequence[i] == '.':
                joined += sequence[i]
                i+=1
            else: 
                joined += ' '
            continue
        joined += sequence[i] + ' '
        i += 1
    return joined, "OK", sequence[i-1]


def cleanFile(fileName, boolean = False, prefix = 'ONMT/FULLVOCAB/'):
    print()
    print(fileName)
    f = open(fileName + '.jsonl','r')

    codeFile = open(prefix +fileName + '-code.txt', 'w')
    textFile = open(prefix +fileName + '-texts.txt', 'w')
    # testsFile = open('I:/datasets/testBTests.txt', 'w')
    print(prefix +fileName + '-errorFile.txt')
    errorFile = open(prefix + 'ERROR/' + fileName + '-errorFile.txt','w')
    index = 0
    lineCount = 1
    while True:
        line = f.readline()
        lineCount += 1
        if len(line) == 0:
            break
        
        dictionary = json.loads(line)
        sequence, status, errorAt = joinFuncText(dictionary['code_sequence'])
        
        if status != 'OK':
            print(errorAt)
            errorFile.write(lineCount + '\n')
        # else: 
        #     print("ERROR AT ", lineCount)
        if boolean:
            # dist = int(len(dictionary['texts'])/10)
            dist = 7
            for i in range(dist):
                text, status, errorAt = joinFuncText(dictionary['texts'][i])

                codeFile.write(text + '\n')
                textFile.write(sequence + '\n')
        else:
            text, status, errorAt = joinFuncText(dictionary['text'])
            codeFile.write(text + '\n')
            textFile.write(sequence + '\n')
            # if status != 'OK':
            #     print(errorAt)
            #     errorFile.write(lineCount + '\n')
            # else:
            #     print(text)
        
        if status != 'OK':
            errorFile.write(line)
        index += 1
        # if index%10 == 0:
        #     print(index)

    errorFile.close()
    textFile.close()
    # testsFile.close()
    codeFile.close()
    f.close()

def joinItems(prefix = 'ONMT/REVERSE/'):
    f = open('itemstest.txt', 'r')
    l = json.loads(f.read())
    f = open('itemstraina.txt', 'r')
    l += json.loads(f.read())
    f = open('itemstrainb.txt', 'r')
    l += json.loads(f.read())
    f = open('itemsFinal.txt', 'w')
    f.write(json.dumps(l))

def graphAllFiles():
    graph('naps.trainA.1.0.jsonl', 'ONMT/FULLVOCAB/itemstraina.txt', True)
    graph('naps.trainB.1.0.jsonl', 'ONMT/FULLVOCAB/itemstrainb.txt')
    graph('naps.test.1.0.jsonl', 'ONMT/FULLVOCAB/itemstest.txt')
    joinItems()

def cleanAllFiles():
    # cleanFile('naps.test.1.0')
    # cleanFile('naps.trainA.1.0', True)
    cleanFile('naps.trainB.1.0')

def runAll():
    graphAllFiles()
    cleanAllFiles()

# joinItems()
# graphAllFiles()
cleanAllFiles()