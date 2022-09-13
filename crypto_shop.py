import time

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import types

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

import asyncio

import random

import string

from key_boards import *

from config import *

from sql import *

from db_class import DBCommands


class FSMClient(StatesGroup):
    products_client = State()
    choose_product = State()
    choose_category = State()
    choose_location = State()
    client_choice = State()
    order = State()


class FSMCaptcha(StatesGroup):
    get_captcha = State()
    input_captcha = State()


class FSMAdmin(StatesGroup):
    opportunities = State()
    input_data = State()

    products = State()
    products_opps = State()
    edit_product = State()
    add_product = State()

    locations = State()
    locations_opps = State()
    edit_location = State()
    add_location = State()

    categories = State()
    categories_opps = State()
    edit_category = State()
    add_category = State()

    sure = State()


class FSMModeratorReply(StatesGroup):
    request_id = State()
    choice = State()
    photo = State()
    caption = State()


loop = asyncio.get_event_loop()

db = loop.run_until_complete(create_pool())

data_base = DBCommands(db)

storage = MemoryStorage()

bot = Bot(token=TOKEN)

dispatcher = Dispatcher(bot=bot, storage=storage)


ADMIN_IDS = [int(admin_id)]


captcha_list = [
    ['v328j', 'AgACAgEAAxkBAAIB22LbCjNDq8FD69GXguRlzk9ZmT1SAAIHqzEbBUzZRqSaBJsgtJlmAQADAgADeAADKQQ'],
    ['1nIQm', 'AgACAgEAAxkBAAIB3GLbCj50nobWir4jDOUKe2L_hjnQAAIIqzEbBUzZRkxEPLsS0GD7AQADAgADeAADKQQ'],
    ['YJNYB', 'AgACAgEAAxkBAAIB3WLbCkq2P49n7tqIFSTwL6deICC3AAIJqzEbBUzZRldolPZeshXhAQADAgADeAADKQQ'],
    ['2q9qC', 'AgACAgEAAxkBAAIB3mLbCl7mB8g4Cx13njKHgCrsbjcLAAIKqzEbBUzZRhUKgVauS1VmAQADAgADeAADKQQ'],
    ['FHtqB', 'AgACAgEAAxkBAAIB32LbDDvrHfojYnB1q225niWFlkALAAIOqzEbBUzZRmrhcUIixteDAQADAgADeAADKQQ'],
    ['Tbvuy', 'AgACAgEAAxkBAAIB4GLbDGrhwe8FZnoqInW91ONGcXsMAAIPqzEbBUzZRtyjR0GXwuL6AQADAgADeAADKQQ'],
    ['fwiXp', 'AgACAgEAAxkBAAIB4WLbDLm8qOLnMpo8wOdhkWQ6-hn6AAIQqzEbBUzZRrTU5UyccGcgAQADAgADeAADKQQ'],
    ['hOvgd', 'AgACAgEAAxkBAAIB4mLbDNP3hg9qNS8rEPd69qkI5WOuAAIRqzEbBUzZRhIKV3b5m2pzAQADAgADeAADKQQ'],
    ['AJknE', 'AgACAgEAAxkBAAIB42LbDQJkhW_YhyWn8aWW0MyG0nROAAISqzEbBUzZRtZmnW-MR2S8AQADAgADeAADKQQ'],
    ['X7k2u', 'AgACAgEAAxkBAAIB5GLbDTPvH-yoNEpq2_qqBxRYdZbAAAITqzEbBUzZRu26xMgeIWbpAQADAgADeAADKQQ'],
    ['ykPQC', 'AgACAgEAAxkBAAIB5WLbDV3Ulg-aq6QDDWDXCQGKp6kXAAIUqzEbBUzZRjv7htTHxlmfAQADAgADeAADKQQ'],
    ['YPcgl', 'AgACAgEAAxkBAAIB5mLbDYj1JM3eD46jC_4F_7h6KT0TAAIVqzEbBUzZRuSgciiUePcLAQADAgADeAADKQQ'],
]


def get_name(message: types.Message):
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username
    name = ''
    if first_name is not None:
        name += first_name
        name += ' '
    if last_name is not None:
        name += last_name
        name += ' '
    if username is not None:
        name += '@'
        name += username

    return name


async def clear_state(state: FSMContext):
    try:
        current_state = state.get_state()
        if current_state is not None:
            await state.finish()
    except Exception as error:
        print(error)


@dispatcher.message_handler(Text(equals='назад', ignore_case=True), state=[FSMAdmin.input_data, FSMAdmin.add_product, FSMAdmin.edit_product, FSMAdmin.add_category, FSMAdmin.edit_category, FSMAdmin.add_location, FSMAdmin.edit_location])
async def cancel_handler(message: types.Message, state: FSMContext):
    await clear_state(state)
    await bot.send_message(message.chat.id, 'Действие отменено', reply_markup=types.ReplyKeyboardRemove())
    await send_moderator_menu(message)
    await FSMAdmin.opportunities.set()


