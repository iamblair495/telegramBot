import logging
import os
import traceback

from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters

import responses
from binance_client import get_spot_balance, get_futures_balance, get_last_deposits

# automatically load .env
load_dotenv()

TELE_API_KEY = os.getenv("TELE_API_KEY")

#the below bit will be added if we add mpesa features
CONS_KEY = os.getenv("CONS_KEY")
CONS_SEC = os.getenv("CONS_SEC")

# Logging setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logging.info("Starting Bot...")

# Commands
async def start(update, context):
    await update.message.reply_text("Hello there! What's up!!")
    logging.info("Start command triggered.")

async def balance_command(update, context):
    logging.info("Balance command triggered.")

    try:
        # Spot account
        logging.info("Calling get_spot_balance...")
        spot_data = get_spot_balance()
        balances = spot_data["balances"]

        total_spot_balance = 0.0
        for asset in balances:
            free = float(asset["free"])
            locked = float(asset["locked"])
            total_spot_balance += free + locked

        # Futures account
        logging.info("Calling get_futures_balance...")
        futures_data = get_futures_balance()
        futures_wallet = float(futures_data["totalWalletBalance"])
        futures_available = float(futures_data["availableBalance"])

        message = (
            "📊 Binance Account Overview\n\n"
            f"Spot Account Balance: ${total_spot_balance:.2f}\n\n"
            "📈 Futures Account\n"
            f"Futures Wallet Balance: ${futures_wallet:.2f}\n"
            f"Available Balance: ${futures_available:.2f}"
        )

        await update.message.reply_text(message)

    except Exception as e:
        logging.error(f"Error fetching balances: {e}")
        logging.error(traceback.format_exc())
        await update.message.reply_text("Failed to fetch account balances.")

async def deposits_command(update, context):
    logging.info("Deposits command triggered.")

    try:
        deposits = get_last_deposits(limit=3)

        if not deposits:
            await update.message.reply_text("No deposit history found.")
            return

        message_lines = ["💰 Last 3 Binance Deposits\n"]

        for d in deposits:
            if d.get("status") != 1:
                continue  # skip pending deposits

            asset = d.get("coin", "N/A")
            amount = d.get("amount", "0")
            network = d.get("network", "N/A")

            message_lines.append(f"• {amount} {asset} via {network}")

        await update.message.reply_text("\n".join(message_lines))

    except Exception as e:
        logging.error(f"Error fetching deposits: {e}")
        logging.error(traceback.format_exc())
        await update.message.reply_text("Failed to fetch deposit history.")

async def help_command(update, context):
    await update.message.reply_text("Try typing anything and I will do my best to respond!!")

async def custom_command(update, context):
    await update.message.reply_text("This is a custom command —> add anything here!")

# Message handler
async def handle_message(update, context):
    text = str(update.message.text)
    logging.info(f"user ({update.message.chat.id}) says: {text}")

    #Get responses from responses.py
    response = await responses.get_response(text)

    await update.message.reply_text(response)

# Error handler
async def error_handler(update, context):
    logging.error(f"Update {update} caused error {context.error}")

# Main Function
def main():
    app = Application.builder().token(TELE_API_KEY).build()

    # Register handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("balance", balance_command))
    app.add_handler(CommandHandler("deposits", deposits_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("custom", custom_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Register error handler
    app.add_error_handler(error_handler)

    # Run the bot
    app.run_polling(1.0)

if __name__ == "__main__":
    main()
