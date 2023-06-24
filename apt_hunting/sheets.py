import os
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from utils.sheets_utils import SCOPES
from utils.sheets_utils import CREDENTIALS_FILE
from utils.sheets_utils import TOKENS_FILE
from utils.sheets_utils import SHEET_HEADERS
from utils.sheets_utils import SHEET_ID_FILE

def create_token():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists(CREDENTIALS_FILE):
        creds = Credentials.from_authorized_user_file(TOKENS_FILE, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKENS_FILE, 'w') as token:
            token.write(creds.to_json())
    return creds

def get_sheet_id(creds):
    if os.path.exists(SHEET_ID_FILE):
        with open(SHEET_ID_FILE, 'r') as file:
            data = json.load(file)
            if data:
                return data['sheet_id']

    return build_sheet(creds, "NYC Apartments")

def append_sheet(creds, sheet_id, listings):
    service = build('sheets', 'v4', credentials=creds)
    body = {
        "majorDimension": "ROWS",
        "values": listings
    }
    request = service.spreadsheets().values().append(spreadsheetId=sheet_id,
                                                     range="Sheet1!A:A",
                                                     valueInputOption="USER_ENTERED", 
                                                     body=body)
    response = request.execute()
    return response

def insert_sheet(creds, sheet_id, listings):
    service = build('sheets', 'v4', credentials=creds)
    body = {
        "majorDimension": "ROWS",
        "values": listings
    }
    request = service.spreadsheets().values().update(spreadsheetId=sheet_id,
                                                    range="Sheet1!A2:P",
                                                    valueInputOption="USER_ENTERED",
                                                    body=body)
    response = request.execute()
    return response

def write_sheet_id_json(sheet_id):
    with open(SHEET_ID_FILE, 'w') as file:
        file.write(json.dumps({"sheet_id": sheet_id}))
    return True

# Builds a sheet and return the ID
def build_sheet(creds, title):
    try:
        service = build('sheets', 'v4', credentials=creds)
        spreadsheet = {
            'properties': {
                'title': title
            }
        }
        spreadsheet = service.spreadsheets().create(body=spreadsheet,
                                                    fields='spreadsheetId') \
            .execute()
        sheet_id = spreadsheet.get('spreadsheetId')
        write_sheet_id_json(sheet_id)

        # Add headers to sheet
        append_sheet(creds, sheet_id, SHEET_HEADERS) 
        # Bold first row
        body = {'requests': [
            {'repeatCell': {
                'range': {'endRowIndex': 1},
                'cell':  {'userEnteredFormat': {'textFormat': {'bold': True}}},
                'fields': 'userEnteredFormat.textFormat.bold',
            }}
        ]}
        service.spreadsheets().batchUpdate(spreadsheetId=sheet_id, body=body).execute()

        return sheet_id
    except HttpError as error:
        return False
    
def build_sheet_url(sheet_id):
    return 'https://docs.google.com/spreadsheets/d/{}/'.format(sheet_id)
