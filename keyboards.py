from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton,ReplyKeyboardMarkup,KeyboardButton
from datetime import datetime
from calendar import monthrange


ikb_start=InlineKeyboardMarkup(row_width=2)
ib1=InlineKeyboardButton(text='Палитра',callback_data='Палитра')
ib2=InlineKeyboardButton(text='Свободные слоты',callback_data='Слоты')
ib3=InlineKeyboardButton(text='Прайс на услуги',callback_data='Прайс')
ib4=InlineKeyboardButton(text='Важная информация',callback_data='Информация')
ib5=InlineKeyboardButton(text='Наш сайт',url="http://crystal-spa.ru/index.php")
ikb_start.add(ib1,ib2).add(ib3).add(ib4,ib5)

ikb_register_to_master = InlineKeyboardMarkup()
ikb_register_to_master.add(InlineKeyboardButton(text='Запись на прием', callback_data='Запись на прием'))

months_list=['','Январь', 'Февраль','Март','Апрель','Май','Июнь','Июль','Август',
            'Сентябрь','Октябрь','Ноябрь','Декабрь']
days_months=[0]
current_year = datetime.now().year
for i in range(1,13):
     days_months.append(monthrange(current_year,i)[1])

def gen_ikb_months():
    ikb_months = InlineKeyboardMarkup()
    for i in  range(1,13):
        ikb_months.add(InlineKeyboardButton(text=days_months[i],callback_data=i))
    return ikb_months

def gen_ikb_days(number_month):
    ikb_days = InlineKeyboardMarkup(row_width=5)
    for i in range(1,number_month+1):
        ikb_days.add(InlineKeyboardButton(text=days_months[i], callback_data=i))
    return ikb_days

def gen_time_ikb(times):
    ikb_times=InlineKeyboardMarkup(row_width=3)
    for time in times:
        ikb_times.add(InlineKeyboardButton(text=time,callback_data=time))
    return ikb_times





