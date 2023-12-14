import asyncio
import os

from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import (
    ChatAdminRequired,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pytgcalls import StreamType
from pytgcalls.exceptions import NoActiveGroupCall, TelegramServerError, UnMuteNeeded
from pytgcalls.types import AudioPiped, HighQualityAudio
from youtube_search import YoutubeSearch

from config import DURATION_LIMIT
from DevuMusic import (
    ASS_ID,
    ASS_MENTION,
    ASS_NAME,
    ASS_USERNAME,
    BOT_NAME,
    BOT_USERNAME,
    LOGGER,
    app,
    app2,
    devudb,
    pytgcalls,
)
from DevuMusic.Helpers.active import add_active_chat, is_active_chat, stream_on
from DevuMusic.Helpers.downloaders import audio_dl
from DevuMusic.Helpers.errors import DurationLimitError
from DevuMusic.Helpers.gets import get_file_name, get_url
from DevuMusic.Helpers.inline import buttons
from DevuMusic.Helpers.queue import put
from DevuMusic.Helpers.thumbnails import gen_qthumb, gen_thumb


@app.on_message(
    filters.command(["play", "vplay", "p"])
    & filters.group
    & ~filters.forwarded
    & ~filters.via_bot
)
async def play(_, message: Message):
    devu = await message.reply_text("» Processing, please wait...")
    try:
        await message.delete()
    except:
        pass

    try:
        try:
            get = await app.get_chat_member(message.chat.id, ASS_ID)
        except ChatAdminRequired:
            return await devu.edit_text(
                f"» I don't have permissions to invite users via link for inviting {BOT_NAME} assistant to {message.chat.title}."
            )
        if get.status == ChatMemberStatus.BANNED:
            unban_butt = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text=f"Unban {ASS_NAME}",
                            callback_data=f"unban_assistant {message.chat.id}|{ASS_ID}",
                        ),
                    ]
                ]
            )
            return await devu.edit_text(
                text=f"» {BOT_NAME} assistant is banned in {message.chat.title}\n\nID : `{ASS_ID}`\nName : {ASS_MENTION}\nUsername : @{ASS_USERNAME}\n\nPlease unban the assistant and play again...",
                reply_markup=unban_butt,
            )
    except UserNotParticipant:
        if message.chat.username:
            invitelink = message.chat.username
            try:
                await app2.resolve_peer(invitelink)
            except Exception as ex:
                LOGGER.error(ex)
        else:
            try:
                invitelink = await app.export_chat_invite_link(message.chat.id)
            except ChatAdminRequired:
                return await devu.edit_text(
                    f"» I don't have permissions to invite users via link for inviting {BOT_NAME} assistant to {message.chat.title}."
                )
            except Exception as ex:
                return await devu.edit_text(
                    f"Failed to invite {BOT_NAME} assistant to {message.chat.title}.\n\nReason : `{ex}`"
                )
        if invitelink.startswith("https://t.me/+"):
            invitelink = invitelink.replace("https://t.me/+", "https://t.me/joinchat/")
        anon = await devu.edit_text(
            f"Please wait...\n\nInviting {ASS_NAME} to {message.chat.title}."
        )
        try:
            await app2.join_chat(invitelink)
            await asyncio.sleep(2)
            await devu.edit_text(
                f"{ASS_NAME} joined successfully,\n\nStarting stream..."
            )
        except UserAlreadyParticipant:
            pass
        except Exception as ex:
            return await devu.edit_text(
                f"Failed to invite {BOT_NAME} assistant to {message.chat.title}.\n\nReason : `{ex}`"
            )
        try:
            await app2.resolve_peer(invitelink)
        except:
            pass

    ruser = message.from_user.first_name
    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    url = get_url(message)
    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"» Sorry baby, tracks longer than {DURATION_LIMIT} minutes are not allowed to play on {BOT_NAME}."
            )

        file_name = get_file_name(audio)
        title = file_name
        duration = round(audio.duration / 60)
        file_path = (
            await message.reply_to_message.download(file_name)
            if not os.path.isfile(os.path.join("downloads", file_name))
            else f"downloads/{file_name}"
        )

    elif url:
        try:
            results = YoutubeSearch(url, max_results=1).to_dict()
            title = results[0]["title"]
            duration = results[0]["duration"]
            videoid = results[0]["id"]

            secmul, dur, dur_arr = 1, 0, duration.split(":")
            for i in range(len(dur_arr) - 1, -1, -1):
                dur += int(dur_arr[i]) * secmul
                secmul *= 60

        except Exception as e:
            return await devu.edit_text(f"Something went wrong\n\n**Error :** `{e}`")

        if (dur / 60) > DURATION_LIMIT:
            return await devu.edit_text(
                f"» Sorry baby, tracks longer than {DURATION_LIMIT} minutes are not allowed to play on {BOT_NAME}."
            )
        file_path = audio_dl(url)
    else:
        if len(message.command) < 2:
            return await devu.edit_text("» What do you wanna play baby?")
        await devu.edit_text("🔎")
        query = message.text.split(None, 1)[1]
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            title = results[0]["title"]
            videoid = results[0]["id"]
            duration = results[0]["duration"]

            secmul, dur, dur_arr = 1, 0, duration.split(":")
            for i in range(len(dur_arr) - 1, -1, -1):
                dur += int(dur_arr[i]) * secmul
                secmul *= 60

        except Exception as e:
            LOGGER.error(str(e))
            return await devu.edit("» Failed to process query, try playing again...")

        if (dur / 60) > DURATION_LIMIT:
            return await devu.edit(
                f"» Sorry baby, tracks longer than {DURATION_LIMIT} minutes are not allowed to play on {BOT_NAME}."
            )
        file_path = audio_dl(url)

    try:
        videoid = videoid
    except:
        videoid = "fuckitstgaudio"
    if await is_active_chat(message.chat.id):
        await put(
            message.chat.id,
            title,
            duration,
            videoid,
            file_path,
            ruser,
            message.from_user.id,
        )
        position = len(devudb.get(message.chat.id))
        qimg = await gen_qthumb(videoid, message.from_user.id)
        await message.reply_photo(
            photo=qimg,
            caption=f"**➻ Added to queue at {position}**\n\n‣ **Title:** [{title[:27]}](https://t.me/{BOT_USERNAME}?start=info_{videoid})\n‣ **Duration:** `{duration}` minutes\n‣ **Requested by:** {ruser}",
            reply_markup=buttons,
        )
    else:
        stream = AudioPiped(file_path, audio_parameters=HighQualityAudio())
        try:
            await pytgcalls.join_group_call(
                message.chat.id,
                stream,
                stream_type=StreamType().pulse_stream,
            )

        except NoActiveGroupCall:
            return await devu.edit_text(
                "**» No active video chat found.**\n\nPlease make sure you started the video chat."
            )
        except TelegramServerError:
            return await devu.edit_text(
                "» Telegram is having some internal problems, please restart the video chat and try again."
            )
        except UnMuteNeeded:
            return await devu.edit_text(
                f"» {BOT_NAME} assistant is muted on video chat,\n\nPlease unmute {ASS_MENTION} on video chat and try playing again."
            )

        imgt = await gen_thumb(videoid, message.from_user.id)
        await stream_on(message.chat.id)
        await add_active_chat(message.chat.id)
        await message.reply_photo(
            photo=imgt,
            caption=f"**➻ Started streaming**\n\n‣ **Title:** [{title[:27]}](https://t.me/{BOT_USERNAME}?start=info_{videoid})\n‣ **Duration:** `{duration}` minutes\n‣ **Requested by:** {ruser}",
            reply_markup=buttons,
        )

    return await devu.delete()
