import os, json
from flask import Flask, request
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

BOT_TOKEN = "7347019252:AAEHLMczv6VtVELaqQ3-46MKwb9GE7mOutE"
CHAT_ID = “7368261029”
STATE_FILE = "state.json"

app = Flask(__name__)
bot = Bot(BOT_TOKEN)

def load_state():
    try:
        return json.load(open(STATE_FILE))
    except:
        return {"done": [], "blacklist": [], "todo": []}

def save_state(s):
    with open(STATE_FILE, "w") as f:
        json.dump(s, f)

def generate_jobs():
    # 模拟示例数据，后续换为你爬虫的结果
    return [
        {"id": "101", "title": "Postdoc in HEP", "link": "https://example.com"},
        {"id": "102", "title": "Diamond Detector Fellowship", "link": "https://example.com"},
    ]

def push():
    state = load_state()
    jobs = generate_jobs()
    sent = 0
    for job in jobs:
        if job["id"] in state["done"] or job["id"] in state["blacklist"]:
            continue
        msg = f"<b>{job['title']}</b>\n{job['link']}"
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ 待办", callback_data=f"todo:{job['id']}"),
             InlineKeyboardButton("❌ 否决", callback_data=f"deny:{job['id']}")]
        ])
        bot.send_message(chat_id=CHAT_ID, text=msg, reply_markup=kb, parse_mode="HTML")
        state["done"].append(job["id"])
        sent += 1
        if sent >= 10:
            break
    save_state(state)
    return sent

@app.route("/trigger")
def trigger():
    sent = push()
    return f"✅ 已推送 {sent} 条岗位信息。"

@app.route("/")
def home():
    return "🔧 Postdoc 推送 Bot 正在运行。访问 /trigger 可立即推送一次。"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
