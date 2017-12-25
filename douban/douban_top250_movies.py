#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
import requests
import asyncio
from bs4 import BeautifulSoup


base_url = 'https://movie.douban.com/top250'
headers = {
    'Host': 'movie.douban.com',
    'User_Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
}

session = requests.session()


def my_print(movie_list):
    columns = ['电影排名: ', '电影名称: ', '电影评分: ', '评分人数: ', '电影简评: ']
    for movie in movie_list:
        for k, v in enumerate(movie):
            print(columns[k], v)
        print('*' * 50)


def save_as_text(movie_list):
    columns = ['电影排名: ', '电影名称: ', '电影评分: ', '评分人数: ', '电影简评: ']
    with open('douban_top250_movies.txt', 'w') as f:
        for movie in movie_list:
            for k, v in enumerate(movie):
                f.write(columns[k] + v + '\n')
            f.write('*' * 50 + '\n')


def get_movie_info(session, url):
    try:
        resp = session.get(url, headers=headers)
    except Exception as e:
        print('request exception', e)

    soup = BeautifulSoup(resp.content, 'html.parser')
    return soup


def parser_soup(soup):
    info_list = []
    movie_list = soup.find(class_='grid_view').find_all('li')
    for movie in movie_list:
        rank = movie.find('em').string
        name = movie.find(class_='info').find(class_='title').string
        score = movie.find('span', 'rating_num').string
        vote_num = movie.find(class_='bd').find_all('span')[-2].string
        vote_num = re.match(r'[0-9]+', vote_num).group(0)

        comment = ''
        if movie.find(class_='inq'):
            comment = movie.find('span', 'inq').string
        info_list.append((rank, name, score, vote_num, comment))
    return info_list


async def schedule_tasks(session, url):
    soup = get_movie_info(session, url)
    return parser_soup(soup)


if __name__ == '__main__':
    movie = []
    tasks = []
    for i in range(10):
        url = base_url + '?start={}&filter='.format(i * 25)
        # soup = get_movie_info(session, url)
        # movie.extend(parser_soup(soup))
        tasks.append(schedule_tasks(session, url))
    loop = asyncio.get_event_loop()
    done, _ = loop.run_until_complete(asyncio.wait(tasks))
    for task in done:
        movie.extend(task.result())
    my_print(movie)
    save_as_text(movie)
