from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import yaml


# If modifying these scopes, delete the file token.json.

def read_portfolio():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    #dirpath = os.path.dirname(os.path.realpath(__file__))
    #dirpath = "\\".join(dirpath.split('\\')[:-1])
    
    with open(f'config.yaml') as file:
        doc = yaml.load(file, Loader=yaml.FullLoader)

    SPREADSHEET_ID = doc['document']['SPREADSHEET_ID']
    RANGE_NAME = doc['document']['RANGE']
    SCOPES = doc['document']['SCOPES']


    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = []
    for range in RANGE_NAME:
        sheet_metadata = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=range,majorDimension='ROWS').execute()
        result.append(sheet_metadata)

    return result


