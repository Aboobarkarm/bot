import os
from dotenv import load_dotenv
from typing import Final

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from crypto_utils import get_bitcoin_summary


# Load environment variables
load_dotenv()
TOKEN: Final = os.getenv("BOT_TOKEN")
BOT_USERNAME: Final = "@AAAppleSeedBot"
PORT: Final = int(os.getenv("PORT", 5000))  # Render automatically sets $PORT


# Telegram Bot application
bot_app = Application.builder().token(TOKEN).build()

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Thanks for chatting with me! I am an Apple.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I am an apple! Please type something so I can respond!")

async def bitcoin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_bitcoin_summary())

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a custom command!.")

# Responses
def handle_response(text: str) -> str:
    processed = text.lower()
    if "hello" in processed:
        return "Hey there!"
    elif "i love python" in processed:
        return "Python loves you too ❤️"
    elif "how are you" in processed:
        return "I’m doing great, thanks for asking!"
    elif "bye" in processed:
        return "Goodbye! See you soon 👋"
    elif "apple" in processed:
        return "Did someone say Apple? 🍎"
    else:
        return "Sorry, I don’t understand that yet."

# Handle messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text = update.message.text
    print(f"User({update.message.chat.id}) in {message_type}: '{text}'")

    if message_type == "group":
        if BOT_USERNAME in text:
            new_text = text.replace(BOT_USERNAME, "").strip()
            response = handle_response(new_text)
        else:
            return
    else:
        response = handle_response(text)

    print("Bot:", response)
    await update.message.reply_text(response)

# Error handler
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")

# Add handlers to bot
bot_app.add_handler(CommandHandler("start", start_command))
bot_app.add_handler(CommandHandler("help", help_command))
bot_app.add_handler(CommandHandler("bitcoin", bitcoin_command))
bot_app.add_handler(CommandHandler("custom", custom_command))
bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
bot_app.add_error_handler(error_handler)

# Run the bot with webhook
if __name__ == "__main__":
    print("Starting bot webhook server...")
    bot_app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"https://bot-1-9dpd.onrender.com/{TOKEN}"  # <-- your Render URL + token
    )
