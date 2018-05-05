import requests
from bs4 import BeautifulSoup
import sys
import itertools
import  time
from threading import Thread
# import PDF


# Global variable to treck the flag

load_flag = 0;
pdf_flag = 0;

def PrintHeadlines(headlines):
    global load_flag
    load_flag = 1
    print "\nHeadlines: "
    print "==================================================="

    for index in range(0,len(headlines)):
        print str(index+1) +" => "+headlines[index]

    print "0 => Press 0 to exit"
    print "----------------------------------------------------"
    selected_index = raw_input("Headline No: ")
    if selected_index == '' or int(selected_index) == 0 :
        exit()
    else:
        return int(selected_index) - 1

def PrintNews(headline,body_content):
    global pdf_flag
    print "==============================================================="
    print headline.encode('utf-8')
    print "-" * len(headline)    # underlining of headline
    print body_content.encode('utf-8')
    print "\n==============================================================="

def TheHinduHeadlines():
    StartProgress()
    # Load the Html Content of the Page. 
    html_doc = requests.get("http://www.thehindu.com/todays-paper/").content
    soup = BeautifulSoup(html_doc,'html.parser')
    headlines_section = soup.find('section',attrs={'id':'section_'})
    
    headline_items = headlines_section.find('ul',attrs={'class':'archive-list'}).find_all('li') #List of all the headlines
    # print(headline_items)

    headlines_texts = []
    headlines_links = []

    for i in range(0,min(5,len(headline_items))) :
        item = headline_items[i].find('a')
        headlines_texts.append(item.text)
        headlines_links.append(item.get('href'))

    while 1:
        url = headlines_links[PrintHeadlines(headlines_texts)]
        html_doc = requests.get(url).content
        soup = BeautifulSoup(html_doc,'html.parser')
        article_content = ""
        if len(html_doc) == 0:
            article_content = "Failed to load content, Open link:" + url
        headline = soup.h1.text
        paragraphs = soup.find_all('p')

        for para in paragraphs:
            article_content = article_content + "\n" + para.text + "       "

        PrintNews(headline, article_content)
    


def TOIHeadlines():
    StartProgress()
    # Load the Html Content of the Page.
    html_doc = requests.get("https://timesofindia.indiatimes.com/").content
    soup = BeautifulSoup(html_doc, 'html.parser')
    headlines_section = soup.find('div', attrs={'class': 'top-story'})

    headline_items = headlines_section.find('ul').find_all(
        'li')  # List of all the headlines
    # print(headline_items)

    headlines_texts = []
    headlines_links = []

    for i in range(0, min(5, len(headline_items))):
        item = headline_items[i].find('a')
        headlines_texts.append(item.text)
        headlines_links.append("https://timesofindia.indiatimes.com" + item.get('href'))

    while 1:
        url = headlines_links[PrintHeadlines(headlines_texts)]
        html_doc = requests.get(url).content
        soup = BeautifulSoup(html_doc, 'html.parser')

        if len(html_doc) == 0:
            article_content = "Failed to load content, Open link:" + url
        else:
            headline = soup.h1.text
            article_content = soup.find('div',attrs={'class':'Normal'}).text
        PrintNews(headline, article_content)

def TheIndianExpressHeadlines():

    StartProgress()
    # Load the Html Content of the Page.
    html_doc = requests.get("http://indianexpress.com/").content
    soup = BeautifulSoup(html_doc, 'html.parser')
    headlines_section = soup.find('div', attrs={'class': 'top-news'})

    headline_items = headlines_section.find('ul').find_all(
        'li')  # List of all the headlines
    # print(headline_items)

    headlines_texts = []
    headlines_links = []

    for i in range(0, min(5, len(headline_items))):
        item = headline_items[i].find('a')
        headlines_texts.append(item.text)
        headlines_links.append(item.get('href'))

    while 1:
        url = headlines_links[PrintHeadlines(headlines_texts)]
        html_doc = requests.get(url).content
        soup = BeautifulSoup(html_doc, 'html.parser')
        article_content = ""
        if len(html_doc) == 0:
            article_content = "Failed to load content, Open link:" + url
        else:
            headline = soup.h1.text
            paragraphs = soup.find_all('p')

            for para in paragraphs:
                article_content = article_content + "\n" + para.text + "       "
        PrintNews(headline, article_content)

def Progress():
    sys.stdout.write("Loading ...")
    for c in itertools.cycle('/-\|'):
        sys.stdout.write('\r\t\t' + c)
        sys.stdout.flush()
        time.sleep(0.2)
        if load_flag:
            break

def StartProgress():
    load_flag = 0

    try:
        t1 = Thread(target=Progress, args=())
        t1.start()
    except:
        print "Error: unable to start thread"

def Help():
    print "This is a command line program to show the headline News from leading newspapers of India."
    print "Give the following code or name as first argument :"
    print "TOI: The Times Of India"
    print "HINDU: The Hindu"
    print "TIE: TheIndian Express"

def main():
    newspaper = ""
    global pdf_flag
    if len(sys.argv)<2:
        Help()
        exit()
    elif len(sys.argv) == 3:
        pdf_flag = 1
        newspaper = sys.argv[2]
    else:
        newspaper = sys.argv[1]

    newspaper = newspaper.strip()
    if newspaper == "TOI" or newspaper == "The Times Of India":
        TOIHeadlines()
    elif newspaper == "TIE" or newspaper == "The Indian Express":
        TheIndianExpressHeadlines()
    elif newspaper == "HINDU" or newspaper == "The Hindu":
        TheHinduHeadlines()
    else:
        print  "No news Paper Given as argument"
        Help()

if __name__ == '__main__':
    main()