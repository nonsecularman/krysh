import os
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, RPCError

# ===== READ FROM HEROKU CONFIG VARS =====
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
OWNER_ID = int(os.environ.get("OWNER_ID"))
# =======================================

app = Client(
    "cleanup-bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command(["cleanup", "clearowner"]) & filters.group)
async def cleanup_owner_commands(client, message):
    # Only OWNER can use
    if not message.from_user or message.from_user.id != OWNER_ID:
        return

    chat_id = message.chat.id
    deleted = 0

    try:
        async for msg in client.get_chat_history(chat_id, limit=500):
            try:
                if (
                    msg.from_user
                    and msg.from_user.id == OWNER_ID
                    and msg.text
                    and msg.text.startswith("/")
                ):
                    await msg.delete()
                    deleted += 1
                    await asyncio.sleep(0.3)

            except FloodWait as e:
                await asyncio.sleep(e.value)

            except RPCError:
                pass

        # confirmation (auto delete)
        info = await message.reply_text(
            f"🧹 Cleanup done\n🗑 Deleted: {deleted} command messages"
        )
        await asyncio.sleep(5)
        await info.delete()
        await message.delete()

    except Exception:
        pass


app.run()
