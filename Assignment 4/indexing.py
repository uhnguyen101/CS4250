#-------------------------------------------------------------------------
# AUTHOR: UyenNghi Nguyen
# FILENAME: indexing.py
# SPECIFICATION: Python indexing
# FOR: CS 4250 - Assignment #4
# TIME SPENT: 2 hours
#-----------------------------------------------------------*/


from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
from pymongo import MongoClient
from nltk.tokenize import RegexpTokenizer
from nltk.util import ngrams
import re

####################################################
# Connect to MongoDB
DB_NAME = 'assignment4'
DB_HOST = 'localhost'
DB_PORT = 27017
try:
    client = MongoClient(host=DB_HOST, port=DB_PORT)
    db = client[DB_NAME]
    documents_collection = db['docs']
    terms_collection = db['terms']
except:
    print('Could not connect to database.')
####################################################

# Function to tokenize document
def tokenize(document):
    tokenized = re.findall(r'\w+', document.lower())
    return tokenized

def n_grams(terms):
    unigrams = list(ngrams(tokenize(terms), 1))
    bigrams = list(ngrams(tokenize(terms), 2))
    trigrams = list(ngrams(tokenize(terms), 3))
    return unigrams + bigrams + trigrams
    # if type == 1:
    #     return unigrams
    # if type == 2:
    #     return bigrams
    # if type == 3:
    #     return trigrams

# Update MongoDB with documents collection
i = 0
docs = ["After the medication, headache and nausea were reported by the patient.", 
        "The patient reported nausea and dizziness caused by the medication.",
        "Headache and dizziness are common effects of this medication.", 
        "The medication caused a headache and nausea, but no dizziness was reported."]
docs_to_add = []
while (i < len(docs)):
    docs_to_add.append({'id' : i + 1,'content': docs[i]}    )
    i = i + 1
documents_collection.insert_many(docs_to_add)

vocabulary_ = {}

def compute_doc_scores(query):
    tokenized_queries = tokenize(query)
    for query_term in tokenized_queries:
        try:
            check = terms.find_one({"_id": vocabulary_.get(query_term)})
            # for doc in check[]
        except Exception as e:
            print(f"Unable to compute document score for query: {e}")

queries = ["nausea and dizziness", 
           "effects", 
           "nausea was reported", 
           "dizziness", 
           "the medication"]

for doc in docs:
    terms = n_grams(doc)
    for term in terms:
        terms_collection.insert_one(
            {"_id": val,
             "pos": pos,
             "tf-idf": tf_idf
             }
        )
        # print(','.join(term).replace(",", " "))
    
output = {}
