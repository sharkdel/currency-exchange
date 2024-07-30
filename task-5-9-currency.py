import sqlite3
import requests

currencies = ['RUB', 'USD', 'EUR']
apikey = '?apikey='
url = 'https://api.freecurrencyapi.com/v1/latest'
user = [1]      # Пользователь не меняется, работает только для пользователя с id = 1


def user_data(user_id):
    """Выводим данные обо всех счетах пользователя"""
    cur.execute("""SELECT * FROM users_balance WHERE UserID = ?;""", user_id)
    user_counts = cur.fetchall()
    print(f"Пользователь: {user_counts[0][0]} имеет на счетах: {round(user_counts[0][1], 2)} RUB, "
          f"{round(user_counts[0][2], 2)} USD, {round(user_counts[0][3], 2)} EUR")
    return user_counts


def amount_money(total_func, name_currency_instead_func):
    """Определяет есть ли у пользователя на счете необходимое количество денег в определенной валюте"""
    result = user_data(user)
    if name_currency_instead_func == currencies[0]:
        if result[0][1] >= total_func:
            return result[0][1] - total_func
        else:
            return print("Недостаточно средств")
    elif name_currency_instead_func == currencies[1]:
        if result[0][2] >= total:
            return result[0][2] - total
        else:
            return print("Недостаточно средств")
    elif name_currency_instead_func == currencies[2]:
        if result[0][3] >= total:
            return result[0][3] - total
        else:
            return print("Недостаточно средств")
    else:
        print("Такого счета нет.")


def get_currency_select(currency, base_currency):
    """Функция получает текущий курс в выбранной валюте"""

    # currency = '&currencies=RUB&base_currency=EUR'   # 1 евро к рублю
    currency_1 = currency  # 1 евро к рублю
    currency_2 = base_currency  # 1 евро к рублю
    url_all = url + apikey + '&currencies=' + currency_1 + '&base_currency=' + currency_2
    currency_course = requests.get(url_all).json()
    return currency_course['data'][currency]


def exchange_money(user_amount_func, name_currency_instead_func, name_currency_choice_func):
    """Функция высчитывает какая сумма будет по текущему курсу в выбранной валюте"""
    count_exchange = user_amount_func * get_currency_select(name_currency_instead_func, name_currency_choice_func)
    return count_exchange


def take_money(money, change_money, name_currency_instead, name_currency_choice):
    """Функция списывает со счета пользователя выбранную сумму для обмена валюты"""
    result = user_data(user)     # Берем конкретного пользователя и его счета
    if name_currency_instead == currencies[0]:  # рубли
        if name_currency_choice == currencies[1]:  # доллары
            update_params = (result[0][1] - change_money, result[0][2] + money, int(result[0][0]))
            cur.execute("""UPDATE users_balance SET Balance_RUB =?, Balance_USD =? WHERE UserID = ?;""", update_params)
            db.commit()
            print("Измение данных в таблице. Произведен обмен рублей на доллары.")
        elif name_currency_choice == currencies[2]:  # евро
            update_params = (result[0][1] - change_money, result[0][3] + money, int(result[0][0]))
            cur.execute("""UPDATE users_balance SET Balance_RUB =?, Balance_EUR =? WHERE UserID = ?;""", update_params)
            db.commit()
            print("Измение данных в таблице. Произведен обмен рублей на евро.")
    elif name_currency_instead == currencies[1]:  # доллары
        print("here")
        if name_currency_choice == currencies[0]:  # рубли
            update_params = (result[0][2] - change_money, result[0][1] + money, int(result[0][0]))
            cur.execute("""UPDATE users_balance SET Balance_USD =?, Balance_RUB =? WHERE UserID = ?;""", update_params)
            db.commit()
            print("Измение данных в таблице. Произведен обмен долларов на рубли.")
        elif name_currency_choice == currencies[2]:  # евро
            update_params = (result[0][2] - change_money, result[0][3] + money, int(result[0][0]))
            cur.execute("""UPDATE users_balance SET Balance_USD =?, Balance_EUR =? WHERE UserID = ?;""", update_params)
            db.commit()
            print("Измение данных в таблице. Произведен обмен долларов на евро.")
    elif name_currency_instead == currencies[2]:  # евро
        if name_currency_choice == currencies[0]:  # рубли
            update_params = (result[0][3] - change_money, result[0][1] + money, int(result[0][0]))
            cur.execute("""UPDATE users_balance SET Balance_EUR =?, Balance_RUB =? WHERE UserID = ?;""", update_params)
            db.commit()
            print("Измение данных в таблице. Произведен обмен евро на рубли.")
        elif name_currency_choice == currencies[1]:  # доллары
            update_params = (result[0][3] - change_money, result[0][2] + money, int(result[0][0]))
            cur.execute("""UPDATE users_balance SET Balance_EUR =?, Balance_USD =? WHERE UserID = ?;""", update_params)
            db.commit()
            print("Измение данных в таблице. Произведен обмен евро на доллары.")


