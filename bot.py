import setting_commands
from aiogram import Bot,executor,Dispatcher,types
from aiogram.dispatcher import filters
from keyboards import *
from config import TOKEN_BOT
from User import *

import db
bot=Bot(TOKEN_BOT)
dp=Dispatcher(bot)

async def on_startup(_):
    dp.start_polling()
    print('БОТ ЗАПУЩЕН!')
    #await setting_commands.set_default_commands(bot)

#Навешиваем обработчик, который будет давать функции start_command реагировать только на сообщение start
@dp.message_handler(commands=['start'])
async def start_command(message:types.Message):

    await bot.send_photo(chat_id=message.chat.id,
                         photo=open('resourses/images/start.jpg','rb'),
                         caption='Добро пожаловать в нашу студию!',
                         reply_markup=ikb_start)
    await message.delete()

@dp.callback_query_handler(text='Слоты')
async def get_free_slots(callback:types.CallbackQuery):
          await db.db_start()
          masters=await db.get_masters(db.cursor)
          for master in masters:
              ikb_register_to_master['inline_keyboard'][0][0]['callback_data']+=f'|{master[0]}|{master[1]}'
              await bot.send_photo(chat_id=callback.chat_instance,
                                   photo=master[4],
                                   caption=f'{masters[1]}',
                                   reply_markup=ikb_register_to_master
                                   )

@dp.callback_query_handler(filters.Text(contains="Запись на прием"))
async def register_to_master(callback:types.CallbackQuery,state:FSMContext):
   await start_FSM(dp,callback.data.split('|'),state)



if __name__ == '__main__':
    executor.start_polling(
        dispatcher=dp,
        skip_updates=True,
        on_startup=on_startup
    )
