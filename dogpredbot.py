import telebot
from telebot import types
from prediction import dog_prediction
 
bot = telebot.TeleBot('6873454657:AAGaDQmn_sA5FpjUTW89hLvyqGdgUAIvP2E')
but1 = types.InlineKeyboardButton('1', callback_data=1)
but2 = types.InlineKeyboardButton('2', callback_data=2)
but3 = types.InlineKeyboardButton('3', callback_data=3)
but4 = types.InlineKeyboardButton('4', callback_data=4)
but5 = types.InlineKeyboardButton('5', callback_data=5)
but6 = types.InlineKeyboardButton('6', callback_data=6)
but7 = types.InlineKeyboardButton('7', callback_data=7)
but8 = types.InlineKeyboardButton('8', callback_data=8)
but9 = types.InlineKeyboardButton('9', callback_data=9)
but10 = types.InlineKeyboardButton('10', callback_data=10)
markup = types.InlineKeyboardMarkup()
markup.row(but1, but2, but3, but4, but5)
markup.row(but6, but7, but8, but9, but10)

questions_file = 'questions.txt'
with open(questions_file, 'r', encoding='utf-8') as file:
    questions = file.readlines()
    questions = [question.strip() for question in questions]

current_question_index = 0
answers = []


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    but11 = types.KeyboardButton('Подбор породы')
    but12 = types.KeyboardButton('Информация')
    markup.row(but11, but12)
    bot.send_message(message.chat.id, "Привет, ну что, готов подобрать себе идеальную породу?", reply_markup=markup)


@bot.message_handler()
def main(message):
    global current_question_index
    if message.text.lower() == 'подбор породы':
        current_question_index = 0
        send_next_question(message.chat.id)
    elif message.text.lower() == 'информация':
        bot.send_message(message.chat.id,
                         'Добро пожаловать в бота, который поможет определить идеальную породу собаки исходя из ваших предпочтений и оценок!')


def send_next_question(chat_id):
    global current_question_index
    if current_question_index < len(questions):
        bot.send_message(chat_id, questions[current_question_index], reply_markup=markup)
        current_question_index += 1


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    global answers
    if callback.data in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']:
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        answers.append(int(callback.data))
        send_next_question(callback.message.chat.id)
    print(answers)
    if len(answers) == len(questions):
        prediction_result = dog_prediction(answers)
        bot.send_message(callback.message.chat.id, f'Для вас идеально подойдет порода - {prediction_result}')
        answers.clear()

bot.polling(none_stop=True)
