from get_chances import main
from collections import deque
import json
from flask import Flask
from flask import request
from time import sleep
import requests
import random
from flask_cors import CORS
import sqlite3
import sys

app = Flask(__name__)
CORS(app)

lis = []
TOKEN = 'JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTgwNDcyOCwiaWF0IjoxNjQwNDAyNDUxLCJleHAiOjE2NDEyNjY0NTF9.7qhmil3o2JUTfyxajUqkBrmZsA6ZvQpz3mLEZPrPkcI'

deq = deque()

bet = 10.0
dict1 = {'0.25': 219, '0.5': 3978, '0.84': 363, '2.0': 5371, '1.0': 11795, '3.0': 11797, '4.0': 771, '5.0': 3486,
         '10.0': 11671}


def make_bet(items_id, auto='1.01'):
    if (items_id is None):
        exchange()
        return
    # print('12345678')
    # return
    i = 0
    response = False
    while not response:
        i += 1
        sleep(1 + random.random())
        response = requests.post('https://api.csgorun.gg/make-bet',
                                 json={'userItemIds': [i for i in items_id], 'auto': auto},
                                 headers={'accept': 'application/json, text/plain, */*',
                                          'accept-encoding': 'gzip, deflate, br',
                                          'accept-language': 'ru,en;q=0.9',
                                          'authorization': TOKEN,
                                          'content-length': '22',
                                          'content-type': 'application/json;charset=UTF-8',
                                          'origin': 'https://csgorun.gg',
                                          'referer': 'https://csgorun.gg/',
                                          'sec-ch-ua': '"Yandex";v="21", " Not;A Brand";v="99", "Chromium";v="93"',
                                          'sec-ch-ua-mobile': '?0',
                                          'sec-ch-ua-platform': '"Windows"',
                                          'sec-fetch-dest': 'empty',
                                          'sec-fetch-mode': 'cors',
                                          'sec-fetch-site': 'same-site',
                                          'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 YaBrowser/21.9.0.1044 Yowser/2.5 Safari/537.36'})
        if i > 4:
            return response

    response.close()


def taktic4(lis: list):
    lis = [i[0] for i in lis]
    if lis[-1] > 1.2 and lis[-2] < 1.2 and lis[-3] < 1.2 and lis[-4] < 1.2:
        return True


def taktic5(lis: list):
    lis = [i[0] for i in lis]
    if lis[-1] < 1.2 and lis[-2] < 1.2 and lis[-3] < 1.2 and lis[-4] < 1.2:
        return True


class Weapon:
    def __init__(self, dict1):
        self.price = dict1['price']
        self.id = dict1['id']

    def get_price(self):
        return self.price

    def get_id(self):
        return self.id


