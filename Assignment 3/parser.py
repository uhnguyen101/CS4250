#-------------------------------------------------------------------------
# AUTHOR: UyenNghi Nguyen
# FILENAME: parser.py
# SPECIFICATION: CS website parser for permanent faculty.
# FOR: CS 4250 - Assignment #3
# TIME SPENT: 2 hours
#-----------------------------------------------------------*/

from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
from pymongo import MongoClient
import re

####################################################
# Create a database connection object using pymongo
DB_NAME = 'CPP'
DB_HOST = 'localhost'
DB_PORT = 27017
try:
    client = MongoClient(host=DB_HOST, port=DB_PORT)
    db = client[DB_NAME]
    pages = db['pages']
    collection = db['faculty']
except:
    print('Could not connect to database.')
####################################################


target_page = 'https://www.cpp.edu/sci/computer-science/faculty-and-staff/permanent-faculty.shtml'
# html = collection.find_one({'url': target_page}).get('html')
# html = collection.find_one()
# print(html)
html = urlopen(target_page).read()
bs = BeautifulSoup(html, 'html.parser')

names_list = []
titles_list = []
offices_list = []
phones_list = []
emails_list = []
webs_list = []

names = bs.find_all('h2', id=False)
titles = bs.find_all('strong', string=re.compile('Title'))
offices = bs.find_all('strong', string=re.compile('Office'))
phones = bs.find_all('strong', string=re.compile('Phone'))
emails = bs.find_all('strong', string=re.compile('Email'))
webs = bs.find_all('strong', string=re.compile('Web'))

for name in names:
    try:
        actual_name = name.text
        names_list.append(actual_name)
    except:
        name.append("No name.")
for title in titles:
    try:
        actual_title = title.find_next_sibling(string=True).strip()
        titles_list.append(actual_title)
    except:
        titles_list.append("No title yet.")
for office in offices:
    try:
        actual_office = office.find_next_sibling(string=True).strip()
        offices_list.append(actual_office)
    except:
        offices_list.append("No office yet.")
for phone in phones:
    try:
        actual_phone = phone.find_next_sibling(string=True).strip()
        phones_list.append(actual_phone)
    except Exception:
        phones_list.append("No phone yet.")
for email in emails:
    try: 
        actual_email = email.find_next_sibling('a')['href'].split(":", 1)[1].strip()
        emails_list.append(actual_email)
    except Exception:
        emails_list.append("No email yet.")
for web in webs:
    try: 
        actual_web = web.find_next_sibling('a')['href']
        webs_list.append(actual_web)
    except Exception:
        webs_list.append("No website yet.")

# verify lists
# print(names_list)
# print(titles_list)
# print(offices_list)
# print(phones_list)
# print(emails_list)
# print(webs_list)

# create list of dictionaries for inputting into MongoDB
professors = []
for prof in range(len(names_list)):
    professors.append(
        {'Name': names_list[prof],
         'Title': titles_list[prof],
         'Office': offices_list[prof],
         'Phone': phones_list[prof],
         'Email': emails_list[prof],
         'Web': webs_list[prof]
         }
    )
# print(professors)

# insert all faculty into MongoDB
collection.insert_many(professors)