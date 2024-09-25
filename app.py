import os
import requests
from flask import Flask, request
import logging

# إعدادات السجل
logging.basicConfig(level=logging.INFO)

# إعدادات البوت
API_URL = os.getenv("API_URL", "http://your-broker-api.com")  # استبدل بهذا إذا كان لديك
API_KEY = os.getenv("API_KEY", "49bc6b48-9134-4a11-abc9-5515f18ed959")
SECRET_KEY = os.getenv("SECRET_KEY", "3C2507CE4528DE3C87BA41C0DF01D6E8")
symbol = "BTCUSDT"

class TradingBot:
    def __init__(self, api_url, api_key, secret_key, symbol):
        self.api_url = api_url
        self.api_key = api_key
        self.secret_key = secret_key
        self.symbol = symbol

    # دالة لفتح صفقة
    def open_trade(self, action):
        order = {
            "symbol": self.symbol,
            "side": action,
            "quantity": 0.006,
            "type": "market"
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/orders",
                headers={"Authorization": f"Bearer {self.api_key}", "secret": self.secret_key},
                json=order
            )
            response.raise_for_status()  # رفع استثناء إذا كان هناك خطأ في الاستجابة
            logging.info(f"Trade opened: {response.json()}")
        except requests.exceptions.HTTPError as err:
            logging.error(f"HTTP error occurred: {err} - {response.text}")  # طباعة الخطأ
        except Exception as err:
            logging.error(f"Other error occurred: {err}")  # طباعة أي خطأ آخر

    # دالة للخروج من الصفقة
    def close_trade(self):
        order = {
            "symbol": self.symbol,
            "side": "sell",  # استخدم "sell" بدلاً من "close"
            "quantity": 0.006,
            "type": "market"
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/orders",
                headers={"Authorization": f"Bearer {self.api_key}", "secret": self.secret_key},
                json=order
            )
            response.raise_for_status()  # رفع استثناء إذا كان هناك خطأ في الاستجابة
            logging.info(f"Trade closed: {response.json()}")
        except requests.exceptions.HTTPError as err:
            logging.error(f"HTTP error occurred: {err} - {response.text}")  # طباعة الخطأ
        except Exception as err:
            logging.error(f"Other error occurred: {err}")  # طباعة أي خطأ آخر

# دالة لاستقبال الإشارات من TradingView
app = Flask(__name__)
bot = TradingBot(API_URL, API_KEY, SECRET_KEY, symbol)

@app.route('/signal', methods=['POST'])
def signal():
    data = request.json
    action = data.get("action")
    
    if action in ["buy", "sell", "exit"]:
        if action == "buy":
            bot.open_trade("buy")
        elif action == "sell":
            bot.open_trade("sell")
        elif action == "exit":
            bot.close_trade()
        return "Signal received", 200
    else:
        return "Invalid action", 400

@app.route('/')
def home():
    return "Trading Bot is running!"

if __name__ == "__main__":
    app.run(port=5000)
