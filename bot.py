import telebot
import yfinance as yf
import pandas as pd
from flask import Flask
import threading

# 1. إعدادات البوت (التوكن بتاعك جاهز)
API_TOKEN = '7511116664:AAH_S_2pLly7I6E_6R33D2hIas3m4_Nia8w'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# 2. دالة تحليل أي سهم في البورصة المصرية
def analyze_stock(ticker_symbol):
    try:
        # إضافة .CA لسحب بيانات البورصة المصرية من Yahoo Finance
        full_ticker = f"{ticker_symbol.upper()}.CA"
        stock = yf.Ticker(full_ticker)
        df = stock.history(period="1mo")
        
        if df.empty:
            return f"❌ كود السهم '{ticker_symbol}' غير صحيح أو لا توجد بيانات حالية (تأكد من كتابة الكود الإنجليزي مثل FWRY)."

        current_price = df['Close'].iloc[-1]
        ma20 = df['Close'].mean()
        
        status = "🟢 إشارة شراء (السعر فوق المتوسط)" if current_price > ma20 else "🔴 إشارة بيع أو انتظار (السعر تحت المتوسط)"
        
        msg = (f"📊 تحليل سهم: {ticker_symbol.upper()}\n"
               f"💰 السعر الحالي: {current_price:.2f} ج.م\n"
               f"📈 متوسط 20 يوم: {ma20:.2f} ج.م\n"
               f"💡 التوصية الفنية: {status}\n"
               f"⚠️ تنبيه: هذا تحليل آلي يعتمد على البيانات التاريخية فقط.")
        return msg
    except Exception as e:
        return "❌ حدث خطأ فني أثناء جلب البيانات، جرب مرة أخرى لاحقاً."

# 3. استقبال الأوامر والرسائل
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "مرحباً بك في بوت المحلل الشامل للبورصة المصرية! 🇪🇬\n\nابعت لي 'كود السهم' بالإنجليزي وهحللهولك فوراً.\nأمثلة:\nFWRY (فوري)\nTMGH (طلعت مصطفى)\nCOMI (التجاري الدولي)\nPHDC (بالم هيلز)")

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    ticker = message.text.strip()
    bot.reply_to(message, f"🔍 جاري سحب بيانات {ticker.upper()} وتحليلها...")
    result = analyze_stock(ticker)
    bot.reply_to(message, result)

# 4. نظام التشغيل المستمر (Web Server)
@app.route('/')
def home():
    return "Bot is Alive!"

def run_flask():
    app.run(host='0.0.0.0', port=8000)

if __name__ == "__main__":
    # تشغيل السيرفر والبوت في وقت واحد
    threading.Thread(target=run_flask).start()
    print("🚀 البوت انطلق بنجاح على السيرفر!")
    bot.infinity_polling()
