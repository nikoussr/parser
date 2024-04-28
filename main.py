from bs4 import BeautifulSoup as b
from selenium import webdriver
import requests
from selenium.webdriver.common.by import By
import time


def get_sourse_html(url):
    driver = webdriver.Edge()
    driver.maximize_window()

    try:
        driver.get(url=url)
        time.sleep(30)

        driver.find_element(By.CLASS_NAME, "styles-module-size_s-awPvv").click()
        print("YESS")
    except Exception as _ex:
        print(_ex)
    finally:
        driver.close()
        driver.quit()
def main():
    get_sourse_html(url = "https://www.avito.ru/tomsk/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?cd=1&context=H4sIAAAAAAAA_0q0MrSqLraysFJKK8rPDUhMT1WyLrYysVLKTczMU7KuBQQAAP__w5qblCAAAAA")

if __name__ == '__main__':
    main()

'''while True:
            find_more_el = driver.find_element("js-pages pagination-pagination-_FSNE")
            if driver.find_element("js-pages pagination-pagination-_FSNE"):
                with open'''