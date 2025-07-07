from telegram import Update
from telegram.ext import (
    ApplicationBuilder, MessageHandler, CommandHandler,
    filters, ContextTypes
)
from cipher_core import process
from flask import Flask
from threading import Thread
import os
import asyncio
import requests

# توکن ربات و کلید OpenRouter
TOKEN = os.getenv("BOT_TOKEN")
AI_KEY = os.getenv("OPENROUTER_API_KEY")

# ⚙️ راه‌اندازی Flask برای باز نگه‌داشتن سرویس Render
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "🤖 ربات رمزگذار هوشمند در حال اجراست."

def run_flask():
    flask_app.run(host='0.0.0.0', port=8080)

# 📡 ارسال پیام به هوش مصنوعی (مدل DeepSeek / OpenRouter)
def ask_ai(prompt):
    try:
        headers = {
            "Authorization": f"Bearer {AI_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "تو یک ربات راهنمای رمزگذاری هستی. به زبان ساده و دوستانه کمک کن."},
                {"role": "user", "content": prompt}
            ]
        }
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ خطا در اتصال به هوش مصنوعی: {e}"

# 🧠 مدیریت پیام‌ها
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if text.startswith("رمزگذاری -"):
        code = text.replace("رمزگذاری -", "").strip()
        result = process(code, mode='encode')
        await update.message.reply_text(result, reply_to_message_id=update.message.message_id)

    elif text.startswith("رمزگشایی -"):
        code = text.replace("رمزگشایی -", "").strip()
        result = process(code, mode='decode')
        await update.message.reply_text(result, reply_to_message_id=update.message.message_id)

    else:
        # اتصال به هوش مصنوعی برای پاسخ هوشمند
        await update.message.reply_text("🤖 در حال پردازش با هوش مصنوعی...")
        reply = ask_ai(text)
        await update.message.reply_text(reply, reply_to_message_id=update.message.message_id)

# پاسخ به /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! من ربات رمزگذار مدنرچ هستم. 🧠\n\n"
        "📌 برای رمزگذاری بنویس:\n"
        "رمزگذاری - 68+{سلام}*\n\n"
        "📌 برای رمزگشایی:\n"
        "رمزگشایی - 68+{四风啊...}*\n\n"
        "سوالی داشتی، راحت بپرس 😊"
    )

# اجرای اصلی ربات
async def main():
    print("🚀 ربات در حال اجراست...")

    Thread(target=run_flask).start()

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    await app.run_polling()

# اجرای امن برای محیط‌هایی مثل Render
if __name__ == "__main__":
    try:
        import nest_asyncio
        nest_asyncio.apply()
        loop = asyncio.get_event_loop()
        loop.create_task(main())
        loop.run_forever()
    except Exception as e:
        print(f"❌ خطا هنگام اجرای ربات: {e}")
