#!/usr/bin/env python
# coding: utf-8

# # Week 3: Getting data—scraping and APIs.

# This week is about getting data from the big ol' Internet, with the Wikipedia as our guinea pig. The main task today is to retrieve the Wikipedia pages of **all Marvel characters** using the MediaWiki **API**. There are three parts to this exercise.
# 
# * Learn the basics of how to retrieve data from Wiki sites using the MediaWiki API
# * Download all Marvel character Wikipedia articles
# * Explore the data
# 
# The data you acquire today, you will be working with for the remainder of the course. Try to get as far as possible, structure the data nicely and write your code so that it makes sense to you in the coming weeks.
# 
# **Advice:** There's an important practice I want you to adopt. It matters in grading. 
# 1. Comment on your approach. It can be code comments or text in a markdown cell below/above the code cell.
# 2. Comment on your results. Discuss:
#     * Do they make sense in relation to what I know about the world?
#     * Is my result what I expected? If not, what is the surprising thing? Is it interesting?
#     * What—interesting or not—insight does my result reveal about the thing I'm analyzing?
# 


# ## Exercises

# **Why use an API?** You could just go ahead and scrape the HTML from a Wikipedia page as simple as:
# 
#     import requests as rq
#     rq.get("https://en.wikipedia.org/wiki/Batman").text
#     
# Well... to navigate data in XML format is not always easy. Therefore, MediaWiki offers its users direct use of its API. To load the MediaWiki markup using the API, one would do something like:
# 
#     rq.get("https://en.wikipedia.org/w/api.php?format=json&action=query&titles=Batman&prop=revisions&rvprop=content").json()
#     
# This returns a JSON object inside which you can find all sorts of information about the page, including the latest revision of the Batman page markup.

# **Helpful code to display JSON object as a tree**

# You learned to "key" into a JSON object in the previous weeks, and maybe you had the thought that these objects were kind of like "trees" in that you enter one branch, which then has multiple branches you can enter and so on. Well to make the exploration of foreign JSON objects easier for you, I wrote some code below that displays a JSON object as a tree. **I put an error inside on purpose**; try to understand what's happening in the code, fix it, and use it if you need it.

# In[24]:


def printJsonTree(d, indent=0):
    """Print tree of keys in JSON object.
    
    Prints the different levels of nested keys in a JSON object. When there
    are no more dictionaries to key into, prints objects type and byte-size.

    Input
    -----
    d : dict
    """
    for key,value in d.items():
        print("\t"*indent + str(key),end=" ")
        if isinstance(value, dict):
            print(); printJsonTree(value, indent+1)
        else:
            print(": " + str(type(d[key])).split("'")[1] + " - " + str(len(str(d[key]))))

def print_json_tree(d, indent=0):
    """Print tree of keys in JSON object.
    
    Prints the different levels of nested keys in a JSON object. When there
    are no more dictionaries to key into, prints objects type and byte-size.

    Input
    -----
    d : dict
    """
    for key,value in d.iteritems():
        print('    ' * indent + unicode(key)),
        if isinstance(value, dict):
            print; print_json_tree(value, indent+1)
        else:
            print(":", str(type(d[key])).split("'")[1], "-", str(len(unicode(d[key]))))
            
# Example
import requests as rq
data = rq.get("https://en.wikipedia.org/w/api.php?format=json&action=query&titles=Batman&prop=revisions&rvprop=content").json()
printJsonTree(data)


# This is what you can expect the output will look like if you made the function work (can you figure out how to read it?):

#     batchcomplete : unicode - 0
#     query
#         pages
#             4335
#                 ns : int - 1
#                 pageid : int - 4
#                 revisions : list - 141926
#                 title : unicode - 6
#     warnings
#         main
#             * : unicode - 267
#         revisions
#             * : unicode - 163

# ### Part 0: Learn to access Wikipedia data with Python

# Figure out how Wikipedia markup works .You'll need to know a bit about formatting of MediaWiki pages so that you can parse the markup that you retrieve from wikipedia. See http://www.mediawiki.org/wiki/Help:Formatting. In particular, look into how links work and how tables work and make sure you can answer the following questions.

# >**Ex. 3.0.1**: How do you link to another Wikipedia page from within a Wikipedia-page, using the wikimedia markup? Write down a simple example that links to a specific section in another page.
# 
# Interwiki links are abbreviations for longer external links that do not necessarily need to be Wiki pages.

# For example, to link to https://en.wikipedia.org/wiki/Helianthus, one can write [[w:Sunflower]]
#     that will link to https://en.wikipedia.org/wiki/Helianthus

