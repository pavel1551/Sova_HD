from aiogram import types
menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
menu.add(
    types.KeyboardButton('Админка')
)

start1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
start1.add(
    types.KeyboardButton('👀 Создать заявку 👀'),
    types.KeyboardButton('❌ Отменить ❌')
)
start2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
start2.add(
    types.KeyboardButton('✅ Отправить ✅'),
    types.KeyboardButton('❌ Отменить ❌')
)
start3 = types.ReplyKeyboardMarkup(resize_keyboard=True)
start3.add(
    types.KeyboardButton('👀 Создать заявку 👀'),
    types.KeyboardButton('⏳ Режим работы ⏳')
)
start4 = types.ReplyKeyboardMarkup(resize_keyboard=True)
start4.add(
    types.KeyboardButton('👀 Создать заявку 👀'),
    types.KeyboardButton('❌ Отменить ❌')
)
back1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
back1.add(
    types.KeyboardButton('❌ Отменить ❌')
)
adm = types.ReplyKeyboardMarkup(resize_keyboard=True)
adm.add(
    # types.KeyboardButton('ЧС'),
    # types.KeyboardButton('Добавить в ЧС'),
    # types.KeyboardButton('Убрать из ЧС')
)
adm.add(types.KeyboardButton('♻️ Рассылка ♻️'))
adm.add(types.KeyboardButton('Найти заявку'))
adm.add('Назад')
back = types.ReplyKeyboardMarkup(resize_keyboard=True)
back.add(
    types.KeyboardButton('Отмена')
)
def fun(user_id):
    quest = types.InlineKeyboardMarkup(row_width=3)
    quest.add(
        types.InlineKeyboardButton(text='Ответить', callback_data=f'{user_id}-ans'),
        types.InlineKeyboardButton(text='Удалить', callback_data='ignor')
    )
    return quest