#-------------------------------------------------------------------------
# AUTHOR: UyenNghi Nguyen
# FILENAME: assignment_1.py
# SPECIFICATION: This program creates a document-term matrix, after the 
# stopwords have been removed and the terms have been stemmed, based on 
# the collection.csv file.
# FOR: CS 4250- Assignment #1
# TIME SPENT: 8 hours
#-----------------------------------------------------------*/

# Importing some Python libraries
import csv
import math
from tabulate import tabulate

documents = []

# Reading the data in a csv file
with open('collection.csv', 'r') as csvfile:
  reader = csv.reader(csvfile)
  for i, row in enumerate(reader):
    if i > 0:  # skipping the header
      documents.append(row[0])

d1 = []
d2 = []
d3 = []

filtered_documents = []

# Conducting stopword removal for pronouns/conjunctions. Hint: use a set to define your stopwords.
stopwords = ["i", "and", "she", "her", "they", "their"]
for document in documents:
  for word in document.split():
    if word.lower() in stopwords:
      document = document.replace(word, "")
  filtered_documents.append(document)

# Conducting stemming. Hint: use a dictionary to map word variations to their stem.
stemming = {
  "loves" : "love",
  "cats" : "cat",
  "dogs" : "dog",
}

stemmed_documents = []

for document in filtered_documents:
  for word in document.split():
    if word in stemming:
      document = document.replace(word, stemming.get(word))
  stemmed_documents.append(document)

# Identifying the index terms.
terms = []

for document in stemmed_documents:
  for word in document.split():
    if word not in terms:
      terms.append(word)

# Building the document-term matrix by using the tf-idf weights.
d1 = stemmed_documents[0].split()
d2 = stemmed_documents[1].split()
d3 = stemmed_documents[2].split()

# initializing lists for each of the caluculated values
d1_count = []
d2_count = []
d3_count = []

tf_d1 = []
tf_d2 = []
tf_d3 = []

df_terms = []

idf_terms = []

tf_idf_d1 = []
tf_idf_d2 = []
tf_idf_d3 = []

total_docs = 3

for term in terms:
  d1_count.append(d1.count(term))
  d2_count.append(d2.count(term))
  d3_count.append(d3.count(term))

# performming cacluations
# tf = count of term / number of terms in doc
# df = occurrence of terms in documents
# idf = log of the number of documents / df
# tf-idf = tf * idf
for i in range(len(terms)):
  tf_d1.append(float("{:.2f}".format(d1_count[i] / sum(d1_count))))
  tf_d2.append(float("{:.2f}".format(d2_count[i] / sum(d2_count))))
  tf_d3.append(float("{:.2f}".format(d3_count[i] / sum(d3_count))))
  df_terms.append(d1_count[i] + d2_count[i] + d3_count[i])
  idf_terms.append(float("{:.2f}".format(math.log((abs(total_docs) / df_terms[i]), 10))))
  tf_idf_d1.append(float("{:.2f}".format(tf_d1[i] * idf_terms[i])))
  tf_idf_d2.append(float("{:.2f}".format(tf_d2[i] * idf_terms[i])))
  tf_idf_d3.append(float("{:.2f}".format(tf_d3[i] * idf_terms[i])))

# adding in headers and labels 
terms.insert(0, "Document-Term\nMatrix")
tf_idf_d1.insert(0, "d1")
tf_idf_d2.insert(0, "d2")
tf_idf_d3.insert(0, "d3")

doc_term_matrix = [
  terms,
  tf_idf_d1,
  tf_idf_d2,
  tf_idf_d3
]

# Printing the document-term matrix.
print(tabulate(doc_term_matrix, headers="firstrow", tablefmt="grid", numalign="right"))