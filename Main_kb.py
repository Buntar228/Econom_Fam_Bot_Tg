from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

kb_main = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
Raspisanie = KeyboardButton('📆Расписание')
Prepodi = KeyboardButton('👩‍🏫Преподаватели')
Kafedri = KeyboardButton('Кафедры ЭФ МГУ')
Meropriatia = KeyboardButton('💃Мероприятия')
Staga = KeyboardButton('💰Помощь с работой')
Psiholog = KeyboardButton('⌛Психологическая помощь')
Svobodnii_kabi = KeyboardButton('🔎Свободные кабинеты')

kb_main.add(Raspisanie).insert(Svobodnii_kabi).add(Prepodi).insert(Meropriatia)
kb_main.add(Kafedri).insert(Staga).add(Psiholog)

pic_btn = [
    InlineKeyboardButton(text='Эта', callback_data='this'),
    InlineKeyboardButton(text='Следующая', callback_data='next'),

]

pic_keyboard = InlineKeyboardMarkup(resize_keyboard=True, one_time_ketboard=False).row(*pic_btn)
