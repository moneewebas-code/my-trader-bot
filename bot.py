import telebot
import yfinance as yf
from flask import Flask
import threading

API_TOKEN = '8506078405:AAGh3bdfwrqSv7Zsq7o52hdEtbINuRPa4sA'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# القاموس السحري - الأكواد دي هي الوحيدة اللي البورصة بتفهمها
STOCKS = {
    "فوري": "FWRY.CA", "طلعت": "TMGH.CA", "بالم": "PHDC.CA",
    "عز": "ESRS.CA", "سي اي بي": "COMI.CA", "cib": "COMI.CA",
    "دهب": "GC=F", "ذهب": "GC=F", "فضه": "SI=F", "دولار": "EGPHM=X",
    "اسهم": "EGX30.CA"
}

def get_pro_analysis(name):
    try:
        ticker = STOCKS.get(name.lower(), None)
        if not ticker:
            return f"❌ الكود '{name}' غير مسجل. جرب (فوري، دهب، طلعت، cib)."
        
        # سحب بيانات 5 أيام فقط لسرعة الرد
        data = yf.download(ticker, period="5d", interval="1d", progress=False)
        if data.empty: return "⚠️ عذراً، البيانات غير متوفرة حالياً."

        current_price = float(data['Close'].iloc[-1])
        prev_price = float(data['Close'].iloc[-2])
        change_pct = ((current_price - prev_price) / prev_price) * 100
        
        # ذكاء اصطناعي بسيط للتحليل
        if change_pct > 0.5:
            advice = "🟢 إيجابي - شراء (صعود)"
        elif change_pct < -0.5:
            advice = "🔴 سلبي - حذر (هبوط)"
        else:
            advice = "🟡 مستقر - مراقبة"

        unit = "ج.م" if ".CA" in ticker or "EGPHM" in ticker else "دولار"
        return (f"🤖 **تحليل الذكاء المالي لـ {name}**\n\n"
                f"💰 السعر: {current_price:.2f} {unit}\n"
                f"📈 التغير: {change_pct:.2f}%\n"
                f"💡 التوصية: {advice}\n"
                f"✅ تم التحديث بنجاح")
    except:
        return "⚠️ السيرفر مضغوط، استنى ثواني وجرب تاني."

@bot.message_handler(func=lambda m: True)
def handle(m):
    txt = m.text.strip().lower()
    bot.reply_to(m, f"🔍 جاري تحليل {txt}...")
    bot.reply_to(m, get_pro_analysis(txt))

@app.route('/')
def health(): return "ACTIVE", 200

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8000)).start()
    bot.infinity_polling(timeout=20)
