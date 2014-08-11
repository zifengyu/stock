# -*- coding: utf-8 -*-
import requests
import bs4
import re
import time
import os

stock_base_dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
output_file = os.path.join(stock_base_dir, 'report', 'bond', time.strftime('%Y%m%d',time.localtime(time.time())) + '.csv')

bond_rate_criteria = ('AAA', 'AA+', 'AA')

def isNum(value):
    try:
        float(value)
    except :
        return False
    else:
        return True
        
def cmp(x,y):
    return int(float(x[1])-float(y[1]))


resp = requests.get('http://bond.eastmoney.com/data/bonddata.html')
soup = bs4.BeautifulSoup(resp.text)

items = soup.select('ul')

count = 0
bonds = []
processed = []
for item in items:
    code = item.select('li.code a')
    if len(code) == 1:
        code = code[0].get_text()
        if code in processed:
            continue
        processed.append(code)
        roi = item.select('li.pricev')[0].get_text()
        day = item.select('li.priced')[0].get_text()      
        price = item.select('li.price')[0].get_text()  
        if isNum(roi) and float(roi) > 0 and isNum(day):        
            xueqiu_code = re.search('quote\.eastmoney\.com/(.*)\.html', item.select('li.name a')[0].attrs['href'], re.I)
            if xueqiu_code:
                xueqiu_code = xueqiu_code.group(1).upper()
                print '-->', xueqiu_code
                resp = requests.get('http://xueqiu.com/S/' + xueqiu_code)
                resp = requests.get('http://xueqiu.com/stock/quote.json?code=' + xueqiu_code, cookies = resp.cookies)                
                info = resp.json()['quotes'][0]
                name = info['name']
                if name.find('PR') == -1:                                      
                    rate, warrant, volume = info['rate'], info['warrant'], info['volume']
                    if rate in bond_rate_criteria and warrant in bond_rate_criteria:                    
                        count += 1
                        bonds.append((str(code),float(roi),int(day),float(price), float(volume),str(rate),str(warrant)))

bonds.sort(cmp=cmp, reverse=True)

fout = open(output_file, 'w')
for bond in bonds:
    print bond
    fout.write(str(bond).replace('(', '').replace(')', '') + '\n')
fout.close()