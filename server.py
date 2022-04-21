from crypt import methods
import json
from flask import Flask,request
import pickle
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import string

def convRev():
    
    return 0
#__________________________________________________________________________________________________________________________
# loading reviews
rawData = []          # the filtered data from the dataset file (should be 21000 samples)
preprocessedData = [] # the preprocessed reviews (just to see how your preprocessing is doing)
trainData = []        # the training data as a percentage of the total dataset (currently 80%, or 16800 samples)
testData = []         # the test data as a percentage of the total dataset (currently 20%, or 4200 samples)
finalData=[]
# the output classes
fakeLabel = 'fake'
realLabel = 'real'

featureDict = {} # A global dictionary of features

def toFeatureVector(Rating, verified_Purchase, product_Category, tokens):
    localDict = {}
    
#Rating

    #print(Rating)
    featureDict["R"] = 1   
    localDict["R"] = Rating

#Verified_Purchase
  
    featureDict["VP"] = 1
            
    if verified_Purchase == "N":
        localDict["VP"] = 0
    else:
        localDict["VP"] = 1

#Product_Category

    if product_Category not in featureDict:
        featureDict[product_Category] = 1
    else:
        featureDict[product_Category] = +1
            
    if product_Category not in localDict:
        localDict[product_Category] = 1
    else:
        localDict[product_Category] = +1
                    
#Text        

    for token in tokens:
        if token not in featureDict:
            featureDict[token] = 1
        else:
            featureDict[token] = +1
            
        if token not in localDict:
            localDict[token] = 1
        else:
            localDict[token] = +1
    
    return localDict

# TEXT PREPROCESSING AND FEATURE VECTORIZATION
# Input: a string of one review
table = str.maketrans({key: None for key in string.punctuation})
def preProcess(text):
    # Should return a list of tokens
    lemmatizer = WordNetLemmatizer()
    filtered_tokens=[]
    lemmatized_tokens = []
    stop_words = set(stopwords.words('english'))
    text = text.translate(table)
    for w in text.split(" "):
        if w not in stop_words:
            lemmatized_tokens.append(lemmatizer.lemmatize(w.lower()))
        filtered_tokens = [' '.join(l) for l in nltk.bigrams(lemmatized_tokens)] + lemmatized_tokens
    return filtered_tokens

# Convert line from input file into an id/text/label tuple
def parseReview(reviewLine):
    # Should return a triple of an integer, a string containing the review, and a string indicating the label
    s=""
    return (reviewLine[0], reviewLine[2], reviewLine[3],reviewLine[4], reviewLine[8], s)

# load data from a file and append it to the rawData
def loadData(line, Text=None):
    # with open(path, encoding="utf8") as f:
    #     reader = csv.reader(f, delimiter='\t')
    #     next(reader)
    #     for line in reader:
    (Id, Rating, verified_Purchase, product_Category, Text, Label) = parseReview(line)
    rawData.append((Id, Rating, verified_Purchase, product_Category, Text, Label))
    # print(line)
            #preprocessedData.append((Id, preProcess(Text), Label))
    # print(rawData)
    for (_, Rating, verified_Purchase, product_Category, Text, Label) in rawData:
        finalData.append((toFeatureVector(Rating, verified_Purchase, product_Category, preProcess(Text)),Label))
    return finalData[-1]

reviewPath = 'review.txt'
# line format = [ID,label(Blank),rating,verified purchase, PRODUCT_CATEGORY, PRODUCT_ID,PRODUCT_TITLE,REVIEW_TITLE,REVIEW_TEXT]


def getLine(jsonData):
    return ['1','',jsonData['rating'],'Y' if jsonData['verified'] == True else 'N',jsonData['category'],jsonData['id'],jsonData['product_title'],jsonData['review_title'],jsonData['review_text']]

line = ['1', '__label2__', '5', 'N', 'Health & Personal Care', 'B001GAOG6M', 'Sundown NaturalsPure Vitamin E-Oil 70000 IU, 2.5 Ounces (Pack of 3)', 'Excellent, high strength Vit E Oil', "One of the best known beauty secrets is how good Vitamin E oil is for uneven skin tone, acne scars, and, of course, dry skin. If you have one of those conditions, it will definitely help you and make your skin feel better. However, you have to buy the most concentrated Vitamin E oil you can find. It's more expensive, but goes a long way. This is probably the most concentrated oil available. By concentrated, I mean at least 25,000 IU per oz of oil."]

print("done")
sample1=['']
#__________________________________________________________________________________________________________________________

# Pkl_Filename = "Pickle_RL_Model.pkl"  
# with open(Pkl_Filename, 'rb') as file:  
#     Pickled_LR_Model = pickle.load(file)

def predictLabels(reviewSamples, classifier):
    return classifier.classify_many(map(lambda t: t[0], reviewSamples))


app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello!"

@app.route("/ping")
def ping_demo():
  return {"statusCode":"","status":"Connected","message":"Live!!!"}

@app.route('/predict/', methods=['POST'])
def getpred():
    if request.method == "POST":
        reviewLine = getLine(request.json)
        reviewText = loadData(reviewLine)

        # return {"data":reviewText};
        # prediction = predictLabels(reviewText,Pickled_LR_Model)[0]
        prediction = "fake"
        print(prediction)
        return {"review_title":request.json['review_title'],"product_title":request.json['product_title'],"review_status":prediction.upper()}
        # return 'The review ' + '"'+ reviewText + '"' + ' is ' + out1[0].upper()
    return "Send POST Request"

if __name__ == '__main__':
    app.run()