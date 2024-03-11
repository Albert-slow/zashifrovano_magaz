from telebot import types


# Кнопка отправки номера
def num_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    number = types.KeyboardButton('Отправить номер', request_contact=True)
    kb.add(number)
    return kb


# Кнопка отправки локации
def loc_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    location = types.KeyboardButton('Отправить локацию', request_location=True)
    kb.add(location)
    return kb


def admin_buttons():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    add_pr = types.KeyboardButton('Добавить продукт')
    del_pr = types.KeyboardButton('Удалить продукт')
    edit_pr = types.KeyboardButton('Изменить количество продукта')
    to_menu = types.KeyboardButton('Перейти в меню')
    kb.add(add_pr, edit_pr, del_pr)
    kb.row(to_menu)
    return kb


# создаём кнопки вывода товара
def main_menu_buttons(all_prods):
    kb = types.InlineKeyboardMarkup(row_width=2)
    cart = types.InlineKeyboardButton(text='Корзина', callback_data='cart')
    prod_buttons = [types.InlineKeyboardButton(text=f'{i[1]}', callback_data=f'{i[0]}') for i in all_prods if i[2] > 0]
    kb.add(*prod_buttons)
    kb.row(cart)
    return kb


# Кнопки с выбором количества
def count_buttons(amount=1, plus_or_minus=''):
    kb = types.InlineKeyboardMarkup(row_width=3)
    minus = types.InlineKeyboardButton(text='-', callback_data='decrement')
    current_amount = types.InlineKeyboardButton(text=str(amount), callback_data=amount)
    plus = types.InlineKeyboardButton(text='+', callback_data='increment')
    to_cart = types.InlineKeyboardButton(text='Добавить в корзину', callback_data='to_cart')
    back = types.InlineKeyboardButton(text='Назад', callback_data='back')
    if plus_or_minus == 'increment':
        amount += 1
        current_amount = types.InlineKeyboardButton(text=str(amount), callback_data=amount)
    elif plus_or_minus == 'decrement':
        if amount > 1:
            amount -= 1
            current_amount = types.InlineKeyboardButton(text=str(amount), callback_data=amount)
    kb.add(minus, current_amount, plus)
    kb.row(to_cart)
    kb.row(back)
    return kb

def cart_buttons():
    kb = types.InlineKeyboardMarkup(row_width=2)
    order = types.InlineKeyboardButton(text='Оформить заказ', callback_data='order')
    back = types.InlineKeyboardButton(text='Назад', callback_data='back')
    clear = types.InlineKeyboardButton(text='Очистить корзину', callback_data='clear')
    kb.add(clear, back)
    kb.row(order)
    return kb
