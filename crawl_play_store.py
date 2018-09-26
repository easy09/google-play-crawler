import time
from bs4 import BeautifulSoup
import sys, io
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.proxy import *
from bottle import route, run
import re
import hashlib


@route('/')
def hello():
    return {'format': '/app/app_name/token', 'example': '/app/com.twitter.android/123456789'}


@route('/app/<name>/<token>')
def index(name, token):
    if token != "20180925":
        return {'message': 'token error'}
    no_of_reviews = 1000

    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    # driver = webdriver.Firefox(executable_path="d:/tools/geckodriver.exe", options=options)
    driver = webdriver.Firefox(executable_path="/sites/geckodriver", options=options)

    wait = WebDriverWait(driver, 10)
    if not name:
        return {'param example': "com.twitter.android"}
    url = "https://play.google.com/store/apps/details?id=" + name + "&showAllReviews=true"
    driver.get(url)
    time.sleep(2)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    page = driver.page_source

    soup_expatistan = BeautifulSoup(page, "html.parser")
    expatistan_table = soup_expatistan.find("h1", class_='AHFaub')
    result = {"title": expatistan_table.text, "reviews": []}
    expatistan_table = soup_expatistan.find("div", class_='W4P4ne')
    expatistan_div = expatistan_table.find_all("div", class_='zc7KVe')

    for ele in expatistan_div:
        user_name = ele.find("span", class_="X43Kjb").text
        stars = ele.find("div", class_="pf5lIe").find_next()['aria-label']
        star_num = re.findall(r'\d', stars)[0]
        review_div = ele.find("div", class_="UD7Dzf")
        try:
            review_div.find_all("span")
        except AttributeError:
            review = ""
        else:
            review = review_div.find_all("span")[0].text
        date = ele.find("span", class_="p2TkOb").text
        try:
            img = ele.find("img")['src']
        except:
            img = ""
        helpful_num = ele.find("div", class_="jUL89d").text
        hash = hashlib.md5((user_name + img + star_num + review + date).encode("utf-8")).hexdigest()
        reviews = {
            "user_name": user_name,
            'img': img,
            'stars': stars,
            "star_num": star_num,
            "review": review,
            'helpful_num': helpful_num,
            "date": date,
            "hash": hash
        }
        if img != "":
            result['reviews'].append(reviews)
    driver.quit()
    return dict(result)


run(host='0.0.0.0', port=8080)
