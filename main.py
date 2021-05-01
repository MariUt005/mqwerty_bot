# pyTelegramBotAPI needed
import telebot
import config
import random
from telebot import types

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    global USERid_MODE
    USERid_MODE[message.chat.id] = [None, None]
    sti = open('stickers/animated_text/hi.tgs', 'rb')
    bot.send_sticker(message.chat.id, sti)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    items = [
        types.KeyboardButton('#2'),
        types.KeyboardButton('#7'),
        types.KeyboardButton('#14')
    ]
    markup.add(items[0], items[1], items[2])

    hi_message = "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот, созданный чтобы " \
                 "<strike>быть подопытным кроликом</strike> помочь тебе с подготовкой к ЕГЭ по русскому.\n\n" \
                 "Выбирай ниже кнопку с номером, который вызывает сложности, и погнали!"

    bot.send_message(
        message.chat.id,
        hi_message.format(message.from_user, bot.get_me()),
        parse_mode='html',
        reply_markup=markup
    )


@bot.message_handler(commands=['manual'])
def manual(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Верните назад!'))
    bot.send_message(message.chat.id, 'Здесь могла быть ваша реклама, но пока что ждем, пока админ напишет, как мной пользоваться :)', reply_markup=markup)


@bot.message_handler(commands=['support'])
def manual(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Верните назад!'))
    bot.send_message(message.chat.id, 'Здесь могла быть ваша реклама, но пока что техподдержки тут нема :)', reply_markup=markup)


@bot.message_handler(commands=['set_stickerpack'])
def manual(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Верните назад!'))
    bot.send_message(message.chat.id, 'Здесь могла быть ваша реклама, но админ пока что не сделал такую фичу :)', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def lalala(message):
    global USERid_MODE
    try:
        if message.chat.type != 'private':
            return
        if message.text == 'Верните назад!':
            welcome(message)
            return
        if not USERid_MODE[message.chat.id][0]:
            if message.text == '#2':
                USERid_MODE[message.chat.id][0] = '#2'
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                items = [
                    'Частицы',
                    'Местоимения',
                    'Хочу все и сразу!',
                    'Верните назад!'
                ]
                for item in items:
                    markup.add(item)
                bot.send_message(message.chat.id, 'Круто, выбери тему из списка ниже:', reply_markup=markup)
            elif message.text == '#7':
                USERid_MODE[message.chat.id][0] = '#7'
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                items = [
                    'Множественное число',
                    'Склонение числительных',
                    'Хочу все и сразу!',
                    'Верните назад!'
                ]
                for item in items:
                    markup.add(item)
                bot.send_message(message.chat.id, 'Круто, выбери тему из списка ниже:', reply_markup=markup)
            elif message.text == '#14':
                USERid_MODE[message.chat.id][0] = '#14'
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                items = [
                    'Хочу все и сразу!',
                    'Верните назад!'
                ]
                for item in items:
                    markup.add(item)
                bot.send_message(message.chat.id, 'Круто, выбери тему из списка ниже:', reply_markup=markup)
            else:
                bot.send_message(message.chat.id, 'I don\'t understand you...')
        elif USERid_MODE[message.chat.id][0] == '#2':
            if message.text == 'Частицы':
                TASK_2.get_task(message.chat.id, 'particles')
            elif message.text == 'Местоимения':
                bot.send_message(message.chat.id, 'Этот режим еще в разработке :)')
            elif message.text == 'Хочу все и сразу!':
                bot.send_message(message.chat.id, 'Этот режим еще в разработке :)')
        elif USERid_MODE[message.chat.id][0] == '#7':
            if message.text == 'Множественное число':
                TASK_7.get_task(message.chat.id, 'plural')
            elif message.text == 'Склонение числительных':
                TASK_7.get_task(message.chat.id, 'numerals')
            elif message.text == 'Хочу все и сразу!':
                TASK_7.get_task(message.chat.id, 'all')
            else:
                bot.send_message(message.chat.id, 'I don\'t understand you...')
        elif USERid_MODE[message.chat.id][0] == '#14':
            if message.text == 'Хочу все и сразу!':
                TASK_14.get_task(message.chat.id, 'all')
            else:
                bot.send_message(message.chat.id, 'I don\'t understand you...')
        else:
            bot.send_message(message.chat.id, 'I don\'t understand you...')
    except Exception as e:
        print(repr(e))
        welcome(message)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global USERid_ANSWER, USERid_MODE
    try:
        if call.message:
            if call.data == 'ready':
                bot.send_message(call.message.chat.id, 'Супер, а теперь проверь себя по списку ниже:')
                answer = ''
                for i in USERid_ANSWER[call.message.chat.id]:
                    answer += i + '\n'
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton('Дальше', callback_data='next'))
                bot.send_message(call.message.chat.id, answer, reply_markup=markup)
            elif call.data == 'next':
                if USERid_MODE[call.message.chat.id][0] == '#2':
                    TASK_2.get_task(call.message.chat.id, USERid_MODE[call.message.chat.id][1])
            elif call.data == USERid_ANSWER[call.message.chat.id]:
                bot.edit_message_text(
                    chat_id=call.message.chat.id, message_id=call.message.message_id,
                    text=call.message.text, reply_markup=None
                )
                sti = open('stickers/animated_text/yes.tgs', 'rb')
                bot.send_sticker(call.message.chat.id, sti)
                bot.send_message(
                    call.message.chat.id,
                    '✅ Cool! Правильный ответ: ' + USERid_ANSWER[call.message.chat.id]
                )

                if USERid_MODE[call.message.chat.id][0] == '#7':
                    TASK_7.get_task(call.message.chat.id, USERid_MODE[call.message.chat.id][1])
                elif USERid_MODE[call.message.chat.id][0] == '#14':
                    TASK_14.get_task(call.message.chat.id, USERid_MODE[call.message.chat.id][1])

            elif call.data != USERid_ANSWER[call.message.chat.id]:
                bot.edit_message_text(
                    chat_id=call.message.chat.id, message_id=call.message.message_id,
                    text=call.message.text, reply_markup=None
                )
                sti = open('stickers/animated_text/no.tgs', 'rb')
                bot.send_sticker(call.message.chat.id, sti)
                bot.send_message(
                    call.message.chat.id,
                    '❌ Oh... Твой ответ был: ' + call.data +
                    '\nА правильно: <b>' + USERid_ANSWER[call.message.chat.id] + '</b>',
                    parse_mode='html'
                )

                if USERid_MODE[call.message.chat.id][0] == '#7':
                    TASK_7.get_task(call.message.chat.id, USERid_MODE[call.message.chat.id][1])
                elif USERid_MODE[call.message.chat.id][0] == '#14':
                    TASK_14.get_task(call.message.chat.id, USERid_MODE[call.message.chat.id][1])
    except Exception as e:
        print(repr(e))
        welcome(call.message)


class Task2:
    def __init__(self):
        # self.particles = [['type', '*particles']]
        self.particles = [
            ['ВОПРОС', 'ЛИ', 'РАЗВЕ', 'НЕУЖЕЛИ'],
            ['ВОСКЛИЦАНИЕ', 'ЧТО ЗА', 'КАК'],
            ['УКАЗАНИЕ', 'ВОТ (А ВОТ)', 'ВОН (А ВОН)'],
            ['СОМНЕНИЕ', 'ВРЯД ЛИ', 'ЕДВА ЛИ'],
            ['УТОЧНЕНИЕ', 'ИМЕННО', 'КАК РАЗ'],
            ['ВЫДЕЛЕНИЕ, ОГРАНИЧЕНИЕ', 'ТОЛЬКО', 'ЛИШЬ', 'ИСКЛЮЧИТЕЛЬНО', 'ПОЧТИ'],
            ['УСИЛЕНИЕ', 'ДАЖЕ', 'ЖЕ', 'НИ', 'ВЕДЬ', 'УЖ', 'ВСЁ-ТАКИ', 'НУ', 'И'],
            ['СМЯГЧЕНИЕ', '-КА']
        ]
        # self.pronouns = [['type', '*pronouns']]
        # TODO: self.pronouns = []

    def get_task(self, chat_id, mode):
        global USERid_MODE
        if mode == 'particles':
            question = self.get_particles(chat_id)
        elif mode == 'pronouns':
            # TODO: self.get_pronouns()
            bot.send_message(chat_id, 'Этот режим еще в разработке :)')
            return
        elif mode == 'all':
            # TODO: self.get_all()
            bot.send_message(chat_id, 'Этот режим еще в разработке :)')
            return
        else:
            return "No such type recognized!" + mode
        USERid_MODE[chat_id][1] = mode

        question = 'Напиши все частицы со значением: <b>' + question + \
                   '</b>\n\nПосле чего нажми на кнопку ниже\n(P.s. формат не важен)'
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Я всё!', callback_data='ready'))
        bot.send_message(chat_id, question, parse_mode='html', reply_markup=markup)

    def get_particles(self, chat_id):
        global USERid_ANSWER

        question_id = random.randint(0, len(self.particles) - 1)
        question = self.particles[question_id][0]

        USERid_ANSWER[chat_id] = self.particles[question_id][1:]
        return question


class Task7:
    def __init__(self):
        self.plural = load_data('data/task7_plural.txt')  # [['question', 'right_answer', 'false_answer']]
        # TODO: self.numerals
        # TODO: self.verbs

    def get_task(self, chat_id, mode):
        global USERid_MODE
        if mode == 'plural':
            question, items = self.get_plural(chat_id)
        elif mode == 'numerals':
            # TODO: self.get_numerals()
            bot.send_message(chat_id, 'Этот режим еще в разработке :)')
            return
        elif mode == 'verbs':
            # TODO: self.get_verbs()
            bot.send_message(chat_id, 'Этот режим еще в разработке :)')
            return
        elif mode == 'all':
            # TODO: self.get_all()
            bot.send_message(chat_id, 'Этот режим еще в разработке :)')
            return
        else:
            return "No such type recognized!" + mode
        USERid_MODE[chat_id][1] = mode
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton(items[0], callback_data=items[0]),
            types.InlineKeyboardButton(items[1], callback_data=items[1]),
        )
        bot.send_message(chat_id, question, reply_markup=markup)

    def get_plural(self, chat_id):
        global USERid_ANSWER

        question_id = random.randint(0, len(self.plural))
        question = self.plural[question_id][0]
        rand = random.randint(1, 2)
        items = [self.plural[question_id][rand], self.plural[question_id][3 - rand]]

        USERid_ANSWER[chat_id] = self.plural[question_id][1]
        return question, items


class Task14:
    def __init__(self):
        self.words = load_data('data/task14.txt', '|')

    def get_task(self, chat_id, mode):
        if mode == 'all':
            question, items = self.get_all(chat_id)
        else:
            return "No such type recognized!" + mode
        USERid_MODE[chat_id][1] = mode
        markup = types.InlineKeyboardMarkup()
        for item in items:
            markup.add(types.InlineKeyboardButton(item, callback_data=item))
        bot.send_message(chat_id, question, reply_markup=markup)

    def get_all(self, chat_id):
        global USERid_ANSWER
        word_id = random.randint(0, len(self.words) - 1)
        temp = self.words[word_id][0].split(' ')
        question = '(' + temp[0] + ')' + temp[1]
        tail = ''
        t = 10
        for i in range(2, len(temp)):
            tail += ' ' + temp[i]
            if '(' in temp[i]:
                t = i
        question += tail

        items = [
            temp[0] + ' ' + temp[1] + tail[:t - 1],
            temp[0] + temp[1] + tail[:t - 1],
            temp[0] + '-' + temp[1] + tail[:t - 1]
        ]
        for i in range(len(items)):
            items[i] = items[i].strip()

        USERid_ANSWER[chat_id] = self.words[word_id][1][:len(self.words[word_id][1])]
        return question, items


def load_data(way, split_char=' '):
    with open(way, encoding='utf-8') as file:
        data = []
        for line in file.readlines():
            data.append(line.split(split_char))
            data[-1][-1] = data[-1][-1].replace('\n', '')
        return data


USERid_ANSWER = {}  # {user_id: 'answer'}
USERid_MODE = {}  # {user_id: ['main mode', 'submode']}

# Run
if __name__ == "__main__":
    TASK_2 = Task2()
    TASK_7 = Task7()
    TASK_14 = Task14()
    bot.polling(none_stop=True)
