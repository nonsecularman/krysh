from pyrogram import filters
from pyrogram.types import Message

from ShrutiMusic import app
from config import OWNER_ID, SUDO_USERS


# ✅ Add Sudo
@app.on_message(filters.command("addsudo") & filters.group)
async def add_sudo(_, message: Message):

    if message.from_user.id != OWNER_ID:
        return await message.reply_text("❌ Only Owner can add sudo!")

    if not message.reply_to_message:
        return await message.reply_text("⚠️ Reply to user then /addsudo")

    user_id = message.reply_to_message.from_user.id
    SUDO_USERS.add(user_id)

    await message.reply_text(f"✅ Added as SUDO!\nUser: `{user_id}`")


# ✅ Remove Sudo
@app.on_message(filters.command("rmsudo") & filters.group)
async def remove_sudo(_, message: Message):

    if message.from_user.id != OWNER_ID:
        return await message.reply_text("❌ Only Owner can remove sudo!")

    if not message.reply_to_message:
        return await message.reply_text("⚠️ Reply to user then /rmsudo")

    user_id = message.reply_to_message.from_user.id
    SUDO_USERS.discard(user_id)

    await message.reply_text(f"✅ Removed from SUDO!\nUser: `{user_id}`")


# ✅ List Sudo Users
@app.on_message(filters.command("sudolist") & filters.group)
async def sudo_list(_, message: Message):

    if message.from_user.id != OWNER_ID:
        return

    if not SUDO_USERS:
        return await message.reply_text("⚠️ No sudo users added yet!")

    text = "✅ **Sudo Users List:**\n\n"
    for x in SUDO_USERS:
        text += f"• `{x}`\n"

    await message.reply_text(text)
