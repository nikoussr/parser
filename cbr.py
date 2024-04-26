import requests
from bs4 import BeautifulSoup
from selenium import webdriver as wd


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


"""def currency_history(url): # 2
    date_1 = str(input("Введите первую дату: "))
    date_2 = str(input("Введите вторую дату: "))
    url = url[0] + date_1 + url[1] + date_2
    return req(url)
    Использовалось для поиска информации по датам из ввода. Всё равно выводит за последнюю неделю"""


def find_currency_history(data):  # 2
    bs = BeautifulSoup(data, "html.parser")
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
        print(f"{i[0]}\t{i[1]}\t\t{i[2]}")


def main():
    url_1 = 'https://cbr.ru/currency_base/daily/'
    url_2 = 'https://cbr.ru/currency_base/dynamics/?UniDbQuery.Posted=True&UniDbQuery.so=1&UniDbQuery.mode=1&UniDbQuery.date_req1=&UniDbQuery.date_req2=&UniDbQuery.VAL_NM_RQ=R01760&UniDbQuery.From=20.04.2024&UniDbQuery.To=44.04.2024'
    """data_curs_CZK = req(url_1)
    CZK_curs = find_currency(data_curs_CZK)"""

    """if CZK_curs:
        change_CZK_to_RUB(15, CZK_curs)
        change_RUB_to_CZK(100, CZK_curs)"""
    data_history_CZK = req(url_2)
    find_currency_history(data_history_CZK)


if __name__ == '__main__':
    main()
