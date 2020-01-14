#!/usr/bin/env python
# coding: utf-8

# # Week 4: Machine learning 1

# Machine learning is a technique for learning patterns in data that enable computers to make decisions and predictions. It's probably one of the hottest skills to master as a scientist or engineer in research or industry today. This week, we'll get an overview of what machine learning is, what it can be used for and what its limits are. Without worrying too much about what goes on behind the scenes, we will play around with a few classifiers in Python and test model performance using cross validation. The exercises today cover:
# 
# * Feature representation
# * Model fitting
# * Model evaluation
# * Prediction results
# 

# ## Exercises

# We want to predict whether a character is a hero or a villain from information that we can extract from their markup. This is a large problem that includes some data wrangling, model fitting and a bit of evaluation. Therefore the problem is split into parts.

# ### Part 1: Feature representation
# In it's raw format, the data cannot be given to a machine learning algorithm. What we must do is extract features from the data and put them into a structured format. This is the same as what we did when we looked at a dog (the data) and extracted into a matrix whether it was fluffy, sad looking, etc. (the features). The feature we will extract here is **team alliances**.
# 
# We can represent the team alliances of each character as a row in a matrix where each column corresponds to a particular team. That should look something like this (numbers are made up):
# 
# <img src="http://ulfaslak.com/computational_analysis_of_big_data/exer_figures/example_boa.png" width="400"/>
# 
# **Note**: The following exercises relies on the dataset you produced in Ex. 3.1.2 (character markup stored on your computer). If you didn't manage to produce the dataset [use mine](https://github.com/ulfaslak/computational_analysis_of_big_data_2018_fall/tree/master/data) and go back and complete it at a later time so that you get the most out of this session.

# > **Ex.4.1.1**: Write a function called `get_alliances` that takes the name of a character and returns a list of teams that the character is allied with. Print the alliances of Iron Man.
# 
# *Hint: There is a place in the character markup where you'll find the team affiliations and you want to write some code that can extract that. The affiliations are not always listed the same way so you should probably try to eyeball some of the documents to get a feel of how the formatting can look.

# In[7]:


from collections import defaultdict
import os
import numpy as np
import re


#re.findall(r"\d{4}\)", re.findall(r"debut.+?\n", lines)[0])[0][:-1]

# \d{4} is matches a digit exactly 4 in length, \D matches non-digit
# . is matches any character EXCEPT newline (\n)
# ? matches the preceding pattern element zero or one time, UNLESS:
    #Modifies the *, +, ? or {M,N}'d regex that comes before to match as few times as possible.
#\n is Matches what the nth marked subexpression matched, where n is a digit from 1 to 9.

#https://stackoverflow.com/questions/809837/python-regex-for-finding-contents-of-mediawiki-markup-links

def getAlly(file):
    #Handle no alliance.
    try:
        temp = []
        f = open(file, 'r')
        lines = f.read()
        #REGEX THAT GRABS ALLIANCES
        #CLOSE#ally = re.findall(r"=(.*)",re.findall(r"alliances(.*)\n",lines)[0])
        #NOPE#ally = re.findall(r"\[\[([\w ]+)(?:\|[\w ]+)?\]\]", re.findall(r"alliances=.+?\n",lines)[0])
        #NOPE#ally = re.findall(r"\[\[([\w ]+)(\|[\w ]+)?\]\]",re.findall(r"alliances.+?\n",lines)[0])
        
        ally = re.findall(ur"\[\[(.+?)\]\]", re.findall(r"alliances.+?\n",lines)[0])
        
        #BASIC#ally = re.findall(r"alliances.+?\n",lines)
        
        if len(ally) == 0:
            ally = re.findall(r"=(.*)",re.findall(r"alliances(.*)\n",lines)[0])
            #print "ally :%r AND length:%r" %(ally,len(ally))


        for a in ally:
            #Catches weird exceptions
            if (
                a == '""' or a == "''" or len(a) == 0 or a == ' ' or
                ' {{Plainlist' in a or ' <!--optional-->' in a or
               ' {{Plain list ' in a or ' <!-- optional -->' in a or
                '<!-- optional -->' in a or '{{plainlist' in a or
                ' {{plainlist' in a or '{{Plain list ' in a or "None" in a
                or 'none' in a or '{{ubl' in a
               ):
                return False
            
            #Catches extra [[ in text
            if "[[" in a:
                a = list(a)
                a.remove("[")
                a = "".join(a)
            #Catches extra info after | or #
            if "|" in a:
                a = list(a)
                i = 0
                for char in a:
                    if char == "|" or char == "#":
                        del a[i:]
                    i+=1
                a = "".join(a)
            #Catches <br> and splits
            if "<br>" in a:
                a = a.split("<br>")
                for item in a:
                    item = catch(item)
                    temp.append(item)
                return temp
            #Catches <br/> and splits
            if "<br/>" in a:
                a = a.split("<br/>")
                for item in a:
                    item = catch(item)
                    temp.append(item)
                return temp
            #Catches A.P.N.G and Gabriel mixed together
            if 'A.P.N.G., Gabriel' in a:
                a = a.split(",")
                for item in a:
                    item = catch(item)
                    temp.append(item)
                return temp
            
            #Catches elements starting/ending with a space (" ")
            a = catch(a)
            
            temp.append(a)

        f.close()

        return temp
    except:
        return False

