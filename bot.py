import telebot
import yfinance as yf
from flask import Flask
import threading

# التوكن الشغال بتاعك
API_TOKEN = '8506078405:AAGh3bdfwrqSv7Zsq7o52hdEtbINuRPa4sA'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# قاموس ذكي للأسهم المصرية
EGYPT_STOCKS = {
    "فوري": "FWRY.CA",
    "طلعت مصطفى": "TMGH.CA",
    "بالم هيلز": "PHDC.CA",
    "سي اي بي": "COMI.CA",
    "هرماس": "HRHO.CA"
}

def get_analysis(user_input):
    try:
        # تحويل العربي لكود إنجليزي لو موجود في القاموس
        ticker = EGYPT_STOCKS.get(user_input, user_input.upper())
        if ".CA" not in ticker: ticker += ".CA"
        
        data = yf.download(ticker, period="1mo", progress=False)
        if data.empty: return "❌ الكود غير صحيح. ابعت (فوري) أو (TMGH)."
        
        price = float(data['Close'].iloc[-1])
        ma = float(data['Close'].mean())
        signal = "🟢 شراء" if price > ma else "🔴 انتظار"
        
        return f"📊 سهم: {user_input}\n💰 السعر الحالي: {price:.2f} ج.م\n💡 التوصية: {signal}"
    except:
        return "❌ عذراً، البورصة مغلقة أو الكود خطأ."

@bot.message_handler(func=lambda m: True)
def handle(m):
    text = m.text.strip()
    bot.reply_to(m, f"🔍 جاري تحليل {text}...")
    bot.reply_to(m, get_analysis(text))

@app.route('/')
def health(): return "OK", 200

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8000)).start()
    bot.infinity_polling(timeout=20, long_polling_timeout=10)
