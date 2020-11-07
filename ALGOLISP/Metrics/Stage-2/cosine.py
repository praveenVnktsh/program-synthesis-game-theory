'''
Takes dumped embedding matrix and computes the cosine similarity and cosimilarities
'''

import json
import numpy as np
from numba import jit
from runstats import Statistics



gtEncodingsFile = open('encodingsGT.txt','r')
predEncodingsFile = open('encodingsPred.txt','r')

output = open('OUTPUT-cosine.csv','w')

gtEmbeddings = np.array(json.load(gtEncodingsFile))
predEmbeddings = np.array(json.load(predEncodingsFile))
print(gtEmbeddings.shape)
sum = 0

def writeToFile(similarities):
    for item in similarities:
        output.write(str(item) + ',')
    output.write('\n')

@jit(nopython=True)
def cosine_similarity_numba(u:np.ndarray, v:np.ndarray):
    uv = 0
    uu = 0
    vv = 0
    for i in range(u.shape[0]):
        uv += u[i]*v[i]
        uu += u[i]*u[i]
        vv += v[i]*v[i]
    cos_theta = 1
    if uu!=0 and vv!=0:
        cos_theta = uv/np.sqrt(uu*vv)
    return cos_theta

def log(diag):
    print('--------------------------')
    print("----------DIAG----------")
    print('Count:', len(diag))
    print('Mean:', diag.mean())
    print('Variance:', diag.variance())
    print('Skewness:', diag.skewness())
    print('kurtosis', diag.kurtosis())

def compute():
    
    diag = Statistics()
    nonDiag = Statistics()
    for j in range(len(gtEmbeddings)):
        for i in range(len(gtEmbeddings)):
            sent = gtEmbeddings[i]
            rcvd = predEmbeddings[j]
            similarity = cosine_similarity_numba(sent, rcvd)
            if i == j:
                diag.push(similarity)
            else:
                nonDiag.push(similarity)

        if j %100 == 0 and j != 0 :
            print('======',j, 'iterations======')
            print('DIAG-------------')
            log(diag)
            print('NONDIAG----------')
            log(nonDiag)

            
    
    log(diag)
    log(nonDiag)
        


compute()