# > **Ex. 3.0.2**: What is the MediaWiki markup to create a simple table like the one below?
# 
# >| True Positive  | False Positive |
# | -------------- |:--------------:|
# | False Negative | True Negative  |

# {|
# 
# ! True Positive || False Positive
# 
# |-
# 
# | False Negative || True Negative
# 
# |}
# 

# > **Ex. 3.0.3**: Figure out how to download pages from Wikipedia. Familiarize yourself with [the API](http://www.mediawiki.org/wiki/API:Main_page) and learn how to extract the markup. The API query that returns the markup of the Batman page is:
#     
# >`api.php?format=json&action=query&titles=Batman&prop=revisions&rvprop=content`
# 
# >1. Explain the structure of this query. What are the parameters and arguments and what do they mean? What happens if you remove `rvprop=content`?
# 2. Download the Batman page data from the API. Extract the markup from the JSON object and save it to a file called "batman.txt".

# 1) The structure of the query is given in a [field=value] or [action=query] section of the url with an ampersand (&) to separate each field/value pair. This url asks for the api through php and asks for the format to be json and passes other arguments like the title of the page requested and the prop is the property of data about a list of pages. The prop=revisions gets the revision ID, while rvprop gets the content.

# In[25]:


import requests as rq
import json
sample = rq.get("https://en.wikipedia.org/w/api.php?format=json&action=query&titles=Batman&prop=revisions&rvprop=content").json()
with open("batman.txt","w", encoding='utf8') as outfile:
    json.dump(sample, outfile)


# ### Part 1: Get data (main part)

# For a good part of this course we will be working with data from Wikipedia. Today, your objective is to crawl a large dataset with good and bad characters from the Marvel characters.

# >**Ex. 3.1.1**: From the Wikipedia API, get a list of all Marvel superheroes and another list of all Marvel supervillains. Use 'Category:Marvel_Comics_supervillains' and 'Category:Marvel_Comics_superheroes' to get the characters in each category.
# 1. How many superheroes are there? How many supervillains?
# 2. How many characters are both heroes and villains? What is the Jaccard similarity between the two groups?
# 
# >*Hint: Google something like "get list all pages in category wikimedia api" if you're struggling with the query.*

# In[26]:


hero1 = rq.get("https://en.wikipedia.org/w/api.php?action=query&format=json&list=categorymembers&cmtitle=Category:Marvel_Comics_superheroes&cmlimit=500").json()
hero2 = rq.get("https://en.wikipedia.org/w/api.php?action=query&format=json&list=categorymembers&cmtitle=Category:Marvel_Comics_superheroes&cmlimit=500&cmcontinue=page|41394d4d042941314b392d2904098c41292f313f394331043b45592d31098e012101dcc2dcbedcbedc09|1375758").json()
numHeros = len(hero1['query']['categorymembers'])+len(hero2['query']['categorymembers'])
villain1 = rq.get("https://en.wikipedia.org/w/api.php?action=query&format=json&list=categorymembers&cmtitle=Category:Marvel_Comics_supervillains&cmlimit=500").json()
villain2 = rq.get("https://en.wikipedia.org/w/api.php?action=query&format=json&list=categorymembers&cmtitle=Category:Marvel_Comics_supervillains&cmlimit=500&cmcontinue=page|3b292d3d044509683f29434f314b4304098c41294b53313f042d4541392d4d098e03063b292d3d044509683f29434f314b4304098c41294b53313f042d4541392d4d098e01252001dcc2dcbcdcc0dcbfdcc2dcc5dcbedcc0dc0a|2256172").json()
villain3 = rq.get("https://en.wikipedia.org/w/api.php?action=query&format=json&list=categorymembers&cmtitle=Category:Marvel_Comics_supervillains&cmlimit=500&cmcontinue=page|4d4543352b394b2f04098c2d4541392d4d098e03064d4543352b394b2f04098c2d4541392d4d098e01250601dcbddcbfdc14|2114226").json()
numVillains = len(villain1['query']['categorymembers'])+len(villain2['query']['categorymembers'])+len(villain3['query']['categorymembers'])
print("The number of superheroes in Marvel is: %r" %numHeros)
print("The number of supervillains in Marvel is: %r" %numVillains)


# In[27]:


h = []
v = []
a = []

#HERO
for k in range(len(hero1['query']['categorymembers'])):
    if hero1['query']['categorymembers'][k] not in h:
        h.append(hero1['query']['categorymembers'][k])

