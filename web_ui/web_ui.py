# web_ui/web_ui.py
from flask import Flask, render_template, request, jsonify
from backend.chatbot.chatbot import chat

app = Flask(__name__, template_folder="templates")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.json
    user_id = data.get("user_id", "web_user")
    message = data.get("message", "")
    resp = chat(user_id, message)
    return jsonify({"response": resp})

if __name__ == "__main__":
    app.run(port=8002, debug=True)
