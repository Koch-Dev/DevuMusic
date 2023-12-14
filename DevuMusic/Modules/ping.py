import time
from datetime import datetime

import psutil
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

import config
from DevuMusic import BOT_NAME, StartTime, app
from DevuMusic.Helpers import get_readable_time


@app.on_message(filters.command("ping"))
async def ping_devu(_, message: Message):
    hmm = await message.reply_photo(
        photo=config.PING_IMG, caption=f"{BOT_NAME} is pinging..."
    )
    upt = int(time.time() - StartTime)
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    start = datetime.now()
    resp = (datetime.now() - start).microseconds / 1000
    uptime = get_readable_time(upt)

    await hmm.edit_text(
        f"""Pong: `{resp}ms`

<b><u>{BOT_NAME} system stats:</u></b>

๏ **Uptime:** {uptime}
๏ **RAM:** {mem}
๏ **CPU:** {cpu}
๏ **Disk:** {disk}""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Support", url=config.SUPPORT_CHAT),
                    InlineKeyboardButton(
                        "Source",
                        url="https://t.me/dx_radhe01",
                    ),
                ],
            ]
        ),
    )
