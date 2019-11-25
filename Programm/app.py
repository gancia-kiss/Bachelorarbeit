
import sys
import json
from flask import Flask,render_template, request, redirect, url_for
app = Flask(__name__)
from flask import jsonify, current_app
# for creating the mapper code
from sqlalchemy import Column, ForeignKey, Integer, String, ARRAY, Text
from sqlalchemy.types import UserDefinedType
# for configuration and class code
from sqlalchemy.ext.declarative import declarative_base

# for creating foreign key relationship between the tables
from sqlalchemy.orm import relationship

# for configuration
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship

# create declarative_base instance
Base = Base2 = declarative_base()


#Class Definition
class Description(Base):
    __tablename__ = 'description'
    id            = Column(Integer, primary_key=True)
    annot_id      = Column(Integer, ForeignKey('annotation_candidate.id'))
    resource      = Column(String, nullable=False)
    label         = Column(String, nullable=False)
    description   = Column(String, nullable=False)
        
    def __init__(self,resource,label,description):
        self.resource    = resource
        self.label       = label
        self.description = description
    @property
    def serialize(self):
        return {
        'resource'   : self.resource,
        'label'      : self.label,
        'description': self.description,
        'annot_id'   : self.annot_id,
        'id'         : self.id,
     }
    
      
class Annotation_candidates(Base):
    __tablename__         = 'annotation_candidate'
    id                    = Column(Integer, primary_key=True)
    text                  = Column(String, nullable=False)
    offset                = Column(Integer, nullable=False)
    resources_candidates  = relationship(Description)
    
    def __init__(self,text,offset,resources_candidates):
        self.text                 = text
        self.offset               = offset
        self.resources_candidates = resources_candidates
    @property
    def serialize(self):
        return {
        'text'                 : self.text,
        'offset'               : self.offset,
        'resources_candidates' : {
                                  'resource'   : self.resources_candidates.resource,
                                  'label'      : self.resources_candidates.label,
                                  'description': self.resources_candidates.description,
                                  'annot_id'   : self.resources_candidates.annot_id,
                                   'id'         : self.resources_candidates.id,
                                  },
        'id'                   : self.id,
     }
    
# creates a create_engine instance at the bottom of the file
engine1 = create_engine('sqlite:///description.db?check_same_thread=False')
Base.metadata.create_all(engine1)

engine = create_engine('sqlite:///annotation_candidate.db?check_same_thread=False')
Base.metadata.create_all(engine)

global session1
global session

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

def build_description(resource,label,description,session1):
    descr = Description(resource = resource,label = label,description = description)
    #print(descr)
    session1.add(descr)
    session1.commit()
    session1.refresh(descr)
    #print(descr.id, descr.resource, descr.label, descr.description)
    return descr
    #return jsonify(Description=descr.serialize)

def build_annot_candidate(offset,text,resources_candidates,session):
    global Annotation_candidates
    annotation_candidate = Annotation_candidates(text = text, offset = offset, resources_candidates = resources_candidates) #ici pose probleme d'apres mon debugger un probleme de Type error. resources_candidates = resources_candidates 
    session.add(annotation_candidate)
    session.commit()
    session.refresh(annotation_candidate)
    return annotation_candidate
    #return jsonify(Annotation_candidates = annotation_candidate.serialize)



import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
#nltk.download('wordnet')
from nltk.corpus import wordnet #wornet loaded
import re

#nltk.download('stopwords')
#nltk.download('punkt')


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
#make_annotation(test.txt)
#stop_words_filtering("pet for food and fabric")

def get_description(w):
    engine1 = create_engine('sqlite:///description.db?check_same_thread=False')
    Base.metadata.bind = engine1

    DBSession = sessionmaker(bind=engine1)
    global session1
    session1  = DBSession()
    synsets = get_synsets(w)
    i = 1
    for syns in synsets:
        build_description(get_source(syns),get_label(syns),get_definitions(syns),session1)
        i = i+1
    description  = session1.query(Description).all()
    description2 = [a.serialize for a in description]
   # print (description2)
   # return description
    return description2
    #return render_template("description.html")

def get_offset(w,text):
    offset = text.index(w)
    return offset

def make_annotation(text):
    engine = create_engine('sqlite:///annotation_candidate.db?check_same_thread=False')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    global session
    session =  DBSession()
    filtered_sentence = stop_words_filtering(text)
    for word in filtered_sentence:
        build_annot_candidate(get_offset(word, text), word, get_description(word),session1)
    return 1


#api funktionen
def get_annotationCandidate():
    annotation_candidate = session1.query(Annotation_candidates).all()
    print (annotation_candidate)
    return jsonify(annotation_candidate=[a.serialize for a in annotation_candidate])


#def get_annotationCandidate(annot_id):
 #   annotation_candidate = session.query(Annotation_candidates).filter_by(id=annot_id).one()
#    return jsonify(annotation_candidate=annotation_candidate.serialize)

@app.route('/')
def index():
  return 'Server Works done!'

@app.route('/annotApi/', methods=['GET'])
def annotsFunction():
    if request.method == 'GET':
        return get_annotationCandidate()
    
@app.route('/annotApi/<string:text>')
def annotsFunction2(text):
   # if request.method == 'POST':
        #request.args.get(file = '' )
    make_annotation(text)
    return get_annotationCandidate() 

@app.route('/annotApi')
def say_hello():
  annotation_candidate = session.query(Annotation_candidate).all()
  return render_template('annotation_candidate.html', annotation_candidate=annotation_candidate)
    
if __name__ == '__main__':
    with app.app_context():
   # app.debug = True
        from werkzeug.serving import run_simple
        run_simple('localhost', 5001, app)




