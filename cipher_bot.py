import os
from flask import Flask, request
from telegram import Update, BotCommand
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from cipher_core import process

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

app = Flask(__name__)
bot_app = ApplicationBuilder().token(TOKEN).build()

START_MESSAGE = (
    "سلام! من ربات رمزگذاری cipher_bot هستم. 🧠\n\n"
    "📌 رمزگذاری:\n"
    "`رمزگذاری - 68+{متن شما}*`\n\n"
    "📌 رمزگشایی:\n"
    "`رمزگشایی - {...}*`\n\n"
    "لطفاً پیام‌ها را دقیق ارسال کنید."
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        START_MESSAGE,
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_to_message_id=update.message.message_id
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if text.startswith("رمزگذاری -"):
        code = text[len("رمزگذاری -"):].strip()
        result = process(code, mode='encode')
        await update.message.reply_text(result, reply_to_message_id=update.message.message_id)

    elif text.startswith("رمزگشایی -"):
        code = text[len("رمزگشایی -"):].strip()
        result = process(code, mode='decode')
        await update.message.reply_text(result, reply_to_message_id=update.message.message_id)

    else:
        msg = (
            "❗️ دستور نامعتبر.\n\n"
            "📌 رمزگذاری:\n"
            "`رمزگذاری - 68+{سلام}*`\n\n"
            "📌 رمزگشایی:\n"
            "`رمزگشایی - {...}*`\n\n"
            "لطفاً از فرمت‌های بالا استفاده کنید."
        )
        await update.message.reply_text(
            msg,
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_to_message_id=update.message.message_id
        )

# ثبت هندلرها
bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

@app.route("/webhook", methods=["POST"])
async def webhook():
    if request.method == "POST":
        data = request.get_json(force=True)
        update = Update.de_json(data, bot_app.bot)
        await bot_app.process_update(update)
    return "OK"

# راه‌اندازی اصلی
if __name__ == "__main__":
    import asyncio
    async def run():
        await bot_app.bot.set_webhook(WEBHOOK_URL)
        app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

    asyncio.run(run())
