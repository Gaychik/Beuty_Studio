import aiogram
from db import cursor,create_client,get_client
from aiogram.contrib.fsm_storage.memory import MemoryStorage#Временный буфер
from aiogram.dispatcher import FSMContext,Dispatcher #Конечный автомат
from aiogram.dispatcher.filters.state import StatesGroup,State
from keyboards import gen_ikb_days,gen_ikb_months,gen_time_ikb
from googlesheet_table import GoogleTable

buffer=MemoryStorage()

class UserProfile(StatesGroup):
    name=State()
    telephone_number=State()
    master=State()
    record_date=State()

dispatcher:Dispatcher=None

async def start_FSM(dp:Dispatcher,data:list,state:FSMContext):
         global dispatcher
         dispatcher=dp
         dispatcher.storage=buffer
         state.update_data(master=data)
         state.set_state(UserProfile.telephone_number)
         await message.answer('Введите свой номер телефона')
async def load_telephone_number(message,state:FSMContext):
    data=message.text
    state.update_data(tel=data)
    if get_client(data,cursor):
        state.set_state(UserProfile.record_date)
        await message.answer('Выберите дату записи',reply_markup=gen_ikb_months())
    else:
        state.set_state(UserProfile.name)
        await message.answer('Введите имя и фамилию')

async def load_name(message,state):
    data = message.text
    state.update_data(name=data)
    state.set_state(UserProfile.record_date)
    await message.answer('Выберите дату записи', reply_markup=gen_ikb_months())

#фукнция ббдует вызываться 3 раза для месяца, дня, времени
async def load_date(callback,state): #Загружаем дату
    data=callback.data
    user_state_data=state.get_data() # получаем данные из буффера в виде словаря
    # user_state_data = {
    #      'master':['+5645378123','Анна Москалева'],
    #     'tel': '+734903853',
    #     'name': 'Юлия Арзамасова',
    #     'date':
    #         {
    #             'month': 'Апрель'
    #
    #         }
    # }
    if 'date' not in user_state_data: # 1 этап добавляем в буфер выбранный месяц
        selected_date={'month':data}
        state.update_data(date=selected_date)
        await callback.message.answer('Выберите день записи')
        await callback.message.edit_reply_markup(reply_markup=gen_ikb_days(int(data)))

    elif 'day' not in user_state_data['date']:# 2 этап добавляем в буфер выбранный день
        user_state_data['date']['day']=data
        state.update_data(date=user_state_data['date'])
        google_table=GoogleTable()
        slots = google_table.getData(user_state_data['master'][1], f'B1:H1')
        await callback.message.answer('Выберите время записи')
        await callback.message.edit_reply_markup(reply_markup=gen_time_ikb([slot for slot in slots if slot == '']))

        #Подключаемся к гугл таблицы для получения времени
        # Отправим набор свободного времени в виде клавиатуры нашему клиенту в чат
    elif 'time' not in user_state_data['date']:  # 3 этап добавляем в буфер выбранное время
        user_state_data['date']['day'] = data
        state.update_data(date=user_state_data['date'])
        if 'name' in user_state_data:
            await db.create_client(user_state_data)
        await callback.reply(f'''Вы успешно записаны к мастеру!
               \nМесяц:{user_state_data['date']['month']}
               \nЧисло:{user_state_data['date']['day']}
               \nВремя:{user_state_data['date']['time']}
               ''')
        await state.finish()












