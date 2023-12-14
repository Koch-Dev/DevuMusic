from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import Message

import config
from DevuMusic import BOT_NAME, app

@app.on_message(
    filters.command(["config", "variables"]) & filters.user(config.OWNER_ID)
)
async def get_vars(_, message: Message):
    try:
        await app.send_message(
            chat_id=int(config.OWNER_ID),
            text=f"""**{BOT_NAME} Config Variables:**

- API_ID: `{config.API_ID}`
- API_HASH: `{config.API_HASH}`

- BOT_TOKEN: `{config.BOT_TOKEN}`
- DURATION_LIMIT: `{config.DURATION_LIMIT}`

- OWNER_ID: `{config.OWNER_ID}`
- SUDO_USERS: `{config.SUDO_USERS}`

- PING_IMG: `{config.PING_IMG}`
- START_IMG: `{config.START_IMG}`
- SUPPORT_CHAT: `{config.SUPPORT_CHAT}`

- SESSION: `{config.SESSION}`""",
            disable_web_page_preview=True,
        )
    except:
        return await message.reply_text("Failed to send the config variables.")
    if message.chat.type != ChatType.PRIVATE:
        await message.reply_text(
            "Please check your PM, I've sent the config variables there."
        )
