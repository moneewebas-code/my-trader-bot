import telebot
import requests
from flask import Flask
import threading

# التوكن الشغال بتاعك
API_TOKEN = '8506078405:AAGh3bdfwrqSv7Zsq7o52hdEtbINuRPa4sA'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# قاموس الأسهم - جبنا روابط مباشرة عشان السيرفر ميهنجش
STOCKS = {
    "فوري": "FWRY", "طلعت": "TMGH", "بالم": "PHDC",
    "عز": "ESRS", "دهب": "GOLD", "دولار": "USD"
}

def get_price(name):
    try:
        # هنا بنستخدم API بديل سريع جداً ومبيعملش بلوك
        ticker = STOCKS.get(name, name.upper())
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}.CA?interval=1d&range=1d"
        # لو ذهب أو دولار بنغير الرابط
        if name in ["دهب", "ذهب"]: url = "https://query1.finance.yahoo.com/v8/finance/chart/GC=F?interval=1d&range=1d"
        
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        price = data['chart']['result'][0]['meta']['regularMarketPrice']
        
        return f"📊 سهم {name}\n💰 السعر: {price:.2f}"
    except:
        return "⚠️ السيرفر مضغوط، ابعت اسم السهم كمان مرة دلوقتي."

@bot.message_handler(func=lambda m: True)
def handle(m):
    text = m.text.strip().lower()
    bot.reply_to(m, "🔍 جاري الفحص السريع...")
    bot.reply_to(m, get_price(text))

@app.route('/')
def health(): return "ALIVE", 200

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8000)).start()
    bot.infinity_polling(timeout=20)
