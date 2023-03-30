import json
import aiohttp
import openai, config, os
import requests
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

openai.api_key = config.openai_key
bot = Bot(config.BOT_TOKEN)
dp = Dispatcher(bot)

messages = [
    {"role": "system", "content": "Ты должен помогать мне с любыми задачами"},
    {"role": "user", "content": "Я - пользователь и хочу получать ответы на любой свой вопрос."},
    {"role": "assistant", "content": "Приветствую! Я весь к вашим услугам, чем вам помочь?"}
]

def update(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Приветствую! Отправьте ваш запрос.')
    
@dp.message_handler()
async def send(message: types.Message):
    update(messages, "user", message.text)
    response = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages = messages,
        max_tokens = 3500
    )
    response['model'] = 'gpt-3.5-turbo'
    await message.answer(response['choices'][0]['message']['content'])
        

if __name__ == '__main__':
    print('Бот запущен...')
    executor.start_polling(dp, skip_updates=True)
    