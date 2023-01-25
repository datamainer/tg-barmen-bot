import telebot
import json
from telebot import types

bot = telebot.TeleBot('')


def json_to_dict(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data



@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    cocktails = types.KeyboardButton("Список коктейлей 🍹")
    markup.add(cocktails)
    
    bot.send_message(message.chat.id, 'Добро подаловать в бар, салага!', reply_markup=markup)


my_dict = json_to_dict('cocktails.json')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data in my_dict:
            value = "\n".join([f"{i+1}. {v}" for i, v in enumerate(my_dict[call.data])])
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"🍸 {call.data.title()}:\n{value.title()}", reply_markup=None)
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Key not found.", reply_markup=None)


@bot.message_handler(commands=['cocktails'])
def send_cocktails(message):
    markup = telebot.types.InlineKeyboardMarkup()
    for key in my_dict.keys():
        btn = telebot.types.InlineKeyboardButton(key, callback_data=key)
        markup.add(btn)
    bot.send_message(message.chat.id, "Выберите коктейль для просмотра рецепта: ", reply_markup=markup)
    

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == 'Список коктейлей 🍹':
        send_cocktails(message)


bot.polling(none_stop=True)
