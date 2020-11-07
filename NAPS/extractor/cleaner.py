import nltk
import json

def graph(filename, fwrite):
  f = open(filename, "r")
  inputfile = f.read()
  print('Read file')
  tokens = nltk.tokenize.word_tokenize(inputfile)
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


def cleanFile(filename ):
  f = open(filename + '.jsonl', 'r')
  fwrite= open(filename + '-modified.txt','w')
  listToOmit = getFinalItems('finalItems1.txt')
  i = 0
  newline = ''
  for line in f.readlines():
    i+= 1
    if i%100 == 0:
      print(i)
    line = json.loads(line)
    text = line['texts']
    code = line['code_sequence']
    newlinetokens = line.split(' ')
    
    finalTokens = []
    index = 0
    for token in newlinetokens:
      index += 1
      if index <= 5:
        finalTokens.append(token)
      else:
        if token not in listToOmit :
          finalTokens.append(token)
        else:
          print(token)
          finalTokens.append('$$CONSTANT$$')

    fwrite.write(' '.join(finalTokens))
  f.close()
  fwrite.close()


# graph('naps.trainA.1.0-text-modified.txt', open('finalItems2.txt', 'w'))

# getFinalItems('finalItems.txt')

cleanFile('naps.trainA.1.0')