@dispatcher.message_handler(commands=['start'])
async def start(message: types.Message):
    if not await data_base.user_exists(str(message.chat.id)):

        text = 'Пройдите каптчу для подтверждения, что вы не робот'
        await bot.send_message(message.chat.id, text, reply_markup=inline_markup_captcha())
        await FSMCaptcha.get_captcha.set()
    else:
        await send_menu(message)


@dispatcher.callback_query_handler(state=FSMCaptcha.get_captcha)
async def get_captcha(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'get_captcha':

        n = random.randrange(0,12)

        async with state.proxy() as file:
            file['number'] = n

        text = 'Введите текст с картины для подтвержения, что вы не робот 🤖'
        await bot.send_photo(chat_id=call.message.chat.id, photo=captcha_list[n][1])
        await bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=reply_markup_captcha(captcha_list))
        await FSMCaptcha.input_captcha.set()


@dispatcher.message_handler(content_types=['text'], state=FSMCaptcha.input_captcha)
async def input_captcha(message: types.Message, state: FSMContext):
    async with state.proxy() as file:
        n = file['number']
    if message.text == captcha_list[n][0]:
        await data_base.add_user(str(message.chat.id), get_name(message))

        for i in ADMIN_IDS:
            text = f'Пользователь {str(await data_base.get_name(str(message.chat.id)))} перешел в бота'
            try:
                await bot.send_message(i, text=text)
            except Exception as e:
                print(e)
        await bot.send_message(chat_id=message.chat.id, text='Каптча пройдена, вы авторизованы', reply_markup=types.ReplyKeyboardRemove())
        await clear_state(state)
        await send_menu(message)
    else:
        n = random.randrange(0,12)

        async with state.proxy() as file:
            file['number'] = n

        text = 'Введите текст с картины для подтвержения, что вы не робот 🤖'
        await bot.send_photo(chat_id=message.chat.id, photo=captcha_list[n][1])
        await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=reply_markup_captcha(captcha_list))
        await FSMCaptcha.input_captcha.set()


@dispatcher.message_handler(commands=['captcha'])
async def get_photo(message: types.Message):
    for i in captcha_list:
        await bot.send_photo(chat_id=message.chat.id, photo=i[1], caption=i[0])


@dispatcher.message_handler(commands=['menu'])
async def start(message: types.Message):
    await send_menu(message)


@dispatcher.message_handler(commands=['moderator'], state=['*'])
async def start_moderator(message: types.Message, state: FSMContext):
    for i in ADMIN_IDS:
        if message.chat.id == i:
            await clear_state(state)
            await send_moderator_menu(message)
            await FSMAdmin.opportunities.set()


async def send_menu(message: types.Message):
    text = await data_base.get_statement_menu()
    if text is None:
        text = 'Главное меню'
    await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=inline_markup_menu(), parse_mode='HTML')


async def edit_to_menu(message: types.Message):
    text = await data_base.get_statement_menu()
    if text is None:
        text = 'Главное меню'
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=text, reply_markup=inline_markup_menu(), parse_mode='HTML')


async def send_moderator_menu(message: types.Message):
    text = 'Меню модератора'
    await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=inline_markup_admin_menu())


async def edit_to_moderator_menu(message: types.Message):
    text = 'Меню модератора'
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=text, reply_markup=inline_markup_admin_menu())


@dispatcher.callback_query_handler()
async def client_opportunities(call: types.CallbackQuery):
    if call.data == 'buy':
        if not await data_base.request_user_exists(str(call.message.chat.id)):
            text = 'Выберите товар из списка 📎'
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=await inline_markup_products_list_client(data_base))
            await FSMClient.choose_product.set()
        else:
            text = 'У вас уже есть одна необработанная заявка, дождитесь пока модераторы ответят вам'
            await bot.send_message(call.message.chat.id, text)
            await send_menu(call.message)
    elif call.data == 'price_list':
        text = 'Cписок всех наших товаров 📎\nНажми на любой, чтобы узнать побольше'
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=await inline_markup_products_list_client(data_base))
        await FSMClient.products_client.set()
    elif call.data == 'support':
        text = await data_base.get_statement_support()
        if text is None:
            text = 'Данные о поддержке обновляются ℹ'
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=inline_markup_back('Назад'))
    elif call.data == 'work':
        text = await data_base.get_statement_work_text()
        if text is None:
            text = 'Данные о работе обновляются ℹ'
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=inline_markup_back('Назад'))
    elif call.data == 'back':
        await edit_to_menu(call.message)
    elif call.data == 'products_back':
        await send_menu(call.message)
    else:
        for i in ADMIN_IDS:
            if call.message.chat.id == i:
                if call.data == 'get_request':
                    text = 'Скопируйте и отправьте сюда номер заявки'
                    await bot.send_message(call.message.chat.id, text, reply_markup=reply_markup_call_off('Главное меню'))
                    await FSMModeratorReply.request_id.set()


