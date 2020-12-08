'''
Generates embeddings and dumps matrix to file
'''

from sentence_transformers import SentenceTransformer
import json
from json import JSONEncoder
import numpy

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

model = SentenceTransformer('I:/datasets/program-synthesis-game-theory/ALGOLISP/Metrics/Stage-2/models/finetuned/')

gtEncodings = open('encodingsGT.txt','w')
predEncodings = open('encodingsPred.txt','w')

gtFile = open('Preds/test/data/metaset3.test-code.txt','r')
predFile = open('Preds/reverse/4l.txt','r')

gtLines = gtFile.readlines()
predLines = predFile.readlines()

try:
    print('Encoding GT')
    referencesEncoded = model.encode(gtLines)
    print('Encoding PRED')
    candidatesEncoded = model.encode(predLines)
    print(referencesEncoded.shape)
    gtWrite = json.dumps(referencesEncoded,  cls=NumpyArrayEncoder)
    predWrite = json.dumps(candidatesEncoded,  cls=NumpyArrayEncoder)
    
except Exception as e:
    print(e)
    gtWrite = json.dumps({})
    predWrite = json.dumps({})
    # continue
gtEncodings.write( gtWrite + '\n')
predEncodings.write( predWrite + '\n')