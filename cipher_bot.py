import os
from telegram import Update, BotCommand
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from cipher_core import process  # این فایل باید در کنار این فایل باشد

TOKEN = os.getenv("BOT_TOKEN")         # توکن ربات تلگرام
WEBHOOK_URL = os.getenv("WEBHOOK_URL") # آدرس کامل وبهوک، مثل https://yourname.onrender.com/webhook

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
        reply_to_message_id=update.message.message_id  # پیام راهنما در پاسخ به پیام کاربر
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if text.startswith("رمزگذاری -"):
        code = text[len("رمزگذاری -"):].strip()
        result = process(code, mode='encode')
        await update.message.reply_text(
            result,
            reply_to_message_id=update.message.message_id
        )

    elif text.startswith("رمزگشایی -"):
        code = text[len("رمزگشایی -"):].strip()
        result = process(code, mode='decode')
        await update.message.reply_text(
            result,
            reply_to_message_id=update.message.message_id
        )

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

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    await app.bot.set_my_commands([
        BotCommand("start", "شروع و راهنمای استفاده"),
    ])

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    await app.start()
    await app.bot.set_webhook(WEBHOOK_URL)  # اتصال به وبهوک
    await app.wait_until_closed()           # منتظر بمان تا اتصال قطع شود (پایدار)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