@dispatcher.callback_query_handler(state=FSMClient.choose_product)
async def choose_product(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'back':
        await clear_state(state)
        await edit_to_menu(call.message)
    else:
        for i in await data_base.get_all_products():
            if call.data == str(i[0]):
                async with state.proxy() as file:
                    file['product'] = str(i[0])

                text = 'Выберите категорию товара'
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=await inline_markup_categories_by_product_client(data_base, str(i[0])))
                await FSMClient.choose_category.set()


@dispatcher.callback_query_handler(state=FSMClient.choose_category)
async def choose_product(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'back':
        await clear_state(state)
        await edit_to_menu(call.message)
    else:
        async with state.proxy() as file:
            product = file['product']
        for i in await data_base.get_all_categories_by_product_name(product):
            if call.data == str(i[0]):
                async with state.proxy() as file:
                    file['category'] = str(i[0])

                text = 'Выберите следующую категорию'
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=await inline_markup_locations_list_client(data_base))
                await FSMClient.choose_location.set()


@dispatcher.callback_query_handler(state=FSMClient.choose_location)
async def choose_product(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'back':
        await clear_state(state)
        await edit_to_menu(call.message)
    else:
        for i in await data_base.get_all_locations():
            if call.data == str(i[0]):
                async with state.proxy() as file:
                    file['location'] = str(i[0])
                    product = file['product']
                    category = file['category']

                text = 'Проверьте корректность вашего заказа' + '\n\n'
                text += f'Товар: <b>{product}</b>' + '\n'
                text += f'Категория: <b>{category}</b>' + '\n'
                text += f'Место: <b>{str(i[0])}</b>'

                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=inline_markup_client_choice(), parse_mode='HTML')
                await FSMClient.client_choice.set()


@dispatcher.callback_query_handler(state=FSMClient.client_choice)
async def choose_product(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'back':
        await clear_state(state)
        await edit_to_menu(call.message)
    else:
        async with state.proxy() as file:
            location = file['location']
            product = file['product']
            category = file['category']

        text = f'Отправьте <code>{await data_base.get_price(product, category)}</code> BTC на кошелек:' + '\n'
        text += f'<code>{await data_base.get_statement_btc_wallet()}</code>' + '\n\n'
        text += '<b>Подробности заказа:</b>' + '\n'
        text += f'Товар: <i>{product}</i>' + '\n'
        text += f'Категория: <i>{category}</i>' + '\n'
        text += f'Локация: <i>{location}</i>' + '\n\n'
        text += 'Только после оплаты нажмите на кнопку <b>"Я оплатил(а)"</b>, после этого с вами свяжутся'

        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=inline_markup_client_order(), parse_mode='HTML')
        await FSMClient.order.set()


