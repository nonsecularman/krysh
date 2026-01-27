# ============================================
# Telegram Spam Cleanup Bot (Pyrogram)
# ============================================
# This bot deletes ONLY:
# - Messages sent by OWNER_ID
# - Messages that are bot commands (start with "/")
# - Only inside GROUP chats
# - Triggered by a single command (/cleanup or /clearowner)
# ============================================

import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, RPCError
from pyrogram.enums import ChatType

# ================== CONFIG ===================
API_ID = 123456          # <-- Your API_ID
API_HASH = "API_HASH"    # <-- Your API_HASH
BOT_TOKEN = "BOT_TOKEN"  # <-- Your BOT_TOKEN
OWNER_ID = 123456789     # <-- Your Telegram User ID
# =============================================

app = Client(
    "owner_cleanup_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Command handler for cleanup
@app.on_message(
    filters.command(["cleanup", "clearowner"])
    & filters.group
)
async def cleanup_owner_commands(client: Client, message):
    """
    Deletes last 500 command messages sent by OWNER_ID in a group
    """

    # Ensure ONLY OWNER can run this command
    if not message.from_user or message.from_user.id != OWNER_ID:
        return

    # Ensure command is used in a group (extra safety)
    if message.chat.type not in (ChatType.GROUP, ChatType.SUPERGROUP):
        return

    deleted_count = 0

    try:
        # Iterate through last 500 messages in the chat
        async for msg in client.get_chat_history(
            chat_id=message.chat.id,
            limit=500
        ):
            # Skip messages without sender or text
            if not msg.from_user or not msg.text:
                continue

            # Check OWNER + command message
            if (
                msg.from_user.id == OWNER_ID
                and msg.text.startswith("/")
            ):
                try:
                    await msg.delete()
                    deleted_count += 1
                    # Small delay to avoid flood limits
                    await asyncio.sleep(0.3)

                except FloodWait as e:
                    # Respect Telegram flood wait
                    await asyncio.sleep(e.value)

                except RPCError:
                    # Ignore deletion errors silently
                    continue

    except RPCError:
        # If bot lacks permissions or other errors occur
        pass

    # Optional confirmation message (auto-delete after 5s)
    try:
        status = await message.reply_text(
            f"🧹 Cleanup done.\nDeleted: {deleted_count} command messages."
        )
        await asyncio.sleep(5)
        await status.delete()
    except RPCError:
        pass


# ================== START BOT =================
if __name__ == "__main__":
    app.run()
