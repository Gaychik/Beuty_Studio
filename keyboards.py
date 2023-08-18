from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton,ReplyKeyboardMarkup,KeyboardButton



ikb_start=InlineKeyboardMarkup(row_width=2)
ib1=InlineKeyboardButton(text='Палитра',callback_data='#')
ib2=InlineKeyboardButton(text='Свободные слоты',callback_data='#')
ib3=InlineKeyboardButton(text='Прайс на услуги',callback_data='#')
ib4=InlineKeyboardButton(text='Важная информация',callback_data='#')
ib5=InlineKeyboardButton(text='Инстаграмм',callback_data='#')

ikb_start.add(ib1,ib2).add(ib3).add(ib4,ib5)