
import json
import logging
import sys
import time
import telepot
from urllib import request
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

# Уникальный ТОКЕН из телеграм бота

TOKEN = '1865996088:AAEBHjhrpohizLqW8lLeIdMrqb8OUuX3JWw'

#Функция создания кнопок в телеграме 

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text='Температура', callback_data='field1')],
                   [InlineKeyboardButton(text='Номер измерения', callback_data='entry_id')],
                   [InlineKeyboardButton(text='Время и дата измерения', callback_data='created_at')],
                   [InlineKeyboardButton(text='GitHub бота', url="https://github.com/JustRuslashka/TeleThingSpeak_bot")],
                     
               ])
   

    bot.sendMessage(chat_id, 'Выбери нужное', reply_markup=keyboard)

#Функция on_callback_query обрабатывает данные из Thingspeak и отображает их в соответствии с нажатой кнопкой
    
def on_callback_query(msg):
    # хранит в переменной ответ в формате GET   

    response = request.urlopen('https://api.thingspeak.com/channels/1392970/feeds.json?results=2')

    # получает данные в виде json

    data = response.read().decode('utf-8')

    # преобразование строки

    data_dict = json.loads(data)

    feeds = data_dict['feeds']
    
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    
    print('Callback Query:', query_id, from_id, query_data)

    if(query_data == 'field1'):
        bot.sendMessage(from_id, text='.')
        bot.sendMessage(from_id, text='________________________________________')
        bot.sendMessage(from_id, text='Результаты при последнем измерении: ' + feeds[1]['field1'] + '°C')
 
        if(feeds[1]['field1']  >= '30.00'):
            bot.sendMessage(from_id, text="Предупреждение о перегреве! ")
        elif (feeds[1]['field1']  <= '0.00'):
            bot.sendMessage(from_id, text="Предупреждение об охлаждении! ")
        elif ( '0.00' < feeds[1]['field1']  < '30.00'):
            bot.sendMessage(from_id, text="-----------------Температура в норме----------------- ")

    elif(query_data == 'entry_id'):
        bot.sendMessage(from_id, text='.')
        bot.sendMessage(from_id, text='________________________________________')
        bot.sendMessage(from_id, text="Номер последнего измерения: " + str(feeds[1]['entry_id']))
        
    elif(query_data == 'created_at'):
        bot.sendMessage(from_id, text='.')
        bot.sendMessage(from_id, text='_________________________________________________')
        bot.sendMessage(from_id, text='Время и дата последнего измерения: ' + feeds[1]['created_at'])
  
    
        
#инициализируем функции


bot = telepot.Bot(TOKEN)
MessageLoop(bot, {'chat': on_chat_message,
                  'callback_query': on_callback_query}).run_as_thread()
print('Listening ...')

while 1:
    time.sleep(10)