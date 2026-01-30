import os
import re
import sys
import json
import time
import asyncio
import requests
import subprocess
import urllib.parse
import yt_dlp
import cloudscraper
import m3u8
import core as helper
from utils import progress_bar
from vars import API_ID, API_HASH, BOT_TOKEN
from aiohttp import ClientSession
from pyromod import listen
from subprocess import getstatusoutput
from pytube import YouTube
from aiohttp import web
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Get environment variables
WEBHOOK = os.getenv("WEBHOOK", "False").lower() == "true"
PORT = int(os.getenv("PORT", 8000))

# Initialize the bot
bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

photo = "https://i.postimg.cc/dVY9nL63/IMG-20250426-130510-655.jpg"
cpphoto = "https://i.postimg.cc/dVY9nL63/IMG-20250426-130510-655.jpg"
appxzip = "https://i.postimg.cc/dVY9nL63/IMG-20250426-130510-655.jpg"
my_name = "A M I T ⚡"
CHANNEL_ID = "-1002607772171"##change it with your channel 🆔 
LOG_CHANNEL = "-1002607772171"

cookies_file_path = os.getenv("COOKIES_FILE_PATH", "youtube_cookies.txt")

# Define aiohttp routes
routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.json_response("your_render_url") ## change it with your host url

async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    return web_app

async def start_bot():
    await bot.start()
    print("Bot is up and running")

async def stop_bot():
    await bot.stop()

async def main():
    if WEBHOOK:
        # Start the web server
        app_runner = web.AppRunner(await web_server())
        await app_runner.setup()
        site = web.TCPSite(app_runner, "0.0.0.0", PORT)
        await site.start()
        print(f"Web server started on port {PORT}")

    # Start the bot
    await start_bot()

    # Keep the program running
    try:
        while True:
            await asyncio.sleep(3600)  # Run forever, or until interrupted
    except (KeyboardInterrupt, SystemExit):
        await stop_bot()
        
class Data:
    START = (
        "🌟 Welcome {0}! 🌟\n\n"
    )
# Define the start command handler
@bot.on_message(filters.command("start"))
async def start(client: Client, msg: Message):
    await client.send_message(
        msg.chat.id,
        Data.START.format(msg.from_user.mention)
    )
    
@bot.on_message(filters.command(["stop"]) )
async def restart_handler(_, m):
    await m.delete()
    await m.reply_text("**STOPPED**🛑", True)
    os.execl(sys.executable, sys.executable, *sys.argv)

# YouTube download helper function
async def download_youtube_video_improved(url, quality, output_name):
    """Improved YouTube download function"""
    try:
        # Try multiple format selections
        format_options = [
            f'bestvideo[height<={quality}]+bestaudio/best[height<={quality}]',
            f'best[height<={quality}]',
            'bestvideo+bestaudio/best',
            'best'
        ]
        
        cookies_available = os.path.exists(cookies_file_path)
        
        for format_str in format_options:
            ydl_opts = {
                'format': format_str,
                'outtmpl': f'{output_name}.%(ext)s',
                'merge_output_format': 'mp4',
                'ignoreerrors': True,
                'no_warnings': True,
                'quiet': True,
                'extractor_args': {
                    'youtube': {
                        'player_client': ['android', 'web'],
                        'skip': ['hls', 'dash'],
                    }
                },
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-us,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                }
            }
            
            # Add cookies if available
            if cookies_available:
                ydl_opts['cookiefile'] = cookies_file_path
            
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    if info:
                        downloaded_file = f"{output_name}.mp4"
                        if os.path.exists(downloaded_file):
                            return downloaded_file
            except Exception as e:
                print(f"Format {format_str} failed: {e}")
                continue
        
        return None
    except Exception as e:
        print(f"YouTube download error: {e}")
        return None

