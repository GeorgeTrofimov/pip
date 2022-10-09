from asyncio import streams
import os
from turtle import title
import telebot
from ast import parse
from aiogram import *
from pytube import YouTube

bot = telebot.TeleBot("5670633455:AAGT69BfD-NhB97BLDmxK4K2d-IC9CKWzis")
dt = Dispatcher(bot)

@dt.message_handler(commands=["start"])
async def start_message(message:types.Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, "Привет, могу для вас загрузить видео с Youtube\n"
                                    "Отправьте мне ссылку" )
    
@dt.message_handler()
async def text_message(message:types.Message):
    chat_id = message.chat.id
    url = message.text
    yt = YouTube(url)
    if message.text.startswith == 'https://youtu.be' or 'https://www.youtube.com/':
        await bot.send_message(chat_id, f"*Приступаю к загрузке видео* : *{yt.title}*\n"
                                        f"*С канала *: [{yt.author}]({yt.channel_url})", parse_mode = "Markdown")
        await download_youtube_video(url, message, bot)

async def download_youtube_video(url, message, bot):
    yt = YouTube(url)
    stream = yt.streams.filter(progressive=True, file_extension="mp4")
    stream.get_highest_resolution().download(f'{message.chat.id}', f'{message.chat.id}_{yt.title}')
    with open(f"*{message.chat.id}/{message.chat.id}_{yt.title}", 'rb') as video:
        await bot.send_video(message.chat.id, video, caption="*Вот ваше видео*", parse_mode='Markdown')
        os.remove(f"{message.chat.id}/{message.chat.id}_{yt.title}")

if __name__ == '__main__':
    executor.start_polling(dt)
