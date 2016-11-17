
from __future__ import print_function
import httplib2
import os
import json
import sys
from googleapiclient.http import MediaFileUpload
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

# try:
#     import argparse
#     flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
# except ImportError:
#     flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Terminal Drive'

def PrintJSON(dict):

    print(json.dumps(dict,indent=4,sort_keys=True))

def UplaodFile(service, file_path):
    """ Upload file to Drive Home folder"""

    filename = file_path.split('/').pop()
    extension = filename.split('.').pop()

    doc_mimeType = {
        'html':'text/html',
        'docx':'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'rtf':'application/rtf',
        'txt':'text/plain',
        'odt':'application/vnd.oasis.opendocument.text',
    }

    xls_mimeType = {
        'csv':'text/csv',
        'xlsx':'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'ods':'application/x-vnd.oasis.opendocument.spreadsheet',

    }

    slide_mimeTypes = {
        'pdf':'application/pdf',
        'odp':'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
    }

    image_mimeTypes = {
        'jpeg':'image/jpeg',
        'png':'image/png',
        'svg':'image/svg+xml'
    }

    upload_mimeType = ''

    if extension in doc_mimeType.keys():
        mimeType = doc_mimeType[extension]
        upload_mimeType = 'application/vnd.google-apps.document'
    elif extension in xls_mimeType:
        mimeType = xls_mimeType[extension]
        upload_mimeType = 'application/vnd.google-apps.spreadsheet'
    elif extension in slide_mimeTypes:
        mimeType = slide_mimeTypes[extension]
        upload_mimeType = 'application/vnd.google-apps.presentation'
    elif image_mimeTypes:
        mimeType = image_mimeTypes[extension]
        upload_mimeType = image_mimeTypes[extension]
    else :
        print ("Unknow Extension Can't uplaod")
        return

    media = MediaFileUpload(file_path,
                            mimetype = mimeType,
                            resumable=True)

    file_metadata = {
        'name': filename,
        'mimeType': upload_mimeType
    }

    file = service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()

    print("File Uploaded Successfully..")
    print('File ID: %s' % file.get('id'))


def WriteToFile(filename,file_content):

    current_path = os.getcwd()
    file_path = os.path.join(current_path, filename)
    file = open(file_path, 'w')
    file.write(file_content)
    file.close()

    # result = service.files().
def GetFile(service,fileId):

    metadata = service.files().get(fileId=fileId,acknowledgeAbuse=None).execute()
    PrintJSON(metadata)

    filename = metadata['name']
    mimeType = metadata['mimeType']

    media_mimeTypes =[
        'image/jpeg',
        'image/png',
        'image/svg+xml'
    ]

    if mimeType in media_mimeTypes:
        file_content  = service.files().get_media(fileId=fileId,acknowledgeAbuse=None).execute()
        WriteToFile(filename,file_content)
    else:
        file_content = service.files().export(fileId=fileId,mimeType='application/pdf').execute()
        WriteToFile(filename,file_content)

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
        # if flags:
        #     credentials = tools.run_flow(flow, store, flags)
        # else: # Needed only for compatibility with Python 2.6
        #     credentials = tools.run(flow, store)
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
        files = {}
        count = 0
        file_map =[]
        for item in items:
            print(str(count) + " "+ format(item['name'] + " "+ item['id']))
            files[item['name']] = item['id']
            count = count + 1
            file_map.append(item['id'])

        view_file = raw_input('Enter Corresponding No:')
        GetFile(service,file_map[int(view_file)])

def Help():
    print("Terminal Drive Instruction Set")
    print("Show Help : drive ")
    print("List Recent Files : drive list")
    print("Upload a file : drive up <filepath>")
    print("Download File : drive down <Filename>")

def main():
    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    for up to 10 files.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    if len(sys.argv) < 2:
        Help()
    else:
        option = sys.argv[1]
        if option == "list":
            ListRecentFiles(service)
        elif option == "up":
            file_path = sys.argv[2]
            UplaodFile(service,file_path)
        elif option == "down":
            filename = sys.argv[2]
            GetFile(service,filename)
        else:
            print("Not An Option")
            Help()
    # ListRecentFiles(service)

# if __name__ == '__main__':
main()