import sqlite3


# Подключение к БД
connection = sqlite3.connect('shop.db', check_same_thread=False)
#Связь между Python и SQL
sql = connection.cursor()


# Создание таблицы пользователей
sql.execute('CREATE TABLE IF NOT EXISTS users ('
            'id INTEGER, '
            'name TEXT, '
            'number TEXT, '
            'location TEXT);')
# Создание таблицы продуктов
sql.execute('CREATE TABLE IF NOT EXISTS products ('
            'pr_id INTEGER PRIMARY KEY AUTOINCREMENT, '
            'pr_name TEXT, '
            'pr_count INTEGER, '
            'pr_description TEXT, '
            'pr_price REAL, '
            'pr_photo TEXT);')
# Создание таблицы корзины
sql.execute('CREATE TABLE IF NOT EXISTS cart('
            'id INTEGER, '
            'user_pr_name TEXT, '
            'user_pr_count INTEGER, '
            'total REAL);')


## Методы для пользователя ##
# Проверка на наличие юзера в БД
def check_user(id):
    check = sql.execute('SELECT * FROM users WHERE id=?;', (id,))
    if check.fetchone():
        return True
    else:
        return False


# Регистрация пользователя
def register(id, name, number, location):
    sql.execute('INSERT INTO users VALUES(?, ?, ?, ?);', (id, name, number, location))
    # Фиксируем изменения
    connection.commit()


## Методы для продуктов ##
# Сторона пользователя
#
def get_pr():
    return sql.execute('SELECT pr_id, pr_name, pr_count FROM products;').fetchall()



# Вывод информации о конкретном продукте
def get_exact_pr(pr_id):
    return sql.execute('SELECT pr_name, pr_description, pr_count, pr_price, pr_photo FROM products WHERE pr_id=?;', (pr_id,)).fetchone()


# Добавление товара в корзину
def add_pr_to_cart(user_id, user_pr, user_pr_count, total):
    sql.execute('INSERT INTO cart VALUES(?, ?, ?, ?);', (user_id, user_pr, user_pr_count, total))
    connection.commit()


# Сторона админа
def add_pr(pr_name, pr_description, pr_count, pr_price, pr_photo):
    sql.execute('INSERT INTO products(pr_name, pr_description, pr_count, pr_price, pr_photo) '
                'VALUES(?, ?, ?, ?, ?);', (pr_name, pr_description, pr_count, pr_price, pr_photo))
    connection.commit()


def del_pr(pr_id):
    sql.execute('DELETE FROM products WHERE pr_id=?;', (pr_id,))
    connection.commit()


def change_pr_count(pr_id, new_count):
    current_count = sql.execute('SELECT pr_count FROM products WHERE pr_id=?;', (pr_id,)).fetchone()
    new_current_count = current_count[0] + new_count
    sql.execute('UPDATE products SET pr_count=? WHERE pr_id=?;', (new_current_count, pr_id))
    connection.commit()


def get_pr_name_id():
    prods = sql.execute('SELECT pr_id, pr_count FROM products;').fetchall()
    all_prods = [i[0] for i in prods if i[1] > 0]
    return all_prods


def check_pr():
    if sql.execute('SELECT * FROM products;').fetchall():
        return True
    else:
        return False


def check_pr_id(id):
    if sql.execute('SELECT pr_id FROM products WHERE id=?;', (pr_id,)).fetchone():
        return True
    else:
        return False


## Методы для корзины ##
# Отображение
def show_cart(user_id):
    return sql.execute('SELECT id, user_pr_name, user_pr_count, total FROM cart WHERE id=?;', (user_id,)).fetchone()


def clear_cart(user_id):
    sql.execute('DELETE FROM cart WHERE id=?;', (user_id,))
    connection.commit()


def make_order(user_id):
    pr_name = sql.execute('SELECT user_pr_name FROM cart WHERE id=?;', (user_id,)).fetchone()
    amount = sql.execute('SELECT user_pr_count FROM cart WHERE id=?;', (user_id,)).fetchone()
    current_count = sql.execute('SELECT pr_count FROM products WHERE pr_name=?;', (pr_name[0],)).fetchone()
    sql.execute('UPDATE products SET pr_count=? WHERE pr_name=?;', (current_count[0] - amount[0], pr_name[0]))
    info = sql.execute('SELECT * FROM cart WHERE id=?;', (user_id,)).fetchone()
    address = sql.execute('SELECT location FROM users WHERE id=?;', (user_id,)).fetchone()
    connection.commit()
    return info, address


