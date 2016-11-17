#!/usr/bin/python
"""
This Script Contain the control of VLC Media Player Through terminal
"""
import sys
import requests
import json
import os
import logging

#### Global Variable #####

username = ''
password = 'password'
vlc_server = 'http://localhost:8080/requests/status.json'

#############################

def PrintJSON(dict):
    """Print nicely formatted JSON"""

    print(json.dumps(dict,indent=4,sort_keys=True))

def FindTwoKeys(id,uri,obj,result_array):
    if id in obj and uri in obj:
        dict = {}
        dict[id] = obj[id]
        dict[uri] = obj[uri]
        result_array.append(dict)
        return
    else:
        for dict in obj['children']:
            FindTwoKeys(id, uri, dict, result_array)


def PlayerPlaylist():
    """ Return the JSON file Playlist of VLC"""
    playlist_url = 'http://localhost:8080/requests/playlist.json'
    response = requests.get(playlist_url, auth=(username, password))
    if response.status_code != 200:
        logging.error("Bad Request.. ")
    playlist = dict(response.json())
    return playlist

def ShowPlaylist():
    playlist = PlayerPlaylist()

    result = []
    FindTwoKeys('id', 'uri', playlist, result)

    print "id           "+"Song Name"

    song_format = [
        'mp3',
        'm4a'
    ]

    for item in result:
        file_extension = item['uri'].split('.').pop()
        song_name = item['uri'].split('/').pop()
        if file_extension in song_format:
            print item["id"]+"......."+song_name

def PlayerStatus(payload={}):
    response = requests.get(vlc_server,params=payload, auth=(username, password))
    if response.status_code != 200:
        logging.error("Bad Request.. ")
    player_status = dict(response.json())
    return player_status

def SetVolume(volume):
    """
    Function is called to set the volume of VLC Media player
    ?command=volume&val=<val>
    """
    safe_volume = 0
    if volume < 0:
        safe_volume = 0
    elif volume > 300:
        safe_volume = 300
    else:
        safe_volume = volume
    payload = {'command':'volume'}
    payload['val'] = safe_volume
    current_status = PlayerStatus(payload)
    set_volume = current_status['volume']
    if set_volume == volume:
        return True
    else:
        return False


def EnqueueToPlaylist(filename):
    """
    Function to add a song from the playlist from filename
    :param filename:
    :return:
    """
    # ?command=in_enqueue&input=<uri>
    payload = {'command':'in_enqueue','input':filename}
    current_status = PlayerStatus(payload)

def ForcePause():
    """
    Change the state of player from stop to play or play to pause
    :return:
    """

    # ?command=pl_pause&id=<id>
    payload = {'command':'pl_pause'}
    current_status = PlayerStatus(payload)

def ForcePlay():
    """
        Change the state of player to play
        :return:
        """

    # ?command=pl_pause&id=<id>
    payload = {'command': 'pl_forceresume'}
    current_status = PlayerStatus(payload)


def PlayNext():
    """
    Play Next Song
    ?command=pl_next
    """
    payload = {'command': 'pl_next'}
    current_status = PlayerStatus(payload)

def PlayPrevious():
    """
    Play Previous Song
    ?command=pl_previous
    """
    payload = {'command': 'pl_previous'}
    current_status = PlayerStatus(payload)

def PlaySongWithId(play_id):
    """ Play song with a given ID
    ?command=pl_play&id=<id>
    """
    payload = {'command':'pl_play','id':play_id}
    current_status = PlayerStatus(payload)

def AddFolderToPlaylist(folder):
    music_folder = "/Users/amit.kumar12/Music"
    folder_map = {
        'eng': 'EnglishSongs',
        'love': 'LoveSongs',
        'new': 'NewSongs',
        'fav': 'FavouriteSongs',
        'pan':'PanjabiSongs'
    }
    folder_path = os.path.join(music_folder,folder_map[folder])
    files = os.listdir(folder_path)
    song_format = [
        'mp3',
        'm4a'
    ]

    for filename in files:
        extension = filename[-3:]
        if extension in song_format:
           EnqueueToPlaylist(os.path.join(folder_path,filename))

    ForcePause()

