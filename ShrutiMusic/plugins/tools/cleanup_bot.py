import asyncio
from pyrogram import filters
from pyrogram.errors import FloodWait
from config import OWNER_ID
from ShrutiMusic import app

@app.on_message(filters.command(["cleanup", "clearowner"]) & filters.group)
async def cleanup_owner_commands(client, message):
    # Only owner can use
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
                await asyncio.sleep(0.4)

        except FloodWait as e:
            await asyncio.sleep(e.value)

        except Exception:
            continue

    # delete command message at last
    try:
        await client.delete_messages(chat_id, command_id)
    except:
        pass
