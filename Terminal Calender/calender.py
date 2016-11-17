
from __future__ import print_function
import httplib2
import os
import json
import sys
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

# try:
#     import argparse
#     flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
# except ImportError:
#     flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Terminal Calender'

def PrintJSON(dict):

    print(json.dumps(dict,indent=4,sort_keys=True))


def AllCalenders(service):
    result = service.calendarList().list(syncToken=None, minAccessRole=None, maxResults=None, showDeleted=None, showHidden=None, pageToken=None).execute()
    print(result['items'])

def AddEvent(service,event_string):

    result = service.events().quickAdd(calendarId='primary', text=event_string, sendNotifications=None).execute()
    PrintJSON(result)
    # print(result)

# def ShowUpcomingBirthdays(service):

# def UpcomingHolidays(service):



def ListUpcomingEvents(service,calenderId):

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId=calenderId, timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        # start = event['start'].get('date')
        start = event['start'].get('dateTime', event['start'].get('date'))
        date = start.split('T')[0]
        time = start.split('T')[1].split('+')[0]
        print(date,"  ",time,"  ", event['summary'])



def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        # if flags:
        #     credentials = tools.run_flow(flow, store, flags)
        # else: # Needed only for compatibility with Python 2.6
        #     credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def Help():
    print("Terminal Calender Instruction Set")
    print("Show Help : calender ")
    print("List Upcoming Events : calender upcoming")
    print("Upload a file : calender add <event_string>")
    # print("Download File : drive down <Filename>")

def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    if len(sys.argv) < 2:
        Help()
    else:
        option = sys.argv[1]
        if option == "upcoming":
            ListUpcomingEvents(service,'primary')
        elif option == "add":
            event_string = sys.argv[2]
            AddEvent(service,event_string)
        elif option == "bday":
            ListUpcomingEvents(service,'#contacts@group.v.calendar.google.com')
        elif option == 'holidays':
            ListUpcomingEvents(service,'en.indian#holiday@group.v.calendar.google.com')
        elif option == 'month':
            os.system('cal')
        else:
            print("Not An Option")
            Help()


if __name__ == '__main__':
    main()