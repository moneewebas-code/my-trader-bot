import telebot
import yfinance as yf

# التوكن بتاعك
bot = telebot.TeleBot('8506078405:AAGh3bdfwrqSv7Zsq7o52hdEtbINuRPa4sA')

@bot.message_handler(func=lambda m: True)
def get_price(m):
    symbol = m.text.strip().upper()
    # بدل ما نهري في الـ Scraping ونلبس بلوك، بنستخدم مكتبة رسمية
    ticker = f"{symbol}.CA" 
    try:
        data = yf.Ticker(ticker).history(period="1d")
        if not data.empty:
            price = data['Close'].iloc[-1]
            bot.reply_to(m, f"✅ سعر {symbol} الآن: {price:.2f} ج.م")
        else:
            bot.reply_to(m, "❌ الكود غلط أو السهم مش موجود.")
    except:
        bot.reply_to(m, "⚠️ فيه مشكلة في الاتصال.")

bot.infinity_polling()
