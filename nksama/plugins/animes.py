from nksama import bot
from pyrogram import *
from pyrogram.types import *

from pyrogram.handlers import MessageHandler

import re

from jikanpy import Jikan
from jikanpy.exceptions import APIException
from telegram import Chat, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CallbackQueryHandler
from telegram.constants import ParseMode

jikan = Jikan()

@bot.on_message(filters.command("character"))
async def character(_, msg: Message):
    res = ""
    query = m.text.split(None, 1)[1]
    search = jikan.search("character", query).get("results")[0].get("mal_id")
    res = jikan.character(search)
    if res:
        name = res.get("name")
        kanji = res.get("name_kanji")
        about = res.get("about")
        about = re.sub(r"\\n", r"\n", about)
        about = re.sub(r"\r\n", r"", about)
        if len(about) > 4096:
            about = about[:4000] + "..."
        image = res.get("image_url")
        url = res.get("url")
        rep = f"<b>{name} ({kanji})</b>\n\n"
        rep += f"<a href='{image}'>\u200c</a>"
        rep += f"<i>{about}</i>"
        keyb = [
            [InlineKeyboardButton("More Information", url=url),
           InlineKeyboardButton("Add to favorite character", callback_data=f"xanime_fvrtchar={name}")]]
        
        
        await msg.reply_text(rep, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyb))
        
