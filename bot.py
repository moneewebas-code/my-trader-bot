import telebot
import yfinance as yf
import pandas as pd
from flask import Flask
import threading

# التوكن الخاص بك جاهز للعمل
API_TOKEN = '7511116664:AAH_S_2pLly7I6E_6R33D2hIas3m4_Nia8w'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

def get_ai_analysis(ticker):
    try:
        full_ticker = f"{ticker.upper()}.CA"
        stock = yf.Ticker(full_ticker)
        df = stock.history(period="60d") # سحب بيانات شهرين لتحليل أدق
        
        if df.empty:
            return "❌ كود السهم غير صحيح أو لا توجد بيانات للبورصة المصرية."

        # حساب المؤشرات الفنية (ذكاء التحليل)
        current_price = df['Close'].iloc[-1]
        ma20 = df['Close'].rolling(window=20).mean().iloc[-1]
        ma50 = df['Close'].rolling(window=50).mean().iloc[-1]
        
        # حساب مؤشر القوة النسبية RSI (لمعرفة هل السهم متشبع شراء أم بيع)
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1  + rs.iloc[-1]))

        # منطق اتخاذ القرار الذكي
        if current_price > ma20 and rsi < 70:
            advice = "🟢 إشارة إيجابية (شراء لنمو محتمل)"
        elif rsi > 75:
            advice = "⚠️ تشبع شرائي (احذر من هبوط تصحيحي)"
        elif current_price < ma20 and rsi > 30:
            advice = "🔴 اتجاه هابط (يفضل الانتظار)"
        elif rsi < 25:
            advice = "🔵 قاع تاريخي (فرصة ارتداد قوية)"
        else:
            advice = "🟡 منطقة عرضية (مراقبة)"

        return (f"🚀 **تحليل ذكي لسهم: {ticker.upper()}**\n\n"
                f"💰 السعر الحالي: {current_price:.2f} ج.م\n"
                f"📈 متوسط 20 يوم: {ma20:.2f}\n"
                f"📉 مؤشر RSI: {rsi:.1f}\n"
                f"💡 النصيحة الفنية: {advice}\n"
                f"🕒 التاريخ: {df.index[-1].strftime('%Y-%m-%d')}")
    except:
        return "❌ حدث خطأ في معالجة البيانات."

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "مرحباً منير! 🤖 أنا بوتك المحلل الذكي.\nابعت لي كود أي سهم (مثل FWRY أو TMGH) وهحللك المؤشرات فوراً.")

@bot.message_handler(func=lambda m: True)
def handle_msg(message):
    ticker = message.text.strip().upper()
    bot.reply_to(message, f"⚙️ جاري تحليل {ticker} باستخدام خوارزميات السوق...")
    bot.reply_to(message, get_ai_analysis(ticker))

@app.route('/')
def home(): return "AI Stock Bot is Healthy!"

if __name__ == "__main__":
    # تشغيل السيرفر على بورت 8000 ليتوافق مع Koyeb
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8000)).start()
    bot.infinity_polling()
