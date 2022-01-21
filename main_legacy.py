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

# {"success":true,"date":"2022-01-08T09:33:20.723Z","data":{"user":{"id":1804728,"steamId":"76561199080583274","name":"[asuka] | CSGORUN.PRO","deposit":624.67,"hasDeposit":true,"depositCount":96,"steamLevel":1,"avatar":"https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/43/430e49102000b83c8ad05f6742fb414b03f95275_medium.jpg","balance":0,"mutedAt":"2021-11-12T16:44:37.000Z","lang":null,"role":1,"items":[{"id":2735915882,"price":0.27,"itemId":346,"name":"AWP | Safari Mesh (Battle-Scarred)","entity":"AWP","description":"Safari Mesh","qualityId":1,"colorId":2,"isSlowWithdraw":false}],"stickers":[{"id":4,"name":null,"url":"https://csgorun.gg/img/stickers/4.png"},{"id":6,"name":null,"url":"https://csgorun.gg/img/stickers/foto2-vosstanovleno.png"},{"id":7,"name":null,"url":"https://csgorun.gg/img/stickers/7.png"},{"id":8,"name":null,"url":"https://csgorun.gg/img/stickers/8.png"},{"id":9,"name":null,"url":"https://csgorun.gg/img/stickers/9.png"},{"id":10,"name":null,"url":"https://csgorun.gg/img/stickers/10.png"},{"id":14,"name":null,"url":"https://csgorun.gg/img/stickers/razreshite_dokopatsya_2.png"},{"id":16,"name":null,"url":"https://csgorun.gg/img/stickers/250kh250.png"},{"id":17,"name":null,"url":"https://csgorun.gg/img/stickers/17.png"},{"id":18,"name":null,"url":"https://csgorun.gg/img/stickers/18.png"},{"id":19,"name":null,"url":"https://csgorun.gg/img/stickers/19.gif"},{"id":20,"name":null,"url":"https://csgorun.gg/img/stickers/20.gif"}]},"notifications":[{"id":19559612,"type":1,"isRead":false,"payload":{"amount":4.543},"createdAt":"2022-01-08T07:50:03.000Z"},{"id":19555193,"type":10,"isRead":false,"payload":{"id":2464205,"amount":"$4.97"},"createdAt":"2022-01-07T23:49:30.000Z"},{"id":19555069,"type":10,"isRead":false,"payload":{"id":2464207,"amount":"$4.98"},"createdAt":"2022-01-07T23:49:10.000Z"},{"id":19554949,"type":10,"isRead":false,"payload":{"id":2464206,"amount":"$4.98"},"createdAt":"2022-01-07T23:49:03.000Z"},{"id":19553180,"type":8,"isRead":false,"payload":{"id":4775684,"name":"Five-SeveN | Fairy Tale (Well-Worn)","error":null,"price":5.43},"createdAt":"2022-01-07T22:50:05.000Z"},{"id":19553171,"type":7,"isRead":false,"payload":{"id":4775684,"name":"Five-SeveN | Fairy Tale (Well-Worn)","error":null,"price":5.43},"createdAt":"2022-01-07T22:49:37.000Z"},{"id":19535551,"type":1,"isRead":false,"payload":{"amount":4.9830000000000005},"createdAt":"2022-01-07T09:03:54.000Z"},{"id":19535004,"type":1,"isRead":true,"payload":{"amount":2.6180000000000003},"createdAt":"2022-01-07T08:22:51.000Z"},{"id":19496007,"type":40,"isRead":true,"payload":{},"createdAt":"2022-01-05T11:31:42.000Z"},{"id":19489517,"type":40,"isRead":true,"payload":{},"createdAt":"2022-01-04T22:30:30.000Z"},{"id":19480167,"type":8,"isRead":true,"payload":{"id":4763170,"name":"Operation Wildfire Case Key","error":null,"price":6.14},"createdAt":"2022-01-04T17:32:07.000Z"},{"id":19480139,"type":7,"isRead":true,"payload":{"id":4763170,"name":"Operation Wildfire Case Key","error":null,"price":6.14},"createdAt":"2022-01-04T17:31:21.000Z"},{"id":19479828,"type":1,"isRead":true,"payload":{"amount":4.9830000000000005},"createdAt":"2022-01-04T17:15:42.000Z"},{"id":19472394,"type":40,"isRead":true,"payload":{},"createdAt":"2022-01-04T11:02:21.000Z"},{"id":19472182,"type":40,"isRead":true,"payload":{},"createdAt":"2022-01-04T10:46:49.000Z"}],"game":{"delta":null,"status":3,"statistic":{"count":0,"totalDeposit":"0.00","totalItems":0},"history":[{"id":2465347,"crash":1.16},{"id":2465346,"crash":10},{"id":2465345,"crash":4.22},{"id":2465344,"crash":1.67},{"id":2465343,"crash":54.74},{"id":2465342,"crash":10.81},{"id":2465341,"crash":1.97},{"id":2465340,"crash":2.29},{"id":2465339,"crash":3.03},{"id":2465338,"crash":1.12},{"id":2465337,"crash":1.16},{"id":2465336,"crash":1.45},{"id":2465335,"crash":3},{"id":2465334,"crash":238.42},{"id":2465333,"crash":1.07},{"id":2465332,"crash":63.8},{"id":2465331,"crash":1},{"id":2465330,"crash":1.36},{"id":2465329,"crash":4.95},{"id":2465328,"crash":1.69},{"id":2465327,"crash":2.55},{"id":2465326,"crash":1.26},{"id":2465325,"crash":1.19},{"id":2465324,"crash":1.1},{"id":2465323,"crash":12.25},{"id":2465322,"crash":1.49},{"id":2465321,"crash":5.48},{"id":2465320,"crash":2.87},{"id":2465319,"crash":1.14},{"id":2465318,"crash":6.07}],"crash":1.33,"bet":null,"hash":"b1f7d9309cd3c1361f294b88eb5fa16b63090e9ff9e72225ce220a7ff9512ce6","bets":[]},"currency":77.2942,"systemMessage":{"ru":"#","en":"#"},"centrifugeToken":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxODA0NzI4IiwiaWF0IjoxNjQxNjM0NDAwfQ.8PzTCr55XyFf337zQSqCH7tdbpHGHe8jHLScbLatLTU","youtubers":[{"id":25153,"steamId":"76561198155649412","name":"NordVi","avatar":"https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/6f/6f8fac07ba58f854bcd7b49efdcea6861023230f_medium.jpg"},{"id":1907505,"steamId":"76561197990354502","name":"twitch.tv/es4xtank","avatar":"https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/70/703408fe04c528fc0713997846facba301887625_medium.jpg"},{"id":88075,"steamId":"76561198252392862","name":"BAGGIMEN YouTube","avatar":"https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/40/40f8243937c31b117de41013b43bc186687fd173_medium.jpg"}],"transaction":null,"raffleAt":"2022-01-08T09:51:50.000Z","totalizatorEventsExist":true,"isGiver":false,"paymentMethods":[{"id":17,"name":"interkassa","titleRu":"Банковская карта #1","titleEn":"Bank Card #1","type":"interkassa","isActive":true,"order":10005,"category":1,"img":"card","minAmount":0.25,"currency":1,"createdAt":"2021-06-16T10:29:31.000Z","updatedAt":"2021-06-25T09:34:21.000Z"},{"id":2,"name":"money-card","titleRu":"Банковская карта #2","titleEn":"Bank card #2","type":"freekassa/36","isActive":true,"order":10004,"category":1,"img":"card","minAmount":0.25,"currency":1,"createdAt":"2021-04-29T18:30:44.000Z","updatedAt":"2021-11-11T13:37:55.000Z"},{"id":3,"name":"enot-card","titleRu":"Банковская карта #3","titleEn":"Bank card #3","type":"enot","isActive":true,"order":10003,"category":1,"img":"card","minAmount":100,"currency":2,"createdAt":"2021-04-29T18:32:23.000Z","updatedAt":"2021-08-09T23:21:18.000Z"},{"id":4,"name":"gamemoney-card","titleRu":"Банковская карта #4","titleEn":"Bank card #4","type":"gamemoney","isActive":true,"order":997,"category":1,"img":"card","minAmount":0.25,"currency":1,"createdAt":"2021-04-29T18:33:19.000Z","updatedAt":"2021-08-10T20:20:43.000Z"},{"id":5,"name":"buy-code","titleRu":"Qiwi","titleEn":"Qiwi","type":"buy-code","isActive":true,"order":996,"category":3,"img":"qiwi","minAmount":0.25,"currency":1,"createdAt":"2021-04-29T18:33:54.000Z","updatedAt":"2021-06-15T17:36:10.000Z"},{"id":18,"name":"clover","titleRu":"Мне повезет","titleEn":"Мне повезет","type":"clover","isActive":true,"order":996,"category":3,"img":"clover","minAmount":0.25,"currency":1,"createdAt":"2021-06-19T18:25:30.000Z","updatedAt":"2021-06-19T18:25:30.000Z"},{"id":14,"name":"new-freekassa","titleRu":"Qiwi 2","titleEn":"Qiwi 2","type":"freekassa/35","isActive":true,"order":995,"category":3,"img":"qiwi","minAmount":0.25,"currency":1,"createdAt":"2021-04-30T20:11:08.000Z","updatedAt":"2021-11-17T13:02:48.000Z"},{"id":6,"name":"money-yandex","titleRu":"ЮMoney (Яндекс.Деньги) #1","titleEn":"Yoomoney (Yandex.Money) #1","type":"freekassa","isActive":true,"order":994,"category":3,"img":"u-money","minAmount":0.25,"currency":1,"createdAt":"2021-04-29T18:35:30.000Z","updatedAt":"2021-06-19T18:26:06.000Z"},{"id":7,"name":"fkwallet","titleRu":"FKWallet","titleEn":"FKWallet","type":"freekassa","isActive":true,"order":994,"category":3,"img":"fk-wallet","minAmount":0.25,"currency":1,"createdAt":"2021-04-29T18:38:03.000Z","updatedAt":"2021-06-15T17:37:39.000Z"},{"id":8,"name":"alfaClick","titleRu":"Альфа.Клик","titleEn":"AlfaClick","type":"money","isActive":true,"order":993,"category":1,"img":"alfa-bank","minAmount":0.25,"currency":1,"createdAt":"2021-04-29T18:39:00.000Z","updatedAt":"2021-06-15T17:37:54.000Z"},{"id":9,"name":"promSviazBank","titleRu":"ПромСвязьБанк","titleEn":"PromSviazBank","type":"money","isActive":true,"order":992,"category":1,"img":"promsviaz","minAmount":0.25,"currency":1,"createdAt":"2021-04-29T18:39:58.000Z","updatedAt":"2021-06-15T17:38:09.000Z"},{"id":10,"name":"mobile","titleRu":"Мобильный телефон","titleEn":"Mobile","type":"money","isActive":true,"order":991,"category":2,"img":"mobile","minAmount":0.25,"currency":1,"createdAt":"2021-04-29T18:40:57.000Z","updatedAt":"2021-06-15T17:38:17.000Z"},{"id":12,"name":"gamemoney","titleRu":"Gamemoney","titleEn":"Gamemoney","type":"gamemoney","isActive":true,"order":989,"category":3,"img":"gamemoney","minAmount":0.25,"currency":1,"createdAt":"2021-04-29T18:42:11.000Z","updatedAt":"2021-06-15T17:39:06.000Z"},{"id":13,"name":"fkk","titleRu":"Free-Kassa","titleEn":"Free-Kassa","type":"freekassa","isActive":true,"order":988,"category":3,"img":"freekassa","minAmount":0.25,"currency":1,"createdAt":"2021-04-29T18:43:03.000Z","updatedAt":"2021-06-15T17:39:29.000Z"}],"online":"2942"}}
app = Flask(__name__)
CORS(app)

