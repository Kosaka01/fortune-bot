import random
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- ЛОГИ ---
logging.basicConfig(level=logging.INFO)

# --- НАСТРОЙКИ ---
TELEGRAM_TOKEN = "mytoken"
GOOGLE_CREDENTIALS_FILE = "service-account.json"  # скачанный JSON
SPREADSHEET_NAME = "predictions"  # название таблицы

# --- ДОСТУП К GOOGLE SHEETS ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_CREDENTIALS_FILE, scope)
client = gspread.authorize(creds)
sheet = client.open(SPREADSHEET_NAME).sheet1

# --- КОМАНДЫ ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот с предсказаниями 🔮 Напиши /predict, чтобы получить своё будущее!")

async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    predictions = sheet.col_values(1)[1:]  # пропускаем заголовок
    if predictions:
        prediction = random.choice(predictions)
        await update.message.reply_text(f"{prediction}")
    else:
        await update.message.reply_text("Увы, предсказаний пока нет 😢")

# --- ЗАПУСК ---
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("predict", predict))

    app.run_polling()

if __name__ == "__main__":
    main()
