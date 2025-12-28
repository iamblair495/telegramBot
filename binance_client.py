import hashlib
import hmac
import logging
import os
import time
import json

import requests
from dotenv import load_dotenv

#load env
load_dotenv()

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")

if not BINANCE_API_KEY or not BINANCE_API_SECRET:
    logging.error("Binance API keys not loaded!!")

def get_spot_balance():
    base_url = "https://api.binance.com"
    endpoint = "/api/v3/account"

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

def get_last_deposits(limit=3):
    base_url = "https://api.binance.com"
    endpoint = "/sapi/v1/capital/deposit/hisrec"

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

    deposits = response.json()

    # Sort newest → oldest and return last N
    deposits.sort(key=lambda x: x["insertTime"], reverse=True)
    return deposits[:limit]

def get_active_positions():
    base_url = "https://fapi.binance.com"
    endpoint = "/fapi/v2/positionRisk"

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

    positions = response.json()

    # Filter only active positions (positionAmt != 0)
    active_positions = [p for p in positions if float(p["positionAmt"]) != 0]
    return active_positions

def get_last_closed_trades(limit=10):
    base_url = "https://fapi.binance.com"
    endpoint = "/fapi/v1/income"

    timestamp = int(time.time() * 1000)
    query_string = f"incomeType=REALIZED_PNL&limit={limit}&timestamp={timestamp}"

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
