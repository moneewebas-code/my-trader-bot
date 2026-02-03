import telebot
import yfinance as yf
import pandas as pd
from flask import Flask
import threading
import os

# 1. التوكن بتاعك جاهز
API_TOKEN = '7511116664:AAH_S_2pLly7I6E_6R33D2hIas3m4_Nia8w'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# 2. خوارزمية الذكاء الاصطناعي للتحليل الفني
def ai_stock_analysis(ticker):
    try:
        symbol = f"{ticker.upper()}.CA"
        # سحب بيانات 60 يوم لتحليل أدق
        df = yf.download(symbol, period="60d", interval="1d", progress=False)
        
        if df.empty:
            return "❌ الكود غير صحيح. ابعت كود السهم بالإنجليزي (FWRY, TMGH, COMI)."

        # حساب مؤشر القوة النسبية RSI (ذكاء السوق)
        close = df['Close']
        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs.iloc[-1]))
        
        current_price = float(close.iloc[-1])
        ma20 = float(close.rolling(window=20).mean().iloc[-1])

        # منطق القرار الذكي
        if rsi < 30:
            advice = "🔵 فرصة شراء (السهم في القاع)"
        elif rsi > 70:
            advice = "⚠️ خطر (تشبع شرائي - السهم غالي)"
        elif current_price > ma20:
            advice = "🟢 إيجابي (صعود مستقر)"
        else:
            advice = "🔴 سلبي (انتظر إشارة دخول)"

        return (f"📊 **تحليل ذكي لسهم: {ticker.upper()}**\n\n"
                f"💰 السعر: {current_price:.2f} ج.م\n"
                f"📉 مؤشر RSI: {rsi:.1f}\n"
                f"💡 النصيحة: {advice}")
    except:
        return "❌ مشكلة في سحب البيانات."

# 3. ميزة إضافية: سعر الدولار
def get_usd():
    try:
        data = yf.download("EGPHM=X", period="1d", progress=False)
        return float(data['Close'].iloc[-1])
    except: return None

@bot.message_handler(commands=['start'])
def welcome(m):
    bot.reply_to(m, "أهلاً يا منير! 🤖 أنا بوتك الذكي.\nابعت كود السهم (FWRY) أو كلمة 'دولار'.")

@bot.message_handler(func=lambda m: m.text.strip() == 'دولار')
def show_usd(m):
    price = get_usd()
    bot.reply_to(m, f"💵 سعر الدولار الرسمي: {price:.2f} ج.م" if price else "❌ تعذر السحب.")

@bot.message_handler(func=lambda m: True)
def handle_msg(m):
    ticker = m.text.strip().upper()
    bot.reply_to(m, f"⚙️ ذكاء البوت يحلل {ticker}...")
    bot.reply_to(m, ai_stock_analysis(ticker))

# 4. حل مشكلة الـ Instance Stopped (البورت 8000)
@app.route('/')
def health(): return "I am Alive", 200

if __name__ == "__main__":
    # تشغيل السيرفر على بورت 8000 عشان Koyeb يفضل Healthy
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8000)).start()
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
