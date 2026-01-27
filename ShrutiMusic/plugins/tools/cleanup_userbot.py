import asyncio
from pyrogram import filters
from pyrogram.errors import FloodWait
from ShrutiMusic.core.userbot import assistants  # 👈 ASSISTANT client

# first assistant userbot
user = assistants[0]

@user.on_message(filters.command(["cleanup", "clearowner"]) & filters.group)
async def cleanup_userbot_handler(client, message):
    if not message.from_user:
        return

    TARGET_ID = message.from_user.id  # 👈 jisne command diya
    chat_id = message.chat.id
    cmd_id = message.id
    deleted = 0

    async for msg in client.get_chat_history(chat_id, limit=500):
        try:
            if msg.id == cmd_id:
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
