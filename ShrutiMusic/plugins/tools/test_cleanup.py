from pyrogram import filters
from ShrutiMusic import app

@app.on_message(filters.command("cleanup") & filters.group)
async def test_cmd(client, message):
    await message.reply_text("✅ CLEANUP COMMAND HIT")
