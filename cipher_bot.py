from telegram import Update
from telegram.ext import (
    ApplicationBuilder, MessageHandler, CommandHandler,
    filters, ContextTypes
)
from cipher_core import process
import os
import asyncio

# توکن از متغیر محیطی خوانده می‌شود
TOKEN = os.getenv("BOT_TOKEN")

# هندلر پیام‌ها
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if text.startswith("رمزگذاری -"):
        code = text.replace("رمزگذاری -", "").strip()
        result = process(code, mode='encode')
        await update.message.reply_text("رمز گزاری و رمز گشایی با حروف چینی:\n" + result)

    elif text.startswith("رمزگشایی -"):
        code = text.replace("رمزگشایی -", "").strip()
        result = process(code, mode='decode')
        await update.message.reply_text("رمز گزاری و رمز گشایی با حروف چینی:\n" + result)

    else:
        await update.message.reply_text(
            "❗️دستور نامعتبر.\n\n"
            "رمزگذاری - 68+{سلام}*\n"
            "رمزگشایی - 68+{四风啊...}*\n"
            "یا رمزگشایی با راهنما:\n(5+:م){...}*"
        )

# هندلر /start
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

# تابع اصلی
async def main():
    print("🚀 ربات در حال اجراست...")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    await app.run_polling()

# اجرای امن
if __name__ == "__main__":
    asyncio.run(main())
