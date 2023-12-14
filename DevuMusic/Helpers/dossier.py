from DevuMusic import BOT_NAME

# PM_START_TEXT
PM_START_TEXT = """
Hey {0},
This is {1}!

A fast and powerful music player bot.
"""

# START_TEXT
START_TEXT = """
Hey {0},
Now {1} can play songs in {2}.

──────────────────
For getting help about me or if you wanna ask something, you can join my [support chat]({3}).
"""

# HELP_TEXT
HELP_TEXT = """
❄ **Available commands for users in {BOT_NAME}:**

- /play: Starts streaming the requested track on video chat.
- /pause: Pauses the current playing stream.
- /resume: Resumes the paused stream.
- /skip: Skips the current playing stream and starts streaming the next track in the queue.
- /end: Clears the queue and ends the current playing stream.

- /ping: Shows the ping and system stats of the bot.
- /sudolist: Shows the list of sudo users of the bot.

- /song: Downloads the requested song and sends it to you.

- /search: Searches the given query on YouTube and shows you the result.
"""

# HELP_SUDO
HELP_SUDO = """
✨ **Sudo commands in {BOT_NAME}:**

- /activevc: Shows the list of currently active voice chats.
- /eval or /sh: Runs the given code on the bot's terminal.
- /speedtest: Runs a speedtest on the bot's server.
- /sysstats: Shows the system stats of the bot's server.

- /setname [text or reply to a text]: Changes the assistant account name.
- /setbio [text or reply to a text]: Changes the bio of the assistant account.
- /setpfp [reply to a photo]: Changes the PFP of the assistant account.
- /delpfp: Deletes the current PFP of the assistant account.
"""

# HELP_DEV
HELP_DEV = """
✨ **Owner commands in {BOT_NAME}:**

- /config: To get all config variables of the bot.
- /broadcast [message or reply to a message]: Broadcasts the message to server chats of the bot.
- /rmdownloads: Clears the cache files downloaded on the bot's server.
- /leaveall: Orders the assistant account to leave all chats.

- /addsudo [username or reply to a user]: Adds the user to sudo users list.
- /rmsudo [username or reply to a user]: Removes the user from sudo users list.
"""