#Initialize Lists
heroA = []
villA = []
ambA = []


#Adds alliance to list based on status of hero/villain/ambiguous


for file in os.listdir("Heroes"):
    if getAlly(os.path.join("Heroes",file)) != False:
        heroA.append(getAlly(os.path.join("Heroes",file)))



for file in os.listdir("Villains"):
    if getAlly(os.path.join("Villains",file)) != False:
        villA.append(getAlly(os.path.join("Villains",file)))
        

for file in os.listdir("Ambiguous"):
    if getAlly(os.path.join("Ambiguous",file)) != False:
        ambA.append(getAlly(os.path.join("Ambiguous",file)))

#Catches entries starting/ending with ' ' or " or '
def catch(string):
    string = list(string)
    if string[0] == ' ' and string[-1] == ' ':
        del string[0]
        del string[-1]
        string = "".join(string)
        return string
    elif string[-1] == ' ':
        del string[-1]
        string = "".join(string)
        return string
    elif string[0] == ' ':
        del string[0]
        string = "".join(string)
        return string
    elif string[0] == '\"' and string[-1] == '\"':
        del string[0]
        del string[-1]
        string = "".join(string)
    else:
        string = "".join(string)
        return string

#Creates dictionaries based on hero/villain/ambiguous status
    
ambDict = defaultdict(set)

for file in os.listdir("Ambiguous"):
    if getAlly(os.path.join("Ambiguous",file)) != False:
        for ally in ambA:
            for name in ally:
                ambDict[name].add(file)

heroDict = defaultdict(set)

for file in os.listdir("Heroes"):
    if getAlly(os.path.join("Heroes",file)) != False:
        for ally in heroA:
            for name in ally:
                heroDict[name].add(file)

villDict = defaultdict(set)

for file in os.listdir("Villains"):
    if getAlly(os.path.join("Villains",file)) != False:
        for ally in villA:
            for name in ally:
                villDict[name].add(file)
                
#Creates comprehensive dictionary of all heroes, villains, and ambiguous characters
allDict = defaultdict(set)

for file in os.listdir("Ambiguous"):
    if getAlly(os.path.join("Ambiguous",file)) != False:
        for ally in ambA:
            for name in ally:
                allDict[name].add(file)

for file in os.listdir("Heroes"):
    if getAlly(os.path.join("Heroes",file)) != False:
        for ally in heroA:
            for name in ally:
                allDict[name].add(file)

for file in os.listdir("Villains"):
    if getAlly(os.path.join("Villains",file)) != False:
        for ally in villA:
            for name in ally:
                allDict[name].add(file)
#Deletes unncessary keys
#del allDict['']

print getAlly(os.path.join("Heroes","Iron Man.txt"))


# > **Ex.4.1.2**: Produce a sorted list called `all_teams` that contains all teams in the entire Marvel universe. Print the first 10.

# In[10]:


#Deletes blank key that is sometimes generated (needs commented out if not needed)
#del allDict['']


#Uses allDict that contains all teams and characters to get list of all teams
all_teams = list(allDict.keys())
all_teams.sort()
#print all_teams[0:10]
allDict['Horror-Hunters'] = allDict['"Horror-Hunters"']
del allDict['"Horror-Hunters"']
all_teams.sort()
print all_teams[0:10]


# > **Ex.4.1.3**: Write a function that takes the name of a character and returns a vector representation of the team alliances for that character. The length of the returned list will be `len(all_teams)` and have 0s in the places corresponding to teams that the character is not on, and 1s in the places corresponding to teams the character is on. Print the sum of the list returned when the input to the function is Iron man.

# In[11]:


import numpy as np
import math

def vect(char):
    vectList = np.zeros(len(all_teams),dtype=int)
    charTeam = getAlly(char)
    for team in all_teams:
        if team in charTeam:
            vectList[all_teams.index(team)] += 1
            #get indice of team and change it in vertList
            
    return vectList
    
t = vect(os.path.join("Heroes","Iron Man.txt"))
print t.sum()


# > **Ex. 4.1.4**: Create the team alliance matrix for the data. This is your feature matrix for the classification problem you will solve later in this exercise set. Therefore, you should also—in a seperate *target* array—store whether characters are heros (denote by 1) or villains (denote by 0). For now, skip ambiguous characters, but write your code in such a way that it won't be too hard to redo this for ambiguous characters. Skip characters that have no team alliances. Print the shapes of your matrix and target array.

# In[12]:


import os

#initialize list of all teams
team_alliance = []
char_type = []

