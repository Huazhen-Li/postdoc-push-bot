import os, json, requests
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def load_state():
    try:
        return json.load(open("state.json"))
    except:
        return {"done": [], "blacklist": [], "todo": []}

def save_state(s):
    json.dump(s, open("state.json","w"))

def push():
    bot = Bot(BOT_TOKEN)
    state = load_state()
    jobs = [
        {"id":"101","title":"Example Postdoc in HEP","link":"https://example.com"},
        {"id":"102","title":"Diamond Detector Fellowship","link":"https://example.com"}
    ]
    sent = 0
    for job in jobs:
        if job["id"] in state["done"] or job["id"] in state["blacklist"]:
            continue
        msg = f"<b>{job['title']}</b>\n{job['link']}"
        kb = InlineKeyboardMarkup([[
            InlineKeyboardButton("✅ 待办", callback_data=f"todo:{job['id']}"),
            InlineKeyboardButton("❌ 否决", callback_data=f"deny:{job['id']}")
        ]])
        bot.send_message(chat_id=CHAT_ID, text=msg, reply_markup=kb, parse_mode="HTML")
        state["done"].append(job["id"])
        sent += 1
        if sent >= 10:
            break
    save_state(state)

if __name__=="__main__":
    push()
