from pyrogram import filters
from pyrogram.types import Message

from RiyaMusic import app
from config import OWNER_ID

GMUTED_USERS = set()


# ✅ /gmute Only Owner
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

    await message.reply_text(f"✅ GMUTED!\nअब `{user_id}` के msg delete होंगे.")


# ✅ /ungmute Only Owner
@app.on_message(filters.command("ungmute") & filters.group)
async def ungmute_user(_, message: Message):

    if message.from_user.id != OWNER_ID:
        return await message.reply_text("❌ Only OWNER can use /ungmute!")

    if not message.reply_to_message:
        return await message.reply_text("⚠️ Reply to user then /ungmute")

    user_id = message.reply_to_message.from_user.id

    if user_id not in GMUTED_USERS:
        return await message.reply_text("⚠️ User not gmutted!")

    GMUTED_USERS.remove(user_id)
    await message.reply_text("✅ UNGMUTED!")


# ✅ Delete Messages
@app.on_message(filters.group)
async def delete_gmuted(_, message: Message):

    if message.from_user and message.from_user.id in GMUTED_USERS:
        try:
            await message.delete()
        except:
            pass
