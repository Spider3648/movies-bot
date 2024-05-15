import requests
from bs4 import BeautifulSoup
import sqlite3
import re

# Підключення до бази даних
conn = sqlite3.connect('Kino.db')
c = conn.cursor()

# Створення таблиці (якщо вона не існує)


# Базова URL-адреса для фільмів
base_url = "https://uaserials.pro/films/page/"

# Функція для отримання даних про фільми зі сторінки
def get_movies_from_page(page_url):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text()
    movies = []
    for movie_div in soup.select('.short-item'):
        title = movie_div.select_one('.th-title').text.strip()
        
        movie_url = movie_div.select_one('.short-img')['href']
        responsemovie = requests.get(movie_url)
        movsoup = BeautifulSoup(responsemovie.text, 'html.parser')

        movie_details = movsoup.select_one('.fcols')
        if movie_details:
            year_element = movie_details.select_one('ul.short-list li:has(> span:contains("Рік:")) a')
            if year_element:
                year = year_element.text.strip()
            else:
                year = ''

        description_element = movsoup.select_one('.ftext')
        if description_element:
            description = description_element.get_text(strip=True)
        else:
            description = ''    
        movies.append({'title': title, 'year': year, 'description': description, 'link': movie_url})
    return movies

# Цикл для обходу кількох сторінок
for page_num in range(1, 6):
    page_url = base_url + str(page_num) + "/"
    movies = get_movies_from_page(page_url)
    for movie in movies:
        c.execute("INSERT INTO Kino (name, god, OPISANIE, LINK_STR) VALUES (?, ?, ?, ?)",
                  (movie['title'], movie['year'], movie['description'], movie['link']))
    conn.commit()

# Закриття з'єднання з базою даних
conn.close()