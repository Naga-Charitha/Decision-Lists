#!/usr/bin/env python
# coding: utf-8

# In[ ]:

### Problem Statement:
#### 1. This program helps in deciding the sense of an ambigous word in a text. For training, it takes an XML file that has the senseid, context and ambiguous word and attempts to predict the sense id in a test data.
#### 2. In order to run the program, we need to install the required libraries and pass arguments through command line.

### Algorithm:

### Step 1: Extraction of training and testing datasets
### Step 2: Preprocess the data
### Step 3: Removal of stop words and punctuations
### Step 4: Read the rules learned from the training data
### Step 5: Apply conditional probability on rules
### Step 6: Calculate log likelihood using rules and conditional probability
### Step 7: Based on the context and rules applied extract the sense of the word
### Step 8: Predict the test data based on the decision rules learned
### Step 9: Write the results into the decision list

### Input:
#### We will pass four files as inputs. They are:
#### 1. The file which has code for execution
#### 2. The file named as "list-train.xml", which contains training data
#### 3. The file named as "list-test.xml", which contains test data
#### 4. An empty text file

### Sample Output:
#### my-decision-list:
#### ['-1_word_telephone', 8.370687406807217, 'phone']
#### ['-1_word_access', 7.238404739325079, 'phone']
#### ['-1_word_car', -6.507794640198696, 'product']
#### ['-1_word_end', 6.339850002884625, 'phone']
#### ['-8_word_telephone', 6.339850002884625, 'phone']
#### ["-1_word_'s", -6.149747119504682, 'product']
#### ['1_word_dead', 5.930737337562887, 'phone']


import nltk
nltk.download('stopwords')

nltk.download('punkt')


from nltk.probability import ConditionalFreqDist
from nltk.probability import ConditionalProbDist
from nltk.probability import LidstoneProbDist
from nltk.tokenize import word_tokenize 
import re
import string,math
from bs4 import BeautifulSoup
import sys
from nltk.corpus import stopwords

training_data=sys.argv[1]
testing_data=sys.argv[2]
dec_list=sys.argv[3]

def arg_eval():
    
    if len(sys.argv) == 4:
        
        files_eval()

    else:
        print('less than four args')
        exit()
        
def files_eval():
    for a in sys.argv[1:3]:
        if not os.path.exists(a):
            print(f"File {a} does not exist!")
            exit()

def pre_process_text(text):
    text = text.lower()
    text = text.replace("lines", "line")
    # removing the standard stop word from the text
    stop_words = set(stopwords.words("english"))
    word_token = word_tokenize(text)
    
    sentence = [w for w in word_token if w not in stop_words and w not in string.punctuation and w!='']
    return sentence  

root = "line"
def get_word(n, context):
    index_of_root = context.index(root)
    index_of_n_word = index_of_root + n
    if len(context) > index_of_n_word and index_of_n_word >= 0:
        return context[index_of_n_word]
    else:
        return ""


def word_freq_count(tk,data,n):
    for ele in data:
        senseid = ele['senseid']
        context = ele['text']
    
        word = get_word(n,context)
        if word != '':
            condition = str(n) + "_word_" + re.sub(r'\_', '', word)
            cfd[condition][senseid] += 1
        
    return cfd

def prod_likelihood(cpd,rule):
    prob_phone_likelihood = cpd[rule].prob("phone")
    prob_product_likelihood = cpd[rule].prob("product")
    div_prob = prob_phone_likelihood / prob_product_likelihood
    if div_prob == 0:
        return 0
    else:
        return math.log(div_prob, 2)


def prod_rule(context, rule):
    rule_scope, rule_type, rule_feature = rule.split("_")
    rule_scope = int(rule_scope)
    
    return get_word(rule_scope, context) == rule_feature


def predict_prob(context, majority_label):
    for rule in decision_list:
        if prod_rule(context, rule[0]):
            if rule[1] > 0:
                return ("phone", context, rule[0])
            elif rule[1] < 0:
                return ("product", context, rule[0])
    return (majority_label, context, "default")

with open(training_data,'r') as data:
    soup = BeautifulSoup(data,'html.parser')

train_data = []
decision_list=[]
for inst in soup.find_all('instance'):
    sinst = dict()
    sinst['id']=inst['id']
    sinst['senseid']=inst.answer['senseid']
    text = ""
    for s in inst.find_all('s'):
        text = text+" "+s.get_text()
    sinst['text'] = pre_process_text(text)
    train_data.append(sinst)

cfd = ConditionalFreqDist()
#tk = nltk.FreqDist() 
#cfd=word_freq_count(tk,train_data,1)
for i in range(1,9):
    #print(-i)
    cfd=word_freq_count(cfd,train_data,i)
    cfd=word_freq_count(cfd,train_data,-i)

cpd = ConditionalProbDist(cfd, LidstoneProbDist, 0.1)



for rule in cpd.conditions():
    likelihood = prod_likelihood(cpd, rule)
    decision_list.append([rule, likelihood, "phone" if likelihood > 0 else "product"])
    
    decision_list.sort(key=lambda rule: math.fabs(rule[1]), reverse=True)


with open(testing_data, 'r') as data:
    test_soup = BeautifulSoup(data, 'html.parser')

test_data = []
for instance in test_soup('instance'):
    sinst = dict()
    sinst['id'] = instance['id']
    text = ""
    for s in instance.find_all('s'):
        text = text+ " "+ s.get_text()
    sinst['text'] = pre_process_text(text)
    test_data.append(sinst)



sense_a = 0.0
sense_b = 0.0
for element in train_data:
    if element['senseid'] == "phone":
        sense_a += 1.0
    elif element['senseid'] == 'product':
        sense_b += 1.0
    else:
        print("No match")

if(sense_a > sense_b):
    prod_majority = "phone"
else:
    prod_majority = "product"



prod_predictions = []
for element in test_data:
    pred, _, r = predict_prob(element['text'], prod_majority)
    id1 = element['id']
    prod_predictions.append(f'<answer instance="{id1}" senseid="{pred}"/>')
    print(f'<answer instance="{id1}" senseid="{pred}"/>')


# Storing the decision list into a file
with open(dec_list, 'w') as output:  
    for listitem in decision_list:
        output.write('%s\n' % listitem)