@dispatcher.callback_query_handler(state=FSMClient.order)
async def handle_order(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'back':
        await clear_state(state)
    elif call.data == 'success':
        numb = ''.join(random.choice(string.digits) for _ in range(random.randrange(8, 16)))

        async with state.proxy() as file:
            location = file['location']
            product = file['product']
            category = file['category']

        name = await data_base.get_name(str(call.message.chat.id))

        await data_base.add_request(numb, str(call.message.chat.id), name)

        for i in ADMIN_IDS:
            text = f'Номер заявки: <code>{numb}</code>' + '\n\n'
            text += '<b>Подробности заказа:</b>' + '\n'
            text += f'Товар: <i>{product}</i>' + '\n'
            text += f'Категория: <i>{category}</i>' + '\n'
            text += f'Локация: <i>{location}</i>' + '\n'
            text += f'Цена: <i>{await data_base.get_price(product, category)} BTC</i>' + '\n\n'

            text += f'Имя клиента: {str(name)}'

            try:
                await bot.send_message(chat_id=i, text=text, parse_mode='HTML', reply_markup=inline_markup_check_request())
            except Exception as e:
                print(e)

        text = f'Ваша заявка #<code>{numb}</code> сейчас находится на расмотрении 🔎' + '\n'
        text += '<i>Ожидайте, с вами скоро свяжутся...</i>'
        await bot.send_message(call.message.chat.id, text, reply_markup=types.ReplyKeyboardRemove(), parse_mode='HTML')
        await clear_state(state)
        await send_menu(call.message)


@dispatcher.message_handler(state=FSMModeratorReply.request_id)
async def check_request_id(message: types.Message, state: FSMContext):
    if message.text == 'Главное меню':
        await bot.send_message(message.chat.id, 'Ок', reply_markup=types.ReplyKeyboardRemove())
        await clear_state(state)
        await send_menu(message)
    else:
        if await data_base.request_exists(message.text):
            async with state.proxy() as file:
                file['request_id'] = message.text

            await bot.send_message(chat_id=message.chat.id, text='Заявка найдена', reply_markup=types.ReplyKeyboardRemove())
            text = f'<code>{message.text}</code>\n\nЧто делаем с данной заявкой?'
            await bot.send_message(message.chat.id, text, reply_markup=inline_markup_request_opps(), parse_mode='HTML')
            await FSMModeratorReply.choice.set()
        else:
            await bot.send_message(message.chat.id, 'Заявки с таким номером нет, либо она уже была обработана.\nПопробуйте ввести номер заявки еще раз либо вернитесь на главное меню', reply_markup=reply_markup_call_off('Главное меню'))
            await FSMModeratorReply.request_id.set()


@dispatcher.callback_query_handler(state=FSMModeratorReply.choice)
async def check_request_id(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'approve':
        text = 'Отправьте фото для подверждения'
        await bot.send_message(call.message.chat.id, text, reply_markup=reply_markup_call_off('Отмена'))
        await FSMModeratorReply.photo.set()
    elif call.data == 'reject':
        async with state.proxy() as file:
            request_id = file['request_id']

        client_id = await data_base.get_request_user_id(request_id)
        text = f'<b>Заявка</b> #<code>{request_id}</code>' + '\n'
        text += 'Ваша заявка не прошла проверку модераторами, заявка отклонена ❌' + '\n\n'
        await data_base.delete_request(request_id)
        await bot.send_message(chat_id=int(client_id), text=text, parse_mode='HTML')
        await bot.send_message(call.message.chat.id, 'Принято ✅', reply_markup=types.ReplyKeyboardRemove())
        await clear_state(state)
        await send_menu(call.message)


@dispatcher.message_handler(content_types=['photo', 'text'], state=FSMModeratorReply.photo)
async def check_request_id(message: types.Message, state: FSMContext):
    async with state.proxy() as file:
        request_id = file['request_id']

    if message.content_type == 'text':
        if message.text == 'Отмена':
            await bot.send_message(chat_id=message.chat.id, text='Действие отменено', reply_markup=types.ReplyKeyboardRemove())
            text = f'<code>{request_id}</code>\n\nЧто делаем с данной заявкой?'
            await bot.send_message(message.chat.id, text, reply_markup=inline_markup_request_opps(), parse_mode='HTML')
            await FSMModeratorReply.choice.set()
    else:
        async with state.proxy() as file:
            file['photo'] = message.photo[-1].file_id

        text = 'Отправьте сообщение к фото'
        await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=reply_markup_call_off('Отмена'))
        await FSMModeratorReply.caption.set()


@dispatcher.message_handler(content_types=['text'], state=FSMModeratorReply.caption)
async def check_request_id(message: types.Message, state: FSMContext):
    async with state.proxy() as file:
        request_id = file['request_id']

    if message.text == 'Отмена':
        await bot.send_message(chat_id=message.chat.id, text='Действие отменено', reply_markup=types.ReplyKeyboardRemove())
        text = f'<code>{request_id}</code>\n\nЧто делаем с данной заявкой?'
        await bot.send_message(message.chat.id, text, reply_markup=inline_markup_request_opps(), parse_mode='HTML')
        await FSMModeratorReply.choice.set()
    else:
        async with state.proxy() as file:
            photo = file['photo']

        client_id = await data_base.get_request_user_id(request_id)
        text = f'<b>Заявка</b> #<code>{request_id}</code>' + '\n'
        text += 'Ваша заявка одобрена модераторами' + '\n\n'
        text += message.text
        await data_base.delete_request(request_id)
        await bot.send_photo(chat_id=int(client_id),photo=photo, caption=text, parse_mode='HTML')
        await bot.send_message(message.chat.id, 'Принято ✅', reply_markup=types.ReplyKeyboardRemove())
        await clear_state(state)
        await send_menu(message)


@dispatcher.callback_query_handler(state=FSMClient.products_client)
async def choose_product_client(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'back':
        await clear_state(state)
        await edit_to_menu(call.message)
    for i in await data_base.get_all_products():
        if call.data == str(i[0]):
            text = f'<b>{str(i[0])}</b>' + '\n\n'
            text += await data_base.get_product_descr(str(i[0]))
            await bot.send_photo(chat_id=call.message.chat.id, photo=await data_base.get_product_photo(str(i[0])), caption=text, reply_markup=inline_markup_products_back(), parse_mode='HTML')
            await clear_state(state)


@dispatcher.callback_query_handler(state=FSMAdmin.opportunities)
async def moderator_opportunities(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'main_menu':
        await clear_state(state)
        await edit_to_menu(call.message)
    elif call.data == 'set_menu_text':
        async with state.proxy() as file:
            file['chapter'] = 'menu'
        text = 'Введите текст для изменения МЕНЮ'
        await bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=reply_markup_call_off('Назад'))
        await FSMAdmin.input_data.set()
    elif call.data == 'set_work_text':
        async with state.proxy() as file:
            file['chapter'] = 'work'
        text = 'Введите текст для изменения раздела РАБОТА'
        await bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=reply_markup_call_off('Назад'))
        await FSMAdmin.input_data.set()
    elif call.data == 'set_support_text':
        async with state.proxy() as file:
            file['chapter'] = 'support'
        text = 'Введите текст для изменения раздела ПОДДЕРЖКА'
        await bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=reply_markup_call_off('Назад'))
        await FSMAdmin.input_data.set()
    elif call.data == 'set_btc_wallet':
        async with state.proxy() as file:
            file['chapter'] = 'btc_wallet'
        text = 'Отправьте ваш Bitcoin Wallet (адресс)'
        await bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=reply_markup_call_off('Назад'))
        await FSMAdmin.input_data.set()
    elif call.data == 'add_moderator':
        async with state.proxy() as file:
            file['chapter'] = 'add_moderator'
        text = 'Введите Chat ID аккаунта, которому сибираетесь дать модераторство\nChat ID можно узнать в этом боте @getmyid_bot' + '\n'
        text += 'Добавляемый аккаунт должен пройти капчу(тем самым он будет в списке участников), только после этого его можно будет добавить в модераторы'
        await bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=reply_markup_call_off('Назад'))
        await FSMAdmin.input_data.set()
    elif call.data == 'sharing':
        async with state.proxy() as file:
            file['chapter'] = 'sharing'
        text = 'Введите текст для рассылки всем пользователям бота'
        await bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=reply_markup_call_off('Назад'))
        await FSMAdmin.input_data.set()
    elif call.data == 'products':
        count = len(await data_base.get_all_products())
        text = f'Количество товаров: {count}' + '\n\n'
        if count:
            text += 'Нажмите на любой товар для его редактирования/удаления или добавьте новый товар'
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=await inline_markup_products_list(data_base))
        await FSMAdmin.products.set()
    elif call.data == 'locations':
        count = len(await data_base.get_all_locations())
        text = f'Количество локаций: {count}' + '\n\n'
        if count:
            text += 'Нажмите на любую локацию для ее редактирования/удаления или добавьте новую'
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=await inline_markup_locations_list(data_base))
        await FSMAdmin.locations.set()