def SortPlaylist():
    """
    Sort PlayList

    ?command=pl_sort&id=<id>&val=<val>
    A non exhaustive list of sort modes:
    0 Id
    1 Name
    3 Author
    5 Random
    7 Track number
    """
    payload = {'command': 'pl_sort', 'id': 0,'val':1}
    current_status = PlayerStatus(payload)

def ToggleRandomPlayback():
    """
    Toggle Random of Player
    ?command=pl_repeat
    """
    payload = {'command': 'pl_random'}
    current_status = PlayerStatus(payload)

def ToggleLoopPlayback():
    """
    Toggle Loop playback of Player
    ?command=pl_repeat
    """

    payload = {'command': 'pl_loop'}
    current_status = PlayerStatus(payload)

def ToggleRepeat():
    """
    Toggle Repeat or Not Repeat
    ?command=pl_repeat
    """
    payload = {'command': 'pl_repeat'}
    current_status = PlayerStatus(payload)

def JumpPlayTime(time):
    """
    Jump by percentage in play
    """
    # ?command=seek&val=<val>

    payload = {'command': 'seek', 'val': time}
    current_status = PlayerStatus(payload)

def DeleteSong():
    """
    Delete a song with given currentpid
    """
    # command=pl_delete&id=13

    current_status = PlayerStatus()
    playlistWithID = []
    FindTwoKeys('id','uri',PlayerPlaylist(),playlistWithID)
    # playlisst = PlayerPlaylist()
    # PrintJSON(playlist)

    currentplid = current_status['currentplid']
    PlayNext()
    payload = {'command': 'pl_delete', 'id': currentplid}
    current_status = PlayerStatus(payload)

    for item in playlistWithID:
        if int(item['id']) == int(currentplid):
            os.remove(item['uri'])

def PlayFavourite():
    print "playing your favourite songs here.."

def EmptyPlaylist():
    """ Empty the current playlist of VLC
    empty playlist:
  ?command=pl_empty
    """
    payload = {'command':'pl_empty'}
    current_status = PlayerStatus(payload)

def IncreaseVolume():
    current_status = PlayerStatus()
    volume = current_status['volume'] + 40
    SetVolume(volume)

def DecreaseVolume():
    current_status = PlayerStatus()
    volume = current_status['volume'] - 40
    SetVolume(volume)

def Forward():
    current_status = PlayerStatus()
    total_time = current_status['length']
    time = current_status['time']
    time = time + total_time/5
    JumpPlayTime(time)

def Help():
    print "Command Line VLC Control"
    print "-----------------------------------"
    print "Next Song: next"
    print "Previous Song : next"
    print "Pause : pause"
    print "Play : play"
    print "Stop : stop"
    print "Increase Volume : up"
    print "Decrease Volume : down"
    print "Set Volume: vol <val>"
    print "Show Playlist : playslit"
    print "Clear Playlist: clear"
    print "Add Folder To Playlist: add <folder>"
    print "Play Specific Song ID: song <id>"
    print "Delete Current Song : del"


if __name__ == '__main__':

    if len(sys.argv) < 2:
        os.system('open -a vlc')
    else:
        option = sys.argv[1]
        if option == "prev":
            PlayPrevious()
        elif option == "next":
            PlayNext()
        elif option == "up":
            IncreaseVolume()
        elif option == "down":
            DecreaseVolume()
        elif option == "pause":
            ForcePause()
        elif option == "play":
            ForcePlay()
        elif option == "mute":
            SetVolume(0)
        elif option == "unmute":
            SetVolume(100)
        elif option == "vol":
            SetVolume(int(sys.argv[2]))
        elif option == "forward":
            Forward()
        elif option == "del":
            DeleteSong()
        elif option == "clear":
            EmptyPlaylist()
        elif option == "song":
            song_id = int(sys.argv[2])
            PlaySongWithId(song_id)
        elif option == "add":
            folder = sys.argv[2]
            AddFolderToPlaylist(folder)
        elif option == "playlist":
            ShowPlaylist()
        else:
            Help()
