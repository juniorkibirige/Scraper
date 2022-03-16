import json
import time
import os
import csv
import selenium.common.exceptions as exc
from bs4 import BeautifulSoup
import requests
import filenameGen as fg
import pathlib

from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from requests_testadapter import Resp

from localstorage import LocalStorage

def convertJsonToCSV():
    with open('products_list.json') as json_file:
        data = json.load(json_file)
    
    excel_file = open('products_list.csv', 'w')
    csv_writer = csv.writer(excel_file)
    
    count = 0
    for product in data:
        if count == 0:
            header = product.keys()
            csv_writer.writerow(header)
            count += 1
        csv_writer.writerow(product.values())
    
    excel_file.close()

class LocalFileAdapter(requests.adapters.HTTPAdapter):
    def build_response_from_file(self, request):
        file_path = request.url[7:]
        with open(file_path, 'rb') as file:
            buff = bytearray(os.path.getsize(file_path))
            file.readinto(buff)
            resp = Resp(buff)
            r = self.build_response(request, resp)

            return r

    def send(self, request, stream=False, timeout=None,
             verify=True, cert=None, proxies=None):

        return self.build_response_from_file(request)


def getHtml(html, fls, c_file):
    with open(fls, 'w') as s:
        s.write(str(html))
    c_file[fls] = 'written'


locnum = []


def switch_to_last_tab():
    browser.switch_to.window(browser.window_handles[-1])


def switch_to_main_tab():
    browser.switch_to.window(browser.window_handles[0])


def close_current_tab():
    browser.close()


def getJson(fil, hotels):
    file_url = pathlib.Path(__file__).parent.__str__() + "/" + fil
    response = requests_session.get("file://"+file_url)
    content = BeautifulSoup(response.content, "html.parser").find_all('tr')
    content.pop(0)

    for product in content:
        cells = product.find_all('td')
        name = cells[0].text
        price = cells[3].text
        hotel_object = {
            "Product Name": name,
            "Price": price,
        }
        hotels.append(hotel_object)


def login2Website():
    usernameInput = browser.find_element_by_xpath(
        '/html/body/div[1]/div[2]/section/div/div/div/div/div/div[2]/form/div[1]/input')
    usernameInput.send_keys(username)
    passwordInput = browser.find_element_by_xpath(
        '/html/body/div[1]/div[2]/section/div/div/div/div/div/div[2]/form/div[2]/input')
    passwordInput.send_keys('Letmein@123Q')
    login = browser.find_element_by_xpath(
        '/html/body/div[1]/div[2]/section/div/div/div/div/div/div[2]/form/div[3]/button')
    login.click()
    time.sleep(5)
    browser.get("https://mobileshop.ug/admin/listproduct")


def file_created(f):
    if os.path.exists(f):
        return True
    else:
        return False


def write_out(hotels):
    with open('hotelData.json', 'a+') as outfile:
        json.dump(hotels, outfile)


username = "master@2021"
role = "admin"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYwNGI4MzZlYmVkYTU3MDVkNTkyODEwYyIsImlhdCI6MTY0NzQyOTcxNywiZXhwIjoxNjUwMDIxNzE3fQ.i9tVKrZZEleSsbDtZoNLPjns8Ecqk3Qg06doRxSXgDA"
pageLinkElements = []

print('Booting ...')
files = fg.getfilenames()
time.sleep(2)
print('*****Loading Beautiful Soup ...')
time.sleep(2)
print('*****Loading requests libraries ...')
c_files = {}
hotelList = []
requests_session = requests.session()
requests_session.mount('file://', LocalFileAdapter())
cap = DesiredCapabilities.FIREFOX
cap['pageLoadStrategy'] = "none"
opt = Options()
opt.add_argument('--headless')
browser = webdriver.Firefox(desired_capabilities=cap)
wait = WebDriverWait(browser, 10)
url = 'https://mobileshop.ug/login/staff'
print('Initializing...')
browser.get(url)
try:
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, '/html/body/div[1]/div[2]/section/div/div/div/div/div/div[2]/form/div[3]/button')))
except exc.TimeoutException:
    print('Please check your Internet Connection,\nPage has failed to load.')
    browser.quit()
    exit(1)
login2Website()
wait.until(EC.element_to_be_clickable(
    (By.XPATH, '/html/body/div/div[2]/div[2]/div[2]/div[1]/div[2]/div[2]/div[2]/nav/ul/li[2]/a[1]')))
pageLinkElements = browser.find_elements_by_xpath(
    '/html/body/div/div[2]/div[2]/div[2]/div[1]/div[2]/div[2]/div[2]/nav/ul/li[2]/a')
print('*****Scrapping ...')
t = 1
uf = 1
for item in pageLinkElements:
    h = browser.page_source
    getHtml(h, files[uf], c_files)
    print('Page ' + str(uf) + ' done')
    try:
        if uf <= pageLinkElements.__len__():
            snext = pageLinkElements[uf]
            snext.click()
            wait.until(EC.element_to_be_clickable(snext))
            time.sleep(20)
        uf += 1
    except IndexError:
        print('No more pages')
        break

browser.quit()
print('Success: All Pages received.')
print('Shutting Down Scraper ...')
time.sleep(2)
print('Creating organised tables and listings from the collected raw data')
for file in files:
    if file_created(file):
        getJson(file, hotelList)
        os.remove(file)
write_out(hotelList)
os.rename('hotelData.json', 'products_list.json')
convertJsonToCSV()
os.remove("products_list.json")
