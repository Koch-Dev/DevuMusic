from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import config
from DevuMusic import BOT_USERNAME

close_key = InlineKeyboardMarkup(
    [[InlineKeyboardButton(text="Close", callback_data="close")]]
)


buttons = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="▷", callback_data="resume_cb"),
            InlineKeyboardButton(text="II", callback_data="pause_cb"),
            InlineKeyboardButton(text="‣‣I", callback_data="skip_cb"),
            InlineKeyboardButton(text="▢", callback_data="end_cb"),
        ]
    ]
)


pm_buttons = [
    [
        InlineKeyboardButton(
            text="ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ",
            url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
        )
    ],
    [InlineKeyboardButton(text="ʜᴇʟᴩ & ᴄᴏᴍᴍᴀɴᴅs", callback_data="devu_help")],
    [
        InlineKeyboardButton(text="📢Channel", url="https://t.me/radhe_rajput001"),
        InlineKeyboardButton(text="💬Group", url=config.SUPPORT_CHAT),
    ],
    [
        InlineKeyboardButton(
            text="Source", url="https://t.me/radhe_rajput001"
        ),
        InlineKeyboardButton(text="Developer", user_id=config.OWNER_ID),
    ],
]


gp_buttons = [
    [
        InlineKeyboardButton(
            text="Wanna Add Me !",
            url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
        )
    ],
    [
        InlineKeyboardButton(text="Channel", url=config.SUPPORT_CHANNEL),
        InlineKeyboardButton(text="Group", url=config.SUPPORT_CHAT),
    ],
    [
        InlineKeyboardButton(
            text="Source", url="https://t.me/dx_radhe01"
        ),
        InlineKeyboardButton(text="Developer", user_id=config.OWNER_ID),
    ],
]


helpmenu = [
    [
        InlineKeyboardButton(
            text="Everyone",
            callback_data="devu_cb help",
        )
    ],
    [
        InlineKeyboardButton(text="Sudo", callback_data="devu_cb sudo"),
        InlineKeyboardButton(text="Owner", callback_data="devu_cb owner"),
    ],
    [
        InlineKeyboardButton(text="Back", callback_data="devu_home"),
        InlineKeyboardButton(text="Close", callback_data="close"),
    ],
]


help_back = [
    [InlineKeyboardButton(text="Group", url=config.SUPPORT_CHAT)],
    [
        InlineKeyboardButton(text="Back", callback_data="devu_help"),
        InlineKeyboardButton(text="Close", callback_data="close"),
    ],
]
