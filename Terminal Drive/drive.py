
from __future__ import print_function
import httplib2
import os
import json
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Terminal Drive'

def PrintJSON(dict):

    print(json.dumps(dict,indent=4,sort_keys=True))

def UplaodFile(service, file_path):
    """ Upload file to Drive Home folder"""

    print("Uploads files to Google Drive")

    # result = service.files().
def GetFile(service,fileId):

    metadata = service.files().get(fileId=fileId,acknowledgeAbuse=None).execute()
    filename = metadata['name']

    current_path = os.getcwd()
    file_path = os.path.join(current_path,filename)
    file = open(file_path,'w')
    file.write(service.files().get_media(fileId=fileId,acknowledgeAbuse=None).execute())
    file.close()
    print(metadata)

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
                                   'drive-python-quickstart.json')

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

def ListRecentFiles(service):
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        # for item in items:
        #     print('{0} ({1})'.format(item['name'], item['id']))
        file = items[0]
        fileId = file['id']
        GetFile(service,fileId)

def main():
    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    for up to 10 files.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    ListRecentFiles(service)
    # file_path = "amit.txt"
    # UplaodFile(service,file_path)

if __name__ == '__main__':
    main()










