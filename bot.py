import telebot
import yfinance as yf
import requests
from flask import Flask
import threading

# التوكن الخاص بك
API_TOKEN = '8506078405:AAGh3bdfwrqSv7Zsq7o52hdEtbINuRPa4sA'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# القاموس الشامل (مصري + عالمي)
STOCKS = {
    "فوري": "FWRY.CA", "طلعت": "TMGH.CA", "بالم": "PHDC.CA",
    "عز": "ESRS.CA", "سي اي بي": "COMI.CA", "cib": "COMI.CA",
    "دهب": "GC=F", "ذهب": "GC=F", "دولار": "EGPHM=X", "اسهم": "EGX30.CA"
}

def get_ai_analysis(name):
    try:
        ticker = STOCKS.get(name.lower(), name.upper())
        if ".CA" not in ticker and ticker not in ["GC=F", "EGPHM=X"]:
            ticker += ".CA"
        
        # سحب بيانات كافية للتحليل الفني
        data = yf.download(ticker, period="1mo", interval="1d", progress=False)
        if data.empty: return "❌ كود غير مدعوم."

        # 1. حساب السعر ونسبة التغير
        current_price = data['Close'].iloc[-1]
        prev_price = data['Close'].iloc[-2]
        change_pct = ((current_price - prev_price) / prev_price) * 100
        
        # 2. ذكاء اصطناعي (تحليل المتوسطات)
        ma20 = data['Close'].mean()
        
        # 3. تحديد التوصية
        if current_price > ma20 and change_pct > 0:
            advice = "🟢 شراء قوي (شمعة إيجابية)"
        elif current_price < ma20 and change_pct < 0:
            advice = "🔴 بيع/انتظار (اتجاه هابط)"
        else:
            advice = "🟡 مراقبة (تذبذب عرضي)"

        emoji = "🚀" if change_pct > 0 else "📉"
        unit = "ج.م" if ".CA" in ticker else "دولار"

        return (f"🤖 **التحليل الذكي لـ {name}**\n\n"
                f"💰 السعر: {current_price:.2f} {unit}\n"
                f"{emoji} التغير: {change_pct:.2f}%\n"
                f"📈 المتوسط: {ma20:.2f}\n"
                f"💡 التوصية: {advice}\n"
                f"📍 الحالة: $100\%$ جاهز")
    except:
        return "⚠️ السيرفر مشغول، كرر المحاولة الآن."

@bot.message_handler(func=lambda m: True)
def handle(m):
    text = m.text.strip().lower()
    bot.reply_to(m, "🧠 جاري تشغيل المحرك الذكي للتحليل...")
    bot.reply_to(m, get_ai_analysis(text))

@app.route('/')
def health(): return "AI ACTIVE", 200

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8000)).start()
    bot.infinity_polling(timeout=30)
