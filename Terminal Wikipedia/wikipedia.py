#!/usr/bin/env python

import urllib2
import sys
import time
import itertools
from threading import Thread
from pyquery import PyQuery as pq
from bs4 import BeautifulSoup

flag = 0


# show progess
def progress():
    global flag
    sys.stdout.write("Searching...")
    for c in itertools.cycle('/-\|'):
        sys.stdout.write('\r\t\t' + c)
        sys.stdout.flush()
        time.sleep(0.2)
        if flag:
            break


def getWikiLink(name):
    nameArr = name.split(' ')
    searchName = "%20".join(nameArr)  # capitalize the first character
    global flag
    # extract the redirect page of search item in wikipedia
    try:
        # url = "https://en.wikipedia.org/wiki/" + searchName
        url = "https://en.wikipedia.org/w/index.php?search=" + searchName + "&title=Special%3ASearch&go=Go"
        req = urllib2.Request(url)
        res = urllib2.urlopen(req)
        interURL = res.geturl()  # this does not give the exact link

        # arr = interURL.split('/')
        # tempName = arr[-1]

        # web scraping of wikipedia is needed to get the exact wikipedia link
        # indexURL = "https://en.wikipedia.org/w/index.php?title=" + tempName + "&redirect=no"
        # response = urllib2.urlopen(indexURL)
        # page_source = response.read()

        # codeLines  = page_source.split('\n')
        # resultURL = interURL

        # for line in codeLines:
        # 	if line.find("redirectMsg") != -1 and line.find("redirectText") != -1 :
        # 		breakWords = line.split()
        # 		getLink = ""
        # 		for word in breakWords:
        # 			if word.find("href") != -1:
        # 				getLink = word.split("\"")[1]
        # 				break
        # 		resultURL = "https://en.wikipedia.org" + getLink
        # 		break

        flag = 1
        sys.stdout.write("\t[DONE]\n")
        print"--------------------------------"
        # f = urllib2.urlopen(resultURL)
        # parsing of the Html content recieved from the urllib
        html_doc = res.read()
        # soup = BeautifulSoup(html_doc, 'html.parser')
        # d = pq(html_doc)
		#print d('p').text()
        # print(soup.get_text())
        # paragraph = soup.find('p')
        # for text in paragraphArr:               # Uncomment the following loop to print all content
        # print(text.get_text())
        # print(paragraph.get_text())
        d = pq(html_doc)
        print d('p').text()
        print "--------------------------------"
        print "Go to wikipedia: ", interURL
    # file  = open("links.txt", "a")
    # file.write(resultURL+'\n')
    # file.close()
    except urllib2.URLError, e:
        flag = 1
        print "Failed !!"


try:
    t1 = Thread(target=progress, args=())
    t1.start()
    t2 = Thread(target=getWikiLink, args=(sys.argv[1],))
    t2.start()
except:
    print "Error: unable to start thread"
