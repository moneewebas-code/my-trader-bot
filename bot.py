import telebot
import yfinance as yf
from flask import Flask
import threading
import time

# 1. التوكن الشغال بتاعك
API_TOKEN = '8506078405:AAGh3bdfwrqSv7Zsq7o52hdEtbINuRPa4sA'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# 2. القاموس الذكي الشامل
STOCKS = {
    "فوري": "FWRY.CA", "طلعت": "TMGH.CA", "بالم": "PHDC.CA",
    "حديد عز": "ESRS.CA", "سي اي بي": "COMI.CA", "دهب": "GC=F",
    "ذهب": "GC=F", "دولار": "EGPHM=X"
}

def get_data_fixed(text):
    try:
        ticker = STOCKS.get(text, text.upper())
        if ".CA" not in ticker and ticker not in ["GC=F", "EGPHM=X"]:
            ticker += ".CA"
        
        # تحسين سحب البيانات لمنع حظر السيرفر
        stock = yf.Ticker(ticker)
        data = stock.history(period="5d") # سحب آخر 5 أيام لضمان وجود بيانات
        
        if data.empty:
            return f"❌ الكود '{text}' مش متاح حالياً، جرب (فوري) أو (طلعت)."

        last_price = data['Close'].iloc[-1]
        prev_price = data['Close'].iloc[-2]
        change = ((last_price - prev_price) / prev_price) * 100
        
        direction = "📈 صعود" if change > 0 else "📉 هبوط"
        unit = "ج.م" if ".CA" in ticker or "EGPHM" in ticker else "دولار"

        return (f"🤖 **تقرير المحلل الذكي لـ: {text}**\n\n"
                f"💰 السعر الحالي: {last_price:.2f} {unit}\n"
                f"📊 التغير اليومي: {change:.2f}% {direction}\n"
                f"💡 الحالة: البوت يعمل بنجاح ✅")
    except Exception as e:
        return "⚠️ البيانات مش واصلة حالياً، جرب كمان دقيقة."

@bot.message_handler(func=lambda m: True)
def handle(m):
    txt = m.text.strip().lower()
    bot.reply_to(m, f"🔍 جاري سحب بيانات {txt}...")
    bot.reply_to(m, get_data_fixed(txt))

@app.route('/')
def health(): return "STABLE", 200

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8000)).start()
    bot.infinity_polling(timeout=60, long_polling_timeout=30)
