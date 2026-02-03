import telebot
import yfinance as yf
import pandas as pd
from flask import Flask
import threading
import time

# 1. التوكن الخاص بك (جاهز للعمل)
API_TOKEN = '7511116664:AAH_S_2pLly7I6E_6R33D2hIas3m4_Nia8w'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# 2. محرك التحليل الذكي (خوارزمية التحليل الفني)
def get_ai_analysis(ticker):
    try:
        # إضافة .CA تلقائياً للبورصة المصرية
        symbol = f"{ticker.upper()}.CA"
        data = yf.download(symbol, period="60d", interval="1d", progress=False)
        
        if data.empty:
            return "❌ الكود ده مش موجود في البورصة المصرية. جرب أكواد زي FWRY أو TMGH."

        # حساب المؤشرات (الذكاء البرمجي)
        current_price = float(data['Close'].iloc[-1])
        ma20 = float(data['Close'].rolling(window=20).mean().iloc[-1])
        
        # حساب مؤشر القوة النسبية RSI
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs.iloc[-1]))

        # منطق اتخاذ القرار
        if rsi < 30:
            advice = "🔵 السهم في منطقة (قاع) - فرصة شراء قوية جداً."
        elif rsi > 70:
            advice = "⚠️ السهم في منطقة (قمة) - خطر، تشبع شرائي وقد يهبط."
        elif current_price > ma20:
            advice = "🟢 إتجاه صاعد - السعر فوق المتوسط."
        else:
            advice = "🔴 إتجاه هابط - يفضل الانتظار."

        return (f"🚀 **تقرير الذكاء المالي لسهم: {ticker.upper()}**\n\n"
                f"💰 السعر الحالي: {current_price:.2f} ج.م\n"
                f"📈 متوسط 20 يوم: {ma20:.2f}\n"
                f"📉 مؤشر القوة (RSI): {rsi:.1f}\n"
                f"💡 النصيحة الفنية: {advice}\n"
                f"🕒 تحديث: {time.strftime('%H:%M:%S')}")
    except Exception as e:
        return f"❌ خطأ فني: تأكد من كتابة الكود صح."

# 3. أوامر البوت
@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "مرحباً يا منير! 🤖 أنا بوتك المحلل الذكي.\nابعت لي كود السهم (FWRY, TMGH, COMI) وهيديك تحليل فني فوري.")

@bot.message_handler(func=lambda m: True)
def handle_msg(message):
    ticker = message.text.strip().upper()
    bot.reply_to(message, f"⚙️ جاري تشغيل خوارزميات التحليل لـ {ticker}...")
    bot.reply_to(message, get_ai_analysis(ticker))

# 4. خادم البقاء (Flask) متوافق مع بورت Koyeb
@app.route('/')
def health_check():
    return "AI Bot is Online!", 200

def run_flask():
    app.run(host='0.0.0.0', port=8000)

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    print("🚀 الوحش انطلق!")
    bot.infinity_polling()