lis = []
TOKEN = 'JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTgwNDcyOCwiaWF0IjoxNjQyMTQ2NjQwLCJleHAiOjE2NDMwMTA2NDB9.WbD5cbollQRtmigEWmKsM2W8rzkmu4fFw2lHSLpXugA'

deq = deque()

bet = 4.0
dict1 = {'0.25': 219, '0.5': 1117, '0.84': 363, '2.0': 662, '1.0': 25000, '3.0': 4860, '4.0': 2233, '5.0': 244,
         '10.0': 99}


def return_bet(k='1.01'):
    res = requests.post('https://api.csgorun.gg/upgrade-bet', headers={'authorization': TOKEN}, json={'coefficient': k})
    print(res.text)
    print(res)


def make_bet(items_id, auto='1.01'):
    if (items_id is None):
        exchange()
        return
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
        if i > 7:
            return response

    response.close()


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
    try:
        pass
    except Exception:
        pass


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


def tactic1(lis: list):
    return lis[-1] < 1.2 and lis[-2] < 1.2 and lis[-3] < 1.2 and lis[-4] >= 1.2


def tactic7(lis: list):
    return lis[-1] < 1.2 and lis[-2] > 1.2


def tactic2(lis: list):
    return lis[-1] < 1.2 and lis[-2] < 1.2 and lis[-3] >= 1.2 and lis[-4] < 1.2


