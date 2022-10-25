import logging
from aiogram import Bot, Dispatcher, executor, types
from config import API_TOKEN, admin
import keyboard as kb
import functions as func
import sqlite3
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import Throttled
from aiogram.utils.markdown import quote_html

import aiogram.utils.markdown as md
from aiogram.types import ParseMode
from aiogram.utils import executor

import  requests

import data
import datetime
import os
from pathlib import Path


from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.callback_data import CallbackData

reg_callback = CallbackData("reg", "status", "chat_id", "nick", "name", "namee", "age", "age2")
storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)
connection = sqlite3.connect('data.db')
q = connection.cursor()
admin_chat_id =-1001535411259
admin = admin_chat_id

class st(StatesGroup):
    item = State()
    item2 = State()
    item3 = State()
    item4 = State()
    item5 = State()

class Form(StatesGroup):
    name = State()  # Будет представлен в хранилище как 'Форма:имя'
    age = State()  # Будет представлен в хранилище как "Форма:возраст"
    gender1 = State()  # Будет представлен в хранилище как "Форма:пол"
    gender = State()
class Anketa(StatesGroup):
    # внутри объявляем Стейты(состояния), далее мы будем вести пользователя по цепочке этих стейтов
    name = State()
    namee = State()
    age = State()
    age2 = State()
def inline(chat_id, nick, name, age):
    confirm = InlineKeyboardButton(
        text="",
        callback_data=reg_callback.new(
            status="1", chat_id=chat_id, nick=nick, name=name, age=age
        ),
    )
    cancel = InlineKeyboardButton(
        text="",
        callback_data=reg_callback.new(
            status="0", chat_id=chat_id, nick="-", name="-", age="-"
        ),
    )
    conf_inline = InlineKeyboardMarkup()
    conf_inline.insert(confirm).insert(cancel)
    return conf_inline
    
    

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer('❕Приветствую, это бот-саппорт❕\nНажми на кнопку\n\n 👀 Создать заявку 👀\n\n  Для создания заявки в Техническую Поддержку.\n❗️Не дублируйте заявки❗️',reply_markup=kb.start3)

@dp.message_handler(content_types=['text'], text='❌ Отменить ❌')
async def cmd_start(message: types.Message):
    await message.answer('❕Приветствую, это бот-саппорт❕\nНажми на кнопку\n\n 👀 Создать заявку 👀\n\n  Для создания заявки в Техническую Поддержку.\n❗️Не дублируйте заявки❗️',reply_markup=kb.start3)

@dp.message_handler(content_types=['text'], text='⏳ Режим работы ⏳')
async def cmd_start(message: types.Message):
    await message.answer('⏳Режим работы⏳\n\n🕗 С 8:00 до 20:00 🕗\n❗️Не дублируйте заявки❗️',reply_markup=kb.start3)

@dp.message_handler(content_types=['text'], text='👀 Создать заявку 👀')
async def name(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, "Введите своё имя:",reply_markup=kb.back1)
    # Переходим на следующий стейт
    await Anketa.name.set()


