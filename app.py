#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import itchat
import json
import requests
import pygal
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from itchat.content import TEXT


count = 0
ts1 = datetime.now().timestamp()
ts2 = ts1

with open('./coin-symbols.json', 'r') as f:
    j = f.read()
    coins = json.loads(j)
    
def get_market(coin):
    url = 'https://api.coinmarketcap.com/v1/ticker/{0}/?convert=CNY'.format(coin)
    r = requests.get(url)
    ticker = r.json()[0]
    price = ticker['price_cny']
    change = ticker['percent_change_24h']
    volume = ticker['24h_volume_cny']
    return (price, change, volume)

def get_ether_balance(address):
    url = 'https://etherscan.io/address/' + address
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    eth = soup.find_all('table')[0].find_all('td')[1].text.replace('\n','').split(' ')[0]
    eth = float(eth.replace(',', ''))
    assets = {'ETH': eth}
    balancelist = soup.find(id='balancelist')
    if balancelist != None:
        for i in balancelist.find_all('li')[:-1]:
            br = i.a.br.text.split('@')[0]
            token = br.split(' ')[1]
            amount = float(br.split(' ')[0].replace(',', ''))
            if token in assets.keys():
                print('Warning: Duplicated token symbol {0}. Using the first one.'.format(token))
                continue
            assets[token] = amount
    return assets

@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    global count
    global ts1, ts2

    if msg.text.upper() in coins.keys() or msg.text.lower() in [coins[i] for i in coins.keys()]:       
        ts2 = datetime.now().timestamp()
        if ts2 - ts1 >= 60:
                count = 1
                ts1 = datetime.now().timestamp()
        if count > 2:
            msg.user.send('查价功能一分钟只能用两次哦！\n不刷屏🙃')
        else:
            if msg.text.upper() in coins.keys():
                coin = coins[msg.text.upper()]
            else:
                coin = msg.text.lower()
            (price, change, volume) = get_market(coin)
            
            price = price.split('.')
            if len(price) == 0:
                price = price[0]
            else:
                if len(price[1]) >= 2:
                    price = price[0] + '.' + price[1][:2]
                else:
                    price = price[0] + '.' + price[1]
            message = '{0}\n当前价格：{1} CNY\n24小时内涨跌：{2}%\n24内交易量：{3} CNY\n数据来源：CoinMarketCap'.format(coin, price, change, volume)
            msg.user.send(message)
            count += 1
    
    elif msg.text[:2] == '0x' and len(msg.text) == 42:
        assets = get_ether_balance(msg.text.lower())
        print(assets)
        message = '来看下这位土豪的资产：\n'
        for k,v in assets.items():
            message += '{0}: {1}\n'.format(k, str(v))
        print(message)
        msg.user.send(message[:-1])
    
    elif msg.text.upper() == 'GBI':
        r = requests.get('http://gbi.inblockchain.com/markets/gbi?json=1')
        gbi = r.json()['gbi']
        message = '区块链全球指数: {0}\n数据来源：INBlockchain\n回复GBI7或GBI30查看走势'.format(str(gbi))
        msg.user.send(message)
        
    elif msg.text.upper() == 'GBI7' or msg.text.upper() == 'GBI30':
        days = int(msg.text[3:])
        start = (datetime.today() - timedelta(days=days)).strftime('%Y-%m-%dT%H:%M:%S')
        url = 'http://gbi.inblockchain.com/markets/gbi/k/minute?start_at={0}+00:00&space=1440&json=1'.format(start)
        r = requests.get(url)
        gbi = r.json()
        line_chart = pygal.Line(show_legend=False, x_label_rotation=30)
        line_chart.title = 'Global Blockchain Index'
        line_chart.x_labels = [d[:10] for d in gbi['dates']]
        line_chart.add('GBI', gbi['gbis'])
        line_chart.render_to_png('./gbichart.png')
        print('OK!!!!!')
        itchat.send_image('./gbichart.png', toUserName=msg.user.userName)

    elif msg.text.upper() == 'MLGB':
        msg.user.send('骂谁呢？')
        
    elif '梭哈' in msg.text:
        msg.user.send('不要怂，一把梭！赢了会所嫩模，输了下海干活！')
    
    else:
        pass


itchat.auto_login(hotReload=True)
itchat.run()
