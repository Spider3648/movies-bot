import sqlite3
import telebot
from telebot import types
import time
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

bot = telebot.TeleBot(os.environ["APITOKEN"])

options = Options()
options.headless = True

#Функція для вибору випадкового фільму в базі даних
def get_random_movie(cur):
    for rand in cur.execute('SELECT * FROM Kino WHERE ID IN (SELECT ID FROM Kino ORDER BY RANDOM() LIMIT 1)'):
        name = rand[1]
        god = rand[2]
        description = rand[3]
        link1 = rand[4]  

        with open("text.txt", "w", encoding='cp1251') as f:
            f.write(str(name) + '\n')
            f.write(str(god) + '\n\n')
            f.write(str(description) + '\n\n')
            f.write(str(link1))

        msg = open("text.txt", "r", encoding='cp1251').read()
        return msg

#Функція для вибору випадкового серіалу в базі даних
def get_random_series(cur):
    for rand in cur.execute('SELECT * FROM Series WHERE ID IN (SELECT ID FROM Series ORDER BY RANDOM() LIMIT 1)'):
        name = rand[1]
        god = rand[2]
        description = rand[3]
        link1 = rand[4] 

        with open("text.txt", "w", encoding='cp1251') as f:
            f.write(str(name) + '\n')
            f.write(str(god) + '\n\n')
            f.write(str(description) + '\n\n')
            f.write(str(link1))

        msg = open("text.txt", "r", encoding='cp1251').read()
        return msg
    
#Функція для вибору випадкового фільму в базі даних
def get_movie_details(cur, word, search_by):
    if search_by == 'name':
        query = 'SELECT NAME, GOD, OPISANIE, LINK_STR FROM Kino WHERE NAME LIKE ? LIMIT 1'
        rows = cur.execute(query, ('%' + word + '%',))
    elif search_by == 'code':
        query = 'SELECT NAME, GOD, OPISANIE, LINK_STR FROM Kino WHERE ID = ? LIMIT 1'
        rows = cur.execute(query, (word,))
    else:
        query = 'SELECT NAME, GOD, OPISANIE, LINK_STR FROM Kino WHERE OPISANIE LIKE ? LIMIT 1'
        rows = cur.execute(query, ('%' + word + '%',))

    row = rows.fetchone()

    if row is None:
        return "Фільм не знайдено!"

    name, god, opisanie, link1 = row

    with open("text.txt", "w", encoding='cp1251') as f:
        f.write(str(name) + '\n')
        f.write(str(god) + '\n\n')
        f.write(str(opisanie) + '\n\n')
        f.write(str(link1))

    msg = open("text.txt", "r", encoding='cp1251').read()
    return msg

#Функція для вибору випадкового серіалу в базі даних
def get_serie_details(cur, word, search_by):

    if search_by == 'name':
        query = 'SELECT NAME, GOD, OPISANIE, LINK_STR FROM Series WHERE NAME LIKE ? LIMIT 1'
        rows = cur.execute(query, ('%' + word + '%',))
    elif search_by == 'code':
        query = 'SELECT NAME, GOD, OPISANIE, LINK_STR FROM Series WHERE ID = ? LIMIT 1'
        rows = cur.execute(query, (word,))
    else:
        query = 'SELECT NAME, GOD, OPISANIE, LINK_STR FROM Series WHERE OPISANIE LIKE ? LIMIT 1'
        rows = cur.execute(query, ('%' + word + '%',))

    row = rows.fetchone()

    if row is None:
        return "Серіал не знайдено!"

    name, god, opisanie, link1 = row

    with open("text.txt", "w", encoding='cp1251') as f:
        f.write(str(name) + '\n')
        f.write(str(god) + '\n\n')
        f.write(str(opisanie) + '\n\n')
        f.write(str(link1))

    msg = open("text.txt", "r", encoding='cp1251').read()
    return msg

