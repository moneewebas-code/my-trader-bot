import telebot
import yfinance as yf
import pandas as pd
from flask import Flask
import threading
import time

# 1. التوكن الخاص بك (تم الدمج بنجاح)
API_TOKEN = '7511116664:AAH_S_2pLly7I6E_6R33D2hIas3m4_Nia8w'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# 2. محرك التحليل الذكي (خوارزمية RSI)
def get_advanced_analysis(ticker):
    try:
        symbol = f"{ticker.upper()}.CA"
        data = yf.download(symbol, period="60d", interval="1d", progress=False)
        
        if data.empty:
            return "❌ كود السهم غير صحيح. جرب أكواد مثل: FWRY, TMGH, COMI"

        # حساب المؤشرات الفنية
        price = float(data['Close'].iloc[-1])
        ma20 = float(data['Close'].rolling(window=20).mean().iloc[-1])
        
        # حساب مؤشر RSI (ذكاء اصطناعي فني)
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs.iloc[-1]))

        # تحليل القرار
        if rsi < 30:
            advice = "🔵 شراء قوي (السهم في منطقة قاع)"
        elif rsi > 70:
            advice = "⚠️ بيع/حذر (السهم في منطقة قمة)"
        elif price > ma20:
            advice = "🟢 صعود مستقر (احتفاظ)"
        else:
            advice = "🔴 اتجاه هابط (انتظار)"

        return (f"📊 **تحليل ذكي: {ticker.upper()}**\n\n"
                f"💰 السعر: {price:.2f} ج.م\n"
                f"📈 مؤشر RSI: {rsi:.1f}\n"
                f"💡 القرار: {advice}")
    except:
        return "❌ خطأ في جلب البيانات."

# 3. خدمات العملات (ذكاء إضافي)
def get_currency_price(symbol):
    try:
        data = yf.download(symbol, period="1d", progress=False)
        return float(data['Close'].iloc[-1])
    except: return None

# 4. أوامر البوت
@bot.message_handler(commands=['start'])
def send_welcome(m):
    bot.reply_to(m, "أهلاً يا منير! 🤖 بوت المحلل الذكي يعمل الآن.\n- ابعت كود السهم للتحليل.\n- ابعت 'دولار' أو 'ريال' للأسعار.")

@bot.message_handler(func=lambda m: m.text.strip() in ['دولار', 'ريال'])
def handle_currency(m):
    sym = "EGPHM=X" if m.text == 'دولار' else "SAR=X" # تقريبي للريال
    price = get_currency_price(sym)
    bot.reply_to(m, f"💵 سعر {m.text} الرسمي: {price:.2f} ج.م" if price else "❌ تعذر السحب")

@bot.message_handler(func=lambda m: True)
def handle_stock(m):
    ticker = m.text.strip().upper()
    bot.reply_to(m, f"⚙️ ذكاء البوت يحلل {ticker} حالياً...")
    bot.reply_to(m, get_advanced_analysis(ticker))

# 5. حل مشكلة Stopped (الرد على السيرفر بانتظام)
@app.route('/')
def ping_server():
    return "Bot is alive and healthy!", 200

def run_server():
    # استخدام بورت 8080 وتنسيقه مع إعدادات السيرفر
    app.run(host='0.0.0.0', port=8000)

if __name__ == "__main__":
    threading.Thread(target=run_server).start()
    print("🚀 البوت انطلق!")
    bot.infinity_polling(timeout=20, long_polling_timeout=10)
