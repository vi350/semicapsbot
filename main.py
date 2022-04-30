import telebot
from telebot import types
from datetime import datetime
import logging
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)


def logq(inline_query, answer):
    print('----------')
    print(datetime.now())
    tolog = "{0} {1}, {2}, {3}\n{4}\n{5}".format(
        inline_query.from_user.first_name,
        inline_query.from_user.last_name,
        inline_query.from_user.username,
        inline_query.from_user.id,
        inline_query.query,
        answer)
    print(tolog)
    tolog = '\n=============\n' + tolog + '\n============='
    logging.info(tolog)


@bot.message_handler(commands=['start'])
def handle_text(message):
    answer = "welcum!"
    bot.send_message(message.from_user.id, answer)
    logq(message, answer)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    answer = 'placeholder'
    '''
    wascapsed = False
    for letter in list(message.text):
        if letter.isalpha():
            if not wascapsed:
                answer += letter.upper()
                wascapsed = True
            else:
                answer += letter.lower()
                wascapsed = False
        else:
            answer += letter
    '''
    bot.send_message(message.chat.id, answer)
    logq(message, answer)


@bot.inline_handler(lambda query: len(query.query) != 0)
def query_text(inline_query):
    answer = ''
    second_answer = ''
    wascapsed = False
    for letter in list(inline_query.query):
        if letter.isalpha():
            if not wascapsed:
                answer += letter.upper()
                second_answer += letter.lower()
                wascapsed = True
            else:
                answer += letter.lower()
                second_answer += letter.upper()
                wascapsed = False
        else:
            answer += letter
            second_answer += letter
    r0 = types.InlineQueryResultArticle('0', answer, types.InputTextMessageContent(answer))
    r1 = types.InlineQueryResultArticle('1', second_answer, types.InputTextMessageContent(second_answer))
    logq(inline_query, answer)
    bot.answer_inline_query(inline_query.id, [r0, r1])


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s  %(message)s',
                        level=logging.INFO, filename='logs/info ' + str(datetime.now())[:-7] + '.txt')
    logging.info("Get me:\n" + str(bot.get_me()) + "\n=========")
    print("Get me:\n", bot.get_me(), "\n==========")
    bot.polling(none_stop=True)
