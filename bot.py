from collections import defaultdict
import requests
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, \
    KeyboardButton
from config import tg_token

bot = Bot(token=tg_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_msg(message: types.Message):
    await message.answer(text='''/get_balance
/update_bet
/edit_tactics
/on
/off''')


@dp.message_handler(commands=['get_balance'])
async def get_balance(message: types.Message):
    response = requests.get('http://127.0.0.1:5000/get_balance')
    await message.answer(response.text)


@dp.message_handler(commands=['update_bet1'])
async def update_bet(message: types.Message):
    response = requests.post('http://127.0.0.1:5000/update_bet1',
                             json={'bet': message.text.split()[1], 'id': message.text.split()[2]})


@dp.message_handler(commands=['update_bet2'])
async def update_bet(message: types.Message):
    response = requests.post('http://127.0.0.1:5000/update_bet2',
                             json={'bet': message.text.split()[1]})


@dp.message_handler(commands=['edit_tactics'])
async def update_bet(message: types.Message):
    response = requests.get('http://127.0.0.1:5000/get_flags', )


@dp.message_handler(commands=['on'])
async def update_bet(message: types.Message):
    response = requests.post('http://127.0.0.1:5000/on', )


@dp.message_handler(commands=['off'])
async def update_bet(message: types.Message):
    response = requests.post('http://127.0.0.1:5000/off', )


if __name__ == '__main__':
    executor.start_polling(dp)
