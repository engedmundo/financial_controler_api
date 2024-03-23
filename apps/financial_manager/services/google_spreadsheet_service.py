from decouple import config
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GoogleSpreadsheetService:
    def __init__(self):
        self.credentials_file_path = "google_api_credentials.json"
        self.creds = Credentials.from_service_account_file(
            self.credentials_file_path
        )
        self.spreadsheet_id = config("READ_SPREADSHEET_ID")
        self.range_name = config("READ_RANGE_NAME")

    def read_spreadsheet(self) -> list:
        try:
            service = build("sheets", "v4", credentials=self.creds)
            result = (
                service.spreadsheets()
                .values()
                .get(
                    spreadsheetId=self.spreadsheet_id,
                    range=self.range_name,
                )
                .execute()
            )
            raw_sheet = result.get("values", [])
            return raw_sheet
        except HttpError as err:
            print(err)
