#loading packages
import nltk
from nltk.corpus import sentence_polarity
import json
import csv

#initialize count
c=0
i= 1000000

#Define class to read columns  of file
class Review(object):
	reviewerID = ""
	asin = ""
	reviewerName = ""
	helpful = ""
	reviewText = ""
	overall = ""
	summary = ""
	unixReviewTime = ""
	reviewTime = ""

#Define a function to update the variables in the class and return them through class constructor
def as_review(line):
	product = Review()
	product.__dict__.update(line)
	return product

#Initializing review list and product review mapping dic. Also variables
allReviewList = []
prodRev = {}

with open('complete.json','r') as jsonfile:
	prevProd = ''
	currProd = ''
	currProdReview = []
	print('Reading JSON file...')
	for line in jsonfile:
		
		if i == 0:
			break
		i-=1
		c +=1
		if c%1000000 == 0:
			print('Records read: ',c)

		obj = json.loads(line, object_hook = as_review)
		currProd = obj.asin
		
		if prevProd == '':
			prevProd = currProd
		
		allReviewList.append(obj.reviewText)
		currProdReview.append(obj.reviewText)
		
		if prevProd != currProd:
			prodRev[currProd] = 	currProdReview
			currProdReview = []
			prevProd = currProd
	prodRev[currProd] =  currProdReview

#taking in pre tagged sentences from the corpus
print('Fetching sentences for polarity')
sentences = sentence_polarity.sents()

#creating a document set of tuple with sentences with respective categories
print('Creating Document sets')
documents = [(sent,cat) for cat in sentence_polarity.categories()
			 for sent in sentence_polarity.sents(categories = cat)]

#review text to be processed
print('Joining all the reviews')
allRevText = ''.join(allReviewList)
allReviewList_words = nltk.word_tokenize(allRevText)
review_words = [w for w in allReviewList_words if w.isalpha()]

#Defining a function to create feature sets
def document_features(doc,review_words):
	doc_words = set(doc)
	features ={}
	for word in review_words:
		features['contains({})'.format(word)] = (word in doc_words)
	return features
	
#creating feature sets for classifier
print('Creating Featuresets...')
feature_sets = [(document_features(sent,review_words), cat) for (sent,cat) in documents]
# print(feature_sets)

#Dividing the data into Training and Test data
train_set, test_set = feature_sets[50:], feature_sets[:50]

#Create a classifier
print('Training classifier..')
classifier = nltk.NaiveBayesClassifier.train(train_set)

#Validating teh accuracy on test dataset
print('Classifier accuracy is: ',nltk.classify.accuracy(classifier, test_set))
print(classifier.show_most_informative_features(20))

negation_words = ['never','no','nothing','nowhere','noone','none','not', 'havent','hasnt','hadnt','cant','couldnt','shouldnt','wont','wouldnt',
				  'dont','doesnt','didnt','isnt','arent','aint']


#adding negative words
# with open('negative-words.txt', encoding = 'latin-1') as txtfile:
# 	for line in txtfile:
# 		line = line.strip('\n')
# 		negation_words.append(line)

# print (negation_words)

#Function to create features using negation words
def not_features(doc,review_words,negation_words):
	features = {}
	for word in review_words:
		features['contains({})'.format(word)] = False
		features['contains(NOT{})'.format(word)] = False
	# go through document words in order
	for i in range(0, len(doc)):
		word = doc[i]
		if ((i + 1) < len(doc)) and ((word in negation_words) or (word.endswith("n't"))):
			i += 1
			features['contains(NOT{})'.format(doc[i])] = (doc[i] in review_words)
		else:
			features['contains({})'.format(word)] = (word in review_words)
	return features

#Classifying sentence for positive or negative reviews
print('Classifying sentences....')
# allwords = []

i = 0
reviewpol = {}

for prod, reviews in prodRev.items():
	i +=1

	revposcount = 0
	revnegcount = 0
	revcount = []

	for each_review in reviews:
		sentences = nltk.sent_tokenize(each_review)
		allwords = []

		for sentence in sentences:
			words = nltk.word_tokenize(sentence)
			wordtokens = [w.lower() for w in words if w.isalpha()]
			allwords.append(wordtokens)

		poscount = 0
		negcount = 0

		for word in allwords:
			inputfeatures = not_features(word,review_words,negation_words)
			if 'pos' == classifier.classify(inputfeatures):
				# print(classifier.classify(inputfeatures))
				poscount +=1
			else:
				negcount +=1

		if poscount < negcount:
			revnegcount +=1
		else:
			revposcount +=1

		revcount.append(len(reviews))
		revcount.append(revposcount)
		revcount.append(revnegcount)

	# print("Product Id ",prod)
	# print("Reviews ",reviews)
	# print("Number of Positive Sentences ",poscount)
	# print("Number of Negative Sentences ",negcount)
	# print("Number of Positive Reviews ",revposcount)
	# print("Number of Negative Reviews ",revnegcount)

	reviewpol[prod] = revcount
# print(reviewpol)

bar = True
with open("sentiment.csv", "w",newline = '') as file:
	print('Writting CSV file!!')
	csv_file = csv.writer(file)
	csv_file.writerow(['ProductID','Total Reviews','Positive Reviews','Negative Reviews'])
	for k,counts in reviewpol.items():
		print (counts)
		if not counts:
			continue
		total = counts[0]
		pos = counts[1]
		neg = counts[2]
		csv_file.writerow([k,total,pos,neg])





