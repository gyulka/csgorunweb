from collections import defaultdict
import requests
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, \
    KeyboardButton

Token = '5007549074:AAEjYzssYbTc1VhSbxPQqrY52H_MQxYskmI'

bot = Bot(token=Token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_msg(message: types.Message):
    await message.answer(text='''/get_balance
/update_bet''')


@dp.message_handler(commands=['/get_balance'])
async def get_balance(message: types.Message):
    response = requests.get('http://127.0.0.1:5000/get_balance')
    await message.answer(response.text)



@dp.message_handler(commands=['/get_balance'])
async def update_bet(message: types.Message):
    response = requests.get('http://127.0.0.1:5000/update_bet',json={'bet':message.text.split()[1],'id':message.text.split()[2]})




if __name__ == '__main__':
    executor.start_polling(dp)
