import logging
import responses
from telegram.ext import Application, CommandHandler, MessageHandler, filters

API_KEY = '7763875651:AAE5WdaEocbKQRlSUxaP5klQB7K6MFGOfLo'

# Logging setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logging.info("Starting Bot...")

# --- Commands ---
async def start(update, context):
    await update.message.reply_text("Hello there! What's up!!")

async def help_command(update, context):
    await update.message.reply_text("Try typing anything and I will do my best to respond!!")

async def custom_command(update, context):
    await update.message.reply_text("This is a custom command — add anything here!")

# --- Message handler ---
async def handle_message(update, context):
    text = update.message.text
    logging.info(f"user ({update.message.chat.id}) says: {text}")
    await update.message.reply_text(text)

# --- Error handler ---
async def error_handler(update, context):
    logging.error(f"Update {update} caused error {context.error}")

# --- Main ---
def main():
    app = Application.builder().token(API_KEY).build()

    # Register handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("custom", custom_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Register error handler
    app.add_error_handler(error_handler)

    # Run the bot
    app.run_polling()

if __name__ == "__main__":
    main()
