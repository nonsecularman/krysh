import json
import os

from pyrogram import filters
from pyrogram.types import Message

from ShrutiMusic import app
from config import OWNER_ID


# ==============================
# ✅ Local GMUTE (Only Current Runtime)
# ==============================
GMUTED_USERS = set()


# ==============================
# ✅ Global GMUTE Database (JSON)
# ==============================
GLOBAL_FILE = "global_gmute.json"


def load_global():
    if not os.path.exists(GLOBAL_FILE):
        return []
    with open(GLOBAL_FILE, "r") as f:
        return json.load(f)


def save_global(data):
    with open(GLOBAL_FILE, "w") as f:
        json.dump(data, f)


def is_global_gmuted(user_id: int):
    return user_id in load_global()


# ==============================
# ✅ /gmute (Local Only)
# ==============================
@app.on_message(filters.command("gmute") & filters.group)
async def gmute_user(_, message: Message):

    if OWNER_ID == 0:
        return await message.reply_text("❌ OWNER_ID not set in Heroku!")

    if message.from_user.id != OWNER_ID:
        return await message.reply_text("❌ Only OWNER can use /gmute!")

    if not message.reply_to_message:
        return await message.reply_text("⚠️ Reply to user then /gmute")

    user_id = message.reply_to_message.from_user.id
    GMUTED_USERS.add(user_id)

    await message.reply_text(
        f"✅ GMUTED (Local)!\nअब `{user_id}` के msg इसी group में delete होंगे."
    )


# ==============================
# ✅ /ungmute (Local Only)
# ==============================
@app.on_message(filters.command("ungmute") & filters.group)
async def ungmute_user(_, message: Message):

    if message.from_user.id != OWNER_ID:
        return await message.reply_text("❌ Only OWNER can use /ungmute!")

    if not message.reply_to_message:
        return await message.reply_text("⚠️ Reply to user then /ungmute")

    user_id = message.reply_to_message.from_user.id

    if user_id not in GMUTED_USERS:
        return await message.reply_text("⚠️ User not locally gmutted!")

    GMUTED_USERS.remove(user_id)

    await message.reply_text("✅ UNGMUTED (Local)!")


# ==============================
# ✅ /globalmute (All Groups)
# ==============================
@app.on_message(filters.command("globalmute") & filters.group)
async def global_mute(_, message: Message):

    if message.from_user.id != OWNER_ID:
        return await message.reply_text("❌ Only OWNER can use /globalmute!")

    if not message.reply_to_message:
        return await message.reply_text("⚠️ Reply to user then /globalmute")

    user_id = message.reply_to_message.from_user.id

    data = load_global()
    if user_id in data:
        return await message.reply_text("⚠️ User already GLOBAL muted!")

    data.append(user_id)
    save_global(data)

    await message.reply_text(
        f"✅ GLOBAL GMUTE DONE!\nअब `{user_id}` आपके bot के सभी groups में muted रहेगा."
    )


# ==============================
# ✅ /globalunmute (All Groups)
# ==============================
@app.on_message(filters.command("globalunmute") & filters.group)
async def global_unmute(_, message: Message):

    if message.from_user.id != OWNER_ID:
        return await message.reply_text("❌ Only OWNER can use /globalunmute!")

    if not message.reply_to_message:
        return await message.reply_text("⚠️ Reply to user then /globalunmute")

    user_id = message.reply_to_message.from_user.id

    data = load_global()
    if user_id not in data:
        return await message.reply_text("⚠️ User not globally muted!")

    data.remove(user_id)
    save_global(data)

    await message.reply_text(
        f"✅ GLOBAL UNMUTE DONE!\nअब `{user_id}` messages भेज सकता है."
    )


# ==============================
# ✅ Auto Delete (Local + Global)
# ==============================
@app.on_message(filters.group)
async def delete_gmuted(_, message: Message):

    if not message.from_user:
        return

    user_id = message.from_user.id

    # Local GMUTE
    if user_id in GMUTED_USERS:
        try:
            return await message.delete()
        except:
            return

    # Global GMUTE
    if is_global_gmuted(user_id):
        try:
            return await message.delete()
        except:
            return
