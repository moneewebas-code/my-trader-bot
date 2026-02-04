import telebot
import yfinance as yf
from flask import Flask
import threading

# التوكن بتاعك
API_TOKEN = '8506078405:AAGh3bdfwrqSv7Zsq7o52hdEtbINuRPa4sA'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# قاموس الأسهم الشامل
STOCKS = {
    "فوري": "FWRY.CA", "طلعت": "TMGH.CA", "بالم": "PHDC.CA",
    "عز": "ESRS.CA", "سي اي بي": "COMI.CA", "دهب": "GC=F",
    "فضه": "SI=F", "دولار": "EGPHM=X", "اسهم": "EGX30.CA"
}

def get_market_data(user_msg):
    try:
        ticker = STOCKS.get(user_msg, user_msg.upper())
        if ".CA" not in ticker and ticker not in ["GC=F", "SI=F", "EGPHM=X"]:
            ticker += ".CA"
        
        # سحب بيانات سنة لضمان عدم وجود أخطاء في الإجازات
        data = yf.download(ticker, period="1y", interval="1d", progress=False)
        
        if data.empty:
            return f"❌ الكود '{user_msg}' غير مسجل. جرب (فوري) أو (دهب)."

        price = float(data['Close'].iloc[-1])
        change = ((price - float(data['Close'].iloc[-2])) / float(data['Close'].iloc[-2])) * 100
        
        icon = "🟢" if change > 0 else "🔴"
        unit = "ج.م" if ".CA" in ticker or "EGPHM" in ticker else "دولار"

        return (f"📊 **تقرير: {user_msg}**\n\n"
                f"💰 السعر: {price:.2f} {unit}\n"
                f"📈 التغير: {change:.2f}% {icon}\n"
                f"✅ البوت يعمل بكفاءة.")
    except Exception:
        return "⚠️ عذراً، حاول مجدداً بعد دقيقة (ضغط سيرفر)."

@bot.message_handler(func=lambda m: True)
def handle_msg(m):
    txt = m.text.strip().lower()
    bot.reply_to(m, f"🔍 ذكاء البوت يبحث عن {txt}...")
    bot.reply_to(m, get_market_data(txt))

@app.route('/')
def health(): return "ACTIVE", 200

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8000)).start()
    bot.infinity_polling(timeout=60, long_polling_timeout=30)
