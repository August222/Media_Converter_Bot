from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType
from config import token
from moviepy.editor import VideoFileClip
import os

bot = Bot(token=token)
dp = Dispatcher(bot)

# START
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_name = message.from_user.first_name
    await message.answer(f'Привет, {user_name}!')
    await message.answer('Отправь мне видео, из которого хочешь извлечь аудио. Жду)')
    

# DOWNLOAD USER VIDEO
@dp.message_handler(content_types=ContentType.VIDEO)
async def download_user_video(message: types.Message):   
    file_id = message.video.file_id
    file = await bot.get_file(file_id)
    await bot.download_file(file.file_path, 'video.mp4')
    await message.answer('Принял твое видео. Обрабатываю...')
    await message.answer('Готово! Придумай название для аудио-файла...')


# CONVERT TO MP3
@dp.message_handler(content_types=['text'])
async def convert(message: types.Message):
    mp3_name = f'{message.text}.mp3'
    await message.answer(f'Отлично! Твой аудио-файл будет сохранен как {mp3_name}')

    mp4_name = 'video.mp4'
    video = VideoFileClip(mp4_name)
    audio = video.audio
    audio.write_audiofile(mp3_name)

    audio.close()
    video.close()

    audio2 = open(f'{mp3_name}', 'rb')
    await bot.send_audio(message.chat.id, audio=audio2)

    os.remove(fr'{mp4_name}')
    os.remove(fr'{mp3_name}')

    await message.answer('Вот твой аудио-файл. Наслаждайся!')


if __name__ == '__main__':
    executor.start_polling(dp)