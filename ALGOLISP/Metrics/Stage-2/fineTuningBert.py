from sentence_transformers import SentenceTransformer, SentencesDataset, InputExample, losses
from torch.utils.data import DataLoader
import numpy as np
import json
from numba import jit
import random
from sentence_transformers import evaluation

model = SentenceTransformer('distilbert-base-nli-mean-tokens')

gtEncodings = open('data/encodingsGT.txt','r')
predEncodings = open('data/encodingsPred.txt','r')

gtEmbeddings = np.array(json.load(gtEncodings))
predEmbeddings = np.array(json.load(predEncodings))


gtText = open('data/GT.txt','r')
predText = open('data/pred.txt','r')

train_examples = []


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

dev1 = []
dev2 = []
scores = []


print('LOADING POSITIVE CASES')
i = 0
while True:
    gt = gtText.readline()
    pred = predText.readline()
    if len(gt) == 0:
        break
    sent = gtEmbeddings[i]
    rcvd = predEmbeddings[i]
    sim = cosine_similarity_numba(sent, rcvd)
    if sim > 0.7:
        sim = 1.0
        if random.randint(0,10) < 3:
            dev1.append(gt)
            dev2.append(pred)
            scores.append(1.0)
    else:
        sim = 0.0
        

    train_examples.append(InputExample(texts = [gt, pred], label = sim))

print("LOADED POSITIVE CASES")

print('LOADING NEGATIVE CASES')
gtText.seek(0)
predText.seek(0)
gt = gtText.readline()
while True:
    gt = gtText.readline()
    pred = predText.readline()
    if len(gt) == 0:
        break
    if random.randint(0,10) < 3:
        dev1.append(gt)
        dev2.append(pred)
        scores.append(0.0)
    train_examples.append(InputExample(texts = [gt, pred], label = 0.0))

    
            

print("LOADED NEGATIVE CASES")


evaluator = evaluation.EmbeddingSimilarityEvaluator(dev1, dev2, scores)

train_dataset = SentencesDataset(train_examples, model)
train_dataloader = DataLoader(train_dataset, shuffle=True, batch_size=16)
train_loss = losses.CosineSimilarityLoss(model)

print('TRAINING MODEL')
model.fit(train_objectives=[(train_dataloader, train_loss)], epochs=1, warmup_steps=100, evaluator = evaluator,  output_path='models/finetuned/')
print('TRAINED MODEL')