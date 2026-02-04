import telebot
import yfinance as yf
from flask import Flask
import threading

# التوكن بتاعك
API_TOKEN = '8506078405:AAGh3bdfwrqSv7Zsq7o52hdEtbINuRPa4sA'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

STOCKS = {"فوري": "FWRY.CA", "طلعت": "TMGH.CA", "دهب": "GC=F", "دولار": "EGPHM=X"}

def get_data(msg):
    try:
        ticker = STOCKS.get(msg, msg.upper())
        if ".CA" not in ticker and ticker not in ["GC=F", "EGPHM=X"]: ticker += ".CA"
        data = yf.download(ticker, period="5d", progress=False)
        if data.empty: return "❌ الكود غير صحيح."
        price = data['Close'].iloc[-1]
        return f"📊 {msg}: {price:.2f}"
    except: return "⚠️ حاول لاحقاً."

@bot.message_handler(func=lambda m: True)
def handle(m):
    bot.reply_to(m, get_data(m.text.strip()))

# دي "النبضة" اللي هتخلي السيرفر صاحي
@app.route('/')
def home(): return "I AM ALIVE", 200

if __name__ == "__main__":
    # تشغيل Flask على بورت 8000
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8000)).start()
    bot.infinity_polling(timeout=90)
