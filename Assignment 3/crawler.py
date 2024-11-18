#-------------------------------------------------------------------------
# AUTHOR: UyenNghi Nguyen
# FILENAME: crawler.py
# SPECIFICATION: CS website crawler for permanent faculty.
# FOR: CS 4250 - Assignment #3
# TIME SPENT: 2 hours
#-----------------------------------------------------------*/

from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
from pymongo import MongoClient

####################################################
# Create a database connection object using pymongo
DB_NAME = 'CPP'
DB_HOST = 'localhost'
DB_PORT = 27017
try:
    client = MongoClient(host=DB_HOST, port=DB_PORT)
    db = client[DB_NAME]
    pages = db['pages']
except:
    print('Could not connect to database.')
####################################################

class List(list):
    def nextURL(self):
        print("url: " + self)
        self.pop(0)
    def addURL(self, url):
        print("url added")
        # print(url)
        self.append(url)
    def clear_frontier(self):
        print("frontier cleared")
        self.clear()
    def done(self):
        print("done")
        if len(self) == 0:
            return True
        else:
            return False

url = 'https://www.cpp.edu/sci/computer-science/'
frontier = List().addURL(url)
not_visited_urls = []
target_page = 'https://www.cpp.edu/sci/computer-science/faculty-and-staff/permanent-faculty.shtml'

html = urlopen(url)

def retrieveHTML(url):
    try:
        html = urlopen(url)
        print('The requested URL was found...')
        return html.read()
    except Exception as e:
        print(e)
        print('The requested URL could not be found!')
    return None

def storePage(url, html):
    print("Storing page: ", url)
    db['pages'].insert_one({'url': url, 'html': html})

def parse(html):
    bs = BeautifulSoup(html, 'html.parser')
    links = []
    for link in bs.find_all('a', href=True):
        if not link.get('href').startswith('https://www.cpp.edu/') and link.get('href').startswith('/'):
            updated_link = 'https://www.cpp.edu' + link.get('href')
            links.append(updated_link)
        elif link.get('href').startswith('#'):
            updated_link = 'https://www.cpp.edu/sci/computer-science/' + link.get('href')
            links.append(updated_link)
        else:
            links.append(link.get('href'))
    return links

def flagTargetPage(url):
    html = retrieveHTML(url)
    bs = BeautifulSoup(html, 'html.parser')
    print(bs.find('h1', class_='cpp-h1'))
    return bs.find('h1', class_='cpp-h1')

# parse(html)
# retrieveHTML(url)
# flagTargetPage(url)

def crawlerThread(frontier):
    while frontier:
        url = frontier.nextURL()
        html = retrieveHTML(url)
        storePage(url, html)
        if target_page in (parse(html)):
            flagTargetPage(url)
            frontier.clear_frontier()
        else:
            for not_visited_urls in parse(html):
                frontier.addURL(not_visited_urls)

crawlerThread(frontier)
