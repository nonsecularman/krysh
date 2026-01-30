from pyrogram import filters
from pyrogram.types import Message

from RiyaMusic import app
from config import OWNER_ID, SUDO_USERS   # ✅ sudo list config se

GMUTED_USERS = set()


# ✅ Function: Owner or Sudo Check
def is_allowed(user_id: int):
    return user_id == OWNER_ID or user_id in SUDO_USERS


# ✅ GMUTE Command (Owner + Sudo)
@app.on_message(filters.command("gmute") & filters.group)
async def gmute_user(_, message: Message):

    if not is_allowed(message.from_user.id):
        return await message.reply_text("❌ Only Owner or Sudo Users can gmute!")

    if not message.reply_to_message:
        return await message.reply_text("⚠️ Reply to user then /gmute")

    user_id = message.reply_to_message.from_user.id
    GMUTED_USERS.add(user_id)

    await message.reply_text(f"✅ GMUTED!\nUser: `{user_id}`")


# ✅ UNGMUTE Command (Owner + Sudo)
@app.on_message(filters.command("ungmute") & filters.group)
async def ungmute_user(_, message: Message):

    if not is_allowed(message.from_user.id):
        return await message.reply_text("❌ Only Owner or Sudo Users can ungmute!")

    if not message.reply_to_message:
        return await message.reply_text("⚠️ Reply to user then /ungmute")

    user_id = message.reply_to_message.from_user.id
    GMUTED_USERS.discard(user_id)

    await message.reply_text("✅ UNGMUTED!")


# ✅ Delete Muted Messages (Ping/Stats Safe)
@app.on_message(filters.group, group=999)
async def delete_gmuted(_, message: Message):

    if not message.from_user:
        return

    if message.from_user.id in GMUTED_USERS:

        # ✅ Commands safe रहें
        if message.text and message.text.startswith("/"):
            return

        try:
            await message.delete()
        except:
            pass
