#-------------------------------------------------------------------------
# AUTHOR: UyenNghi Nguyen
# FILENAME: title of the source file
# SPECIFICATION: Updating a Mongo database with PyMongo.
# FOR: CS 4250 - Assignment #2
# TIME SPENT: 2 hours
#-----------------------------------------------------------*/

# IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with
# standard arrays

# importing some Python libraries
import string
from pymongo import MongoClient

def connectDataBase():

    # Create a database connection object using pymongo
    DB_NAME = "CPP"
    DB_HOST = "localhost"
    DB_PORT = 27017

    try:
        client = MongoClient(host=DB_HOST, port=DB_PORT)
        db = client[DB_NAME]
        db.create_collection("documents")
        return db 
    except:
        print("Could not connect to database.")

def createDocument(col, docId, docText, docTitle, docDate, docCat):

    # create a dictionary (document) to count how many times each term appears in the document.
    # Use space " " as the delimiter character for terms and remember to lowercase them.
    remove = str.maketrans('', '', string.punctuation)
    docTextFormatted = docText.translate(remove).lower()
    terms = docTextFormatted.split()

    # create a list of dictionaries (documents) with each entry including a term, its occurrences, and its num_chars. Ex: [{term, count, num_char}]
    termsList = []
    for term in terms:
        termDict = {
            "term": term,
            "count": terms.count(term),
            "num_chars": len(term)
        }
        termsList.append(termDict)

    #Producing a final document as a dictionary including all the required fields
    doc = {
        "_id": docId,
        "title": docTitle,
        "text": docText,
        "date": docDate,
        "category": docCat,
        "terms": termsList
    }

    # Insert the document
    col.insert_one(doc)

def deleteDocument(col, docId):

    # Delete the document from the database
    col.delete_one({"_id": docId})

def updateDocument(col, docId, docText, docTitle, docDate, docCat):

    # Delete the document
    col.delete_one({"_id": docId})

    # Create the document with the same id
    createDocument(col, docId, docText, docTitle, docDate, docCat)

def getIndex(col):

    # Query the database to return the documents where each term occurs with their corresponding count. Output example:
    # {'baseball':'Exercise:1','summer':'Exercise:1,California:1,Arizona:1','months':'Exercise:1,Discovery:3', ...}
    # We are simulating an inverted index here in memory.
    pipeline = [
        {"$unwind": {"path": "$terms"}},
        {"$group": {
            "_id": "$terms",
            "title": "$title"
        }},
        {"$project": {
            "term": "$_id.term",
            "title": "title",
            "count": "$_id.count"
        }}
    ]
    terms = col.aggregate(pipeline)
    for term in terms:
        print(f"{term["terms.term"]}: {term["title"]}: {term["terms.count"]}")