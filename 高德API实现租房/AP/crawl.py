#-*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import csv

url = "http://cd.58.com/pinpaigongyu/pn/{page}/?minprice=1000_1500"

page = 0

csv_file = open("rent.csv","w",newline='' )
csv_writer = csv.writer(csv_file, delimiter=',')

while True:
    page += 1
    print("fetch: ", url.format(page=page))
    response = requests.get(url.format(page=page))
    html = BeautifulSoup(response.text,"lxml")
    house_list = html.select(".list > li")

    # 循环在读不到新的房源时结束
    if not house_list:
        break

    for house in house_list:
        house_title = house.select("h2")[0].string.encode("utf8")
        house_url = urljoin(url, house.select("a")[0]["href"])
        house_info_list = house_title.split()

        # 如果第二列是公寓名则取第一列作为地址
        if "公寓" in house_info_list[1].decode('utf-8') or "青年社区" in house_info_list[1].decode('utf-8'):
            house_location = house_info_list[0]
        else:
            house_location = house_info_list[1]
            house_money = house.select(".money")[0].select("b")[0].string.encode("utf8")
            house_money = house_money.decode('utf-8')
            house_title = house_title.decode('utf-8')
            house_location = house_location.decode('utf-8')
         #   print(type(house_title), type(house_location), type(house_money), type(house_url))
            csv_writer.writerow([house_title, house_location, house_money, house_url])
csv_file.close()
