#(©)Codexbotz

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from bot import Bot
from config import OWNER_ID
import subprocess
import uuid
import os

# Temporary store for download URLs per user
user_links = {}

@Bot.on_callback_query()
async def callback_handler(bot: Bot, query: CallbackQuery):
    data = query.data

    if data == "about":
        await query.message.edit_text(
            text = f"<b>○ ᴏᴡɴᴇʀ : <a href='tg://user?id={OWNER_ID}'>ᴍɪᴋᴇʏ</a>\n○ ᴍʏ ᴜᴘᴅᴀᴛᴇs : <a href='https://t.me/CodeFlix_Bots'>ᴄᴏᴅᴇғʟɪx ʙᴏᴛs</a>\n○ ᴍᴏᴠɪᴇs ᴜᴘᴅᴀᴛᴇs : <a href='https://t.me/Team_Netflix'>ᴛᴇᴀᴍ ɴᴇᴛғʟɪx</a>\n○ ᴏᴜʀ ᴄᴏᴍᴍᴜɴɪᴛʏ : <a href='https://t.me/otakuflix_network'>ᴏᴛᴀᴋᴜғʟɪx ɴᴇᴛᴡᴏʀᴋ</a>\n○ ᴀɴɪᴍᴇ ᴄʜᴀᴛ : <a href='https://t.me/weebzonex'>ᴡᴇᴇʙ ᴢᴏɴᴇ</a></b>",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("⚡️ ᴄʟᴏsᴇ", callback_data="close"),
                    InlineKeyboardButton("🍁 ᴘʀᴇᴍɪᴜᴍ", url="https://t.me/OtakuFlix_Network/4639")
                ]
            ])
        )

    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass

    elif data.startswith("download|"):
        await query.answer()
        format_code = data.split("|")[1]
        user_id = query.from_user.id
        url = user_links.get(user_id)

        if not url:
            return await query.message.edit("URL not found. Please restart with /download.")

        msg = await query.message.reply("Downloading selected quality...")

        filename = f"{uuid.uuid4().hex}.mp4"

        try:
            # Download via yt-dlp
            cmd = ["yt-dlp", "-f", format_code, "-o", filename, url]
            subprocess.run(cmd, check=True)

            await msg.edit("Uploading...")

            try:
                await query.message.reply_video(video=filename, supports_streaming=True)
            except:
                await query.message.reply_document(document=filename)

        except Exception as e:
            await msg.edit(f"Download failed: {e}")
        finally:
            if os.path.exists(filename):
                os.remove(filename)

#⋗  ᴛᴇʟᴇɢʀᴀᴍ - @Codeflix_bots


#- ᴄʀᴇᴅɪᴛ - Github - @Codeflix-bots , @erotixe
#- ᴘʟᴇᴀsᴇ ᴅᴏɴ'ᴛ ʀᴇᴍᴏᴠᴇ ᴄʀᴇᴅɪᴛ..
#- ᴛʜᴀɴᴋ ʏᴏᴜ ᴄᴏᴅᴇғʟɪx ʙᴏᴛs ғᴏʀ ʜᴇʟᴘɪɴɢ ᴜs ɪɴ ᴛʜɪs ᴊᴏᴜʀɴᴇʏ 
#- ᴛʜᴀɴᴋ ʏᴏᴜ ғᴏʀ ɢɪᴠɪɴɢ ᴍᴇ ᴄʀᴇᴅɪᴛ @Codeflix-bots  
#- ғᴏʀ ᴀɴʏ ᴇʀʀᴏʀ ᴘʟᴇᴀsᴇ ᴄᴏɴᴛᴀᴄᴛ ᴍᴇ -> ᴛᴇʟᴇɢʀᴀᴍ @codeflix_bots Community @Otakflix_Network </b>
