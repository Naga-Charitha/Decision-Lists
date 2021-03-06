#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import re
import sys

f1=sys.argv[1]
f2=sys.argv[2]

def arg_eval():

    if len(sys.argv) == 3:

        files_eval()
    
    else:
        print('less than two args')
        exit()
        
def files_eval():
    for a in sys.argv[1:3]:
        if not os.path.exists(a):
            print(f"File {a} does not exist!")
            exit()


def get_pairs(mylist):
    meaning = {}
    keys = []
    for string in mylist:
        search = re.search('<answer instance="(.*)" senseid="(.*)"/>', string, re.IGNORECASE)
        key = search.group(1)
        keys.append(key)
        value = search.group(2)
        meaning[key] = value
    return meaning, keys

with open(f1, 'r') as data:
    data1 = [line.rstrip('\n') for line in data]
answers, keys = get_pairs(data1)


with open(f2, 'r') as data:
    data2 = [line.rstrip('\n') for line in data]
predictions, keys = get_pairs(data2)

matched = 0
for key in keys:
    if(answers[key]==predictions[key]):
        matched = matched + 1

phone_acc = 0
for key in keys:
    if(answers[key]=="phone"):
        phone_acc += 1
phone_acc = (float(phone_acc)/float(len(keys)))*100
print(str(phone_acc)+'%')


total_acc = (float(matched)/float(len(keys)))*100
print(str(total_acc)+'%')

prediction_list = []
for values in predictions:
    prediction_list.append(predictions[values])

answers_list = []
for values in answers:
    answers_list.append(answers[values])
    

dataframe_1 = pd.Series( (values for values in prediction_list) )
dataframe_2 = pd.Series( (values for values in answers_list) )    
    

confusion_matrix = pd.crosstab(dataframe_1, dataframe_2)
print("Confusion matrix is\n"  +str(confusion_matrix))
    

