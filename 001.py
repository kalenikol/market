import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

import pickle
import urllib.request

from PIL import Image
from resizeimage import resizeimage

options = Options()
options.add_argument("--user-data-dir=C:\\Users\\Anton\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1")

description = []

def take_features():
    ### СКАЧИВАЕМ ХАРАКТЕРИСТИКИ И ВОЗВРАЩАЕМСЯ НА ГЛАВНУЮ ###
    a = driver.find_element(By.CLASS_NAME, "title").text
    print(a)
    time.sleep(5)
    driver.find_elements_by_xpath("//*[contains(text(), 'Все характеристики')]")[0].click()
    time.sleep(5)
    for number in range(2, 12):
        div_string = '/html/body/div[2]/div[7]/div[1]/div/div/div/div[%s]' % number
        c = driver.find_element_by_xpath(div_string).text
        # print(c)
        if c == 'Перед покупкой уточняйте характеристики и комплектацию у продавца.':
            break
        # read_description(c)
        write_description_to_file(c)
    time.sleep(3)
    driver.find_elements_by_xpath("//*[contains(text(), 'Описание')]")[0].click()
    time.sleep(2)
    ### СКАЧИВАЕМ ХАРАКТЕРИСТИКИ И ВОЗВРАЩАЕМСЯ НА ГЛАВНУЮ ###


def press_some_button():
    ### КНОПКА ЕЩЕ ###
    try:
        if driver.find_element_by_xpath('.//*[@class="_19EZnB_hta"]'):
            driver.find_element_by_xpath('.//*[@class="_19EZnB_hta"]').click()
    except:
        print("Нет кнопки ЕЩЕ")
    time.sleep(2)
    ### КНОПКА ЕЩЕ ###

def click_on_image():
    driver.find_element_by_xpath('.//*[@class="_3Wp6VWi5D1"]').click()

def read_description(string):
    a = string.split('\n')
    print(a)
    with open('data.pickle', 'wb') as f:
        pickle.dump(a, f)

def write_description_to_file(str):
    data = str.split("\n")
    f = open('out.txt', 'a', encoding='UTF-8')
    str = "<h4>" + data.pop(0) + "<h4><br>\n"
    f.write(str)

    while data:
        str = data.pop(0) + " " + data.pop(0) + "<br>\n"
        f.write(str)


def init_driver():
    driver = webdriver.Chrome(options=options, executable_path='chromedriver.exe',
                              service_args=['--marionette-port', '2828'])
    driver.wait = WebDriverWait(driver, 5)
    return driver


def lookup(driver, query):
    driver.get("https://market.yandex.ru/product--naushniki-technics-rp-dj1210/264360")
    try:
        take_features()
        press_some_button()
        click_on_image()


        image = driver.find_elements_by_xpath(".//*[@class=\"_2gUfndCf6w\"]")
        print(len(image))
        time.sleep(2)
        print("HERE???")
        for x in range(0, len(image)):
            try:
                driver.find_elements_by_xpath(".//*[@class=\"_2gUfndCf6w\"]")[x].click()
                time.sleep(2)
                print(x)
                img = driver.find_element_by_xpath('//body//img[@class="_1E9hbWWgop"]')
                url = img.get_attribute('src')
                short_name = str(x) + '.jpg'
                thumb_name = 'image/th_' + short_name
                name = 'image/' + short_name
                urllib.request.urlretrieve(url, name)
                im = Image.open(name)
                time.sleep(1)

                fill_color = '#FFFFFF'
                image = Image.open(name)
                if image.mode in ('RGBA', 'LA'):
                    background = Image.new(image.mode[:-1], image.size, fill_color)
                    background.paste(image, image.split()[-1])
                    image = background
                image.save('3.jpg', "JPEG", quality=95)

                # image._colorspace(image='3.jpg', colorspace='RGBA', format='JPEG')

                # with open('3.jpg', 'r+b') as f:
                #     with Image.open(f) as image:
                cover = resizeimage.resize_contain(image, [600, 600])
                if cover.mode in ('RGBA', 'LA'):
                    background = Image.new(cover.mode[:-1], cover.size, fill_color)
                    background.paste(cover, cover.split()[-1])
                    cover = background
                cover.save(thumb_name, "JPEG")


            except:
                print("OOOps!")


    except TimeoutException:
        print("Box or Button not found in google.com")


if __name__ == "__main__":
    driver = init_driver()
    lookup(driver, "Selenium")
    while True:
        time.sleep(1)
    driver.quit()