"""Создание новой базы данных. На каждую базу данных должно быть свое подключение, иначе будет ошибка!"""
db = sqlite3.connect('exchanger.db')  # Создание базы данных
print("Подключились к базе данных")
cur = db.cursor()  # переменная для управления базой данных

"""Создание таблицы"""
cur.execute("""CREATE TABLE IF NOT EXISTS users_balance(
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    Balance_RUB FLOAT,
    Balance_USD FLOAT,
    Balance_EUR FLOAT);
""")
db.commit()  # Сохранение запроса
print("Создание таблицы users_balance")

"""Добавить пользователя с данными 100000, 1000, 1000"""
data_user = (100000, 1000, 1000)
cur.execute("""INSERT INTO users_balance(Balance_RUB, Balance_USD, Balance_EUR)
    VALUES(?, ?, ?);""", data_user)
db.commit()
print("Добавление пользователя с данными в таблицу")


print("Добро пожаловать в наш обменный пункт, курс валют следующий:")
print(f"1 USD = {get_currency_select('RUB', 'USD')} RUB")
print(f"1 EUR = {get_currency_select('RUB', 'EUR')} RUB")
print(f"1 USD = {get_currency_select('EUR', 'USD')} EUR")
print(f"1 EUR = {get_currency_select('USD', 'EUR')} USD")
print("Введите цифру валюты которую желаете получить: \n1. RUB\n2. USD\n3. EUR\nВаш выбор: ", end="")
user_choice = input()
if user_choice in ["1", "2", "3"]:      # Если выбор первой валюты верен
    if user_choice == "1":
        name_currency_choice = currencies[0]
    elif user_choice == "2":
        name_currency_choice = currencies[1]
    elif user_choice == "3":
        name_currency_choice = currencies[2]
    print("Какая сумма вас интересует?\nВведите: ", end="")
    while True:
        try:
            user_amount = int(input())
            break
        except ValueError:
            print("Сумма указывается в цифрах!")
    print("Какую валюту готовы предложить взамен? \n1. RUB\n2. USD\n3. EUR\nВаш выбор: ", end="")
    user_choice_instead = input()
    if user_choice_instead in ["1", "2", "3"]:      # Если выбор второй валюты верен
        if user_choice_instead == user_choice:
            name_currency_instead = name_currency_choice
            print("Обмен одинаковых валют невозможен.")
        elif user_choice_instead == "1":
            name_currency_instead = currencies[0]
        elif user_choice_instead == "2":
            name_currency_instead = currencies[1]
        elif user_choice_instead == "3":
            name_currency_instead = currencies[2]
    else:
        name_currency_instead = "0"     # Если выбор второй валюты не соответствует
        print("Ваш ввод не соответствует цифрам 1, 2, 3.")
    if name_currency_instead in currencies and user_amount > 0 and name_currency_instead != name_currency_choice:
        total = exchange_money(user_amount, name_currency_instead, name_currency_choice)
        print(f"Для получения {user_amount} {name_currency_choice} на вашем счете должно быть {round(total, 2)} "
              f"{name_currency_instead} ")
        change_money = amount_money(total, name_currency_instead)       # Определяем есть ли необходимое количество денег
        if change_money:
            print(
                f"На вашем {name_currency_instead} счете достаточно денег. После обмена, на нем останется {round(change_money, 2)} "
                f"{name_currency_instead} "
                "\nНажмите 'y', если желаете произвести обмен.")
            print("Ваш выбор: ", end="")
            select = input()
            if select == 'y':
                take_money(user_amount, total, name_currency_instead, name_currency_choice)     # Производим обмен
                user_data(user)      # Пользователь не меняется, работает только для пользователя с id = 1
            else:
                print("Выход. Обмен не произведен.")
    elif user_amount <= 0:      # Если введенная сумма меньше или равна нулю
        print("Отрицательная или нулевая сумма. Обмен не возможен.")
else:       # Выбор валюты которую желаете получить
    print("Ваш ввод не соответствует цифрам 1, 2, 3.")