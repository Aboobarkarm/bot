import os
from dotenv import load_dotenv
from typing import Final

from flask import Flask, request, abort
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Load environment variables
load_dotenv()
TOKEN: Final = os.getenv("BOT_TOKEN")
BOT_USERNAME: Final = "@AAAppleSeedBot"
PORT: Final = int(os.getenv("PORT", 5000))  # Default to 5000 if not set

# Flask app
app = Flask(__name__)

# Telegram Bot application
bot_app = Application.builder().token(TOKEN).build()
bot = Bot(token=TOKEN)

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Thanks for chatting with me! I am an Apple.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I am an apple! Please type something so I can respond!")

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
bot_app.add_handler(CommandHandler("custom", custom_command))
bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
bot_app.add_error_handler(error_handler)

# Flask route for Telegram webhook
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot)
        bot_app.update_queue.put_nowait(update)  # send update to bot
        return "OK"
    else:
        abort(403)

# Optional route to check server is running
@app.route("/")
def index():
    return "Bot is running!"

# Run Flask
if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(host="0.0.0.0", port=PORT)
