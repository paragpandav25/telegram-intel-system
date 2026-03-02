import asyncio
from telethon import TelegramClient
from telethon.tl.types import PeerChannel
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta

# =========================
# CONFIGURATION
# =========================

import os

api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]

SERVICE_ACCOUNT_FILE = "service_account.json"
SHEET_ID = os.environ["SHEET_ID"]

CHANNELS = [
    "stockupdate9",
    "stockmarkets19",
    "Brokerage_report",
    "fundamental3", 
    "Equity_Insights"
]


# =========================
# GOOGLE SHEET SETUP
# =========================

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    SERVICE_ACCOUNT_FILE, scope
)

client_gs = gspread.authorize(creds)
sheet = client_gs.open_by_key(SHEET_ID).worksheet("Messages")



# =========================
# TELEGRAM FETCH FUNCTION
# =========================

from datetime import datetime, timedelta, timezone

async def fetch_messages():
    async with TelegramClient("session_name", api_id, api_hash) as client:

        since_time = datetime.now(timezone.utc) - timedelta(days=1)

        rows = [["Timestamp", "Channel", "Message"]]

        for channel in CHANNELS:
            async for message in client.iter_messages(channel):

                if message.date < since_time:
                    break

                if message.text:
                    rows.append([
                        message.date.strftime("%Y-%m-%d %H:%M:%S"),
                        channel,
                        message.text
                    ])

        # Single write call (IMPORTANT)
        sheet.update("A1", rows)

        print("Done fetching messages.")

# =========================
# RUN SCRIPT
# =========================

asyncio.run(fetch_messages())
