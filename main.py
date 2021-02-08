# PIP and integrated libs
import telebot
import time
import os
import urllib.request
import datetime
import requests
import json
import sqlite3
import logging
import threading

# Logging init
logging.basicConfig(level=logging.DEBUG)
logging.debug("Logging started.")

# Non PIP libs
import asciiart # Draws hello
from colored_logger import * # Making terminal looking better
from scheduler import scheduler # Schedules any function call using threading
from database import * # Main application database
from typehelper import * # Provides regex-based str-to-int

# Modules import
from kubiki import mp_dice
from darts import darts
from slot import slot
from Krush import Krush
from Roulette import Roulette
from dice1 import dice1
from balance import balance
import menu # Stores menus for singleplayer and multiplayer
from deposite import deposite
from bet import bet
from basket import basket

# Databese init
database_name = 'USERS.db'
db = table(database_name)

# Bot init

bot = telebot.TeleBot('1231881164:AAGYkbn_D71JaKa_XX9f8_VRJKZChyQi43c', threaded = False) # Creating bot

# Modules init
bet = bet(db, bot)
deposite = deposite(db, bot)
darts = darts(db, bot)
slot = slot(db, bot)
Krush = Krush(db, bot)
Roulette = Roulette(db, bot)
balance = balance(db, bot)
basket = basket(db, bot)
dice1 = dice1(db, bot)
menu_main = menu.main(db, bot)
menu_single = menu.singleplayer(db, bot)
menu_multi = menu.multiplayer(db, bot)
mp_dice = mp_dice(db, bot)
class modules:
    executable = [deposite, menu_main, basket, darts, dice1, menu_single, menu_multi, mp_dice, slot, balance, Roulette, Krush]
    rollable = [darts, slot, dice1, basket]
    multi = [Krush, Roulette]
    
# Ahaha classic
asciiart.hello()

# Payment info
QIWI_TOKEN = '62f8c2a139f7496f227b20434f5c0aba'
QIWI_ACCOUNT = '+79668560407'

# Default keyboard
keyboard = telebot.types.ReplyKeyboardMarkup(True, True) 
keyboard.row('Одиночная игра🕹', 'Дуэли⚔')
keyboard.row('Пополнить счет💰', 'Вывести деньги💰')
keyboard.row('Баланс💰', 'Помощь❓')

@bot.message_handler(commands=['start']) # Start message handler
def start_message(message):
    db.create_user(message.chat.id) # Default parameters stored in database.py
    menu_main.start(message.chat.id)

@bot.callback_query_handler(func=lambda call: True) #Inline call handler. Used for payment checking.
def callback_inline(call):
    print(call)
    if call.game_short_name != None:
        for module in modules.multi:
            if module.multigame(call):
                break # Break if module rolled
    else:
        deposite.check_payment(call, QIWI_TOKEN, QIWI_ACCOUNT)

@bot.message_handler(content_types=['text']) # Most of user messages
def send_text(message):

    msg_text = message.text.lower()
    user_id = message.chat.id
    user_action = db.get_action(user_id)
    user_action = user_action[0] if user_action else None

    data = [msg_text, user_id, user_action] # Modules feed data. Just unpack it with * :) 
    logging.debug(f'Feeding modules with {data}')
        
    if msg_text and user_id and user_action:
        logging.debug(f'Feeding modules with {data}')
        for module in modules.executable:
            print("gggg")
            if module.execute(*data):
                print("break")
                break # Break if module executed
    else:
        bot.send_message(message.chat.id, 'Пользователь не найден в базе данных. Попробуйте отправить /start. Если это не решило проблему, обратитесь в техническую поддержку.') 

@bot.message_handler(content_types=['dice']) # Blitz Kids - Roll The Dice 🎸
def dice(message):
    for module in modules.rollable:
        logging.debug(module)
        user_action = db.get_action(message.chat.id)
        user_action = user_action[0] if user_action else None
        data = [message.chat.id, message.dice.emoji, message.dice.value, user_action]
        if module.roll(*data):
            break # Break if module rolled

if __name__ == "__main__":
    bot.polling()