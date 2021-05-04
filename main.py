# pyTelegramBotAPI needed
import telebot
import config
from random import randint
from telebot import types


# Init bot
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
        types.KeyboardButton('#9'),
        types.KeyboardButton('#10'),
        types.KeyboardButton('#11'),
        types.KeyboardButton('#12'),
        types.KeyboardButton('#13'),
        types.KeyboardButton('#14'),
        types.KeyboardButton('#15')
    ]
    markup.add(items[0], items[1], items[2])
    markup.add(items[3], items[4], items[5])
    markup.add(items[6], items[7], items[8])

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
            if message.text in ['#2', '#7', '#9', '#14']:
                go2task_main_menu(message.chat.id, message.text)
            elif message.text in ['#1', '#3', '#4', '#5', '#6', '#8', '#10', '#11', '#12', '#13', '#15', '#16', '#17', '#18', '#19', '#20', '#21', '#22', '#23', '#24', '#25', '#26', '#27']:
                bot.send_message(message.chat.id, 'Этот режим еще в разработке :)')
            else:
                bot.send_message(message.chat.id, 'I don\'t understand you...')
        elif USERid_MODE[message.chat.id][0] in ['#2', '#7', '#9', '#14']:
            choose_mode(message.chat.id, USERid_MODE[message.chat.id][0], message.text)
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
                elif USERid_MODE[call.message.chat.id][0] == '#9':
                    TASK_9.get_task(call.message.chat.id, USERid_MODE[call.message.chat.id][1])
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


# Send task main menu and set mode
def go2task_main_menu(chat_id, task_num):
    unique_menu_options = {
        '#2': ['Частицы', 'Местоимения'],
        '#7': ['Множественное число', 'Склонение числительных', 'Глагольные формы'],
        '#9': ['Слово - тип']
    }
    items = []
    if task_num in unique_menu_options.keys():
        for item in unique_menu_options[task_num]:
            items.append(item)
    if task_num in ['#2', '#7', '#14']:
        items.append('Хочу все и сразу!')
    items.append('Верните назад!')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for item in items:
        markup.add(item)

    USERid_MODE[chat_id][0] = task_num

    bot.send_message(chat_id, 'Круто, выбери тему из списка ниже:', reply_markup=markup)


def choose_mode(chat_id, task_num, task_mode):
    modes = {
        '#2': {
            'Частицы': 'particles',
            'Местоимения': 'pronouns',
            'Хочу все и сразу!': 'all'
        },
        '#7': {
            'Множественное число': 'plural',
            'Склонение числительных': 'numerals',
            'Глагольные формы': 'verbs',
            'Хочу все и сразу!': 'all'
        },
        '#9': {
            'Слово - тип': 'word_type'
        },
        '#14': {
            'Хочу все и сразу!': 'all'
        }
    }
    if task_mode in modes[task_num].keys():
        if task_num == '#2':
            TASK_2.get_task(chat_id, modes[task_num][task_mode])
        elif task_num == '#7':
            TASK_7.get_task(chat_id, modes[task_num][task_mode])
        elif task_num == '#9':
            TASK_9.get_task(chat_id, modes[task_num][task_mode])
        elif task_num == '#14':
            TASK_14.get_task(chat_id, modes[task_num][task_mode])
    else:
        bot.send_message(chat_id, 'I don\'t understand you...')


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

        question_id = randint(0, len(self.particles) - 1)
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

        question_id = randint(0, len(self.plural))
        question = self.plural[question_id][0]
        rand = randint(1, 2)
        items = [self.plural[question_id][rand], self.plural[question_id][3 - rand]]

        USERid_ANSWER[chat_id] = self.plural[question_id][1]
        return question, items


class Task9:
    def __init__(self):
        # TODO: class Task9
        self.check = load_data('data/task9_check.txt', ' ')
        self.dict = load_data('data/task9_dict.txt', ' ')
        self.alternation = load_data('data/task9_alternation.txt', ' ')

    def get_task(self, chat_id, mode):
        if mode == 'word_type':
            question, items = self.get_word_type(chat_id)
        else:
            return "No such type recognized!" + mode
        USERid_MODE[chat_id][1] = mode
        markup = types.InlineKeyboardMarkup()
        for item in items:
            markup.add(types.InlineKeyboardButton(item, callback_data=item))
        bot.send_message(chat_id, question, reply_markup=markup)

    def get_word_type(self, chat_id):
        global USERid_ANSWER
        type = randint(0, 2)
        if type == 0:
            word_id = randint(0, len(self.check) - 1)
            question = self.check[word_id]
        elif type == 1:
            word_id = randint(0, len(self.dict) - 1)
            question = self.dict[word_id]
        elif type == 2:
            word_id = randint(0, len(self.alternation) - 1)
            question = self.alternation[word_id]

        items = ['Проверяем', 'Не проверяем', 'Чередуем']

        USERid_ANSWER[chat_id] = items[type]
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
        word_id = randint(0, len(self.words) - 1)
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


# Run
if __name__ == "__main__":
    TASK_2 = Task2()
    TASK_7 = Task7()
    TASK_9 = Task9()
    TASK_14 = Task14()

    USERid_ANSWER = {}  # {user_id: 'answer'}
    USERid_MODE = {}  # {user_id: ['main mode', 'submode']}

    bot.polling(none_stop=True)
