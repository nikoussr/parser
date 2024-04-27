import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth



def req(url: str):
    '''Парсит код страницы'''
    response = requests.get(url)
    data = response.text
    return data


def find_currency(data):
    """Находит курс кроны"""
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


def change_CZK_to_RUB(CZK, CZK_curs):
    """Перевод крон в рубли"""
    return print(f"{CZK} чешских крон = {(CZK * CZK_curs).__round__(5)} рублей")


def change_RUB_to_CZK(RUB, CZK_curs):
    """Перевод рублей в кроны"""
    return print(f"{RUB} рублей = {(RUB / CZK_curs).__round__(5)} чешских крон")


def get_currency_data(start_date: str, end_date: str):
    """"""
    url = f'https://www.cbr.ru/currency_base/dynamics/?UniDbQuery.Posted=True&UniDbQuery.mode=1&UniDbQuery.date_req1=&UniDbQuery.date_req2=&UniDbQuery.VAL_NM_RQ=R01760&UniDbQuery.From={start_date}&UniDbQuery.To={end_date}'
    response = requests.get(url)
    dates = []  # массив для дат
    rates = []  # массив для курса

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', class_='data')

        if table:
            rows = table.find_all('tr')

            # print(f"Дата\t\tКоличество\tЦена")
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 3:
                    date = cols[0].text
                    count = cols[1].text
                    rate = float(cols[2].text.replace(',', '.'))
                    dates.append(date)
                    rates.append(rate)
                    # print(f'{date}\t {count}\t\t {rate}')

        """Строим таблицу"""
        plt.figure(figsize=(12, 6))
        plt.plot(dates, rates, marker='o', color='b')
        plt.title('Динамика курса чешской кроны')
        plt.xlabel('Дата')
        plt.ylabel('Курс чешской кроны за 10 ед. руб.')
        plt.xticks(rotation=45)
        plt.grid(True)

        print('Сохранение данных, подождите...')

        """Сохранение графика"""
        plt.savefig('currency_chart.png')
        save_to_google_drive('currency_chart.png', 'currency_chart.png')

        """Сохранение файла"""
        with open(f'currency_data.txt', 'w') as file:
            for date, rate in zip(dates, rates):
                file.write(f'{date}\t{10}\t{rate}\n')
        save_to_google_drive('currency_data.txt', 'currency_data.txt')
        plt.show()

        return print(f"График и файл сохранены")
def save_to_google_drive(file_path, file_name):
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # Аутентификация через локальный веб-сервер
    drive = GoogleDrive(gauth)

    file = drive.CreateFile({'title': file_name})
    file.SetContentFile(file_path)
    file.Upload()



def main():
    url_1 = 'https://cbr.ru/currency_base/daily/'
    while True:
        print('Выберите действие:')
        print('1. Перевод CZK в RUB')
        print('2. Перевод RUB в CZK')
        print('3. Получить историю курса валюты')
        print('0. Выход\n')
        choice = input('Введите номер действия: ')
        print('=' * 80)

        if choice == '1':
            print("Для выхода - 0")
            data_curs_CZK = req(url_1)
            CZK_curs = find_currency(data_curs_CZK)
            while True:
                if CZK_curs:
                    CZK_count = float(input("Введите количество крон: "))
                    if CZK_count == 0:
                        print('=' * 80)
                        break
                    change_CZK_to_RUB(CZK_count, CZK_curs)

        elif choice == '2':
            print("Для выхода - 0")
            data_curs_CZK = req(url_1)
            CZK_curs = find_currency(data_curs_CZK)
            while True:
                if CZK_curs:
                    RUB_count = float(input("Введите количество рублей: "))
                    if RUB_count == 0:
                        print('=' * 80)
                        break
                    change_RUB_to_CZK(RUB_count, CZK_curs)

        elif choice == '3':
            start_date = input('Введите начальную дату (в формате dd_mm_yyyy): ')
            end_date = input('Введите конечную дату (в формате dd_mm_yyyy): ')
            get_currency_data(start_date, end_date)
            print('=' * 80)
        elif choice == '0':
            print('Выход из программы.')
            break
        else:
            print('Некорректный ввод. Пожалуйста, выберите 1 или 2.')


if __name__ == '__main__':
    main()