for i in range(len(hero2['query']['categorymembers'])):
    if hero2['query']['categorymembers'][i] not in h:
        h.append(hero2['query']['categorymembers'][i])


#VILLAIN
for k in range(len(villain1['query']['categorymembers'])):
    if villain1['query']['categorymembers'][k] not in v:
        v.append(villain1['query']['categorymembers'][k])

for i in range(len(villain2['query']['categorymembers'])):
    if villain2['query']['categorymembers'][i] not in v:
        v.append(villain2['query']['categorymembers'][i])
    
for j in range(len(villain3['query']['categorymembers'])):
    if villain3['query']['categorymembers'][j] not in v:
        v.append(villain3['query']['categorymembers'][j])

#AMBIGUOUS
for item in h:
    if item in v:
        a.append(item)
#REMOVE AMBIGUOUS FROM HERO/VILLAIN
for thing in a:
    if thing in h:
        h.remove(thing)
    if thing in v:
        v.remove(thing)


# In[28]:


allHero = []

for i in range(len(hero1['query']['categorymembers'])):
    allHero.append(hero1['query']['categorymembers'][i]['title'])
for j in range(len(hero2['query']['categorymembers'])):
    allHero.append(hero2['query']['categorymembers'][j]['title'])
    
allVillain = []

for k in range(len(villain1['query']['categorymembers'])):
    allVillain.append(villain1['query']['categorymembers'][k]['title'])
for l in range(len(villain2['query']['categorymembers'])):
    allVillain.append(villain2['query']['categorymembers'][l]['title'])
for m in range(len(villain3['query']['categorymembers'])):
    allVillain.append(villain3['query']['categorymembers'][m]['title'])
    

both = len(set(allHero) & set(allVillain))
print("The number of characters who are both heros and villains is: %r" %both)
intersection = len(list(set(allHero) & set(allVillain)))
union = len(list(set().union(allHero,allVillain)))
jaccard = float(intersection)/union
print("The Jaccard Similiarity is: %r" %jaccard)
print("The true number of heros is: %r" %(len(h)))
print("The true number of villains is: %r" %len(v))


# >**Ex. 3.1.2**: Using this list you now want to download all data you can about each character. However, because this is potentially Big Data, you cannot store it your computer's memory. Therefore, you have to store it in your harddrive somehow. 
# * Create three folders on your computer, one for *heroes*, one for *villains*, and one for *ambiguous*.
# * For each character, download the markup on their pages and save in a new file in the corresponding hero/villain/ambiguous folder.
# 
# >*Hint: Some of the characters have funky names. The first problem you may encounter is problems with encoding. To solve that you can call `.encode('utf-8')` on your markup string. Another problem you may encounter is that characters have a slash in their names. This, you should just replace with some other meaningful character.*

# In[7]:


import os #ONLY RUN ONCE to create directories
#os.mkdir("Heroes")
#os.mkdir("Villains")
#os.mkdir("Ambiguous")


# In[ ]:



#print h[0]['title'].encode('utf-8')
#print h[0]['pageid']


# wh = (rq.get("https://en.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&rvprop=content&rvslots=main&pageids=2388262").json())
# print wh['query']['pages']['2388262']['revisions'][0]['slots']['main']['*'].encode('utf-8')


# TESTING --SUCCESS!
# with open(str(h[0]['title'].encode('utf-8')) + ".txt", "w") as test:
#     data = (rq.get("https://en.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&rvprop=content&rvslots=main&pageids=2388262").json())
#     test.write(str(data['query']['pages']['2388262']['revisions'][0]['slots']['main']['*'].encode('utf-8')))
# test.close()
# t = open("Abigail Brand.txt","r")
# tr = t.read()
# print tr
# t.close()
# path = os.path.join("Heroes", str(h[0]['title'].encode('utf-8')) + ".txt")
# f = open(path,"w")
# f.write("TEST")
# f.close()

#WRITES HERO FILES
for i in range(len(h)):
    temp = str(h[i]['title'].encode('utf-8'))
    pid = str(h[i]['pageid'])
    for char in temp:
        if char in "\\/\"\'":
            temp = temp.replace(char,"-")
    
    path = os.path.join("Heroes", temp + ".txt")
    f = open(path,"w")
    data = (rq.get("https://en.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&rvprop=content&rvslots=main&pageids=" + pid).json())
    f.write(str(data['query']['pages'][pid]['revisions'][0]['slots']['main']['*'].encode('utf-8')))
    f.close()
