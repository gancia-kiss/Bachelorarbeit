#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import nltk
#from nltk.corpus import stopwords
#from nltk.tokenize import word_tokenize 
#nltk.download('wordnet')
from nltk.corpus import wordnet #wornet loaded
import plotly.figure_factory as ff
import numpy as np
#import re


def get_hypernym(syns):
    hypernymList = []
    paths = wordnet.synset(syns).hypernym_paths() #all Hypernym extract
    for weg in paths:
        hypernymList = hypernymList + [synset.name() for synset in weg]
   # print(hypernymList)
    hypernymList = list(dict.fromkeys(hypernymList )) #remove duplicate
    return hypernymList
def get_directhypernym(syns):
    hypernymList = [hyp.name() for hyp in  wordnet.synset(syns).hypernyms()]
    return hypernymList


# In[2]:


get_directhypernym("wheeled_vehicle.n.01")


# In[18]:


def get_synsetsList(ideen):
    synsetsDict  = {}
    for idee in ideen_list:  #jeder idee durchlaufen
        annotiert = idee.get("annotations")
        if annotiert :
            for candidate in idee['annotations']: #word in eine idee  
                if candidate['validated'] == True: #wenn diese word annotiert ist
                    for resources in candidate['resource_candidates']: #annotation candidates durchlaufen
                        if resources["selected"] == True: #wenn ein kandidates ausgewählt ist
                            if not synsetsDict.get(resources["source"]): #wenn diese synsets noch nicht existiert
                                synsetsDict[resources["source"]] = []  # fügt diese synsets in synsetList
                                synsetsDict[resources["source"]].append(idee['id']) #fügt die idee_id die diese synset beinhaltet
                            else:
                                synsetsDict[resources["source"]].append(idee['id']) #idee_id einfügen           
                    #print(synsets)
                else:
                    print("not choice")
        else:
            print("candidate was not annotiert")
    return synsetsDict
def get_hypernymDict(ideen_list,synsetsDict):
    hypernymDict = {}
    #for idee in ideen_list:  #jeder idee durchlaufen 
    for key in synsetsDict.keys(): #hypernym von jeder synsets builden
            hypernymList = get_hypernym(key)
            for hypernym in hypernymList:
                if not hypernymDict.get(hypernym): #wenn das Hypernym noch nicht existiert
                    hypernymDict[hypernym]= []
                    hypernymDict[hypernym].extend(synsetsDict[key]) #alle idee_id in der zugehörigen hypernym einfügen
                    #get_hypernym(key)
                #break
                else: #sonst fügt die idee id nur
                    hypernymDict[hypernym].extend(synsetsDict[key])
                hypernymDict[hypernym] = list(dict.fromkeys(hypernymDict[hypernym] )) #remove duplicate
                    
    return hypernymDict
                
    
   # print(key)


# In[19]:


# read file
with open('export.json', 'r') as myfile:
    data = myfile.read()

# parse file
ideen_list   = json.loads(data)
synsetsList  = get_synsetsList(ideen_list)
hypernymList = get_hypernymDict(ideen_list,synsetsList)


# In[20]:


#for key in hypernymList.keys():
    #print(len(hypernymList[key]))
for idee in ideen_list:
    for id in hypernymList['physical_entity.n.01']:
        if idee['id'] == id:
            print(idee['content'])
#print(hypernymList['entity.n.01'])


# In[21]:


#Dendrogramm
#class Node(list):
  #  def __init__(self, parent=None):
 #       self.parent = parent
    
 #   def append(self, node):
 #       if isinstance(node, Node):
  #          if node.parent == None:
 #               node.parent = self
  #          list.append(self, node)


#c1 = Node()
#c2 = Node()
#root.append(c1)
#root.append(c2)

#c2.append( Node() )


# In[22]:


