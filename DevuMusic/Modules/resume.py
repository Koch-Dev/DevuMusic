from pyrogram import filters
from pyrogram.types import Message

from DevuMusic import app, pytgcalls
from DevuMusic.Helpers import admin_check, close_key, is_streaming, stream_on


@app.on_message(filters.command(["resume"]) & filters.group)
@admin_check
async def res_str(_, message: Message):
    try:
        await message.delete()
    except:
        pass

    if await is_streaming(message.chat.id):
        return await message.reply_text("Did you remember that you paused the stream?")
    await stream_on(message.chat.id)
    await pytgcalls.resume_stream(message.chat.id)
    return await message.reply_text(
        text=f"➻ Stream resumed 💫\n│ \n└ by: {message.from_user.mention} 🥀",
        reply_markup=close_key,
    )
