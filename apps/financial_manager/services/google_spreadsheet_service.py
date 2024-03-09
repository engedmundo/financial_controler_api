import os.path

from decouple import config
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError



class GoogleSpreadsheetService:
    def __init__(self):
        self.creds = None
        # If modifying these scopes, delete the file token.json.
        self.scopes = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
]
        self.spreadsheet_id = config("READ_SPREADSHEET_ID")
        self.range_name = config("READ_RANGE_NAME")
        self.credentials_file_path = "google_api_credentials.json"
        self.token_file_path = "google_api_token.json"
        self.check_credentials()


    def check_credentials(self) -> None:
        if os.path.exists(self.token_file_path):
            self.creds = Credentials.from_authorized_user_file(self.token_file_path, self.scopes,)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file_path,
                    self.scopes,
                )
                self.creds = flow.run_local_server(port=0)

            with open(self.token_file_path, "w") as token:
                token.write(self.creds.to_json())


def main():
    creds = None

    try:
        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API
        result = service.spreadsheets().values().get(
            spreadsheetId=READ_SPREADSHEET_ID,
            range=READ_RANGE_NAME,
            ).execute()
        raw_sheet = result.get("values", [])
    except HttpError as err:
        print(err)

def treat_currency_value(value: str) -> float:
    if not value:
        return 0.0

    without_currency = value.replace("R$ ", "")
    numeric_value = without_currency.replace(".", "").replace(",", ".").strip()
    return float(numeric_value)