#!/usr/bin/python
from __future__ import print_function

from email import errors
import webbrowser
import httplib2
import os
import base64
import json
import sys
import os
from email.mime.text import MIMEText
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

########## Global Variables #################

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
# SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
SCOPES = 'https://mail.google.com/'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail From Terminal Geek'


def PrintJSON(dict):

    print(json.dumps(dict,indent=4,sort_keys=True))

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
                                   'gmail-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def ShowUnreadEmail(service):
    """
    Fetch Unread emails from gmail and show them here.
    """
    try:
        results = service.users().messages().list(userId='me').execute()
    except errors.HttpError, error:
        print('An error occurred: %s' % error)

    messages = results.get('messages',[])

    for message in messages:
        message_id = message['id']
        try:
            msg_data = service.users().messages().get(userId='me',id=message_id).execute()
            MarkRead(service,message_id)
        except errors.HttpError, error:
            print('An error occurred: %s' % error)

        payload = msg_data['payload']
        labels = msg_data['labelIds']
        attached_file = payload['filename']
        body = payload['body']
        headers = payload['headers']
        snippet = msg_data['snippet']

        print("--------------------------------------------------")
        print("Message ID : "+message_id)
        options =[
            'To',
            'From',
            'Subject',
            'Date',
            'List-unsubscribe'
        ]
        unsubscribe_url = ""
        for item in headers:
            if item['name'] in options:
                print(item['name']+" : "+item['value'])
        print (",  ".join(labels))
        print("Mail Snippet : "+snippet)
        if attached_file != '':
            print ("Attached File : "+attached_file)
            # DownloadAttachment(attachmentId)
        # break
        user_response = raw_input("Action : ")
        resp = user_response.rstrip()
        if resp == '-o':
            try:
                file = open("mail.html", "w")
                item = payload['parts'][1]
                content = item['body']
                temp_data = content['data']
                file.write(base64.urlsafe_b64decode(str(temp_data)))
                file.close()
                webbrowser.open_new('file://' + os.getcwd() + '/mail.html')
            except :
                print("Undable to Parse Data..")

        elif resp == '-d':
            DeleteMessage(service,message_id)
        elif resp == '-t':
            TrashMail(service,message_id)
        elif resp == '-u':
            webbrowser.open_new(unsubscribe_url)
        elif resp == '-w':
            send_msg = {}
            send_msg['From'] = raw_input("From : ")
            send_msg['To'] = raw_input("To :")
            send_msg['Subject'] = raw_input("Subject : ")
            send_msg['body'] = raw_input("Body : ")

            print("Your Message look this : ")
            PrintJSON(send_msg)
            action = raw_input("Do you want to send the message (y/n) : ")

            if action == 'y' or action == 'yes':
                SendMessage(service,CreateMessage(send_msg))
            else:
                print('Saving to Drafts ...')
                SaveToDrafts(service,CreateMessage(send_msg))
        elif resp == '-e':
            sys.exit()
        else :
            print(" ")

def ProfileDetails(service):
    """ Gives Profile Details of the person"""
    try:
        results = service.users().getProfile(userId='me').execute()
    except errors.HttpError, error:
        print('An error occurred: %s' % error)
    PrintJSON(results)

def DeleteMessage(service, messageId):
    """ Delete a message permanently"""

    try:
        results = service.users().messages().delete(userId='me',id=messageId).execute()
        print("Message Deleted ..")
    except errors.HttpError, error:
        print('An error occurred: %s' % error)
    print(results)

def TrashMail(service,messageId):
    """ Move a Mail to Trash"""
    try:
        results = service.users().messages().trash(userId='me', id=messageId).execute()
        print("Mailed moved to trash..")
    except errors.HttpError, error:
        print('An error occurred: %s' % error)
    # print(results)

def ShowLabels(service):
    """
    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])
def MarkRead(service,messageId):

    label_body = {
    "removeLabelIds": [ 'UNREAD'],
    "addLabelIds": [ ],
  }
    try:
        results = service.users().messages().modify(userId='me', id=messageId, body=label_body).execute()
    except errors.HttpError, error:
        print('An error occurred: %s' % error)

def CreateMessage(send_msg):
  """Create a message for an email.
  """
  message = MIMEText(send_msg['body'])
  message['to'] = send_msg['To']
  message['from'] = send_msg['From']
  message['subject'] = send_msg['Subject']
  return {'raw': base64.b64encode(message.as_string())}

def SendMessage(service, message):
  """Send an email message.
  """
  try:
    message = (service.users().messages().send(userId='me', body=message).execute())
    print ('Mail Sent Succsessfully Message Id: %s' % message['id'])
    return message
  except errors.HttpError, error:
    print('An error occurred: %s' % error)

def SaveToDrafts(service,message):

    try:
        message = (service.users().drafts().create(userId='me', body=message).execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError, error:
        print('An error occurred: %s' % error)

def main():
    """
    Creates a Gmail API service object.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    ShowUnreadEmail(service)

if __name__ == '__main__':
    main()
