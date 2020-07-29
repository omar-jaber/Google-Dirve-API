from __future__ import print_function
from oauth2client import client, tools
from oauth2client.file import Storage
from googleapiclient import discovery, errors
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import httplib2
import os, io

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


class auth():
    def __init__(self, SCOPES, CLIENT_SECRET_FILE, APPLICATION_NAME):
        self.SCOPES = SCOPES
        self.CLIENT_SECRET_FILE = CLIENT_SECRET_FILE
        self.APPLICATION_NAME = APPLICATION_NAME

    def getCredentials(self):
        
        """Gets valid user credentials from storage.
        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.
        Returns:
            Credentials, the obtained credential.
        """
        cwd_dir = os.getcwd()
        credential_dir = os.path.join(cwd_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'google-drive-credentials.json')

        store = Storage(credential_path)
        credential = store.get()
        if not credential or credential.invalid:
            flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
            flow.user_agent = self.APPLICATION_NAME
            if flags:
                credential = tools.run_flow(flow, store, flags)
            else:  # Needed only for compatibility with Python 2.6
                credential = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credential


SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'
authInst = auth(SCOPES, CLIENT_SECRET_FILE, APPLICATION_NAME)
credentials = authInst.getCredentials()
http = credentials.authorize(httplib2.Http())
dirve_service = discovery.build('drive', 'v3', http=http)

def listFiles(size):
    results = dirve_service.files().list(
        pageSize=size, fields="nextPageToken, files(id, name)").execute()

    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id']))


def uplodeFile(fileName, filePath, mimetype):
    file_metadata = {'name': fileName}
    media = MediaFileUpload(filePath, mimetype=mimetype)
    file = dirve_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print('File ID: %s' % file.get('id'))


def downlodeFile(fileId, filePath, mimeType):
    request = dirve_service.files().export_media(fileId=fileId,
                                                 mimeType=mimeType)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))

    with io.open(filePath, 'wb') as f:
        fh.seek(0)
        f.write(fh.read())


def update_file(file_id, new_title, new_description, new_mime_type,
                                new_filename, new_revision):
    """Update an existing file's metadata and content.

    Args:
        service: Drive API service instance.
        file_id: ID of the file to update.
        new_title: New title for the file.
        new_description: New description for the file.
        new_mime_type: New MIME type for the file.
        new_filename: Filename of the new content to upload.
        new_revision: Whether or not to create a new revision for this file.
    Returns:
        Updated file metadata if successful, None otherwise.
    """
    try:
        # File metadata
        file_metadata = {
            'name': new_title,
            'description': new_description
        }

        # File's new content.
        media_body = MediaFileUpload(
                new_filename, mimetype=new_mime_type) # In this case the file is small so no resumable flag needed

        # Send the request to the API.
        updated_file = dirve_service.files().update(
                fileId=file_id,
                body=file_metadata,
                media_body=media_body).execute()
        return updated_file
    except Exception as e:
        print ('An error occurred: %s' % e)
        return None



#put your own information

#to upload : 
fileName=""
filePath=""
mimetype=""

# to download :
fileId=""
filePath=""
mimeType=""


# to update file :
file_id=""
new_filename=""
new_title=""
new_description=""
new_mime_type=""
new_revision=True or False 




x = int(input("if you want to uplode enter 1\nif you want to downlode enter 2\nif you want to update enter 3\n"))
if x == 1:
    uplodeFile(fileName=fileName, filePath=filePath, mimetype= mimetype)
if x == 2:
    downlodeFile(fileId=fileId ,filePath=filePath, mimeType=mimeType)
if x == 3:
    update_file(file_id=file_id, new_filename = new_filename, new_title=new_title
                ,new_description= new_description , new_mime_type = new_mime_type, new_revision=new_revision)


