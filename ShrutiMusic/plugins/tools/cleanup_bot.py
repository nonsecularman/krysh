import os
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
OWNER_ID = int(os.environ.get("OWNER_ID"))

app = Client(
    "cleanup-bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    in_memory=True
)

@app.on_message(filters.command(["cleanup", "clearowner"], prefixes="/") & filters.group)
async def cleanup_handler(client, message):
    if not message.from_user or message.from_user.id != OWNER_ID:
        return

    chat_id = message.chat.id
    command_id = message.id
    deleted = 0

    async for msg in client.get_chat_history(chat_id, limit=500):
        try:
            # skip the cleanup command itself
            if msg.id == command_id:
                continue

            if (
                msg.from_user
                and msg.from_user.id == OWNER_ID
                and msg.text
                and msg.text.startswith("/")
            ):
                await client.delete_messages(chat_id, msg.id)
                deleted += 1
                await asyncio.sleep(0.5)

        except FloodWait as e:
            await asyncio.sleep(e.value)

        except Exception:
            continue

    try:
        await client.delete_messages(chat_id, command_id)
    except:
        pass


app.run()
