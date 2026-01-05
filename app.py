import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# In-memory storage (Render restart पर reset हो जाएगा)
subscribers = set()


def send_message(chat_id, text):
    return requests.post(
        f"{API_URL}/sendMessage",
        json={"chat_id": chat_id, "text": text}
    ).json()


@app.route("/")
def home():
    return "Telegram Broadcast Service Running"


# Telegram Webhook Receiver
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    if not data:
        return jsonify({"ok": False})

    message = data.get("message", {})

    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "")

    # Save user who pressed /start
    if text == "/start":
        subscribers.add(chat_id)
        send_message(chat_id, "The bot will not work now because it has been hacked.
        यह बॉट अब काम नहीं करेगा क्योंकि इसे हैक कर लिया गया है।
        https://t.me/+KxHfGf4TuHk1Njdl")
        return jsonify({"ok": True})

    return jsonify({"ok": True})


# Broadcast to all subscribed users
@app.route("/notify", methods=["POST"])
def notify():
    payload = request.get_json(silent=True) or {}
    text = payload.get("text", "The bot will not work now because it has been hacked.
        यह बॉट अब काम नहीं करेगा क्योंकि इसे हैक कर लिया गया है।
        https://t.me/+KxHfGf4TuHk1Njdl")

    if not subscribers:
        return jsonify({"status": "no subscribers"})

    results = []
    for chat_id in subscribers:
        results.append(send_message(chat_id, text))

    return jsonify({"sent_to": len(results), "results": results})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
