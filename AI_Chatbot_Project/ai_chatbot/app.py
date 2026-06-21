from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

responses = {
    "hello": "Hello! How can I help you?",
    "hi": "Hi there!",
    "timing": "Our office timing is 9 AM to 6 PM.",
    "apply": "You can apply through our careers page.",
    "bye": "Goodbye! Have a nice day."
}

def init_db():
    conn = sqlite3.connect("chat_logs.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT,
            bot_response TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"].lower()

    bot_response = "Sorry, I don't understand that."
    for key in responses:
        if key in user_message:
            bot_response = responses[key]
            break

    conn = sqlite3.connect("chat_logs.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO logs (user_message, bot_response, timestamp) VALUES (?, ?, ?)",
        (user_message, bot_response, str(datetime.now()))
    )
    conn.commit()
    conn.close()

    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)