@dispatcher.message_handler(state=FSMAdmin.input_data)
async def input_data(message: types.Message, state: FSMContext):
    async with state.proxy() as file:
        chapter = file['chapter']

    text = 'Выполнено ✅'

    if chapter == 'menu':
        await data_base.set_statement_menu(message.text)
        await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=types.ReplyKeyboardRemove())
        await send_moderator_menu(message)
        await FSMAdmin.opportunities.set()
    elif chapter == 'work':
        await data_base.set_statement_work_text(message.text)
        await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=types.ReplyKeyboardRemove())
        await send_moderator_menu(message)
        await FSMAdmin.opportunities.set()
    elif chapter == 'support':
        await data_base.set_statement_support(message.text)
        await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=types.ReplyKeyboardRemove())
        await send_moderator_menu(message)
        await FSMAdmin.opportunities.set()
    elif chapter == 'btc_wallet':
        await data_base.set_statement_btc_wallet(message.text)
        await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=types.ReplyKeyboardRemove())
        await send_moderator_menu(message)
        await FSMAdmin.opportunities.set()
    elif chapter == 'add_moderator':
        try:
            chat_id = int(message.text)
            if await data_base.user_exists(str(chat_id)):
                if chat_id not in ADMIN_IDS:
                    ADMIN_IDS.append(chat_id)
                    await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=types.ReplyKeyboardRemove())
                    await send_moderator_menu(message)
                    await FSMAdmin.opportunities.set()
                else:
                    await bot.send_message(message.chat.id, 'Данный аккаунт уже модератор в боте')
                    await send_moderator_menu(message)
                    await FSMAdmin.opportunities.set()
            else:
                text = 'Аккаунта с таким Chat ID нет в списке участников\nПройдите капчу с этого аккаунта в боте, а потом добавляйте его в модераторы'
                await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=reply_markup_call_off('Назад'))
                await FSMAdmin.input_data.set()
        except Exception as e:
            text = 'Некорректный ввод, введите chat_id в виде последовательности цифр'
            await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=reply_markup_call_off('Назад'))
            await FSMAdmin.input_data.set()
    elif chapter == 'sharing':
        for i in await data_base.get_all_users():
            try:
                await bot.send_message(chat_id=int(i[0]), text=message.text)
            except Exception as e:
                print(e)

        await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=types.ReplyKeyboardRemove())
        await send_moderator_menu(message)
        await FSMAdmin.opportunities.set()


