gtCodeFile = open("GT_CODE.txt",'r')
gtDescFile = open("GT_DESC.txt",'r')
predS1CodeFile = open("PRED_S1_CODE.txt",'r')
predS2DescFile = open("PRED_S2_DESC.txt",'r')
output = open('OUTPUT.txt','w')
i = 0

counts = [899, 2012, 2159, 2396, 2503, 2624, 3016, 3366, 4390, 4401, 4755, 4840, 4989, 5791, 6859, 7132, 7324, 8197, 9428]

s1correct = 0
total = len(counts)
while True:
    
    gtCode = gtCodeFile.readline()
    gtDesc = gtDescFile.readline()
    predS1Code = predS1CodeFile.readline()
    predS2Desc = predS2DescFile.readline()

    if i in counts:
        output.write('LINE Number = ' + str(i+1) + '\n')
        output.write('GT CODE =      ' + str(gtCode))
        output.write('\n')
        output.write('PRED S1 CODE = ' + str(predS1Code))
        output.write('\n')
        output.write('GT DESC =      ' + str(gtDesc))
        output.write('PRED S2 CODE = ' + str(predS2Desc))
        output.write('-------------------------\n')
        output.write('-------------------------\n')
        if gtCode == predS1Code:
            s1correct += 1



    if len(gtCode) == 0:
        break

    i += 1

print('S1 exact matches = ', s1correct)
print('Total = ', total)