from pyrogram import filters
from pyrogram.types import Message

from BrandrdXMusic import app
from config import OWNER_ID


@app.on_message(filters.command("purge50") & filters.user(OWNER_ID))
async def purge_1000(_, message: Message):

    chat_id = message.chat.id
    deleted = 0

    await message.reply_text("🧹 Deleting your last 50 messages...")

    try:
        async for msg in app.get_chat_history(chat_id, limit=200):

            # Only delete OWNER messages
            if msg.from_user and msg.from_user.id == OWNER_ID:
                try:
                    await app.delete_messages(chat_id, msg.id)
                    deleted += 1
                except:
                    pass

            # Stop after deleting 50
            if deleted >= 50:
                break

        await app.send_message(chat_id, f"✅ Deleted {deleted} of your messages!")

    except Exception as e:
        await app.send_message(chat_id, f"❌ Error: {e}")
