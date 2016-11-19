from pyquery import PyQuery as pq
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
    print headline
    print "-" * len(headline)    # underlining of headline
    print body_content
    print "\n==============================================================="

def TheHinduHeadlines():
    StartProgress()
    content = pq(url="http://www.thehindu.com/todays-paper/")
    headlines = content(".tpaper").find('a')   # CSS class selector
    length = len(headlines)

    headline_arr = []
    link_arr = []
    for i in range(0,min(5,length)):
        headline = headlines.eq(i).text()     # anchor text from links
        link = headlines.eq(i).attr('href')
        headline_arr.append(headline)
        link_arr.append(link)
    while 1:
        url = link_arr[PrintHeadlines(headline_arr)]
        content = pq(url)
        article_content = content(".article-text").find('p').text()
        headline = content("h1").text()
        PrintNews(headline,article_content)

def TOIHeadlines():
    StartProgress()
    content = pq(url="http://timesofindia.indiatimes.com/")
    headlines = content(".top-story")
    length = len(headlines.find('li'))

    headline_arr = []
    link_arr = []
    for i in range(0, min(5, length)):
        headline = headlines.find('li').eq(i).text()  # anchor text from links
        link = "http://timesofindia.indiatimes.com/" + headlines.find('li').eq(i).find('a').eq(0).attr('href')
        headline_arr.append(headline)
        link_arr.append(link)

    while 1:
        url = link_arr[PrintHeadlines(headline_arr)]
        content = pq(url)
        article_content = content(".Normal").text()
        if len(article_content) == 0:
            article_content = "Failed to load content, Open link:" + url
        headline = content("h1").text()
        # article_content = "".join(article_content.split('+'))
        PrintNews(headline, article_content)

def HindustanTimesHeadlines():
    StartProgress()
    content = pq(url="http://www.hindustantimes.com/")
    headlines = content(".top_story_row").find('a')
    length = len(headlines)

    headline_arr = []
    link_arr = []
    for i in range(1, length):
        headline = headlines.eq(i).text()  # anchor text from links
        link = headlines.eq(i).attr('href')
        headline_arr.append(headline)
        link_arr.append(link)

    while 1:
        url = link_arr[PrintHeadlines(headline_arr)]
        content = pq(url)
        article_content = content("#div_storyContent").text()
        headline = content("h1").text()
        PrintNews(headline, article_content)

def TheIndianExpressHeadlines():
    StartProgress()
    content = pq(url="http://indianexpress.com/")

    headlines = content(".right-part").eq(0).find('a')
    length = len(headlines)
    headline_arr = []
    link_arr = []

    main_story_link = content('h1').find('a').attr('href')
    main_headline = content('h1').find('a').text()
    headline_arr.append(main_headline)
    link_arr.append(main_story_link)

    for i in range(1, length):
        headline = headlines.eq(i).text()  # anchor text from links
        link = headlines.eq(i).attr('href')
        headline_arr.append(headline)
        link_arr.append(link)

    while 1:
        url = link_arr[PrintHeadlines(headline_arr)]
        content = pq(url)
        article_content = content('.full-details').find('p').text()
        headline = content("h1").text()
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
    print "HT: Hindustan Times"
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
    elif newspaper == "HT" or newspaper == "Hindustan Times":
        HindustanTimesHeadlines()
    else:
        print  "No news Paper Given as argument"
        Help()

if __name__ == '__main__':
    main()