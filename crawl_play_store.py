import time
from bs4 import BeautifulSoup
import sys, io
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.proxy import *
no_of_reviews = 1000

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
# driver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')
# driver = webdriver.Firefox(executable_path='d:/tools/geckodriver.exe')
# driver = webdriver.Firefox(executable_path='c:/soft/geckodriver.exe')

# dcap = dict(DesiredCapabilities.PHANTOMJS)
# dcap["phantomjs.page.settings.userAgent"] = (
#     "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0")
# driver = webdriver.PhantomJS("d:/tools/phantomjs.exe", desired_capabilities=dcap)

options = webdriver.FirefoxOptions()
options.add_argument('-headless')
driver = webdriver.Firefox(options=options)

wait = WebDriverWait(driver, 10)

# Append your app store urls here
urls = [
    # "https://play.google.com/store/apps/details?id=com.flipkart.android&hl=en&showAllReviews=true",
    "https://play.google.com/store/apps/details?id=com.twitter.android&showAllReviews=true"
    # "https://play.google.com/store/apps/details?id=com.amazon.mShop.android.shopping"
    # "http://m.toutiao.com"
]

result = []
for url in urls:
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
    # expand_div = soup_expatistan.find("div", class_="feed-infinite-wrapper")
    # expand_li = expand_div.find_all("li")
    # for li in expand_li:
    #     print(li.text)
    expatistan_table = soup_expatistan.find("h1", class_='AHFaub')
    result.append({"title": expatistan_table.text, "reviews": []})

    expatistan_table = soup_expatistan.find("div", class_='W4P4ne')
    expatistan_div = expatistan_table.find_all("div", class_='zc7KVe')

    index = len(result) - 1

    for ele in expatistan_div:
        user_name = ele.find("span", class_="X43Kjb")
        star_num = ele.find("div", class_="pf5lIe").find_next()['aria-label']
        review_div = ele.find("div", class_="UD7Dzf")
        try:
            review_div.find_all("span")
        except AttributeError:
            review = review_div
        else:
            review = review_div.find_all("span")[0].text

        date = ele.find("span", class_="p2TkOb")
        reviews = {
            "user_name": user_name.text,
            "star_num": star_num,
            "review": review,
            "date": date.text
        }
        result[index]['reviews'].append(reviews)
    driver.quit()
print(result)
