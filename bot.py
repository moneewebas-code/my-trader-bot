import telebot
import yfinance as yf
import pandas_ta as ta
import os
from flask import Flask
from threading import Thread

# 1. إعداد سيرفر وهمي عشان Render ما يقفلش البوت
app = Flask('')
@app.route('/')
def home():
    return "Bot is Running!"

def run():
    app.run(host='0.0.0.0', port=8080)

# 2. إعداد البوت بتاعك
TOKEN = '8506078405:AAEo4lemoQyeVr5-tZLEQNA6JuArNxZrs9o'
bot = telebot.TeleBot(TOKEN)

def get_full_analysis(symbol):
    try:
        data = yf.download(symbol, period="1mo", interval="1d", progress=False)
        if data.empty or len(data) < 14:
            return "⚠️ البيانات غير كافية حالياً."
        
        last_price = data['Close'].iloc[-1]
        data['RSI'] = ta.rsi(data['Close'], length=14)
        rsi_val = data['RSI'].iloc[-1]

        if rsi_val < 35: signal = "🟢 فرصة شراء"
        elif rsi_val > 65: signal = "🔴 منطقة بيع"
        else: signal = "🟡 منطقة انتظار"
            
        return f"📊 السعر: {last_price:.2f} ج.م\n📈 RSI: {rsi_val:.1f}\n💡 التوصية: {signal}"
    except:
        return "❌ خطأ في سحب البيانات."

@bot.message_handler(func=lambda m: True)
def handle_msg(message):
    stocks = {'فوري': 'FWRY.CA', 'cib': 'COMI.CA', 'طلعت': 'TMGH.CA', 'دهب': 'AZG.CA'}
    text = message.text.lower().strip()
    if text in stocks:
        bot.reply_to(message, f"🤖 المحلل الذكي بيراجع {text}...")
        bot.reply_to(message, get_full_analysis(stocks[text]))
    else:
        bot.reply_to(message, "ابعت اسم السهم (فوري، دهب، cib)")

# 3. تشغيل السيرفر والبوت مع بعض
def start_bot():
    t = Thread(target=run)
    t.start()
    print("🚀 البوت انطلق على السيرفر!")
    bot.infinity_polling()

if __name__ == "__main__":
    start_bot()