@dispatcher.callback_query_handler(state=FSMAdmin.products)
async def choose_products_admin(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'back':
        await clear_state(state)
        await edit_to_moderator_menu(call.message)
        await FSMAdmin.opportunities.set()
    elif call.data == 'add_product':
        async with state.proxy() as file:
            file['set_product'] = 'set_name'
        text = 'Отправьте название товара в виде текста'
        await bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=reply_markup_call_off('Назад'))
        await FSMAdmin.add_product.set()
    else:
        for i in await data_base.get_all_products():
            if call.data == str(i[0]):
                async with state.proxy() as file:
                    file['product'] = str(i[0])

                text = 'Выберите, что хотите сделать с данным товаром'
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=inline_markup_product_opportunities())
                await FSMAdmin.products_opps.set()


@dispatcher.message_handler(content_types=['text', 'photo'], state=FSMAdmin.add_product)
async def add_product(message: types.Message, state: FSMContext):
    async with state.proxy() as file:
        status = file['set_product']

    if status == 'set_name':
        if message.content_type == 'text':
            async with state.proxy() as file:
                file['name'] = message.text
                file['set_product'] = 'set_description'

            text = 'Отправьте описание товара в виде текста'
            await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=reply_markup_call_off('Назад'))
            await FSMAdmin.add_product.set()
        else:
            await bot.send_message(chat_id=message.chat.id, text='Отправьте данные для названия товара в виде текста', reply_markup=reply_markup_call_off('Назад'))
            await FSMAdmin.add_product.set()
    elif status == 'set_description':
        if message.content_type == 'text':
            async with state.proxy() as file:
                file['description'] = message.text
                file['set_product'] = 'set_photo'

            text = 'Отправьте фото товара'
            await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=reply_markup_call_off('Назад'))
            await FSMAdmin.add_product.set()
        else:
            await bot.send_message(chat_id=message.chat.id, text='Отправьте данные для описания товара в виде текста', reply_markup=reply_markup_call_off('Назад'))
            await FSMAdmin.add_product.set()
    elif status == 'set_photo':
        if message.content_type == 'photo':
            async with state.proxy() as file:
                name = file['name']
                description = file['description']

            await data_base.add_product(name, description, message.photo[-1].file_id)

            text = 'Данные приняты'
            await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=types.ReplyKeyboardRemove())
            await send_moderator_menu(message)
            await FSMAdmin.opportunities.set()
        else:
            await bot.send_message(chat_id=message.chat.id, text='Отправьте фото товара', reply_markup=reply_markup_call_off('Назад'))
            await FSMAdmin.add_product.set()


@dispatcher.callback_query_handler(state=FSMAdmin.products_opps)
async def choose_product_opps(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'back':
        await clear_state(state)
        await edit_to_moderator_menu(call.message)
        await FSMAdmin.opportunities.set()
    elif call.data == 'categories':
        async with state.proxy() as file:
            product = file['product']

        count = len(await data_base.get_all_categories_by_product_name(product))
        text = f'Количество категорий: {count}' + '\n\n'
        if count:
            text += 'Нажмите на любую категорию для ее редактирования/удаления или добавьте новую'

        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=await inline_markup_categories_by_product_admin(data_base, product))
        await FSMAdmin.categories.set()

    else:
        if call.data == 'delete_product':
            async with state.proxy() as file:
                file['what'] = 'products'
            text = 'Вы уверены что хотите удалить данный товар?'
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=inline_markup_sure())
            await FSMAdmin.sure.set()
        else:
            text = 'Отправьте ...'
            if call.data == 'edit_name':
                async with state.proxy() as file:
                    file['edit'] = 'name'

                text = 'Отправьте новое название товара'
            elif call.data == 'edit_description':
                async with state.proxy() as file:
                    file['edit'] = 'description'

                text = 'Отправьте новое описание товара'
            elif call.data == 'edit_photo':
                async with state.proxy() as file:
                    file['edit'] = 'photo'

                text = 'Отправьте новое фото товара'

            await bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=reply_markup_call_off('Назад'))
            await FSMAdmin.edit_product.set()