# Вы можете использовать состояние '*', если вам нужно обработать все состояния
@dp.message_handler(state='*', content_types=['text'], text='❌ Отменить ❌')
@dp.message_handler(Text(equals='❌ Отменить ❌', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Разрешить пользователю отменить любое действие
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Отменить состояние и сообщить об этом пользователю
    await state.finish()
    # И снимите клавиатуру (на всякий случай)
    await message.reply('Хорошо, отменил', reply_markup=types.ReplyKeyboardRemove())
    await message.answer('❕Приветствую, это бот-саппорт❕\nНажми на кнопку\n\n 👀 Создать заявку 👀\n\n  Для создания заявки в Техническую Поддержку.\n❗️Не дублируйте заявки❗️',reply_markup=kb.start3)


@dp.message_handler(state=Anketa.name, content_types=types.ContentTypes.TEXT)
async def age(message: types.Message, state: FSMContext):
    # Записываем ответ в storage
    await state.update_data(name=message.text)
    await bot.send_message(
        message.chat.id, "Введите Ваш телефон (внутренний или мобильный)",reply_markup=kb.back1
    )
    await Anketa.namee.set()

@dp.message_handler(state=Anketa.namee, content_types=types.ContentTypes.TEXT)
async def namee(message: types.Message, state: FSMContext):
    await state.update_data(namee=message.text)
    await bot.send_message(message.chat.id, "Введите своё сообщение:",reply_markup=kb.back1)
    # Переходим на следующий стейт
    await Anketa.age.set()


@dp.message_handler(state=Anketa.age, content_types=types.ContentTypes.TEXT)
async def fun(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    data = await state.get_data()
    
    # Отправляем сообщение в чат админов с анкетой и добавляем 2 инлайн кнопки с callback данными
    await message.reply(
        f'<b>Имя:</b> {data.get("name")}\n'
        f'<b>Номер телефона:</b> {data.get("namee")}\n'
        f'<b>Сообщение:</b> {data.get("age")}', parse_mode='HTML'
    )
    await bot.send_message(
        message.chat.id, "👆 Заявка успешно заполнена, отправить⁉️",reply_markup=kb.start2
    )
    await Anketa.age2.set()

@dp.message_handler(content_types=['text'], text='✅ Отправить ✅',state=Anketa.age2)
@dp.throttled(func.antiflood, rate=3)
async def fun(message: types.Message, state: FSMContext):
    await state.update_data(age2=message.text)
    data = await state.get_data()
    path = len([nomID for nomID in os.listdir('C:/Users/p.samoilov.SOVA/Desktop/SovTest/All_applications') if os.path.isfile(os.path.join('C:/Users/p.samoilov.SOVA/Desktop/SovTest/All_applications',nomID))])
    #print(path)
    #print(path+1)
    Namid = path+1
    NamID = str(Namid)
    my_file = open(f"C:/Users/p.samoilov.SOVA/Desktop/SovTest/All_applications/"+NamID+".txt", "w+",encoding='utf-8')
    # Отправляем сообщение в чат админов с анкетой и добавляем 2 инлайн кнопки с callback данными
    await bot.send_message(
        admin,
        f"<b>!Получена заявка №{NamID}\nID: </b>{message.chat.id}\n<b>От:</b> @{message.from_user.username}   <a href='tg://user?id={message.from_user.id}'>{quote_html(message.from_user.full_name)}</a>\n"
        f'<b>Имя:</b> {data.get("name")}\n'
        f'<b>Номер телефона:</b> {data.get("namee")}\n'
        f'<b>🖋Сообщение🖋</b>\n {data.get("age")}',reply_markup=kb.fun(message.chat.id), parse_mode='HTML'
    )

    my_file.write(   
                f"<b>!Получена заявка №{NamID}\nID: </b>{message.chat.id}\n<b>От:</b> @{message.from_user.username}\n<a href='tg://user?id={message.from_user.id}'>{quote_html(message.from_user.full_name)}</a>\n"
                f'<b>Имя:</b> {data.get("name")}\n'
                f'<b>Номер телефона:</b>{data.get("namee")}\n'  
                f'<b>Сообщение</b>\n {data.get("age")}'
                )
    
    await message.answer(f"✅ Заявка отправлена.\n🌐 Номер заявки №"+NamID,reply_markup=kb.start3)
    # Заканчиваем "опрос" 
    my_file.close()

    dirName = f'C:/Users/p.samoilov.SOVA/Desktop/SovTest/{message.chat.id}'
    try:
        # создание папки
        os.makedirs(dirName)
        await bot.send_message(
            admin,
            f"<b>☠️Зарегистрирован новый пользователь☠️\nID: </b>{message.chat.id}\n<b>Линк:</b> @{message.from_user.username}   <a href='tg://user?id={message.from_user.id}'>{quote_html(message.from_user.full_name)}</a>\n", parse_mode='HTML'
            )
        print("Папка " , dirName ,  " создана") 
    except FileExistsError:
        print("Папка " , dirName ,  " уже существует или невозможно создать")
    a=datetime.datetime.now().strftime('%d-%m-%Y_%H.%M-%S') 
    my_file = open(f"C:/Users/p.samoilov.SOVA/Desktop/SovTest/{message.chat.id}/"+a+".txt", "w+",encoding='utf-8')
    my_file.write(   
                f"<b>!Получена заявка №{NamID}\nID: </b>{message.chat.id}\n<b>От:</b> @{message.from_user.username}\n<a href='tg://user?id={message.from_user.id}'>{quote_html(message.from_user.full_name)}</a>\n"
                f'<b>Имя:</b> {data.get("name")}\n'
                f'<b>Номер телефона:</b>{data.get("namee")}\n'  
                f'<b>Сообщение</b>\n {data.get("age")}'
                )
    my_file.close()
    await state.finish() 
@dp.callback_query_handler(lambda call: True) # Inline часть
async def cal(call, state: FSMContext):
	if 'ans' in call.data:
		a = call.data.index('-ans')
		ids = call.data[:a]
		await call.message.answer('Введите ответ пользователю:', reply_markup=kb.back)
		await st.item2.set() # админ отвечает пользователю
		await state.update_data(uid=ids)
	elif 'ignor' in call.data:
		await call.answer('Удалено')
		await bot.delete_message(call.message.chat.id, call.message.message_id)
		await state.finish()
        
@dp.message_handler(state=st.item2)
async def proc(message: types.Message, state: FSMContext):
	if message.text == 'Отмена':
		await message.answer('Отмена! Возвращаю назад.', reply_markup=kb.menu)
		await state.finish()
	else:
		await message.answer('✅ Сообщение отправлено в КЦ.', reply_markup=kb.menu)
		data = await state.get_data()
		id = data.get("uid")
		await state.finish()
		await bot.send_message(id, '⚠️Вам поступил ответ от администратора:\n\n❕Текст: {}'.format(message.text))

@dp.message_handler(content_types=['text'], text='Админка')
async def handfler(message: types.Message, state: FSMContext):
	func.join(chat_id=message.chat.id)
	q.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
	result = q.fetchone()
	if result[0] == 0:
		if message.chat.id == admin:
			await message.answer('🔐 Добро пожаловать в админ-панель.', reply_markup=kb.adm)

@dp.message_handler(content_types=['text'], text='Назад')
async def handledr(message: types.Message, state: FSMContext):
	await message.answer('🔐Добро пожаловать, администратор🔐', reply_markup=kb.menu)

@dp.message_handler(content_types=['text'], text='ЧС')
async def handlaer(message: types.Message, state: FSMContext):
	func.join(chat_id=message.chat.id)
	q.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
	result = q.fetchone()
	if result[0] == 0:
		if message.chat.id == admin:
			q.execute(f"SELECT * FROM users WHERE block == 1")
			result = q.fetchall()
			sl = []
			for index in result:
				i = index[0]
				sl.append(i)

			ids = '\n'.join(map(str, sl))
			await message.answer(f'ID пользователей в ЧС:\n{ids}')


@dp.message_handler(content_types=['text'], text='Добавить в ЧС')
async def hanadler(message: types.Message, state: FSMContext):
	func.join(chat_id=message.chat.id)
	q.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
	result = q.fetchone()
	if result[0] == 0:
		if message.chat.id == admin:
			await message.answer('🖋 Введите id пользователя, которого нужно заблокировать.\nДля отмены нажмите кнопку ниже', reply_markup=kb.back)
			await st.item3.set()

@dp.message_handler(content_types=['text'], text='Убрать из ЧС')
async def hfandler(message: types.Message, state: FSMContext):
	func.join(chat_id=message.chat.id)
	q.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
	result = q.fetchone()
	if result[0] == 0:
		if message.chat.id == admin:
			await message.answer('🖋 Введите id пользователя, которого нужно разблокировать.\nДля отмены нажмите кнопку ниже', reply_markup=kb.back)
			await st.item4.set()

@dp.message_handler(content_types=['text'], text='♻️ Рассылка ♻️')
async def hangdler(message: types.Message, state: FSMContext):
	func.join(chat_id=message.chat.id)
	q.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
	result = q.fetchone()
	if result[0] == 0:
		if message.chat.id == admin:
			await message.answer('🖋 Введите текст для рассылки.\n\nДля отмены нажмите на кнопку ниже', reply_markup=kb.back)
			await st.item.set()

@dp.callback_query_handler(lambda call: True) # Inline часть
async def cal(call, state: FSMContext):
	if 'ans' in call.data:
		a = call.data.index('-ans')
		ids = call.data[:a]
		await call.message.answer('Введите ответ пользователю:', reply_markup=kb.back)
		await st.item2.set() # админ отвечает пользователю
		await state.update_data(uid=ids)
	elif 'ignor' in call.data:
		await call.answer('Удалено')
		await bot.delete_message(call.message.chat.id, call.message.message_id)
		await state.finish()

@dp.message_handler(state=st.item2)
async def proc(message: types.Message, state: FSMContext):
	if message.text == 'Отмена':
		await message.answer('Отмена! Возвращаю назад.', reply_markup=kb.menu)
		await state.finish()
	else:
		await message.answer('✅ Сообщение отправлено в КЦ.', reply_markup=kb.menu)
		data = await state.get_data()
		id = data.get("uid")
		await state.finish()
		await bot.send_message(id, '⚠️Вам поступил ответ от администратора:\n\n❕Текст: {}'.format(message.text))

@dp.message_handler(state=st.item)
async def process_name(message: types.Message, state: FSMContext):
	q.execute(f'SELECT user_id FROM users')
	row = q.fetchall()
	connection.commit()
	text = message.text
	if message.text == 'Отмена':
		await message.answer('Отмена! Возвращаю назад.', reply_markup=kb.adm)
		await state.finish()
	else:
		info = row
		await message.answer('🌐Рассылка начата!', reply_markup=kb.adm)
		for i in range(len(info)):
			try:
				await bot.send_message(info[i][0], str(text))
			except:
				pass
		await message.answer('✅Рассылка завершена!', reply_markup=kb.adm)
		await state.finish()


@dp.message_handler(content_types=['text'], text='Найти заявку')
async def hangdler(message: types.Message, state: FSMContext):
	func.join(chat_id=message.chat.id)
	q.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
	result = q.fetchone()
	if result[0] == 0:
		if message.chat.id == admin:
			await message.answer('🖋 Введите номер заявки:\n\nДля отмены нажмите на кнопку ниже', reply_markup=kb.back)
			await st.item5.set()


@dp.message_handler(state=st.item5)
async def process_name(message: types.Message, state: FSMContext):
    q.execute(f'SELECT user_id FROM users')
    row = q.fetchall()
    connection.commit()
    text = message.text
    Yesss = f'C:/Users/p.samoilov.SOVA/Desktop/SovTest/All_applications/'+str(text)+'.txt'
    try:
        # создание папки
        os.path.split(Yesss)
        with open('C:/Users/p.samoilov.SOVA/Desktop/SovTest/All_applications/'+str(text)+'.txt','r',encoding='utf-8') as f:
            homework = f.read()
        await message.answer('Найдена заявка №'+str(text)+':', reply_markup=kb.adm)
        await bot.send_message(message.chat.id, f'{str(homework)}', reply_markup=kb.fun(message.chat.id), parse_mode='HTML')
    except FileNotFoundError:
        await message.answer('Ошибка, скорее всего не верный номер!', reply_markup=kb.adm)

    await state.finish()
    

@dp.message_handler(state=st.item3)
async def proce(message: types.Message, state: FSMContext):
	if message.text == 'Отмена':
		await message.answer('Отмена! Возвращаю назад.', reply_markup=kb.adm)
		await state.finish()
	else:
		if message.text.isdigit():
			q.execute(f"SELECT block FROM users WHERE user_id = {message.text}")
			result = q.fetchall()
			connection.commit()
			if len(result) == 0:
				await message.answer(' ❗️Такой пользователь не найден в базе данных.', reply_markup=kb.adm)
				await state.finish()
			else:
				a = result[0]
				id = a[0]
				if id == 0:
					q.execute(f"UPDATE users SET block = 1 WHERE user_id = {message.text}")
					connection.commit()
					await message.answer('❌ Пользователь успешно заблокирован.', reply_markup=kb.adm)
					await state.finish()
					await bot.send_message(message.text, '‼️ Вы были заблокированы администрацией.‼️')
				else:
					await message.answer('❗️ Данный пользователь уже имеет блокировку.', reply_markup=kb.adm)
					await state.finish()
		else:
			await message.answer('Ты вводишь буквы...\nВведи ID')

@dp.message_handler(state=st.item4)
async def proc(message: types.Message, state: FSMContext):
	if message.text == 'Отмена':
		await message.answer('Отмена! Возвращаю назад.', reply_markup=kb.adm)
		await state.finish()
	else:
		if message.text.isdigit():
			q.execute(f"SELECT block FROM users WHERE user_id = {message.text}")
			result = q.fetchall()
			connection.commit()
			if len(result) == 0:
				await message.answer('Такой пользователь не найден в базе данных.⁉️', reply_markup=kb.adm)
				await state.finish()
			else:
				a = result[0]
				id = a[0]
				if id == 1:
					q.execute(f"UPDATE users SET block = 0 WHERE user_id = {message.text}")
					connection.commit()
					await message.answer('✅Пользователь успешно разбанен.', reply_markup=kb.adm)
					await state.finish()
					await bot.send_message(message.text, '✅Вы были разблокированы администрацией.')
				else:
					await message.answer('Данный пользователь не заблокирован.♻️', reply_markup=kb.adm)
					await state.finish()
		else:
			await message.answer('Ты вводишь буквы...\nВведи ID')






if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)