from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GoogleTable:
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SAMPLE_SPREADSHEET_ID = '1FmMqRZT6PZxc5UqtNHS5WVWbcnAIgwvp1tr37k-puh4'
    def __init__(self):
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
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
        self.service = build('sheets', 'v4', credentials=creds)
    def getData(self,work_sheet,range_name):
            sheet =self.service.spreadsheets()
            result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                       range=f'{work_sheet}!{range_name}').execute()
            values = result.get('values', [])
            if not values:
                print('No data found.')
                return
            return values
    def UpdateData(self,work_sheet,range_name,values):
        data=[
            {
                'range':f'{work_sheet}!{range_name}',
                'values':values
            }
        ]
        body={
            'valueInputOption':'USER_ENTERED',
            'data':data
        }
        sheet = self.service.spreadsheets()
        result = sheet.values().batchUpdate(spreadsheetId=self.SAMPLE_SPREADSHEET_ID,
                                    body=body).execute()
        print(f'{result.get("totalUpdatedCells")} ячеек было обновлено')
