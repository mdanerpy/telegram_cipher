# app.py
from flask import Flask, request
import asyncio
import os
from cipher_bot import main

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ ربات رمزگذار فعال است!"

@app.route('/webhook', methods=['POST'])
def webhook():
    return "✅ درخواست وبهوک دریافت شد", 200

if __name__ == '__main__':
    asyncio.run(main())
