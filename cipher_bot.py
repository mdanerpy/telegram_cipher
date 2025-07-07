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

# توکن از محیط گرفته می‌شود
TOKEN = os.getenv("BOT_TOKEN")

# ⚙️ راه‌اندازی سرور Flask برای پورت Render
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "🤖 ربات رمزگذار در حال اجراست."

def run_flask():
    flask_app.run(host='0.0.0.0', port=8080)

# 🧠 پیام‌های اصلی ربات
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

    elif "سلام" in text or "چطور" in text or "راهنما" in text:
        await update.message.reply_text(
            "🧠 من ربات رمزگذار مدنرچ هستم.\n"
            "📌 برای رمزگذاری:\n"
            "رمزگذاری - 68+{سلام}*\n\n"
            "📌 برای رمزگشایی:\n"
            "رمزگشایی - 68+{四风啊...}*\n\n"
            "📌 رمزگشایی با راهنما:\n"
            "رمزگشایی - (5+:م){四风啊...}*",
            reply_to_message_id=update.message.message_id
        )

    elif "؟" in text or "چرا" in text or "کار نکرد" in text:
        await update.message.reply_text(
            "❓ مشکلی پیش اومده؟ مطمئن شو فرمت دستور درست باشه:\n\n"
            "✅ رمزگذاری - 68+{متن}*\n"
            "✅ رمزگشایی - 68+{متن}*",
            reply_to_message_id=update.message.message_id
        )

    else:
        await update.message.reply_text(
            "❗️دستور نامعتبر.\n\n"
            "📌 رمزگذاری:\n"
            "رمزگذاری - 68+{سلام}*\n\n"
            "📌 رمزگشایی:\n"
            "رمزگشایی - 68+{四风啊...}*\n\n"
            "📌 رمزگشایی با راهنما:\n"
            "رمزگشایی - (5+:م){四风啊...}*",
            reply_to_message_id=update.message.message_id
        )

# پاسخ به /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! من ربات رمزگذار مدنرچ هستم. 🧠\n\n"
        "📌 رمزگذاری:\n"
        "رمزگذاری - 68+{سلام}*\n\n"
        "📌 رمزگشایی:\n"
        "رمزگشایی - 68+{四风啊...}*\n\n"
        "📌 رمزگشایی با راهنما:\n"
        "رمزگشایی - (5+:م){四风啊...}*"
    )

# اجرای اصلی ربات
async def main():
    print("🚀 ربات در حال اجراست...")

    # اجرای Flask برای فعال نگه‌داشتن Render
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
