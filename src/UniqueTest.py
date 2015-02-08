'''
Created on Jun 18, 2014

@author: junaed
'''
directory="/home/junaed/ubidata/Data/"
filename="Nexus4.csv"

inputfile = open(directory+filename, "r")
cids = set()

i = 0
for line in inputfile:
    if 'cid' in line:
        i+=1
        tokens = line.split(';')
        if tokens[2] != "(invalid date)" and tokens[2] != None and len(tokens) >= 5:
#             print(tokens[4])
            cids.add(tokens[4].strip())
    pass

inputfile.close()

print(len(cids))
print(i)
# for item in cids:
#     print(item)