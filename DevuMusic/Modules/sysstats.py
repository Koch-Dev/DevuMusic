from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pytgcalls.__version__ import __version__ as pytgver
import psutil
import socket
import platform
import re
import uuid
from sys import version as pyver
from DevuMusic import BOT_NAME, SUDOERS, app
from DevuMusic.Modules import ALL_MODULES

@app.on_message(filters.command(["stats", "sysstats"]) & SUDOERS)
async def sys_stats(_, message: Message):
    sysrep = await message.reply_text(
        f"Getting {BOT_NAME} system stats, it'll take a while..."
    )
    try:
        await message.delete()
    except Exception as del_error:
        print(f"Error deleting message: {del_error}")

    try:
        sudoers = len(SUDOERS)
        mod = len(ALL_MODULES)
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(socket.gethostname())
        architecture = platform.machine()
        processor = platform.processor()
        mac_address = ":".join(re.findall("..", "%012x" % uuid.getnode()))
        sp = platform.system()
        ram = str(round(psutil.virtual_memory().total / (1024.0**3))) + " GB"
        p_core = psutil.cpu_count(logical=False)
        t_core = psutil.cpu_count(logical=True)
        
        try:
            cpu_freq = psutil.cpu_freq().current
            cpu_freq = f"{round(cpu_freq / 1000, 2)} GHz" if cpu_freq >= 1000 else f"{round(cpu_freq, 2)} MHz"
        except Exception as freq_error:
            cpu_freq = f"Failed to fetch ({freq_error})"
        
        hdd = psutil.disk_usage("/")
        total, used, free = map(lambda x: f"{x / (1024.0**3):.2f} GB", (hdd.total, hdd.used, hdd.free))
        platform_release = platform.release()
        platform_version = platform.version()

        await sysrep.edit_text(
            f"""
<u>{BOT_NAME} System Stats</u>

<b>Python:</b> {pyver.split()[0]}
<b>Pyrogram:</b> {pyrogram.__version__}
<b>PyTGCalls:</b> {pytgver}
<b>Sudoers:</b> {sudoers}
<b>Modules:</b> {mod}

<b>IP:</b> {ip_address}
<b>MAC:</b> {mac_address}
<b>Hostname:</b> {hostname}
<b>Platform:</b> {sp}
<b>Processor:</b> {processor}
<b>Architecture:</b> {architecture}
<b>Platform Release:</b> {platform_release}
<b>Platform Version:</b> {platform_version}

<b>Storage:</b>
<b>Available:</b> {total}
<b>Used:</b> {used}
<b>Free:</b> {free}

<b>RAM:</b> {ram}
<b>Physical Cores:</b> {p_core}
<b>Total Cores:</b> {t_core}
<b>CPU Frequency:</b> {cpu_freq}
""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Close",
                            callback_data=f"forceclose abc|{message.from_user.id}",
                        ),
                    ]
                ]
            ),
        )
    except Exception as stats_error:
        await sysrep.edit_text(f"Failed to fetch system stats: {stats_error}")
