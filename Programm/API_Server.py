#!/usr/bin/env python
# coding: utf-8

# In[37]:


import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
#nltk.download('wordnet')
from nltk.corpus import wordnet #wornet loaded
import re
import json
from flask import Flask,render_template, request, redirect, url_for
#app = Flask(__name__)
from flask import jsonify, current_app

#Methode definition
def get_synsets(w):
    syns = wordnet.synsets(w)
    return syns

def get_definitions(syns):
    return syns.definition()

def get_label(syns):
    lemmas = syns.lemmas()
    name = lemmas[0].name()
    return name

def get_source(syns):
    return syns.lexname()

def get_offset(w,text):
    offset = text.index(w)
    return offset

def stop_words_filtering(text):
    reg_exp = r"[a-zA-Z0-9]+"
    #stop_words = []
    stop_words = set(stopwords.words('english')) #stopwords just for englisch text
    word_tokens= []
    b = []
    a = re.compile(reg_exp)
#example = "Pet food for shoes and fabric"    
        
    b = b + a.findall(text)     
    filtered_sentence =  [w for w in b if not w in stop_words] 
    filtered_sentence = [] 
    for w in b: #just filtern stopword in a text
        if w not in stop_words: 
            filtered_sentence.append(w)           
    return filtered_sentence 

#def add_elementToRessourcedict(word, ressourcedict):
def build_ressources_candidates(word):
    ressourcedict = {}
    synsets = get_synsets(word)
    i = 1
    for syns in synsets:
        ressourcedict["Candidate"+str(i)]                = {}
        ressourcedict["Candidate"+str(i)]["synset_id"]   = i
        ressourcedict["Candidate"+str(i)]["source"]      = get_source(syns)
        ressourcedict["Candidate"+str(i)]["label"]       = get_label(syns)
        ressourcedict["Candidate"+str(i)]["description"] = get_definitions(syns)
        i=i+1
    return ressourcedict


# In[38]:


def build_annot_candidates(text):
    annotDict = {}
    Woerter = stop_words_filtering(text)
    j=1
    for w in Woerter:
        annotDict["Annot"+ str(j)]                         = {}
        annotDict["Annot"+str(j)]["offset"]                = get_offset(w,text)
        annotDict["Annot"+str(j)]["text"]                  = w
        annotDict["Annot"+str(j)]["ressources_candidates"] = build_ressources_candidates(w)
        j=j+1
    return annotDict
    


# In[ ]:





# In[ ]:


app = Flask(__name__)

@app.route('/')
def index():
  return 'Server Works done!'
    
@app.route('/annotApi/<string:text>')
def annotsFunction2(text):
    annotation = build_annot_candidates(text)
    return json.dumps(annotation)

    
if __name__ == '__main__':
    with app.app_context():
   # app.debug = True
        from werkzeug.serving import run_simple
        run_simple('localhost', 5001, app)


# In[ ]:




