import os
import json
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Application, CommandHandler, ContextTypes, InlineQueryHandler
import uuid

# --- Переменные окружения ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
creds_json = json.loads(os.getenv("GOOGLE_CREDS"))

# --- Google Sheets ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
client = gspread.authorize(creds)
sheet = client.open("predictions").sheet1

# --- команды ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот с предсказаниями 🔮 Напиши /predict или вызови меня через inline: @open_predictions_bot")

async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    predictions = sheet.col_values(1)[1:]
    if predictions:
        text = random.choice(predictions)
        await update.message.reply_text(f"🔮 {text}")
    else:
        await update.message.reply_text("Увы, предсказаний пока нет 😢")

# --- inline-режим ---
async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    predictions = sheet.col_values(1)[1:]

    if not predictions:
        return

    # одно случайное предсказание
    prediction = random.choice(predictions)
    user = update.inline_query.from_user.first_name

    results = [
        InlineQueryResultArticle(
            id=str(uuid.uuid4()),
            title="Получить предсказание 🔮",
            input_message_content=InputTextMessageContent(
                f"Предсказание для {user}:\n\n{prediction}"
            )
        )
    ]

    await update.inline_query.answer(results, cache_time=0)

# --- запуск ---
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("predict", predict))
    app.add_handler(InlineQueryHandler(inline_query))

    app.run_polling()

if __name__ == "__main__":
    main()
