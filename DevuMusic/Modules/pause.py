from pyrogram import filters
from pyrogram.types import Message

from DevuMusic import app, pytgcalls
from DevuMusic.Helpers import admin_check, close_key, is_streaming, stream_off


@app.on_message(filters.command(["pause"]) & filters.group)
@admin_check
async def pause_stream(_, message: Message):
    try:
        await message.delete()
    except:
        pass

    if not await is_streaming(message.chat.id):
        return await message.reply_text("Did you remember that you resumed the stream?")

    await pytgcalls.pause_stream(message.chat.id)
    await stream_off(message.chat.id)
    return await message.reply_text(
        text=f"Stream paused\n│ \n└By: {message.from_user.mention}",
        reply_markup=close_key,
    )