#Функція для вибору типу пошуку
def handle_movie_search(message):
    chat_id = message.chat.id
    if message.text == 'Пошук фільму за кодом':
        bot.send_message(chat_id, "Введіть код:")
        bot.register_next_step_handler(message, search_movies, search_by='code')
    elif message.text == 'Пошук серіалу за кодом':
        bot.send_message(chat_id, "Введіть код:")
        bot.register_next_step_handler(message, search_series, search_by='code')
    elif message.text == 'Пошук фільму за назвою':
        bot.send_message(chat_id, "Введіть назву:")
        bot.register_next_step_handler(message, search_movies, search_by='name')
    elif message.text == 'Пошук серіалу за назвою':
        bot.send_message(chat_id, "Введіть назву:")
        bot.register_next_step_handler(message, search_series, search_by='name')
    elif message.text == 'Пошук фільму за описом':
        bot.send_message(chat_id, "Введіть опис:")
        bot.register_next_step_handler(message, search_movies, search_by='description')
    elif message.text == 'Пошук серіалу за описом':
        bot.send_message(chat_id, "Введіть опис:")
        bot.register_next_step_handler(message, search_series, search_by='description')

#Загальна функція для пошуку фільмів
def search_movies(message, search_by):
    chat_id = message.chat.id
    word = message.text
    db = sqlite3.connect('Kino.db')
    cur = db.cursor()
    if search_by == 'name' or search_by == 'description' or search_by == 'code':
        bot.send_message(chat_id, "Обробляю запит...")
        movie_details = get_movie_details(cur, word, search_by)
        bot.send_message(chat_id, movie_details)

    else:
        bot.send_message(chat_id, "Невірний запит. Спробуйте ще раз.")
    db.close()

#Загальна функція для пошуку серіалів
def search_series(message, search_by):
    chat_id = message.chat.id
    word = message.text
    db = sqlite3.connect('Series.db')
    cur = db.cursor()
    if search_by == 'name' or search_by == 'description' or search_by == 'code':
        bot.send_message(chat_id, "Обробляю запит...")
        movie_details = get_serie_details(cur, word, search_by)
        bot.send_message(chat_id, movie_details)
    else:
        bot.send_message(chat_id, "Невірний запит. Спробуйте ще раз.")
    db.close()

#Функція для встановлення кнопок та вітального повідомлення
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Пошук фільму за кодом')
    itembtn2 = types.KeyboardButton('Пошук серіалу за кодом')
    itembtn3 = types.KeyboardButton('Пошук фільму за назвою')
    itembtn4 = types.KeyboardButton('Пошук серіалу за назвою')
    itembtn5 = types.KeyboardButton('Пошук фільму за описом')
    itembtn6 = types.KeyboardButton('Пошук серіалу за описом')
    itembtn7 = types.KeyboardButton('Випадковий фільм')
    itembtn8 = types.KeyboardButton('Випадковий серіал')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7, itembtn8)
    bot.send_message(chat_id, "Вітаю. Цей бот допоможе вам знайти ваші улюблені фільми та серіали. Що вам знайти?", reply_markup=markup)

#Функція для обробки запитів користувача
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    chat_id = message.chat.id
    if message.text in ['Пошук фільму за кодом', 'Пошук серіалу за кодом', 'Пошук фільму за назвою', 'Пошук серіалу за назвою', 'Пошук фільму за описом', 'Пошук серіалу за описом']:
        handle_movie_search(message)
    elif message.text == 'Випадковий фільм':
        bot.send_message(chat_id, "Обробляю запит...")
        db = sqlite3.connect('Kino.db')
        cur = db.cursor()
        random_movie = get_random_movie(cur)
        bot.send_message(chat_id, random_movie)
        db.close()
    elif message.text == 'Випадковий серіал':
        bot.send_message(chat_id, "Обробляю запит...")
        db = sqlite3.connect('Series.db')
        cur = db.cursor()
        random_movie = get_random_series(cur)
        bot.send_message(chat_id, random_movie)
        db.close()

bot.polling()