@dispatcher.callback_query_handler(state=FSMAdmin.sure)
async def make_sure(call: types.CallbackQuery, state: FSMContext):
    print('as')
    if call.data == 'yes':
        async with state.proxy() as file:
            what = file['what']

        print(what)

        if what == 'products':
            async with state.proxy() as file:
                product = file['product']
            await data_base.delete_product(product)
        elif what == 'location':
            async with state.proxy() as file:
                location = file['location']
            await data_base.delete_location(location)
        elif what == 'category':
            async with state.proxy() as file:
                product = file['product']
                category = file['category']
            await data_base.delete_category(product, category)

        await clear_state(state)
        await edit_to_moderator_menu(call.message)
        await FSMAdmin.opportunities.set()
    elif call.data == 'no':
        await clear_state(state)
        await edit_to_moderator_menu(call.message)
        await FSMAdmin.opportunities.set()


@dispatcher.message_handler(content_types=['text', 'photo'], state=FSMAdmin.edit_product)
async def edit_product(message: types.Message, state: FSMContext):
    async with state.proxy() as file:
        status = file['edit']
        product = file['product']

    text = 'Выполнено ✅'

    if status == 'name' or status == 'description':
        if message.content_type == 'text':
            if status == 'name':
                await data_base.edit_product_name(product, message.text)
                await bot.send_message(message.chat.id, text, reply_markup=types.ReplyKeyboardRemove())
                await send_moderator_menu(message)
                await FSMAdmin.opportunities.set()
            else:
                await data_base.edit_product_descr(product, message.text)
                await bot.send_message(message.chat.id, text, reply_markup=types.ReplyKeyboardRemove())
                await send_moderator_menu(message)
                await FSMAdmin.opportunities.set()
        else:
            await bot.send_message(message.chat.id, 'Отправьте данные в виде текста', reply_markup=reply_markup_call_off('Назад'))
            await FSMAdmin.edit_product.set()
    elif status == 'photo':
        if message.content_type == 'photo':
            photo_id = message.photo[-1].file_id
            await data_base.edit_product_photo(product, photo_id)
            await bot.send_message(message.chat.id, text, reply_markup=types.ReplyKeyboardRemove())
            await send_moderator_menu(message)
            await FSMAdmin.opportunities.set()
        else:
            await bot.send_message(message.chat.id, 'Отправьте данные в виде фото', reply_markup=reply_markup_call_off('Назад'))
            await FSMAdmin.edit_product.set()


@dispatcher.callback_query_handler(state=FSMAdmin.locations)
async def choose_locations_admin(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'back':
        await clear_state(state)
        await edit_to_moderator_menu(call.message)
        await FSMAdmin.opportunities.set()
    elif call.data == 'add_location':
        text = 'Отправьте название названия локации для ее создания'
        await bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=reply_markup_call_off('Назад'))
        await FSMAdmin.add_location.set()
    else:
        for i in await data_base.get_all_locations():
            if call.data == str(i[0]):
                async with state.proxy() as file:
                    file['location'] = str(i[0])

                text = 'Выберите, что хотите сделать с данной локацией'
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text=text, reply_markup=inline_markup_locations_opportunities())
                await FSMAdmin.locations_opps.set()


@dispatcher.message_handler(content_types=['text'], state=FSMAdmin.add_location)
async def add_location(message: types.Message, state: FSMContext):
    await data_base.add_location(message.text)

    text = 'Данные приняты'
    await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=types.ReplyKeyboardRemove())
    await send_moderator_menu(message)
    await FSMAdmin.opportunities.set()


@dispatcher.callback_query_handler(state=FSMAdmin.locations_opps)
async def choose_location_opps(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'back':
        await clear_state(state)
        await edit_to_moderator_menu(call.message)
        await FSMAdmin.opportunities.set()
    else:
        if call.data == 'delete_location':
            async with state.proxy() as file:
                file['what'] = 'location'
            text = 'Вы уверены что хотите удалить данную локацию?'
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=inline_markup_sure())
            await FSMAdmin.sure.set()
        else:
            if call.data == 'edit_location':
                text = 'Отправьте новое название для локации'
                await bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=reply_markup_call_off('Назад'))
                await FSMAdmin.edit_location.set()


@dispatcher.message_handler(content_types=['text'], state=FSMAdmin.edit_location)
async def edit_product(message: types.Message, state: FSMContext):
    text = 'Выполнено ✅'
    async with state.proxy() as file:
        location = file['location']

    await data_base.edit_location(location, message.text)

    await bot.send_message(message.chat.id, text, reply_markup=types.ReplyKeyboardRemove())
    await send_moderator_menu(message)
    await FSMAdmin.opportunities.set()


