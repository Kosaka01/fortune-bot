import os
import json
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Загружаем токен из переменных окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Загружаем JSON с кредами из переменных окружения
creds_json = json.loads(os.getenv("GOOGLE_CREDS"))

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
client = gspread.authorize(creds)

# Подключаемся к таблице
sheet = client.open("predictions").sheet1

# --- команды ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот с предсказаниями 🔮 Напиши /predict")

async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    predictions = sheet.col_values(1)[1:]  # пропускаем заголовок
    if predictions:
        await update.message.reply_text(f"🔮 {random.choice(predictions)}")
    else:
        await update.message.reply_text("Увы, предсказаний пока нет 😢")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("predict", predict))
    app.run_polling()

if __name__ == "__main__":
    main()

