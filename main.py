import requests
import pandas as pd
import os.path
from google.oauth2.credentials import Credentials
from gspread_dataframe import set_with_dataframe
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

# Define constants
SAMPLE_SPREADSHEET_ID_INPUT = '1x3C1QnFaHdhg_le5Q7H3i-m1hW2Mvcrc0yYv61sqsQ'
CLEAR_RANGE = "A2:J"
TOKENS_RANGE_NAME = 'GET ALL TOKENS!A2:J5000'
FIATS_RANGE_NAME = 'GET ALL FIATS!A2:J5000'
SAMPLE_RANGE_NAME = 'GET ALL CRYPTOCURRENCIES!A2:J5000'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def main():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)
    return service

def update_sheet(service, sheet_id, sheet_range, df, sheet_index=0):
    # Load data from the sheet
    result = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=sheet_range).execute()
    values = result.get('values', [])
    # Convert the data into a Pandas dataframe
    df_old = pd.DataFrame(values[1:], columns=values[0])
    # Append new data to the dataframe
    df_concat = pd.concat([df_old, df], ignore_index=True)
    # Save the updated data to the sheet
    worksheet = service.spreadsheets().worksheets().get(spreadsheetId=sheet_id, sheetId=sheet_index).execute()
    worksheet_title = worksheet['properties']['title']
    set_with_dataframe(service.open_by_key(sheet_id).worksheet(worksheet_title), df_concat)
    
def clear_sheet(service, sheet_id, sheet_range, sheet_index=0):
    worksheet = service.spreadsheets().worksheets().get(spreadsheetId=sheet_id, sheetId=sheet_index).execute()
    worksheet_title = worksheet['properties']['title']
    service.spreadsheets().values().clear(spreadsheetId=sheet_id, range=sheet_range).execute()

# STEP 1: GET ALL TOKENS
url = "https://cryptfolio.com/api/currencies/tokens"
response = requests.get(url)
currencies = response.json()['result']['currencies']
df_tokens = pd.DataFrame.from_records(currencies)

service = main()
clear_sheet(service, SAMPLE_SPREADSHEET_ID_INPUT, TOKENS_RANGE_NAME)
update_sheet(service, SAMPLE_SPREADSHEET_ID_INPUT, TOKENS_RANGE_NAME, df_tokens)
print("#------------- STEP 1 - GET TOKENS - COMPLETE -------------------------#")

# STEP 2: GET ALL FIATS
url = "https://cryptfolio.com/api/currencies/fiat"
response = requests.get(url)
currencies = response.json()['result']['currencies']
df_fiats = pd.DataFrame.from_records(currencies)

clear_sheet(service, SAMPLE_SPREADSHEET_ID_INPUT, FIATS_RANGE_NAME, 1)
update_sheet(service, SAMPLE_SPREADSHEET_ID_INPUT, FIATS_RANGE_NAME, df_fiats, 1)
print("#------------- STEP 2 - GET FIATS - COMPLETE -------------------------#")

# STEP 2: GET ALL CRYPTOCURRENCIES
url = "https://cryptfolio.com/api/currencies/cryptocurrencies"
response = requests.get(url)
currencies = response.json()['result']['currencies']
df_fiats = pd.DataFrame.from_records(currencies)

clear_sheet(service, SAMPLE_SPREADSHEET_ID_INPUT, FIATS_RANGE_NAME, 2)
update_sheet(service, SAMPLE_SPREADSHEET_ID_INPUT, FIATS_RANGE_NAME, df_fiats, 2)
print("#-------------STEP 3 - GET CRYPTOCURRENCIES - COMPLETE -------------------------#")