@dispatcher.callback_query_handler(state=FSMAdmin.categories)
async def choose_category_admin(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'back':
        await clear_state(state)
        await edit_to_moderator_menu(call.message)
        await FSMAdmin.opportunities.set()
    elif call.data == 'add_category':
        async with state.proxy() as file:
            file['set_category'] = 'set_name'
        text = 'Отправьте название категории в виде текста'
        await bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=reply_markup_call_off('Назад'))
        await FSMAdmin.add_category.set()
    else:
        async with state.proxy() as file:
            product = file['product']

        for i in await data_base.get_all_categories_by_product_name(product):
            if call.data == str(i[0]):
                async with state.proxy() as file:
                    file['category'] = str(i[0])

                text = 'Выберите, что хотите сделать с данной категорией'
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=inline_markup_categories_opportunities())
                await FSMAdmin.categories_opps.set()


@dispatcher.message_handler(content_types=['text', 'photo'], state=FSMAdmin.add_category)
async def add_product(message: types.Message, state: FSMContext):
    async with state.proxy() as file:
        status = file['set_category']
        product = file['product']
    if status == 'set_name':
        async with state.proxy() as file:
            file['new_category'] = message.text
            file['set_category'] = 'price'

        text = 'Введите цену данной категории в BTC'
        await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=reply_markup_call_off('Назад'))
        await FSMAdmin.add_category.set()
    elif status == 'price':
        try:
            price = float(message.text)
            if price > 0:
                async with state.proxy() as file:
                    category = file['new_category']

                await data_base.add_category(product, category, str(price))

                text = 'Данные приняты'
                await bot.send_message(message.chat.id, text, reply_markup=types.ReplyKeyboardRemove())
                await send_moderator_menu(message)
                await FSMAdmin.opportunities.set()
            else:
                text = '⛔Некорректный ввод, число должно быть больше нуля\nОтправьте новую цену в BTC'
                await bot.send_message(message.chat.id, text=text, reply_markup=reply_markup_call_off('Назад'))
                await FSMAdmin.add_category.set()
        except Exception as e:
            text = '⛔Некорректный ввод, введите число\nОтправьте новую цену в BTC'
            await bot.send_message(message.chat.id, text=text, reply_markup=reply_markup_call_off('Назад'))
            await FSMAdmin.add_category.set()


@dispatcher.callback_query_handler(state=FSMAdmin.categories_opps)
async def choose_categories_opps(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'back':
        await clear_state(state)
        await edit_to_moderator_menu(call.message)
        await FSMAdmin.opportunities.set()
    else:
        if call.data == 'delete_category':
            async with state.proxy() as file:
                file['what'] = 'category'
            text = 'Вы уверены что хотите удалить данную категорию?'
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=inline_markup_sure())
            await FSMAdmin.sure.set()
        else:
            text = 'Отправьте ...'
            if call.data == 'edit_category':
                async with state.proxy() as file:
                    file['edit_category'] = 'name'

                text = 'Отправьте новое название категории'
            elif call.data == 'edit_price':
                async with state.proxy() as file:
                    file['edit_category'] = 'price'

                text = 'Отправьте новую цену в BTC'

            await bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=reply_markup_call_off('Назад'))
            await FSMAdmin.edit_category.set()


@dispatcher.message_handler(content_types=['text'], state=FSMAdmin.edit_category)
async def edit_category(message: types.Message, state: FSMContext):
    async with state.proxy() as file:
        status = file['edit_category']
        product = file['product']
        category = file['category']

    text = 'Выполнено ✅'

    if status == 'name':
        await data_base.edit_category_name(product, category, message.text)
        await bot.send_message(message.chat.id, text, reply_markup=types.ReplyKeyboardRemove())
        await send_moderator_menu(message)
        await FSMAdmin.opportunities.set()
    elif status == 'price':
        try:
            price = float(message.text)
            if price > 0:
                await data_base.edit_price(product, category, str(price))
                await bot.send_message(message.chat.id, text, reply_markup=types.ReplyKeyboardRemove())
                await send_moderator_menu(message)
                await FSMAdmin.opportunities.set()
            else:
                text = '⛔Некорректный ввод, число должно быть больше нуля\nОтправьте новую цену в BTC'
                await bot.send_message(message.chat.id, text=text, reply_markup=reply_markup_call_off('Назад'))
                await FSMAdmin.edit_category.set()
        except Exception as e:
            text = '⛔Некорректный ввод, введите число\nОтправьте новую цену в BTC'
            await bot.send_message(message.chat.id, text=text, reply_markup=reply_markup_call_off('Назад'))
            await FSMAdmin.edit_category.set()


try:
    asyncio.run(executor.start_polling(dispatcher=dispatcher, skip_updates=False))
except Exception as error:
    print(error)