#WRITES VILLAIN FILES
for i in range(len(v)):
    temp = str(v[i]['title'].encode('utf-8'))
    pid = str(v[i]['pageid'])
    for char in temp:
        if char in "\\/\"\'":
            temp = temp.replace(char,"-")
    
    path = os.path.join("Villains", temp + ".txt")
    f = open(path,"w")
    data = (rq.get("https://en.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&rvprop=content&rvslots=main&pageids=" + pid).json())
    f.write(str(data['query']['pages'][pid]['revisions'][0]['slots']['main']['*'].encode('utf-8')))
    f.close()
#WRITES AMBIGUOUS FILES
for i in range(len(a)):
    temp = str(a[i]['title'].encode('utf-8'))
    pid = str(a[i]['pageid'])
    for char in temp:
        if char in "\\/\"\'":
            temp = temp.replace(char,"-")
    
    path = os.path.join("Ambiguous", temp + ".txt")
    f = open(path,"w")
    data = (rq.get("https://en.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&rvprop=content&rvslots=main&pageids=" + pid).json())
    f.write(str(data['query']['pages'][pid]['revisions'][0]['slots']['main']['*'].encode('utf-8')))
    f.close()


# ### Part 2: Explore data

# #### Page lengths

# >**Ex. 3.2.1**: Extract the length of the page of each character, and plot the distribution of this variable for each class (heroes/villains/ambiguous). Can you say anything about the popularity of characters in the Marvel universe based on your visualization?
# 
# >*Hint: The simplest thing is to make a probability mass function, i.e. a normalized histogram. Use `plt.hist` on a list of page lengths, with the argument `normed=True`. Other distribution plots are fine too, though.*

# In[36]:


import numpy as np
import matplotlib
import matplotlib.pyplot as plt

len_hero = []
len_villain = []
len_ambiguous = []
#Gets lengths of page EXCLUDING blank lines
def numLines(file):
    count = 0
    with open (file) as f:
        for line in f:
            if line != '\n' or line != "":
                count += 1
    return count
#GET HERO PAGE LENGTHS
for i in range(len(h)):
    temp = str(h[i]['title'].encode('utf-8'))
    for char in temp:
        if char in "\\/\"\'":
            temp = temp.replace(char,"-")
    path = os.path.join("Heroes", temp + ".txt")
    len_hero.append(numLines(path))
#GET VILLAIN PAGE LENGTHS
for k in range(len(v)):
    temp = str(v[k]['title'].encode('utf-8'))
    for char in temp:
        if char in "\\/\"\'":
            temp = temp.replace(char,"-")
    path = os.path.join("Villains", temp + ".txt")
    len_villain.append(numLines(path))
#GET AMBIGUOUS PAGE LENGTHS
for j in range(len(a)):
    temp = str(a[j]['title'].encode('utf-8'))
    for char in temp:
        if char in "\\/\"\'":
            temp = temp.replace(char,"-")
    path = os.path.join("Ambiguous", temp + ".txt")
    len_ambiguous.append(numLines(path))
    


plt.hist(len_hero, density=True)
plt.title("Hero Page Lengths")
plt.ylabel("Percent of Articles")
plt.xlabel("Page Length")
plt.show()

plt.hist(len_villain, density=True)
plt.title("Villain Page Lengths")
plt.ylabel("Percent of Articles")
plt.xlabel("Page Length")
plt.show()

plt.hist(len_ambiguous, density=True)
plt.title("Ambiguous Page Lengths")
plt.ylabel("Percent of Articles")
plt.xlabel("Page Length")
plt.show()


# >**Ex. 3.2.2**: Find the 10 characters from each class with the longest Wikipedia pages. Visualize their page lengths with bar charts. Comment on the result.

# In[48]:


len_hero.sort(reverse=True)
print len_hero[0:10]
len_villain.sort(reverse=True)
print len_villain[0:10]
len_ambiguous.sort(reverse=True)
print len_ambiguous[0:10]

length = [1,2,3,4,5,6,7,8,9,10]

plt.bar(length,len_hero[0:10])
plt.title("10 Longest Hero Page Lengths")
plt.ylabel("Length of Page")
plt.xlabel("Page")
plt.show()

plt.bar(length,len_villain[0:10])
plt.title("10 Longest Villain Page Lengths")
plt.ylabel("Length of Page")
plt.xlabel("Page")
plt.show()

plt.bar(length,len_ambiguous[0:10])
plt.title("10 Longest Ambiguous Page Lengths")
plt.ylabel("Length of Page")
plt.xlabel("Page")
plt.show()


# #### Timeline

