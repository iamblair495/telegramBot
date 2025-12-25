import logging
import responses
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import os
from dotenv import load_dotenv
import requests
from requests.auth import HTTPBasicAuth

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
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("custom", custom_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Register error handler
    app.add_error_handler(error_handler)

    # Run the bot
    app.run_polling(1.0)

if __name__ == "__main__":
    main()
