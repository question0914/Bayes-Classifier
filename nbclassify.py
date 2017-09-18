import sys
import re

textFile = sys.argv[1]

ratio = 0.75  # The proportion of training data
size = 0  # Lines of reviews being processed

# Four classes
c1 = "truthful"
c2 = "deceptive"
c3 = "positive"
c4 = "negative"

prior = list()  # prior probability of 4 classes

user = []   # User name

Dict = {}   # Dictionary to store P(feature|class)

classlist1 = list()  # truthful or deceptive
classlist2 = list()  # positive or negative


def splitfile(fileContent):
    splitter = re.compile('\s+| |\W+')
    words = [s.lower() for s in splitter.split(fileContent) if 2 < len(s) < 20]

    words = [word for word in words if word.isalpha()]
    with open(r'stoplist.txt') as f:
        stopwords = f.read()
    stopwords = stopwords.split('\n')
    stopwords = set(stopwords)
    words = [word for word in words if word not in stopwords]
    return words


#  Read nbmodel.txt to load the model
with open("nbmodel.txt", "r")as model:
    data = model.read()
    line = data.splitlines()

p = line[0].split(" ")
prior.append(0.0)
for i in range(1, len(p)):
    prior.append(float(p[i]))   # Get prior probability

for j in range(1, len(line)):
    attr = line[j].split(" ")
    Dict[attr[0]] = {c1: 0.0, c2: 0.0, c3: 0.0, c4: 0.0}
    Dict[attr[0]][c1] = float(attr[1])
    Dict[attr[0]][c2] = float(attr[2])
    Dict[attr[0]][c3] = float(attr[3])
    Dict[attr[0]][c4] = float(attr[4])

#  Read the test file
with open(textFile, "r")as test:
    rawData = test.read()
    review = rawData.splitlines()

# Process the last 25% data

for i in range(0, len(review)):
    # P(class|document)
    p1 = 1.0
    p2 = 1.0
    p3 = 1.0
    p4 = 1.0
    line = review[i].split(" ")
    user.append(line[0])
    words = splitfile(review[i])
    for w in words:
        if w in Dict:
          p1 = p1*Dict[w][c1]*10000  # Calculate P(doc|class)
          p2 = p2*Dict[w][c2]*10000
          p3 = p3*Dict[w][c3]*10000
          p4 = p4*Dict[w][c4]*10000
    if p1*prior[1] >= p2*prior[2]:
        classlist1.append(c1)
    else:
        classlist1.append(c2)
    if p3*prior[3] >= p4*prior[4]:
        classlist2.append(c3)
    else:
        classlist2.append(c4)


with open("nboutput.txt","w")as outFile:
    for i in range(0,len(user)):
        outFile.write(user[i]+" "+classlist1[i]+" "+classlist2[i]+"\n")
