import os
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")

app = Client(
    "cleanup-userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

@app.on_message(filters.command(["cleanup", "clearowner"]) & filters.group)
async def cleanup_owner_commands(client, message):
    if not message.from_user:
        return

    TARGET_ID = message.from_user.id  # 👈 dynamic owner
    chat_id = message.chat.id
    command_id = message.id
    deleted = 0

    async for msg in client.get_chat_history(chat_id, limit=500):
        try:
            if msg.id == command_id:
                continue

            if (
                msg.from_user
                and msg.from_user.id == TARGET_ID
                and msg.text
                and msg.text.startswith("/")
            ):
                await msg.delete()
                deleted += 1
                await asyncio.sleep(0.4)

        except FloodWait as e:
            await asyncio.sleep(e.value)
        except Exception:
            continue

    try:
        await message.reply_text(
            f"✅ Cleanup done\n🗑 Deleted {deleted} command messages"
        )
    except:
        pass


app.run()
