import hmac
import hashlib
import os
import time
import traceback
import logging
import requests

from dotenv import load_dotenv

import json

#load env
load_dotenv()

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")

if not BINANCE_API_KEY or not BINANCE_API_SECRET:
    logging.error("Binance API keys not loaded!!")

def get_futures_balance():
    #fetchess futures accnt balance using read-only API returning JSON response
    base_url = "https://fapi.binance.com"
    endpoint = "/fapi/v2/account"

    # Returns timestamp of the action performed
    timestamp = int(time.time() * 1000)
    query_string = f"timestamp={timestamp}"

    signature = hmac.new(
        BINANCE_API_SECRET.encode(),
        query_string.encode(),
        hashlib.sha256
    ).hexdigest()

    url = f"{base_url}{endpoint}?{query_string}&signature={signature}"
    headers = {"X-MBX-APIKEY": BINANCE_API_KEY}

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return response.json()