#goes through all hero teams, skips those without a team
for x in os.listdir("Heroes"):
    if getAlly(os.path.join("Heroes",x))!= False:
        temp = vect(os.path.join("Heroes",x))
        if (temp.sum() > 0):
            team_alliance.append(vect(os.path.join("Heroes",x)))
            char_type.append(1)

#goes through all villain teams, skips those without a team
for y in os.listdir("Villains"):
    if getAlly(os.path.join("Villains",y)) != False:
        temp = vect(os.path.join("Villains",y))
        if temp.sum() > 0:
            team_alliance.append(vect(os.path.join("Villains",y)))
            char_type.append(0)

#goes through all ambiguous teams, skips those without a team
# for z in os.listdir("Ambiguous"):
#     if getAlly(os.path.join("Ambiguous",z)) != False:
#         temp = vect(os.path.join("Ambiguous",z))
#         if temp.sum() > 0:
#             team_alliance.append(vect(os.path.join("Ambiguous",z)))
#             char_type.append(2)

team_alliance = np.matrix(team_alliance, dtype=int)
char_type = np.array(char_type, dtype=int)
print(team_alliance[0:2])
print(char_type[0:2])


# ### Part 2: Model fitting

# > **Ex. 4.2.1**: Train a classifier on all of your data and test its accuracy.
# 
# >* If your team alliance matrix is `X_ta` and your target array is `y_ta` you can do this by instantiating a model like:
# >
#         from sklearn.naive_bayes import BernoulliNB
#         model = BernoulliNB()
#         model.fit(X_ta, y_ta)  # <--- This is the training/fitting/learning step
#         
# > The `BernoulliNB` is a version of the Naive Bayes classifier which associates certain features with labels and asks what the probability of a label for a data point is given its features. You are free to use any other classifier if you want. Popular ones are trees, random forests, support vector machines, feed forward neural networks, logistic regression, and the list goes on. With `sklearn`, they are just as easy to employ as the `BernoulliNB` classifier.
# 
# 
# >1. Test the accuracy of your model. You can use the `.predict` method on the `model` object to get predictions for a matrix of data points. Report the accuracy of your model on the same data that you trained the model on, alongside the baseline accuracy of a "dumb" model that only guesses for the majority class.
# 
# >2. Report the precision, recall and F1 scores, with respect to the minority class (heroes). `sklearn` has implementations that you can use if you are short for time. Extra credit for doing it using only basic linear algebra operations with `numpy`, though.

# In[32]:


import random
import numpy as np

from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score


guess = [random.randint(0,1) for _ in range(len(char_type))]

model = BernoulliNB()
model.fit(team_alliance,char_type)
model.predict(team_alliance)

print "Accuracy for training is: %r" %accuracy_score(char_type, model.predict(team_alliance))
print "Accuracy for guessing is: %r" %accuracy_score(char_type, guess)

print "Recall score is: %r" %recall_score(char_type,model.predict(team_alliance))
print "Precison score is: %r" %precision_score(char_type,model.predict(team_alliance))
print "F1 Score is: %r" %f1_score(char_type,model.predict(team_alliance))


# ### Part 3: Model evaluation

# > **Ex. 4.3.1**: Investigate how well your model generalizes. You may have noticed that the performance seemed a little too good to be true in Ex 4.2.1.
# 1. Why did you get such a high accuracy in the previous exercise?
# 
# High accuracy in prediction happened because we were testing on the training data in full. This has a small training and a small testing error.
# 
# 2. Split your data into a test and training set of equal size. Train the model only on the training set and report its accuracy and F1 scores (for both classes) on both the training and test sets.
# 3. Comment on the difference you observe.
# 
# > *Hint: Watch out for unbalanced class proportions! You may want to randomly reorder the rows of your datapoints and target labels so your training and test sets have the same amount of heroes and villains.*

# In[ ]:


from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score





# > **Ex. 4.3.2**: Implement cross validation. The performance of a classifier is strongly dependent on the amount of data it is trained on. In Ex. 4.3.1 you train it on only half of the data and test it on the other half. If you rerun that code multiple times, with random 50/50 partitions, you are gonna see a lot of uncertainty in performance. Cross validation solves this problem by training on a larger subset of the data and testing on a smaller one, and taking the average performance over K-folds of this process.
# 1. Implement cross validation over $K=10$ folds. For each fold you must record the training and test accuracies. In the end, visualize the distributions of test- and training accuracy as histograms in the same plot. It's important that you comment on the result.

# In[ ]:





# ### Part 4: Predicting good vs. evil

# >**Ex. 4.4.1**: Let's put our classifier to use!
# * Retrain your model on all of your data.
# * Create a team alliance representation of the ambiguous characters
# * Use the model the estimate the probability that each character is a villain (let's call this *villainness*). You can use the `.predict_proba` method on the model to get probability estimates rather than class assignments.
# * **Visualize the "heroness" distribution for all ambiguous characters**. Comment on the result.

# In[ ]:




