import datetime

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import matplotlib.pyplot as plt

from selenium.webdriver.common.by import By


def req(url: str):  # all
    response = requests.get(url)
    data = response.text
    return data


def find_currency(data):  # 1
    bs = BeautifulSoup(data, "html.parser")
    table = bs.find('table', class_='data')
    table_rows = table.find_all('tr')
    mas = []
    for tr in table_rows:
        td = tr.find_all('td')
        for i in td:
            if i.text.strip() == 'CZK':
                for j in td:
                    mas.append(j.text.strip())
    return float(str(mas[4]).replace(',', '.')) / int(mas[2])


def change_CZK_to_RUB(CZK, CZK_curs):  # 1
    return print(f"{CZK} чешских крон = {(CZK * CZK_curs).__round__(5)} рублей")


def change_RUB_to_CZK(RUB, CZK_curs):  # 1
    return print(f"{RUB} рублей = {(RUB / CZK_curs).__round__(5)} чешских крон")


def currency_history(url):  # 2
    date_1 = str(input("Введите первую дату: "))
    date_2 = str(input("Введите вторую дату: "))
    url = url[0] + date_1 + url[1] + date_2
    return req(url)


"""def find_currency_history(data):  # 2
    date_1 = str(input("Введите первую дату: "))
    date_2 = str(input("Введите вторую дату: "))
    bs = BeautifulSoup(data, "html.parser")
    choose_date_input_1= bs.find('input', class_ = 'datepicker-filter_input-from')['value'] = date_1
    choose_date_input_2= bs.find('input', class_ = 'datepicker-filter_input-to')['value'] = date_2
    print(choose_date_input_1, ' ', choose_date_input_2)
    print(data)
    table = bs.find('table', class_='data')
    table_rows = table.find_all('tr')
    mas = []
    for tr in table_rows:
        td = tr.find_all('td')
        element = []
        for i in td:
            element.append(i.text.strip())
        mas.append(element)
    mas = mas[2:]
    mas.reverse()
    print(f"Дата:\t\tЕдиниц:\tЦена:")
    for i in mas:
        print(f"{i[0]}\t{i[1]}\t\t{i[2]}")"""


def get_currency_data(start_date: str, end_date: str):
    url = f'https://www.cbr.ru/currency_base/dynamics/?UniDbQuery.Posted=True&UniDbQuery.mode=1&UniDbQuery.date_req1=&UniDbQuery.date_req2=&UniDbQuery.VAL_NM_RQ=R01760&UniDbQuery.From={start_date}&UniDbQuery.To={end_date}'
    response = requests.get(url)
    dates = []  # массив для дат
    rates = []  # массив для курса

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', class_='data')

        if table:
            rows = table.find_all('tr')

            print(f"Дата\t\tКоличество\tЦена")
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 3:
                    date = cols[0].text
                    count = cols[1].text
                    rate = float(cols[2].text.replace(',', '.'))
                    dates.append(date)
                    rates.append(rate)
                    print(f'{date}\t {count}\t\t {rate}')

        """Строим таблицу"""
        plt.figure(figsize=(12, 6))
        plt.plot(dates, rates, marker='o', color='b')
        plt.title('Динамика курса чешской кроны')
        plt.xlabel('Дата')
        plt.ylabel('Курс чешской кроны за 10 ед. руб.')
        plt.xticks(rotation=45)
        plt.grid(True)

        """Сохранение таблицы"""
        plt.savefig(f'picture.png')

        """Сохранение файла"""
        with open(f'rates', 'w') as file:
            for date, rate in zip(dates, rates):
                file.write(f'{date}\t{10}\t{rate}\n')
        plt.show()

        return print(f"График и файл сохранены")


def main():
    url_1 = 'https://cbr.ru/currency_base/daily/'
    # CZK_curs = find_currency(data_curs_CZK)

    """if CZK_curs:
        change_CZK_to_RUB(15, CZK_curs)
        change_RUB_to_CZK(100, CZK_curs)"""
    # Пример использования
    start_date = input("Введите первую дату: ")
    end_date = input("Введите вторую дату: ")
    get_currency_data(start_date, end_date)


if __name__ == '__main__':
    main()
