import json
import tokenize
import io
def prepostProcess(fileName, prefix, basename):
    fi = open(fileName, 'r')
    # outFileCode = open('formatted/' + prefix + 'codeTokens - ' + basename + '.txt', 'w')
    print(tokenize.tokenize(fi.readline))

def preprocess(fileName, prefix = ''):
    basename = fileName.split('.')[0]
    inFile = open('data/' + fileName, 'r', encoding= 'UTF-8')

    outFileText = open('formatted/' + prefix + 'intent - ' + basename + '.txt', 'w')
    outFileCode = open('formatted/' + prefix + 'code - ' + basename + '.txt', 'w')
    outFileRewritten = open('formatted/' + prefix + 'rewrittenIntent - ' + basename + '.txt', 'w')

    while True  :
        line = json.loads(inFile.readline())
        if len(line) == 0:
            break

        try:
            intent = line['intent']#.encode('unicode-escape')
            code = line['snippet']#.encode('unicode-escape')
            if line['rewritten_intent'] == None:
                rewrittenIntent = intent
            else:
                rewrittenIntent = line['rewritten_intent']#.encode('unicode-escape')


            # print(tokenize.generate_tokens(io.BytesIO(code.encode()).readline))
            finalCode = ''
            for token in tokenize.tokenize(io.BytesIO(code.encode()).readline):
                # print(token.string, end = ' ')
                if token.string != 'utf-8':
                    finalCode += token.string + ' '
            # print(finalCode)
            code = finalCode
            # print()


        except Exception as e:
            print('Error',e)
            continue

        outFileText.write( json.dumps(intent)[1:-1])
        outFileText.write( '\n')
        # outFileText = 
        outFileRewritten.write(json.dumps(rewrittenIntent)[1:-1])
        outFileRewritten.write( '\n')
        outFileCode.write( json.dumps(code)[1:-1])
        outFileCode.write( '\n')
        
    inFile.close()
    outFileText.close()
    outFileCode.close()


    # prepostProcess('formatted/' + prefix + 'code - ' + basename + '.txt', prefix, basename)


def preprocess(fileName, prefix = ''):
    basename = fileName.split('.')[0]
    inFile = open('data/' + fileName, 'r', encoding= 'UTF-8')

    outFileText = open('formatted/' + prefix + 'intent - ' + basename + '.txt', 'w')
    outFileCode = open('formatted/' + prefix + 'code - ' + basename + '.txt', 'w')
    outFileRewritten = open('formatted/' + prefix + 'rewrittenIntent - ' + basename + '.txt', 'w')

    for line in json.load(inFile):
        try:
            intent = line['intent']#.encode('unicode-escape')
            code = line['snippet']#.encode('unicode-escape')
            if line['rewritten_intent'] == None:
                rewrittenIntent = intent
            else:
                rewrittenIntent = line['rewritten_intent']#.encode('unicode-escape')


            # print(tokenize.generate_tokens(io.BytesIO(code.encode()).readline))
            finalCode = ''
            for token in tokenize.tokenize(io.BytesIO(code.encode()).readline):
                # print(token.string, end = ' ')
                if token.string != 'utf-8':
                    finalCode += token.string + ' '
            # print(finalCode)
            code = finalCode
            # print()


        except Exception as e:
            print('Error',e)
            continue

        outFileText.write( json.dumps(intent)[1:-1])
        outFileText.write( '\n')
        # outFileText = 
        outFileRewritten.write(json.dumps(rewrittenIntent)[1:-1])
        outFileRewritten.write( '\n')
        outFileCode.write( json.dumps(code)[1:-1])
        outFileCode.write( '\n')
        
    inFile.close()
    outFileText.close()
    outFileCode.close()


    # prepostProcess('formatted/' + prefix + 'code - ' + basename + '.txt', prefix, basename)

# preprocess('conala-test.json', prefix = 'test/' )
# preprocess('conala-train.json', prefix = 'train/' )
preprocess('conala-mined.jsonl', prefix = 'mined/' )