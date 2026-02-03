import telebot
import yfinance as yf
import pandas as pd
from flask import Flask
import threading
import os

# 1. إعدادات البوت والتوكن الخاص بك
API_TOKEN = '7511116664:AAH_S_2pLly7I6E_6R33D2hIas3m4_Nia8w'
bot = telebot.TeleBot(API_TOKEN)
server = Flask(__name__)

# 2. محرك التحليل الذكي (خوارزمية RSI و Moving Averages)
def analyze_stock_logic(ticker):
    try:
        # البحث في البورصة المصرية تلقائياً
        symbol = f"{ticker.upper()}.CA"
        df = yf.download(symbol, period="60d", interval="1d", progress=False)
        
        if df.empty:
            return "❌ لم أجد هذا السهم. جرب الأكواد الإنجليزية (مثل: FWRY, TMGH, COMI)."

        # حساب المؤشرات الفنية (الذكاء البرمجي)
        last_close = float(df['Close'].iloc[-1])
        ma20 = float(df['Close'].rolling(window=20).mean().iloc[-1])
        
        # حساب مؤشر RSI (مؤشر القوة النسبية)
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs.iloc[-1]))

        # التحليل والقرار
        if rsi < 30:
            status = "🔵 فرصة ذهبية: السهم في منطقة قاع (تشبع بيعي) - احتمالية ارتداد قوية."
        elif rsi > 70:
            status = "⚠️ تنبيه: السهم في منطقة قمة (تشبع شرائي) - خطر جني الأرباح."
        elif last_close > ma20:
            status = "🟢 اتجاه إيجابي: السعر مستقر فوق المتوسط."
        else:
            status = "🔴 اتجاه حذر: السعر تحت المتوسط."

        return (f"🚀 **التقرير الذكي لسهم: {ticker.upper()}**\n\n"
                f"💰 السعر الحالي: {last_close:.2f} ج.م\n"
                f"📈 متوسط 20 يوم: {ma20:.2f}\n"
                f"📉 مؤشر القوة (RSI): {rsi:.1f}\n"
                f"💡 التحليل: {status}")
    except:
        return "❌ حدث خطأ فني أثناء جلب البيانات. حاول مرة أخرى."

# 3. خدمات إضافية (تحويل العملات)
def get_usd_price():
    try:
        usd_data = yf.download("EGPHM=X", period="1d", progress=False)
        return float(usd_data['Close'].iloc[-1])
    except:
        return None

# 4. أوامر البوت
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "أهلاً يا منير! 🤖 أنا بوتك للذكاء المالي.\n\n"
                          "🔹 ابعت كود السهم (مثل: FWRY) للتحليل الفني.\n"
                          "🔹 ابعت كلمة 'دولار' لمعرفة السعر الحالي.")

@bot.message_handler(func=lambda m: m.text.lower() in ['دولار', 'سعر الدولار'])
def usd_handler(message):
    price = get_usd_price()
    if price:
        bot.reply_to(message, f"💵 سعر الدولار الرسمي حالياً: {price:.2f} ج.م")
    else:
        bot.reply_to(message, "❌ تعذر جلب سعر العملة حالياً.")

@bot.message_handler(func=lambda m: True)
def stock_handler(message):
    ticker = message.text.strip().upper()
    bot.reply_to(message, f"⚙️ جاري تشغيل خوارزميات التحليل لـ {ticker}...")
    result = analyze_stock_logic(ticker)
    bot.reply_to(message, result)

# 5. إعدادات السيرفر لضمان بقاء البوت Healthy (Port 8000)
@server.route('/')
def health(): return "AI Bot is Running", 200

if __name__ == "__main__":
    threading.Thread(target=lambda: server.run(host='0.0.0.0', port=8000)).start()
    bot.infinity_polling()
