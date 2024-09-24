import requests
from flask import Flask, request

# إعدادات البوت
API_URL = "http://your-broker-api.com"  # استبدل بهذا إذا كان لديك
API_KEY = "49bc6b48-9134-4a11-abc9-5515f18ed959"
SECRET_KEY = "3C2507CE4528DE3C87BA41C0DF01D6E8"
symbol = "BTCUSDT"

# دالة لفتح صفقة
def open_trade(action):
    order = {
        "symbol": symbol,
        "side": action,
        "quantity": 0.006,
        "type": "market"
    }
    
    response = requests.post(
        f"{API_URL}/orders",
        headers={"Authorization": f"Bearer {API_KEY}", "secret": SECRET_KEY},
        json=order
    )
    print(response.json())

# دالة للخروج من الصفقة
def close_trade():
    order = {
        "symbol": symbol,
        "side": "close",
        "quantity": 0.006,
        "type": "market"
    }
    
    response = requests.post(
        f"{API_URL}/orders",
        headers={"Authorization": f"Bearer {API_KEY}", "secret": SECRET_KEY},
        json=order
    )
    print(response.json())

# دالة لاستقبال الإشارات من TradingView
app = Flask(__name__)

@app.route('/signal', methods=['POST'])
def signal():
    data = request.json
    action = data.get("action")
    
    if action in ["buy", "sell", "exit"]:
        if action == "buy":
            open_trade("buy")
        elif action == "sell":
            open_trade("sell")
        elif action == "exit":
            close_trade()
        return "Signal received", 200
    else:
        return "Invalid action", 400

@app.route('/')
def home():
    return "Trading Bot is running!"

if __name__ == "__main__":
    app.run(port=5000)
