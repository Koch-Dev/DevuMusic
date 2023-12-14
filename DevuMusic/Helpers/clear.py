from DevuMusic import devudb
from DevuMusic.Helpers import remove_active_chat


async def _clear_(chat_id):
    try:
        devudb[chat_id] = []
        await remove_active_chat(chat_id)
    except:
        return
