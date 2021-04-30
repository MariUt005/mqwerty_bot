import telebot
import config
import random

from telebot import types

ANSWER = {}
FALSE = {}

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('top.tgs', 'rb')
    bot.send_sticker(message.chat.id, sti)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Random Num")
    item2 = types.KeyboardButton("How are you?")
    words7 = types.KeyboardButton("/7")
    markup.add(item1, item2, words7)



    bot.send_message(message.chat.id,
                     "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот, созданный чтобы быть подопытным кроликом.".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':
        if message.text == 'Random Num':
            bot.send_message(message.chat.id, str(random.randint(0, 100)))
        elif message.text == 'How are you?':

            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Good!", callback_data='good')
            item2 = types.InlineKeyboardButton("Bad...", callback_data='bad')
            markup.add(item1, item2)
            bot.send_message(message.chat.id, 'Nice, and you?', reply_markup=markup)
        elif message.text == '/7':
            question = get_7(message.chat.id)
            markup = types.InlineKeyboardMarkup(row_width=2)
            if random.randint(0, 2) == 0:
                item1 = types.InlineKeyboardButton(ANSWER[message.chat.id], callback_data=ANSWER[message.chat.id])
                item2 = types.InlineKeyboardButton(FALSE[message.chat.id], callback_data=FALSE[message.chat.id])
            else:
                item1 = types.InlineKeyboardButton(FALSE[message.chat.id], callback_data=FALSE[message.chat.id])
                item2 = types.InlineKeyboardButton(ANSWER[message.chat.id], callback_data=ANSWER[message.chat.id])
            markup.add(item1, item2)
            bot.send_message(message.chat.id, question, reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'I don\'t understand you...')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            print(ANSWER)
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Cool!')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Don\'t worry!')
            elif call.data == ANSWER[call.message.chat.id]:
                sti = open('top.tgs', 'rb')
                bot.send_sticker(call.message.chat.id, sti)
                bot.send_message(call.message.chat.id, '✅ Cool! Правильный ответ: ' + ANSWER[call.message.chat.id])
                question = get_7(call.message.chat.id)
                markup = types.InlineKeyboardMarkup(row_width=2)
                if random.randint(0, 2) == 0:
                    item1 = types.InlineKeyboardButton(ANSWER[call.message.chat.id], callback_data=ANSWER[call.message.chat.id])
                    item2 = types.InlineKeyboardButton(FALSE[call.message.chat.id], callback_data=FALSE[call.message.chat.id])
                else:
                    item1 = types.InlineKeyboardButton(FALSE[call.message.chat.id], callback_data=FALSE[call.message.chat.id])
                    item2 = types.InlineKeyboardButton(ANSWER[call.message.chat.id], callback_data=ANSWER[call.message.chat.id])
                markup.add(item1, item2)
                bot.send_message(call.message.chat.id, question, reply_markup=markup)
            elif call.data == FALSE[call.message.chat.id]:
                sti = open('no.tgs', 'rb')
                bot.send_sticker(call.message.chat.id, sti)
                bot.send_message(call.message.chat.id, '❌ Oh... Правильный ответ: ' + ANSWER[call.message.chat.id])
                question = get_7(call.message.chat.id)
                markup = types.InlineKeyboardMarkup(row_width=2)
                if random.randint(0, 2) == 0:
                    item1 = types.InlineKeyboardButton(ANSWER[call.message.chat.id], callback_data=ANSWER[call.message.chat.id])
                    item2 = types.InlineKeyboardButton(FALSE[call.message.chat.id], callback_data=FALSE[call.message.chat.id])
                else:
                    item1 = types.InlineKeyboardButton(FALSE[call.message.chat.id], callback_data=FALSE[call.message.chat.id])
                    item2 = types.InlineKeyboardButton(ANSWER[call.message.chat.id], callback_data=ANSWER[call.message.chat.id])
                markup.add(item1, item2)
                bot.send_message(call.message.chat.id, question, reply_markup=markup)


            #remove inline buttons
            #bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
            #                      text="😊 Как дела?",
            #                      reply_markup=None)

            # show alert
            #bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="ЭТО ТЕСТОВОЕ УВЕДОМЛЕНИЕ!!11")
    except Exception as e:
        print(repr(e))


def get_7(chat_id):
    global ANSWER, FALSE
    file = open('words7.txt', encoding='utf-8')
    words = []
    file = file.readlines()
    for i in file:
        words.append(i.split())
    answer_id = random.randint(0, len(words))
    question = words[answer_id][0]
    ANSWER[chat_id] = words[answer_id][1]
    FALSE[chat_id] = words[answer_id][2]
    return question


#RUN
bot.polling(none_stop=True)