from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from cipher_core import process
import asyncio

# 🔐 توکن واقعی رباتت رو جایگزین کن
TOKEN = "7677479368:AAHIAs-H6yPIzrvorwbO3qqv3HENfUJ6qrQ"

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

    elif text == "/start":
        await update.message.reply_text(
            "سلام! من ربات رمزگذار مدنرچ هستم. 🧠\n\n"
            "📌 رمزگذاری:\n"
            "رمزگذاری - 68+{سلام}*\n\n"
            "📌 رمزگشایی:\n"
            "رمزگشایی - 68+{四风啊...}*\n\n"
            "📌 رمزگشایی با راهنما:\n"
            "رمزگشایی - (5+:م){四风啊...}*",
            reply_to_message_id=update.message.message_id
        )

    else:
        await update.message.reply_text(
            "❗️دستور نامعتبر.\n\n"
            "رمزگذاری - 68+{سلام}*\n"
            "رمزگشایی - 68+{متن رمزی}*\n"
            "یا رمزگشایی با راهنما:\n(5+:م){...}*",
            reply_to_message_id=update.message.message_id
        )

if __name__ == "__main__":
    print("🚀 ربات در حال اجراست...")

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(app.run_polling())