# >**Ex. 3.2.3**: We are interested in knowing if there is a time-trend in the debut of characters.
# * Extract into three lists, debut years of heroes, villains, and ambiguous characters.
# * Do all pages have a debut year? Do some have multiple? How do you handle these inconsistencies?
# * For each class, visualize the amount of characters introduced over time. You choose how you want to visualize this data, but please comment on your choice. Also comment on the outcome of your analysis.
# 
# >*Hint: The debut year is given on the debut row in the info table of a character's Wiki-page. There are many ways that you can extract this variable. You should try to have a go at it yourself, but if you are short on time, you can use this horribly ugly regular expression code:*
# 
# >*`re.findall(r"\d{4}\)", re.findall(r"debut.+?\n", markup_text)[0])[0][:-1]`*

# In[56]:


import re
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from collections import Counter


heroYear = []
villainYear = []
ambiguousYear = []

def getYear(file):
    #Handle no debut date.
    try:
        f = open(file, 'r')
        lines = f.read()
        year = re.findall(r"\d{4}\)", re.findall(r"debut.+?\n", lines)[0])[0][:-1]
        f.close()
        return year
    except:
        return False
##

for file in os.listdir("Heroes"):
    if getYear(os.path.join("Heroes",file)) != False:
        heroYear.append(getYear(os.path.join("Heroes",file)))
for file in os.listdir("Villains"):
    if getYear(os.path.join("Villains",file)) != False:
        villainYear.append(getYear(os.path.join("Villains",file)))
for file in os.listdir("Ambiguous"):
    if getYear(os.path.join("Ambiguous",file)) != False:
        ambiguousYear.append(getYear(os.path.join("Ambiguous",file)))
        
heroYear.sort()
villainYear.sort()
ambiguousYear.sort()

countHero = Counter(heroYear)
countVill = Counter(villainYear)
countAmb = Counter(ambiguousYear)


hList = sorted(countHero.keys())
hValues = []
for item in hList:
    hValues.append(countHero[item])
    
vList = sorted(countVill.keys())
vValues = []
for thing in vList:
    vValues.append(countVill[thing])

aList = sorted(countAmb.keys())
aValues = []
for item in aList:
    aValues.append(countAmb[item])
    
aList = list(aList)
aList = [int(i) for i in aList]
hList = list(hList)
hList = [int(j) for j in hList]
vList = list(vList)
vList = [int(k) for k in vList]


plt.plot(aList,aValues)
plt.title("Ambiguous Debuts")
plt.ylabel("Number of Debuts")
plt.xlabel("Year of Debut")
plt.show()


plt.plot(np.array(hList),np.array(hValues))
plt.title("Hero Debuts")
plt.ylabel("Number of Debuts")
plt.xlabel("Year of Debut")
plt.show()


plt.plot(np.array(vList),np.array(vValues))
plt.title("Villain Debuts")
plt.ylabel("Number of Debuts")
plt.xlabel("Year of Debut")
plt.show()


# #### Alliances

# >**Ex. 3.2.4**: In this exercise you want to find out what the biggest alliances in the Marvel universe are. The data you need for doing this is in the *alliances*-field of the markup of each character. Below I suggest steps you can take to solve the problem if you get stuck.
# * Write a regex that extracts the *alliances*-field of a character's markup.
# * Write a regex that extracts each team from the *alliance*-field.
# * Count the number of members for each team (hint: use a `defaultdict`).
# * Inspect your team names. Are there any that result from inconsistencies in the information on the pages? How do you deal with this?
# * **Print the 10 largest alliances and their number of members.**

# In[3]:


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
            #Catches very weird exception of empty array with len of 1 somehow
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

#Catches entries starting/ending with ' '
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
del allDict['']


#function that gets n largest alliances given dictionary, string is title of 
    #character type (HERO, VILLAIN, AMBIGUOUS, ALL, ETC...)
def getNLargeAlly(num, dct, string):
    n = 0
    while n < num:
        index = []
        length = []
        for key in dct:
            length.append(len(dct[key]))
        temp = sorted(length)
        i = 0
        #print temp[-num:]
        for l in length:
            if l == temp[-1]:
                index.append(i)
            i += 1
        print "Largest %r Alliances for %r Characters" %(num,string)
        for k in index:
            print "Alliance %r has %r members." % (list(dct.keys())[index[k]], len(dct[list(dct.keys())[index[k]]]))
            n += 1
            if n > num:
                break
    return

getNLargeAlly(10,heroDict,"Heroes")
getNLargeAlly(10,villDict,"Villains")
getNLargeAlly(10,ambDict,"Ambiguous")
getNLargeAlly(10,allDict,"All")
        