#from plotly.figure_factory import create_dendrogram
#import numpy as np
#import pandas as pd
#from . import hierarchy
#import scipy
#import scipy.spatial
#from scipy.cluster import hierarchy
#from scipy.cluster.hierarchy import dendrogram, linkage
#from plotly.figure_factory import create_dendrogram
#import scipy.cluster.hierarchy as sch
#import scipy.spatial as scs
#
#from scipy import hierarchy
    
#Index = ['A','B','C','D','E','F','G','H','I','J']
#df    = pd.DataFrame(abs(np.random.randn(10, 10)), index=Index)
#fig   = create_dendrogram(df, labels=Index)
#fig.show()


# In[23]:


from anytree import Node, RenderTree
from anytree.exporter import DotExporter
# graphviz needs to be installed for the next line!
#DotExporter(udo).to_picture("udo.png")
import sys

#print('test')
def get_key(key,dictionaryTree):
    found = []
    for a in (i for i in dictionaryTree.values()):
    #for key in dictionaryTree.keys():
        if key in a:
            #print(key,a)
            found = [j for j, value in d.items() if value == a]
            #print(list(d.keys())[list(d.values()).index(key)])
            #print(found)
            #for i in found:
             #   print (i)
    return found
def build_dictionary(dictionaryTree):
    for element in dictionaryTree.copy():
        #print(element)
        if element == "entity.n.01":
            pass
        else:
            hypernymList = get_directhypernym(element)
            if not hypernymList:
                dictionaryTree["entity.n.01"].append(element)
            else:
                for hypernym in hypernymList:
                   # found = get_key(hypernym)
                    if hypernym in dictionaryTree.keys():
                        dictionaryTree[hypernym].append(element)
                    else:
                        dictionaryTree[hypernym] = []
                        dictionaryTree[hypernym].append(element)
        #else:
           # hypernym.child = b         
        #dictionaryTree[hypernym] = []
        #dictionaryTree[hypernym].append(syns)
       # hypernym = Node(hypernym,child = syns)
    # if element in testlist:
    #print testlist.index(element)
   # b = syns 
    #b = Node(syns)
     #hypernym.child = b
       # elif hypernym in (dictionaryTree[key] for key in dictionaryTree.key()):
        #elif not found:
    return dictionaryTree
    
def analyse(synsetsDict,dictionaryTree):
    
    #f = open(filename,'w')
#print >>f, 'whatever'     # Python 2.x
    #dictionaryTree["entity.n.01"] = []
    for syns in synsetsDict.keys(): #hypernym von jeder synsets builden
        if syns == "entity.n.01":
            dictionaryTree["entity.n.01"] = []
        else:
            hypernymList = get_directhypernym(syns)
            dictionaryTree["entity.n.01"] = []
            for hypernym in hypernymList:
                dictionaryTree[hypernym] = []
                dictionaryTree[hypernym].append(syns)       
    while len(dictionaryTree["entity.n.01"]) != len(synsetsDict.keys()):
        build_dictionary(dictionaryTree)
    #print(dictionaryTree)
   # print(len(dictionaryTree))
    #sys.stdout = open('file.txt', 'w+')
    #print(dictionaryTree) # Python 3.x
    return dictionaryTree
        #if (len(dictionaryTree["entity.n.01"]) != len(synsetsDict.keys())):
             #hypernym = Node(hypernym,child = syns)
        #treeset(syns,dictionaryTree)
    #for key in dictionaryTree.keys():
           # a = key+".png"
           # DotExporter(b).to_picture(a)


# In[ ]:


# read file
if __name__ == '__main__':
    dictionaryTree = {}
    with open('export.json', 'r') as myfile:
        data = myfile.read()
# parse file
    ideen_list   = json.loads(data)
    synsetsList  = get_synsetsList(ideen_list)
    #print(synsetsList.keys())
    analyse(synsetsList,dictionaryTree)
    #print(dictionaryTree["entity.n.01"])
    
#hypernymList = get_hypernymDict(ideen_list,synsetsList)


# In[ ]:





# In[ ]:




