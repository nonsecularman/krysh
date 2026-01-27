from pyrogram import filters
from pyrogram.types import Message

from ShrutiMusic import app
from config import OWNER_ID

# Owner Only Command: /clearall
@app.on_message(filters.command("clearall") & filters.user(OWNER_ID))
async def clear_all_messages(_, message: Message):
    chat_id = message.chat.id

    msg = await message.reply_text("🧹 Clearing messages...")

    deleted = 0

    try:
        # Delete last 100 messages (you can increase)
        async for m in app.get_chat_history(chat_id, limit=100):
            try:
                await app.delete_messages(chat_id, m.id)
                deleted += 1
            except:
                continue

        await msg.edit_text(f"✅ Deleted {deleted} messages successfully!")

    except Exception as e:
        await msg.edit_text(f"❌ Error: {e}")
