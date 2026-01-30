from pyrogram import filters
from pyrogram.types import Message

from ShrutiMusic import app
from config import OWNER_ID

# अगर sudo list config में है तो import करो
try:
    from config import SUDO_USERS
except:
    SUDO_USERS = []

GMUTED_USERS = set()


# ✅ Owner or Sudo Check
def is_allowed(user_id: int):
    return user_id == OWNER_ID or user_id in SUDO_USERS


# ✅ GMUTE Command
@app.on_message(filters.command("gmute") & filters.group)
async def gmute_user(_, message: Message):

    if not is_allowed(message.from_user.id):
        return await message.reply_text("❌ Only Owner or Sudo can gmute!")

    if not message.reply_to_message:
        return await message.reply_text("⚠️ Reply to user then /gmute")

    user_id = message.reply_to_message.from_user.id
    GMUTED_USERS.add(user_id)

    await message.reply_text(f"✅ GMUTED!\nUser: `{user_id}`")


# ✅ UNGMUTE Command
@app.on_message(filters.command("ungmute") & filters.group)
async def ungmute_user(_, message: Message):

    if not is_allowed(message.from_user.id):
        return await message.reply_text("❌ Only Owner or Sudo can ungmute!")

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

        # ✅ Commands safe
        if message.text and message.text.startswith("/"):
            return

        try:
            await message.delete()
        except:
            pass
