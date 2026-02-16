import os
import json
import gspread
from google.oauth2.service_account import Credentials


def get_sheet():
    creds_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    creds_dict = json.loads(creds_json)

    credentials = Credentials.from_service_account_info(
        creds_dict,
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
    )

    client = gspread.authorize(credentials)
    sheet = client.open("webhoot").sheet1

    return sheet


def email_exists(email: str) -> bool:
    sheet = get_sheet()
    records = sheet.get_all_records()

    for row in records:
        if row.get("email") == email:
            return True

    return False