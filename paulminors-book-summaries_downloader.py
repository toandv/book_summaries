# https://www.crummy.com/software/BeautifulSoup/bs4/doc/
# https://docs.python.org/3/library/queue.html

import urllib.request
from bs4 import BeautifulSoup
import queue
import threading


def download_file(url):
    file_name = url.split("/")[-1]
    urllib.request.urlretrieve(url, file_name)
    print(file_name + " downloaded")

def worker():
    while True:
        item = q.get()
        if item is None:
            break
        do_work(item)
        q.task_done()        

def do_work(item):
    download_file(item)

q = queue.Queue()
threads = []
for i in range(20):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)      
    

html_doc = urllib.request.urlopen("https://paulminors.com/resources/book-summaries/download/").read()
soup = BeautifulSoup(html_doc, 'html.parser')
pdf_urls = [link.get('href') for link in soup.find_all('a') if (link.get('href') != None and link.get('href').endswith('pdf'))]

print('About to download ' + str(len(pdf_urls))  + ' pdf files')

for pdf_url in pdf_urls:
    q.put(pdf_url)

q.join()
for i in range(20):
    q.put(None)
for t in threads:
    t.join()   