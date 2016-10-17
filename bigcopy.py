from __future__ import print_function
import httplib2
import os

from apiclient import errors
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
SCOPES = 'https://www.googleapis.com/auth/drive.file https://www.googleapis.com/auth/drive.metadata.readonly https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'
FILE_NAME = 'test_copy.txt'

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

def retrieve_file(service):
  """Retrieve a list of File resources.

  Args:
    service: Drive API service instance.
  Returns:
    List of File resources.
  """
  file_id = 0
  page_token = None
  query = "name='%s'" % FILE_NAME
  while True:
    response = service.files().list(q="name='test'",
                                    spaces='drive',
                                    fields='nextPageToken, files(id, name)',
                                    pageToken=page_token).execute()
    for file in response.get('files', []):
        # Process change
        print('Found file: %s (%s)' % (file.get('name'), file.get('id')))
        file_id = file.get('id')
    page_token = response.get('nextPageToken', None)
    if page_token is None:
        break;
  print(file_id)
  return file_id 
    
def copy_file(service, origin_file_id, copy_title):
  """Copy an existing file.

  Args:
    service: Drive API service instance.
    origin_file_id: ID of the origin file to copy.
    copy_title: Title of the copy.

  Returns:
    The copied file if successful, None otherwise.
  """
  copied_file = {'title': copy_title}
  try:
    return service.files().copy(
        fileId=origin_file_id, body=copied_file).execute()
  except errors.HttpError, error:
    print('An error occurred: %s' % error)
  return None

def main():
  """Comment
  Creates a Google Drive API service object and outputs the names and IDs
  for up to 10 files.
  """

  credentials = get_credentials()
  http = credentials.authorize(httplib2.Http())
  service = discovery.build('drive', 'v3', http=http)

  copy_file(service, retrieve_file(service), 'testing')
  
  """comment
  results = service.files().list(
      pageSize=10,fields="nextPageToken, files(id, name)").execute()
  items = results.get('files', [])
  if not items:
      print('No files found.')
  else:
      print('Files:')
      for item in items:
          print('{0} ({1})'.format(item['name'], item['id']))
  """

if __name__ == '__main__':
    main()