class Inventory:
    def set_balance(self, x):
        self.balance = x
        for i in range(int(self.balance / bet)):
            sleep(0.2)
            res = requests.post('https://api.csgorun.gg/marketplace/exchange-items',
                                headers={'accept': 'application/json, text/plain, */*',
                                         'accept-encoding': 'gzip, deflate, br',
                                         'accept-language': 'ru,en;q=0.9',
                                         'authorization': TOKEN,
                                         'content-length': '22',
                                         'content-type': 'application/json;charset=UTF-8',
                                         'origin': 'https://csgorun.gg',
                                         'referer': 'https://csgorun.gg/',
                                         'sec-ch-ua': '"Yandex";v="21", " Not;A Brand";v="99", "Chromium";v="93"',
                                         'sec-ch-ua-mobile': '?0',
                                         'sec-ch-ua-platform': '"Windows"',
                                         'sec-fetch-dest': 'empty',
                                         'sec-fetch-mode': 'cors',
                                         'sec-fetch-site': 'same-site',
                                         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 YaBrowser/21.9.0.1044 Yowser/2.5 Safari/537.36'},
                                json={'userItemIds': [],
                                      'wishItemIds': [dict1[str(bet)]]})

    def __init__(self):
        global lis
        self.lis = lis

    def update(self, lis, x):
        self.lis.clear()
        self.lis.extend(lis)
        for i in self.lis:
            x += i.get_price()

    def price(self):
        x = 0.0
        for i in self.lis:
            x += i.get_price()
        return x

    def get_smallest(self, k=1):
        if self.lis:
            return [i.get_id() for i in sorted(self.lis, key=lambda x: x.get_price())][:k]
        return None

    def get_more(self, x):
        return [i for i in self.lis if i.get_price() > x]


def exchange(flag=False, flag2=False, x=bet):
    if not flag2:
        res = requests.post('https://api.csgorun.gg/marketplace/exchange-items',
                            headers={'accept': 'application/json, text/plain, */*',
                                     'accept-encoding': 'gzip, deflate, br',
                                     'accept-language': 'ru,en;q=0.9',
                                     'authorization': TOKEN,
                                     'content-length': '22',
                                     'content-type': 'application/json;charset=UTF-8',
                                     'origin': 'https://csgorun.gg',
                                     'referer': 'https://csgorun.gg/',
                                     'sec-ch-ua': '"Yandex";v="21", " Not;A Brand";v="99", "Chromium";v="93"',
                                     'sec-ch-ua-mobile': '?0',
                                     'sec-ch-ua-platform': '"Windows"',
                                     'sec-fetch-dest': 'empty',
                                     'sec-fetch-mode': 'cors',
                                     'sec-fetch-site': 'same-site',
                                     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 YaBrowser/21.9.0.1044 Yowser/2.5 Safari/537.36'},
                            json={'userItemIds': [i.get_id() for i in Inventory().get_more(x)] if not flag else [
                                i.get_id() for i in Inventory().lis], 'wishItemIds': [dict1[str(bet)]]})
    elif (flag2 and len([i.get_id() for i in Inventory().get_more(x)]) >= 1) or len(Inventory().lis) == 0:
        res = requests.post('https://api.csgorun.gg/marketplace/exchange-items',
                            headers={'accept': 'application/json, text/plain, */*',
                                     'accept-encoding': 'gzip, deflate, br',
                                     'accept-language': 'ru,en;q=0.9',
                                     'authorization': TOKEN,
                                     'content-length': '22',
                                     'content-type': 'application/json;charset=UTF-8',
                                     'origin': 'https://csgorun.gg',
                                     'referer': 'https://csgorun.gg/',
                                     'sec-ch-ua': '"Yandex";v="21", " Not;A Brand";v="99", "Chromium";v="93"',
                                     'sec-ch-ua-mobile': '?0',
                                     'sec-ch-ua-platform': '"Windows"',
                                     'sec-fetch-dest': 'empty',
                                     'sec-fetch-mode': 'cors',
                                     'sec-fetch-site': 'same-site',
                                     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 YaBrowser/21.9.0.1044 Yowser/2.5 Safari/537.36'},
                            json={'userItemIds': [i.get_id() for i in Inventory().get_more(x)],
                                  'wishItemIds': [dict1[str(bet)]]})


@app.route('/')
def index():
    return 'Hello World'


@app.route('/get_token', methods=['GET'])
def func1():
    return TOKEN


def get_coef():
    con = sqlite3.connect('db1.db')
    coeff = 3.3
    maxx = coeff, 0, 0
    while coeff < 10:
        coeff += 0.1
        x9 = con.execute('select crash from crashes').fetchall()[-1000:]

        stat = []
        deq = deque()
        for i in x9:
            i = i[0]
            deq.append(i)
            if deq.__len__() >= 6:
                if deq[0] < 1.2 and deq[1] < 1.2 and deq[2] < 1.2:
                    stat.append(deq[3])
                # stat.append(deq[0])
                deq.popleft()
        if stat:
            x = 0
            for i in stat:
                if i >= coeff:
                    x += 1
            if (x / stat.__len__() - 1 / coeff) > 0.08 and x / stat.__len__() > 0.3 and maxx[2] <= (
                    x / stat.__len__() - 1 / coeff):
                maxx = coeff, x / stat.__len__(), x / stat.__len__() - 1 / coeff
    return maxx


# @app.route('/make_bet', methods=['POST'])
def func2(bet='1.2'):
    make_bet(Inventory().get_smallest(), bet)
    return 'ok'


def func3(bet='1.2'):
    make_bet(Inventory().get_smallest(2), bet)
    return 'ok'


@app.route('/update_inv', methods=['POST'])
def update_inv():
    dict2 = json.loads(request.data.decode('utf-8'))
    inv = Inventory()
    lis = list(map(lambda x: Weapon(x), dict2['userItemIds']))
    inv.update(lis, dict2['balance'])
    inv.set_balance(dict2['balance'])
    exchange(flag2=True)
    return '1'


@app.route('/init', methods=['POST'])
def init():
    exchange(True)
    return '1'


@app.route('/append', methods=['POST'])
def append():
    dict1 = json.loads(request.data.decode('utf-8'))
    con = sqlite3.connect('db1.db')
    try:
        con.execute('insert into crashes(id,crash) values(?,?)', (dict1['id'], dict1['crash']))
        con.commit()
        x = con.execute('select crash from crashes').fetchall()[-7:]
        dchance = main() - (1 / 1.2)
        if taktic5(x):
            func2()
        elif all(i[0] < 1.2 for i in x[-3:]):
            print('make bet')
            func2(bet='3.2')
        elif all(i[0] < 1.2 for i in x[-2:]):
            print('make bet')
            func2()
        elif taktic4(x):
            func3()
        elif dchance > 0.1:
            func2()
        elif dchance > 0.05:
            func2()
    except sqlite3.IntegrityError as error:
        pass
    return 'ok'


def download_last(debug=True, i=2308923):
    con = sqlite3.connect('db1.db')

    flag = True
    while flag:
        response = requests.get(f'https://api.csgorun.gg/games/{i}')
        if not response:
            # pass
            flag = False
        else:
            try:
                con.execute('insert into crashes(id,crash) values(?,?)', (i, response.json()['data']['crash']))
                con.commit()
            except sqlite3.IntegrityError as error:
                i = con.execute('select id from crashes').fetchall()[-1][0]
                if debug:
                    print('начал качать')
            i += 1
    if debug:
        print('закончил качать')


@app.route('/get_balance')
def get_balance():
    return str(Inventory().price())


@app.route('/update_bet')
def update_bet():
    global bet
    dict2 = json.loads(request.data.decode('utf-8'))
    bet = float(dict2['bet'])
    dict1[str(bet)] = dict2['id']
    exchange(True)
    return 'ok'


if __name__ == "__main__":
    # download_last()
    exchange(True)
    app.run('0.0.0.0', port=5000)