# m3u8 handler - MAIN FIXES APPLIED HERE
@bot.on_message(filters.command(["advance"]))
async def txt_handler(bot: Client, m: Message):
    editable = await m.reply_text(f"**🔹Send me the TXT file and wait.**")
    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
    await input.delete(True)
    file_name, ext = os.path.splitext(os.path.basename(x))
    credit = f"𝗦𝗣𝗜𝗗𝗬™🇮🇳"
    try:    
        with open(x, "r") as f:
            content = f.read()
        content = content.split("\n")
        links = []
        for i in content:
            links.append(i.split("://", 1))
        os.remove(x)
    except:
        await m.reply_text("Invalid file input.")
        os.remove(x)
        return
   
    await editable.edit(f"Total links found are **{len(links)}**\n\nSend From where you want to download initial is **1**")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text = input0.text
    await input0.delete(True)
    try:
        arg = int(raw_text)
    except:
        arg = 1
    await editable.edit("**Enter Your Batch Name or send d for grabing from text filename.**")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text0 = input1.text
    await input1.delete(True)
    if raw_text0 == 'd':
        b_name = file_name
    else:
        b_name = raw_text0

    await editable.edit("**Enter resolution.\n Eg : 480 or 720**")
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    await input2.delete(True)
    try:
        if raw_text2 == "144":
            res = "144x256"
        elif raw_text2 == "240":
            res = "240x426"
        elif raw_text2 == "360":
            res = "360x640"
        elif raw_text2 == "480":
            res = "480x854"
        elif raw_text2 == "720":
            res = "720x1280"
        elif raw_text2 == "1080":
            res = "1080x1920" 
        else: 
            res = "UN"
    except Exception:
            res = "UN"
    
    await editable.edit("**Enter Your Name or send 'de' for use default.\n Eg : 𝗦𝗣𝗜𝗗𝗬™👨🏻‍💻**")
    input3: Message = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    await input3.delete(True)
    if raw_text3 == 'de':
        CR = credit
    else:
        CR = raw_text3

    await editable.edit("**Enter Your PW Token For 𝐌𝐏𝐃 𝐔𝐑𝐋  or send 'unknown' for use default**")
    input4: Message = await bot.listen(editable.chat.id)
    raw_text4 = input4.text
    await input4.delete(True)
    if raw_text4 == 'unknown':
        MR = raw_text4
    else:
        MR = raw_text4
        
    await editable.edit("Now send the **Thumb url**\n**Eg :** ``\n\nor Send `no`")
    input6 = message = await bot.listen(editable.chat.id)
    raw_text6 = input6.text
    await input6.delete(True)
    await editable.delete()

    thumb = input6.text
    thumb_path = None
    if thumb.startswith("http://") or thumb.startswith("https://"):
        try:
            getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
            thumb_path = "thumb.jpg"
        except:
            thumb_path = None
    else:
        thumb = "no"

    count = int(raw_text)    
    try:
        for i in range(arg-1, len(links)):
            if len(links[i]) < 2:
                continue
                
            Vxy = links[i][1].replace("file/d/","uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing","")
            url = "https://" + Vxy
            
            # Your existing URL processing logic
            if "acecwply" in url:
                cmd = f'yt-dlp -o "{name}.%(ext)s" -f "bestvideo[height<={raw_text2}]+bestaudio" --hls-prefer-ffmpeg --no-keep-video --remux-video mkv --no-warning "{url}"'
       
            elif '/master.mpd' in url:
                vid_id = url.split("/")[-2]
                url = f"https://anonymouspwplayerr-c96de7802811.herokuapp.com/pw?url={url}&token={raw_text4}"
            
            name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
            name = f'{str(count).zfill(3)}) {name1[:60]} {my_name}'

            # FIXED SECTION: Improved YouTube download handling
            if "youtube.com" in url or "youtu.be" in url:
                try:
                    # Use improved YouTube download function
                    quality_int = int(raw_text2) if raw_text2.isdigit() else 720
                    downloaded_file = await download_youtube_video_improved(url, quality_int, name)
                    
                    if downloaded_file and os.path.exists(downloaded_file):
                        cc = f'**🎞️ VID_ID: {str(count).zfill(3)}.\n\n Title: {name1} @Spidy_Universe {raw_text2}p.mp4\n\n📚 Batch Name: {b_name}\n\n📥 Extracted By : {CR}\n\n**━━━━━✦ＳＰＩＤΣＲ⚡✦━━━━━**'
                        
                        # Send the video
                        await bot.send_video(
                            chat_id=m.chat.id,
                            video=downloaded_file,
                            caption=cc,
                            thumb=thumb_path if thumb_path else None,
                            supports_streaming=True
                        )
                        count += 1
                        os.remove(downloaded_file)
                        time.sleep(1)
                        continue
                    else:
                        await m.reply_text(f"Failed to download YouTube video: {name}")
                        continue
                except Exception as e:
                    await m.reply_text(f"YouTube download error: {str(e)}")
                    continue
            
            # Original non-YouTube handling
            if "youtu" in url:
                ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
            else:
                ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"
            
            if "jw-prod" in url:
                cmd = f'yt-dlp -o "{name}.mp4" "{url}"'
            elif "youtube.com" in url or "youtu.be" in url:
                # Fallback for YouTube if above method fails
                cmd = f'yt-dlp --cookies youtube_cookies.txt -f "{ytf}" "{url}" -o "{name}.mp4"'
            else:
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'

            try:  
                cc = f'**🎞️ VID_ID: {str(count).zfill(3)}.\n\n Title: {name1} @Spidy_Universe {res}.mkv\n\n📚 Batch Name: {b_name}\n\n📥 Extracted By : {CR}\n\n**━━━━━✦ＳＰＩＤΣＲ⚡✦━━━━━**'
                cc1 = f'**📁 PDF_ID: {str(count).zfill(3)}.\n\n Title: {name1} @Spidy_Universe.pdf\n\n📚 Batch Name: {b_name}\n\n📥 Extracted By : {CR}\n\n**━━━━━✦ＳＰＩＤΣＲ⚡✦━━━━━**'
                    
                if "drive" in url:
                    try:
                        ka = await helper.download(url, name)
                        copy = await bot.send_document(chat_id=m.chat.id,document=ka, caption=cc1)
                        count+=1
                        os.remove(ka)
                        time.sleep(1)
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue

                elif ".pdf" in url:
                    try:
                        await asyncio.sleep(1)
                        url = url.replace(" ", "%20")
                        scraper = cloudscraper.create_scraper()
                        response = scraper.get(url)

                        if response.status_code == 200:
                            with open(f'{name}.pdf', 'wb') as file:
                                file.write(response.content)

                            await asyncio.sleep(1)
                            copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                            count += 1
                            os.remove(f'{name}.pdf')
                        else:
                            await m.reply_text(f"Failed to download PDF: {response.status_code} {response.reason}")

                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue
                          
                else:
                    Show = f"📥 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠 »\n\n📝 Title:- `{name}`\n\n**🔗 𝐓𝐨𝐭𝐚𝐥 𝐔𝐑𝐋 »** ✨{len(links)}✨\n\n⌨ 𝐐𝐮𝐥𝐢𝐭𝐲 » {raw_text2}`\n\n**🔗 𝐔𝐑𝐋 »** `{url}`\n\n**𝐁𝐨𝐭 𝐌𝐚𝐝𝐞 𝐁𝐲 ✦ 🅂🄿🄸🄳🅈**"
                    prog = await m.reply_text(Show)
                    res_file = await helper.download_video(url, cmd, name)
                    filename = res_file
                    await prog.delete(True)
                    await helper.send_vid(bot, m, cc, filename, thumb, name, prog)
                    count += 1
                    time.sleep(1)

            except Exception as e:
                await m.reply_text(
                    f"⌘ 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠 𝐈𝐧𝐭𝐞𝐫𝐮𝐩𝐭𝐞𝐝\n\n⌘ 𝐍𝐚𝐦𝐞 » {name}\n⌘ 𝐋𝐢𝐧𝐤 » `{url}`\n⌘ 𝐄𝐫𝐫𝐨𝐫 » `{str(e)}`"
                )
                continue

    except Exception as e:
        await m.reply_text(f"Overall error: {e}")
    
    # Cleanup
    if thumb_path and os.path.exists(thumb_path):
        os.remove(thumb_path)
        
    await m.reply_text("🔰Done🔰")
    await m.reply_text("✨Thankyou For Choosing")


if __name__ == "__main__":
    # Check for YouTube cookies
    if os.path.exists("youtube_cookies.txt"):
        print("YouTube cookies file found.")
    else:
        print("No YouTube cookies file found. Some downloads may fail.")
    
    # Run the bot
    bot.run()
