import time
from webscraper import getHtml

c_files = {}


def gethoteldata(link, driver, wait, EC, By, files):
    driver.execute_script('''window.open("''' + link + '''", "_blank");''')
    time.sleep(2)
    driver.switch_to.window(driver.window_handles[0])
    driver.close()
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(20)
    t = 1
    hotel = 0
    while t == 1:
        uf = 1
        while uf != 12:
            try:
                snext = driver.find_element_by_xpath(
                    "/html/body/c-wiz[2]/div/c-wiz/div/div[1]/div/div[4]/div/div[2]/c-wiz/div[4]/c-wiz[1]/div/div")
                driver.execute_script("arguments[0].click();", snext)
                wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, '.M9Bg4d > span:nth-child(3) > span:nth-child(1) > span:nth-child(1)')))
                h = driver.page_source
                print('Page ' + str(uf + 1) + ' done')
                getHtml(h, files[uf], c_files)
                uf += 1
            except AttributeError:
                t = 0
