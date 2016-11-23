#!/usr/bin/python
from pyquery import PyQuery as pq
import sys
import urllib2

def SearchMeaning(word):
    dict_url = "http://www.merriam-webster.com/dictionary/"+word
    try:
        content = pq(dict_url)
        meanings = content('div.inner-box-wrapper').find('ul').eq(0).text()
        mean_array = meanings.split(':')
        mean_array.pop(0)
        for mean in mean_array:
            print "--------------------------------------------------------"
            print "==> "+mean

    except urllib2.HTTPError:
        print "--------------------------------------------------------"
        print 'Url Unreachable.. '
        Help()

def Help():
    print "Dictionary Meanings from Merriam-Webster."
    print "Meaning Definition: dict <Single Word>"

if __name__ == '__main__':
    if len(sys.argv)<2:
        Help()
        exit()
    else:
        word = sys.argv[1]
        SearchMeaning(word)