def tactic3(lis: list):
    return False
    return lis[-1] < 2 and lis[-2] > 8 and lis[-3] >= 8 and lis[-4] < 8


def tactic4(lis: list):
    return lis[-1] < 1.2 and lis[-2] >= 2 and lis[-3] >= 2 and lis[-4] >= 2


def taktic5(lis: list):
    if lis[-1] > 1.2 and lis[-2] < 1.2 and lis[-3] < 1.2 and lis[-4] < 1.2:
        return True


def taktic6(lis: list):
    if lis[-1] < 1.2 and lis[-2] < 1.2:
        return True


def taktic5(lis: list):
    if lis[-1] > 1.2 and lis[-2] < 1.2 and lis[-3] < 1.2 and lis[-4] < 1.2:
        return True


@app.route('/append', methods=['POST'])
def append():
    dict1 = json.loads(request.data.decode('utf-8'))
    con = sqlite3.connect('db1.db')
    try:
        return_bet(str(float(dict1['crash']) - 0.04))
        con.execute('insert into crashes(id,crash) values(?,?)', (dict1['id'], dict1['crash']))
        con.commit()
        x = con.execute('select crash from crashes').fetchall()[-7:]
        x = [i[0] for i in x]
        if tactic1(x):
            func2(bet='1.2')
        elif taktic6(x) or tactic2(x) or tactic3(x) or taktic5(x):
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


@app.route('/update_bet1', methods=['POST'])
def update_bet():
    global bet
    dict2 = json.loads(request.data.decode('utf-8'))
    bet = float(dict2['bet'])
    dict1[str(bet)] = dict2['id']
    exchange(True)
    return 'ok'


@app.route('/update_bet2', methods=['POST'])
def update_bet3():
    global bet
    dict2 = json.loads(request.data.decode('utf-8'))
    bet = float(dict2['bet'])
    exchange(True)
    return 'ok'


@app.route('/get_bet')
def get_bet():
    return str(bet)


if __name__ == "__main__":
    exchange(True)
    exchange(True)
    app.run('0.0.0.0', port=5000)
