#!/usr/bin/python
from pyquery import PyQuery as pq
import re
import youtube_dl
import sys
import sqlite3
import os
import shutil

class MyLogger(object):
    def debug(self, msg):
        # print(msg)
        pass

    def warning(self, msg):
        # print(msg)
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print "Done.."
        print "-----------------------------------------------------------------"


def DownloadMP3(url):

    #options for youtube download
    ydl_opts = {
        'format': '140',
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        video_title = info_dict.get('title', None)
        print "Downloading.. : " + video_title
        ydl.download([url])

def SelectMusicFolder(folder_name):
    # Look for Music direcorty in the
    home_dir = os.path.expanduser('~')
    music_dir = home_dir + "/Music/"+folder_name
    try:
        os.chdir(music_dir)
        print "Downloading Music to: "+ music_dir
    except OSError:
        os.mkdir(music_dir)
        os.chdir(music_dir)
        print "New Folder Created Downloading Music : "+ music_dir
    except:
        print "Something went wrong.."

def LoadHistoryArray():

    database_path = os.path.expanduser('~') + "/Library/Application Support/Google/Chrome/Default"
    history_db = os.path.join(database_path, 'History')
    temp_file = os.getcwd() + '/History'
    shutil.copy(history_db, temp_file)

    history = []
    conn = sqlite3.connect(temp_file)
    c = conn.cursor()
    sql_query = "select last_visit_time, url from  urls"

    for row in c.execute(sql_query):
        datetime = row[0]
        url = row[1]
        domain = ""
        try:
            domain = url.split('/')[2]
        except:
            print "Url too short to find domain"
        # create a dict item
        history_item = {}
        history_item['datetime'] = datetime
        history_item['url'] = url
        history_item['domain'] = domain
        history.append(history_item)

    conn.close()
    return history

def FavouriteMusic():
    SelectMusicFolder('FavouriteMusic')
    history = LoadHistoryArray()
    history_dict = {}
    for item in history:
        if item["domain"] != "www.youtube.com":
            continue
        elif "watch" not in item["url"]:
            continue
        else:
            song_url = item["url"].split("&")[0]
            history_dict[song_url] = history_dict.get(song_url,0) + 1

    for item in sorted(history_dict.items(), key=lambda x: x[1]):

        youtube_song_url = item[0]
        playing_frequency = item[1]

        if playing_frequency > 2:
            try:
                DownloadMP3(youtube_song_url)
            except:
                print "Can't download"



def SearchSong(song_title):
    SelectMusicFolder('SearchedSongs')
    SEARCH_URL = "https://www.youtube.com/results?search_query="
    formatted_title = "+".join(song_title.split(' '))
    search_query = SEARCH_URL+formatted_title
    page_content = pq(search_query)
    # print time.time() - start
    result_div = page_content('#results').find('ol.item-section')

    fetched_url = ''
    index = 0
    while 1:
        song_url = result_div.find('a').eq(index).attr('href')
        index = index + 1
        if 'watch' in song_url:
            # print time.time()-start
            fetched_url = 'https://www.youtube.com'+song_url
            break
    DownloadMP3(fetched_url)
    # print fetched_url
def OnlyHindi(title):
    if re.search("Malayalam|Tamil|Telugu|Gujarati|Kannada",title) != None:
        return False
    else:
        return True


def SongFilter(title):
    # Remove juke box or collections of songs
    if re.search("Show|show",title)!= None:
        return False
    if re.search("Lyrical|Lyric|Video Song|Full Video Song|Official Video Song|Song",title) != None:
        return True

    return False

def LatestMusicFromChannel(channel_url):
    channel_name = channel_url.split('/')[-2]
    SelectMusicFolder(channel_name.title())
    channel_content = pq(channel_url)
    videos = channel_content("#channels-browse-content-grid")
    video_list = videos("li")

    for i in range(0,len(videos('li'))):
        song_data = videos('li').eq(i)
        song_title = song_data.find('h3').text()
        song_url= song_data.find('a').attr('href')
        views = song_data('li').eq(3).text()
        uploaded_on = song_data('li').eq(4).text()
        if song_url == None:
            continue
        if SongFilter(song_title) and OnlyHindi(song_title):
            print song_title
            try:
                DownloadMP3("https://www.youtube.com"+song_url)
            except:
                print "Can't download"

def YoutubeTrendingMusic():
    SelectMusicFolder('TrendingMusic')    # Selecting the destination where the music file will be saved
    channel = pq("https://www.youtube.com/channel/UCAh9DbAZny_eoGFsYlH2JZw")
    music_url = channel('.branded-page-module-title').eq(1).find('a').attr('href')
    music_url = "https://www.youtube.com"+music_url

    content = pq(music_url)
    content = content("#pl-video-table")
    playlist = content(".pl-video-title")
    video_owners = content(".pl-video-owner")

    length = len(playlist)
    for i in range(0,length):
        relative_url = playlist.eq(i).find('a').attr('href')
        list_url = "https://www.youtube.com" + relative_url
        download_url =list_url.split('&')[0]
        title = playlist.eq(i).find('a').text()
        owner = video_owners.eq(i).find('a').text()
        if SongFilter(title) and OnlyHindi(title):
            print title
            try:
                DownloadMP3(download_url)
            except:
                print "Can't download"


def Help():
    print "Youtube Audio Downloader"
    print "-----------------------------------"
    print "Trending on Youtube India : music trending"
    print "Search Song: music search '<Song Title>'"
    print "Favourite : music fav "
    print "Recent From Tseries : music tseries"
    print "Recent From Sony Music India : music sony"
    print "Recent From any youtube channel  : music channel <channel_url>"
    print "From URL : music url <url>"


if __name__ == '__main__':

    if len(sys.argv) < 2:
        Help()
    else:
        option = sys.argv[1]
        if option == "fav":
            FavouriteMusic()
        elif option == "trending":
            YoutubeTrendingMusic()
        elif option == "search":
            song_title = sys.argv[2]
            SearchSong(song_title)
        elif option == "tseries":
            LatestMusicFromChannel('https://www.youtube.com/user/tseries/videos')
        elif option == "sony":
            LatestMusicFromChannel('https://www.youtube.com/user/sonymusicindiaSME/videos')
        elif option == "zee":
            LatestMusicFromChannel('https://www.youtube.com/user/zeemusiccompany/videos')
        elif option == "channel":
            youtube_channel = sys.argv[2]
            LatestMusicFromChannel(youtube_channel)
        elif option == "url":
            youtube_url = sys.argv[2]
            SelectMusicFolder(folder_name="URLDownload")
            DownloadMP3(youtube_urls)
        else:
            Help()
