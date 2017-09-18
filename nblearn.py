import sys
import re

textFile = sys.argv[1]

labelFile = sys.argv[2]

ratio = 0.75  # The proportion of training data
size = 0  # Lines of reviews being processed

# Four classes
c1 = "truthful"
c2 = "deceptive"
c3 = "positive"
c4 = "negative"

prior1 = 0.0  # truthful
prior2 = 0.0  # deceptive
prior3 = 0.0  # positive
prior4 = 0.0  # negative

numOfc1 = 0.0   # total number of word in class one
numOfc2 = 0.0
numOfc3 = 0.0
numOfc4 = 0.0


Dict = {}  # dictionary to store words

# split a line by tokenizer and remove stop words
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


# Get the class of each review
classlist1 = list()  # Truthful or deceptive
classlist2 = list()  # Positive 0r negative

with open(labelFile, "r") as inFile:
        data = inFile.read()

line = data.splitlines()

# size = (int)(len(line)*ratio)
size = len(line)

for l in line:
    wordlist = l.split(' ')
    classlist1.append(wordlist[1])
    classlist2.append(wordlist[2])


# Get the prior probability P(class)
for i in range(0, size):
    if classlist1[i] == "truthful":
        prior1 += 1
    else:
        prior2 += 1

    if classlist2[i] == "positive":
        prior3 += 1
    else:
        prior4 += 1

amount = prior1+prior2+prior3+prior4
p1 = prior1/amount
p2 = prior2/amount
p3 = prior3/amount
p4 = prior4/amount

# Get P(feature|class)
with open(textFile, "r")as inFile:
    data = inFile.read()

line = data.splitlines()

for i in range(0, size):
    words = splitfile(line[i])
    for j in range(0, len(words)):
        if words[j] not in Dict:
            if classlist1[i] == "truthful" and classlist2[i] == "positive":
                # Smooth the data when counting numbers of words
               Dict[words[j]] = {c1: 1.01, c2: 0.01, c3: 1.1, c4: 0.1}

            elif classlist1[i] == "truthful" and classlist2[i] == "negative":
               Dict[words[j]] = {c1: 1.01, c2: 0.01, c3: 0.1, c4: 1.1}

            elif classlist1[i] == "deceptive" and classlist2[i] == "positive":

               Dict[words[j]] = {c1: 0.01, c2: 1.01, c3: 1.1, c4: 0.1}

            else:
               Dict[words[j]] = {c1: 0.01, c2: 1.01, c3: 0.1, c4: 1.1}

        else:
            if classlist1[i] == c1:
                temp = Dict[words[j]][c1]
                temp += 1
                Dict[words[j]][c1] = temp

            else:
                temp = Dict[words[j]][c2]
                temp += 1
                Dict[words[j]][c2] = temp

            if classlist2[i] == c3:
                temp = Dict[words[j]][c3]
                temp += 1
                Dict[words[j]][c3] = temp

            else:
                temp = Dict[words[j]][c4]
                temp += 1
                Dict[words[j]][c4] = temp

# Remove words appear too much, too little times or each of the word's class is too close in document
remove = []
for w in Dict:
    if Dict[w][c1]+Dict[w][c2]+Dict[w][c3]+Dict[w][c4] <= size/125 or Dict[w][c1]+Dict[w][c2]+Dict[w][c3]+Dict[w][c4] > 1.35*size:
        remove.append(w)
    elif abs(Dict[w][c1]-Dict[w][c2]) == 0 and abs(Dict[w][c3]-Dict[w][c4]) == 0:
        remove.append(w)
for w in remove:
    del Dict[w]

# Count the total number of each class
for w in Dict:
   numOfc1 += Dict[w][c1]
   numOfc2 += Dict[w][c2]
   numOfc3 += Dict[w][c3]
   numOfc4 += Dict[w][c4]

# Write into nbmodel.txt
with open("nbmodel.txt", "w")as outFile:
    outFile.write("P(class) %f" % p1)
    outFile.write(" %f" % p2)
    outFile.write(" %f" % p3)
    outFile.write(" %f\n" % p4)
    for w in Dict:
        outFile.write(w)
        outFile.write(" %.8f" % (Dict[w][c1]/numOfc1))
        outFile.write(" %.8f" % (Dict[w][c2]/numOfc3))
        outFile.write(" %.8f" % (Dict[w][c3]/numOfc3))
        outFile.write(" %.8f\n" % (Dict[w][c4]/numOfc4))










