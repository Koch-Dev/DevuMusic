from pyrogram import filters
from pyrogram.types import Message

from config import OWNER_ID
from DevuMusic import SUDOERS, app


@app.on_message(filters.command(["addsudo"]) & filters.user(OWNER_ID))
async def sudoadd(_, message: Message):
    try:
        await message.delete()
    except:
        pass
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(
                "» Reply to a user's message or provide username/user ID."
            )
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        if int(user.id) in SUDOERS:
            return await message.reply_text(f"» {user.mention} is already a sudo user.")
        try:
            SUDOERS.add(int(user.id))
            await message.reply_text(f"Added {user.mention} to sudo users list.")
        except:
            return await message.reply_text("Failed to add user to sudoers.")

    if message.reply_to_message.from_user.id in SUDOERS:
        return await message.reply_text(
            f"» {message.reply_to_message.from_user.mention} is already a sudo user."
        )
    try:
        SUDOERS.add(message.reply_to_message.from_user.id)
        await message.reply_text(
            f"Added {message.reply_to_message.from_user.mention} to sudo users list."
        )
    except:
        return await message.reply_text("Failed to add user to sudoers.")


@app.on_message(filters.command(["delsudo", "rmsudo"]) & filters.user(OWNER_ID))
async def sudodel(_, message: Message):
    try:
        await message.delete()
    except:
        pass
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(
                "» Reply to a user's message or provide username/user ID."
            )
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        if int(user.id) not in SUDOERS:
            return await message.reply_text(
                f"» {user.mention} is not in sudo users list."
            )
        try:
            SUDOERS.remove(int(user.id))
            return await message.reply_text(
                f"» Removed {user.mention} from sudo users list."
            )
        except:
            return await message.reply_text(f"Failed to remove user from sudoers.")
    else:
        user_id = message.reply_to_message.from_user.id
        if int(user_id) not in SUDOERS:
            return await message.reply_text(
                f"» {message.reply_to_message.from_user.mention} is not in sudo users list."
            )
        try:
            SUDOERS.remove(int(user_id))
            return await message.reply_text(
                f"» Removed {message.reply_to_message.from_user.mention} from sudo users list."
            )
        except:
            return await message.reply_text(f"Failed to remove user from sudoers.")


@app.on_message(filters.command(["sudolist", "sudoers", "sudo"]))
async def sudoers_list(_, message: Message):
    hehe = await message.reply_text("» Getting sudo users list...")
    text = "<u>**Owner :**</u>\n"
    count = 0
    user = await app.get_users(OWNER_ID)
    user = user.first_name if not user.mention else user.mention
    count += 1
    text += f"{count}➤ {user}\n"
    smex = 0
    for user_id in SUDOERS:
        if user_id != OWNER_ID:
            try:
                user = await app.get_users(user_id)
                user = user.first_name if not user.mention else user.mention
                if smex == 0:
                    smex += 1
                    text += "\n<u>**Sudoers :**</u>\n"
                count += 1
                text += f"{count}➤ {user}\n"
            except Exception:
                continue
    if not text:
        await message.reply_text("» No sudo users found.")
    else:
        await hehe.edit_text(text)
