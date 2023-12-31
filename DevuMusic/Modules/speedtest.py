import asyncio
import speedtest
from pyrogram import filters
from DevuMusic import SUDOERS, app

def testspeed(m):
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        m = m.edit("**⇆ Running download speed test...**")
        test.download()
        m = m.edit("**⇆ Running upload speed test...**")
        test.upload()
        test.results.share()
        result = test.results.dict()
        m = m.edit("**↻ Sharing speed test results...**")
    except Exception as e:
        return m.edit(str(e))
    return result

@app.on_message(filters.command(["speedtest", "spt"]) & SUDOERS)
async def speedtest_function(_, message):
    m = await message.reply_text("**» Running speed test...**")
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, testspeed, m)
    output = f"""✯ **Speedtest Results** ✯
    
<u>**❥͜͡Client:**</u>
**» __ISP:__** {result['client']['isp']}
**» __Country:__** {result['client']['country']}
  
<u>**❥͜͡Server:**</u>
**» __Name:__** {result['server']['name']}
**» __Country:__** {result['server']['country']}, {result['server']['cc']}
**» __Sponsor:__** {result['server']['sponsor']}
**» __Latency:__** {result['server']['latency']}  
**» __Ping:__** {result['ping']}"""
    msg = await app.send_photo(chat_id=message.chat.id, photo=result["share"], caption=output)
    await m.delete()
