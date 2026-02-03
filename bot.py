import telebot
import yfinance as yf
from flask import Flask
import threading

# التوكن الشغال بتاعك
API_TOKEN = '8506078405:AAGh3bdfwrqSv7Zsq7o52hdEtbINuRPa4sA'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# القاموس الذكي الشامل (عشان يفهم كل طلباتك)
STOCKS = {
    "فوري": "FWRY.CA", "طلعت": "TMGH.CA", "طلعت مصطفى": "TMGH.CA",
    "بالم": "PHDC.CA", "حديد عز": "ESRS.CA", "سي اي بي": "COMI.CA",
    "دهب": "GC=F", "ذهب": "GC=F", "دولار": "EGPHM=X", "السويدي": "SWDY.CA"
}

def analyze_smart(text):
    try:
        ticker = STOCKS.get(text, text.upper())
        if ".CA" not in ticker and ticker not in ["GC=F", "EGPHM=X"]: ticker += ".CA"
        
        data = yf.download(ticker, period="30d", progress=False)
        if data.empty: return f"❌ الكود '{text}' غير مدعوم حالياً."

        price = float(data['Close'].iloc[-1])
        ma = float(data['Close'].mean())
        # ذكاء اصطناعي بسيط لتحليل الحالة
        signal = "🟢 شراء / صعود" if price > ma else "🔴 انتظار / هبوط"
        unit = "ج.م" if ".CA" in ticker or "EGPHM" in ticker else "دولار"

        return (f"🤖 **تحليل ذكي لـ: {text}**\n\n"
                f"💰 السعر: {price:.2f} {unit}\n"
                f"💡 الحالة: {signal}\n"
                f"📈 متوسط 30 يوم: {ma:.2f} {unit}")
    except: return "❌ البورصة مغلقة أو فيه مشكلة في البيانات."

@bot.message_handler(func=lambda m: True)
def handle(m):
    txt = m.text.strip().lower()
    bot.reply_to(m, analyze_smart(txt))

@app.route('/')
def health(): return "ONLINE", 200

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8000)).start()
    bot.infinity_polling()
