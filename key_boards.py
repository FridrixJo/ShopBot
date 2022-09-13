from aiogram import types
from db_class import DBCommands


def reply_markup_captcha(captcha_list: list):
    kb = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True, one_time_keyboard=True)
    for i in captcha_list:
        btn = types.KeyboardButton(text=i[0])
        kb.add(btn)

    return kb


def inline_markup_captcha():
    kb = types.InlineKeyboardMarkup(row_width=1)

    btn = types.InlineKeyboardButton('Продолжить', callback_data='get_captcha')

    kb.add(btn)

    return kb


def inline_markup_menu():
    kb = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton('Покупка 🛒', callback_data='buy')
    btn2 = types.InlineKeyboardButton('Товары 🧾', callback_data='price_list')
    btn3 = types.InlineKeyboardButton('Работа ', callback_data='work')
    btn4 = types.InlineKeyboardButton('Помощь 🆘', callback_data='support')

    kb.add(btn1, btn2, btn3, btn4)

    return kb


def inline_markup_admin_menu():
    kb = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton('Установить текст МЕНЮ', callback_data='set_menu_text')
    btn2 = types.InlineKeyboardButton('Установить текст ПОДДЕРЖКА', callback_data='set_support_text')
    btn3 = types.InlineKeyboardButton('Установить текст РАБОТА', callback_data='set_work_text')
    btn4 = types.InlineKeyboardButton('Установить BTC Wallet', callback_data='set_btc_wallet')
    btn5 = types.InlineKeyboardButton('Товары', callback_data='products')
    btn6 = types.InlineKeyboardButton('Locations', callback_data='locations')
    btn7 = types.InlineKeyboardButton('Рассылка пользователям', callback_data='sharing')
    btn8 = types.InlineKeyboardButton('Добавить модератора', callback_data='add_moderator')
    btn9 = types.InlineKeyboardButton('Главное меню', callback_data='main_menu')

    kb.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9)

    return kb


async def inline_markup_products_list(db: DBCommands):
    kb = types.InlineKeyboardMarkup(row_width=1)

    for i in await db.get_all_products():
        btn = types.InlineKeyboardButton(text=str(i[0]), callback_data=str(i[0]))
        kb.add(btn)

    btn1 = types.InlineKeyboardButton(text='Добавить товар ➕', callback_data='add_product')
    btn2 = types.InlineKeyboardButton(text='Назад ↩', callback_data='back')

    kb.add(btn1, btn2)

    return kb


async def inline_markup_products_list_client(db: DBCommands):
    kb = types.InlineKeyboardMarkup(row_width=1)

    for i in await db.get_all_products():
        btn = types.InlineKeyboardButton(text=str(i[0]), callback_data=str(i[0]))
        kb.add(btn)

    btn = types.InlineKeyboardButton(text='Назад ↩', callback_data='back')

    kb.add(btn)

    return kb


async def inline_markup_locations_list(db: DBCommands):
    kb = types.InlineKeyboardMarkup(row_width=1)

    for i in await db.get_all_locations():
        btn = types.InlineKeyboardButton(text=str(i[0]), callback_data=str(i[0]))
        kb.add(btn)

    btn1 = types.InlineKeyboardButton(text='Добавить локацию ➕', callback_data='add_location')
    btn2 = types.InlineKeyboardButton(text='Назад ↩', callback_data='back')

    kb.add(btn1, btn2)

    return kb


async def inline_markup_locations_list_client(db: DBCommands):
    kb = types.InlineKeyboardMarkup(row_width=1)

    for i in await db.get_all_locations():
        btn = types.InlineKeyboardButton(text=str(i[0]), callback_data=str(i[0]))
        kb.add(btn)

    btn = types.InlineKeyboardButton(text='Назад ↩', callback_data='back')

    kb.add(btn)

    return kb


async def inline_markup_categories_by_product_client(db: DBCommands, product_name: str):
    kb = types.InlineKeyboardMarkup(row_width=1)

    for i in await db.get_all_categories_by_product_name(product_name):
        btn = types.InlineKeyboardButton(text=str(i[0]), callback_data=str(i[0]))
        kb.add(btn)

    btn = types.InlineKeyboardButton(text='Назад ↩', callback_data='back')

    kb.add(btn)

    return kb


