import sqlite3
import telebot
from telebot import types
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

bot = telebot.TeleBot("token")

options = Options()
options.headless = True


@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(row_width=3)
    itembtn1 = types.KeyboardButton('Поиск по названию')
    itembtn2 = types.KeyboardButton('Поиск по описанию')
    itembtn3 = types.KeyboardButton('Случайный')
    markup.add(itembtn1, itembtn2, itembtn3)
    bot.send_message(chat_id, "Что найти?", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    s = ''
    if message.text == 'Поиск по названию':
        s = "название"
        chat_id = message.chat.id
        bot.send_message(chat_id, "Введите название:")
    elif message.text == 'Поиск по описанию':
        s = "описание"
        chat_id = message.chat.id
        bot.send_message(chat_id, "Введите описание:")
    elif message.text == 'Случайный':
        chat_id = message.chat.id
        bot.send_message(chat_id, "Обрабатываю запрос...")

        db = sqlite3.connect('Triangle_Kino.db')
        cur = db.cursor()

        for rand in cur.execute('SELECT * FROM Triangle_Kino WHERE ID IN (SELECT ID FROM Triangle_Kino ORDER BY RANDOM() LIMIT 1)'):
            print(rand)
            name = rand[2]
            god = rand[3]
            description = rand[4]
            link1 = rand[5]

            q = open("text.txt", "w")
            q.write(str(name) + '\n')
            q.write(str(god) + '\n\n')
            q.write(str(description) + '\n\n')
            q.write(str(link1))
            q.close()

            msg = open("text.txt", "r").read()
            chat_id = message.chat.id
            bot.send_message(chat_id, msg)
    else:
        chat_id = message.chat.id
        bot.send_message(chat_id, "Обрабатываю запрос...")

        db = sqlite3.connect('Triangle_Kino.db')
        cur = db.cursor()

        word = message.text
        r = open("text.txt", "r")
        readR = r.read()

        if readR == "название":
            driver = webdriver.Firefox(options=options)

            name_list = []
            opisanie_list = []
            god_list = []
            Link1_list = []
            Link2_list = []

            for name in cur.execute('SELECT NAME FROM Triangle_Kino WHERE NAME LIKE ?', ('%' + word + '%',)):
                name_list.append(name[0])

            for description in cur.execute('SELECT OPISANIE FROM Triangle_Kino WHERE NAME LIKE ?', ('%' + word + '%',)):
                opisanie_list.append(description[0])

            for god in cur.execute('SELECT GOD FROM Triangle_Kino WHERE NAME LIKE ?', ('%' + word + '%',)):
                god_list.append(god[0])

            for Link1 in cur.execute('SELECT LINK_STR FROM Triangle_Kino WHERE NAME LIKE ?', ('%' + word + '%',)):
                Link1_list.append(Link1[0])

            for film in Link1_list:
                try:
                    driver.get(film)
                    time.sleep(2)
                    driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
                    element2 = driver.find_element(By.XPATH, """/html/body/div/pjsdiv/pjsdiv[1]/video""")

                    itog = str(element2.get_attribute('src'))
                    a1 = itog.split('/240.mp4')
                    a2 = str(a1[0]) + "/720.mp4"
                    print(a2)

                    Link2_list.append(a2)

                except:
                    print("Ошибка")

                    Link2_list.append("Ошибка")

            driver.quit()

            i = 0
            while i < len(name_list):
                q = open("text.txt", "w")
                q.write(str(name_list[i]))
                q.write('\n')
                q.write(str(god_list[i]))
                q.write('\n')
                q.write('\n')
                q.write(str(opisanie_list[i]))
                q.write('\n')
                q.write('\n')
                q.write(str(Link1_list[i]))
                q.write('\n')
                q.write('\n')
                q.write(str(Link2_list[i]))
                q.close()

                msg = open("text.txt", "r")
                msgR = msg.read()
                chat_id = message.chat.id
                bot.send_message(chat_id, msgR)
                time.sleep(1)
                i = i + 1

        elif readR == "описание":

            driver = webdriver.Firefox(options=options)
            z = open('text.txt', 'w')
            z.seek(0)
            z.close()
            name_list = []
            opisanie_list = []
            god_list = []
            Link1_list = []
            Link2_list = []
            for name in cur.execute('SELECT NAME FROM Triangle_Kino WHERE OPISANIE LIKE ?', ('%' + word + '%',)):
                print(name)
                name_list.append(name[0])

            for description in cur.execute('SELECT OPISANIE FROM Triangle_Kino WHERE OPISANIE LIKE ?', ('%' + word + '%',)):
                print(description)
                opisanie_list.append(description[0])

            for god in cur.execute('SELECT GOD FROM Triangle_Kino WHERE OPISANIE LIKE ?', ('%' + word + '%',)):
                print(god)
                god_list.append(god[0])

            for Link1 in cur.execute('SELECT LINK_STR FROM Triangle_Kino WHERE OPISANIE LIKE ?', ('%' + word + '%',)):
                print(Link1)
                Link1_list.append(Link1[0])

            for film in Link1_list:

                try:
                    driver.get(film)
                    time.sleep(2)

                    driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
                    element2 = driver.find_element(By.XPATH, """/html/body/div/pjsdiv/pjsdiv[1]/video""")

                    print(element2.get_attribute('src'))

                    itog = str(element2.get_attribute('src'))

                    a1 = itog.split('/240.mp4')
                    a2 = str(a1[0]) + "/720.mp4"
                    print(a2)

                    Link2_list.append(a2)

                except:

                    print("Ошибка")

                    Link2_list.append("Ошибка")

            i = 0
            driver.quit()
            while i < len(name_list):
                q = open("text.txt", "w")
                q.write(str(name_list[i]))
                q.write('\n')
                q.write(str(god_list[i]))
                q.write('\n')
                q.write('\n')
                q.write(str(opisanie_list[i]))
                q.write('\n')
                q.write('\n')
                q.write(str(Link1_list[i]))
                q.write('\n')
                q.write('\n')
                q.write(str(Link2_list[i]))
                q.close()

                msg = open("text.txt", "r")
                msgR = msg.read()
                chat_id = message.chat.id
                bot.send_message(chat_id, msgR)
                time.sleep(1)
                i = i + 1


bot.polling()
