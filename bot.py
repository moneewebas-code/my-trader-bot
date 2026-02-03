import telebot
import yfinance as yf
from flask import Flask
import threading

# التوكن الجديد بتاعك (8506078405)
API_TOKEN = '8506078405:AAGh3bdfwrqSv7Zsq7o52hdEtbINuRPa4sA'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

def get_analysis(ticker):
    try:
        # البحث في البورصة المصرية
        data = yf.download(f"{ticker.upper()}.CA", period="1mo", progress=False)
        if data.empty: return "❌ كود السهم غير صحيح."
        price = float(data['Close'].iloc[-1])
        ma = float(data['Close'].mean())
        signal = "🟢 شراء" if price > ma else "🔴 انتظار"
        return f"📊 سهم: {ticker.upper()}\n💰 السعر: {price:.2f} ج.م\n💡 التوصية: {signal}"
    except: return "❌ خطأ في سحب البيانات."

@bot.message_handler(func=lambda m: True)
def handle(m):
    ticker = m.text.strip().upper()
    bot.reply_to(m, f"🔍 جاري تحليل {ticker}...")
    bot.reply_to(m, get_analysis(ticker))

@app.route('/')
def health(): return "OK", 200

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8000)).start()
    # تشغيل البوت بنظام يمنع التوقف
    bot.infinity_polling(timeout=20, long_polling_timeout=10)