async def inline_markup_categories_by_product_admin(db: DBCommands, product_name: str):
    kb = types.InlineKeyboardMarkup(row_width=1)

    for i in await db.get_all_categories_by_product_name(product_name):
        btn = types.InlineKeyboardButton(text=str(i[0]), callback_data=str(i[0]))
        kb.add(btn)

    btn1 = types.InlineKeyboardButton(text='Добавить категорию ➕', callback_data='add_category')
    btn2 = types.InlineKeyboardButton(text='Назад ↩', callback_data='back')

    kb.add(btn1, btn2)

    return kb


def inline_markup_product_opportunities():
    kb = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton('Редактировать название товара', callback_data='edit_name')
    btn2 = types.InlineKeyboardButton('Редактировать описание товара', callback_data='edit_description')
    btn3 = types.InlineKeyboardButton('Редактировать фото товара', callback_data='edit_photo')
    btn4 = types.InlineKeyboardButton('Удалить товар', callback_data='delete_product')
    btn5 = types.InlineKeyboardButton('Категории', callback_data='categories')
    btn6 = types.InlineKeyboardButton('Назад ↩️', callback_data='back')

    kb.add(btn1, btn2, btn3, btn4, btn5, btn6)

    return kb


def inline_markup_locations_opportunities():
    kb = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton('Редактировать локацию', callback_data='edit_location')
    btn2 = types.InlineKeyboardButton('Удалить локацию', callback_data='delete_location')
    btn3 = types.InlineKeyboardButton('Назад ↩️', callback_data='back')

    kb.add(btn1, btn2, btn3)

    return kb


def inline_markup_categories_opportunities():
    kb = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton('Редактировать название категории', callback_data='edit_category')
    btn2 = types.InlineKeyboardButton('Редактировать цену', callback_data='edit_price')
    btn3 = types.InlineKeyboardButton('Удалить категорию', callback_data='delete_category')
    btn4 = types.InlineKeyboardButton('Назад ↩️', callback_data='back')

    kb.add(btn1, btn2, btn3, btn4)

    return kb


def inline_markup_sure():
    kb = types.InlineKeyboardMarkup(row_width=2)

    btn1 = types.InlineKeyboardButton('Да, удалить', callback_data='yes')
    btn2 = types.InlineKeyboardButton('Нет, оставить', callback_data='no')

    kb.add(btn1, btn2)

    return kb


def inline_markup_edit():
    kb = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton('Редактировать описание', callback_data='edit')
    btn2 = types.InlineKeyboardButton('Назад ↩️', callback_data='back')

    kb.add(btn1, btn2)

    return kb


def inline_markup_edit_options():
    kb = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton('Редактировать', callback_data='edit')
    btn2 = types.InlineKeyboardButton('Назад ↩️', callback_data='back')

    kb.add(btn1, btn2)

    return kb


def inline_markup_client_choice():
    kb = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton('Продолжить ➡', callback_data='continue')
    btn2 = types.InlineKeyboardButton('Начать сначала', callback_data='back')

    kb.add(btn1, btn2)

    return kb


def inline_markup_client_order():
    kb = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton('Я оплатил(а)', callback_data='success')
    btn2 = types.InlineKeyboardButton('Отменить заказ', callback_data='back')

    kb.add(btn1, btn2)

    return kb


def inline_markup_back(text):
    kb = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text + ' ↩️', callback_data='back')

    kb.add(btn1)

    return kb


def inline_markup_products_back():
    kb = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton('На главное меню ↩️', callback_data='products_back')

    kb.add(btn1)

    return kb


def reply_markup_call_off(text):
    kb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton(text=text)

    kb.add(btn1)

    return kb


def reply_markup_back_or_menu(btn1_text, btn2_text):
    kb = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton(text=btn1_text)
    btn2 = types.KeyboardButton(text=btn2_text)

    kb.add(btn1, btn2)

    return kb


def inline_markup_ok():
    kb = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton('OK ✅', callback_data='ok')

    kb.add(btn1)

    return kb


def inline_markup_check_request():
    kb = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton('ОТВЕТИТЬ НА ЗАЯВКУ', callback_data='get_request')

    kb.add(btn1)

    return kb


def inline_markup_request_opps():
    kb = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton('Одобрить заявку ✅', callback_data='approve')
    btn2 = types.InlineKeyboardButton('Отклонить заявку ❌', callback_data='reject')

    kb.add(btn1, btn2)

    return kb


def inline_markup_reject():
    kb = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton('Да, отклонить заявку ❌', callback_data='sure_reject')
    btn2 = types.InlineKeyboardButton('Заблокировать этого клиента', callback_data='block')

    kb.add(btn1, btn2)

    return kb

