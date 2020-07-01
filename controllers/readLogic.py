import os
import io
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import sys, getopt
import re

import nltk
#import numpy as np
import random
import string # to process standard python strings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings("ignore")

nltk.download('punkt') # first-time use only
nltk.download('wordnet') # first-time use only
nltk.download('words')# first-time use only

import pyrebase

firebaseConfig = {
    "apiKey" : "AIzaSyCTXm1JFbHiAqfLOHqh5IpGMzb4aYOtQV8",
    "authDomain" : "alnitekfiles.firebaseapp.com",
    "databaseURL" : "https://alnitekfiles.firebaseio.com",
    "projectId" : "alnitekfiles",
    "storageBucket" : "alnitekfiles.appspot.com",
    "messagingSenderId" : "428880692455",
    "appId" : "1:428880692455:web:7204f05e801606f9728e42"
  };
#Initialize Firebase
#firebase.initializeApp(firebaseConfig);

# Initializing connection with Firebase
firebase = pyrebase.initialize_app(firebaseConfig)

# Getting reference to storage feature of Firebase
storage = firebase.storage()

# //////////////////// Functions for Cloud Storage of Firebase \\\\\\\\\\\\\\\\\\\\ #

def dataFromFirebase(data):
    path_on_cloud = data #"docs/pdfs/" + 
    #path_local = "Local Data/" + data
    #storage.child(path_on_cloud).download(path_local)
    #print("Data : " + data + " successfully downloaded from firebase!")
    url = storage.child(path_on_cloud).get_url('GET')
    print("URL of " + data + " is :" + url)
    return url


def getFilesInAllSubFolder(folder):
    all_file_list = []
    with os.scandir(folder) as entries:
        for entry in entries:
            filename = os.path.join(folder, entry.name)
            #abs_fname = os.path.abspath(filename)
            if os.path.isfile(filename):
                #print(filename +" is a file")
                all_file_list.append(filename)
            else:
                #print(filename +" is a folder")
                all_file_list = all_file_list + getFilesInAllSubFolder(filename)
    
    return all_file_list

lemmer = nltk.stem.WordNetLemmatizer()
#WordNet is a semantically-oriented dictionary of English included in NLTK.
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

def clean_text(text):
    text = text.replace('\n', ' ')
    text = text.replace('[', '')
    text = text.replace(']', '')
    text = re.sub('�', '', text)
    text = re.sub('\s+',' ',text)
    return text

def pdf_dict():
    corpus_folder = 'docs'
    allFileList = getFilesInAllSubFolder(corpus_folder)
    final_dict = {}
    pdf_sent_tokens_all = []
    #ppt_sent_tokens_all = []
    append_write = 'w'
    text_file = open('sample1.txt', append_write)
    for filename in allFileList:
        #print(filename)
        if filename.endswith(".pdf"):
            try:
                with open('sample1.txt', append_write) as text_file:
                    #tok[filename] = storage.child(filename).put(filename,user['idToken'])
                    #url[filename] = storage.child(filename).get_url("tok"+filename['downloadTokens'])
                    #print("url-filename", url[filename])
                    finalText, resultDict, sent_tokens_all = convert(filename, final_dict) #get string of text content of pdf
                    #print("inside pdf all",sent_tokens_all)
                    pdf_sent_tokens_all = pdf_sent_tokens_all + sent_tokens_all
                    text_file.write(finalText)
                    #print("inside pdf")
                    text_file.close()
                    pdf_file.close()
            except:
                #print("skipping file due to encoding error "+filename)
                file = open(filename, encoding="iso-8859-1")
                text = file.read()
        if text_file.mode == 'w':
            append_write = 'a'
            resultDict = final_dict
    text_file.close()
    
    res_sen_list = pdf_sent_tokens_all
    return resultDict, res_sen_list


def response(user_response, resultDict, sent_tokens):
    robo_response=''
    sent_tokens.append(user_response)
    #print("sent_tokens_all_files", sent_tokens)
    #lemmer = nltk.stem.WordNetLemmatizer()
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    #print(idx)
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    sent_tokens.remove(user_response)
    #print("final dict", final_dict)
    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I don't understand you. Want to try something else?"
        return robo_response, None
    else:
        response_sen1 = sent_tokens[idx+2]
        robo_response = robo_response+sent_tokens[idx]+sent_tokens[idx+1]+sent_tokens[idx+2]+sent_tokens[idx+3]
        if response_sen1 in resultDict:
            fvalue = resultDict[response_sen1]
        else:
            fvalue = "could not find"
        #print("response_sen1--", response_sen1)
        print("final dict", fvalue)
        firebasePath = dataFromFirebase(fvalue[0])
        json_dict = {"ans" : robo_response, "filePath" : firebasePath, "pageNo" : fvalue[1]}
        return json_dict

set_sent_tokens = set()
def sen_dict(clean_txt, final_dict, fname, p_num):
    sent_tokens = nltk.sent_tokenize(clean_txt.lower())# converts to list of sentences
    #print("sent_tokens inside sen_dict",sent_tokens)
    for i in sent_tokens:
        if i in set_sent_tokens:
            final_dict[i].append([fname,p_num])
            final_dict.update(final_dict)
            #print("final_list1",final_dict[i])
            #print("final_list1",final_dict)
        else:
            dict1 = {i : [fname,p_num]}
            final_dict.update(dict1)
            #print("final_dict",final_dict)
            set_sent_tokens.add(i)
        #print("set_sent_tokens",set_sent_tokens)
    return final_dict, sent_tokens  
    
#converts pdf, returns its text content as a string
def convert(fname, final_dict):
    output = io.StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    page_no = 0
    sent_tokens_all = []
    infile = open(fname, 'rb')
    finalText=""
    #for page in PDFPage.get_pages(infile, pagenums):
    for pageNumber, page in enumerate(PDFPage.get_pages(infile)):
        if pageNumber == page_no:
            interpreter.process_page(page)
            
        converter.close()
        text = output.getvalue()
        clean_txt = clean_text(text)
        result, sent_tokens = sen_dict(clean_txt,final_dict,fname,page_no+1)
        finalText = finalText+text
        sent_tokens_all = sent_tokens_all + sent_tokens
        #print(page_no+1)
        #print(result)
        output.truncate(0)
        output.seek(0)
        #print(finalText)
        page_no += 1
    #print("sent_tokens_all", sent_tokens_all)    
    return finalText, result, sent_tokens_all
    infile.close()
