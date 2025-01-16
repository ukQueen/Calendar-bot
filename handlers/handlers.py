
from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (CallbackQuery, FSInputFile, Message,  ReplyKeyboardRemove)


import dataBase.dataBase as db
import handlers.keyboards as kb

class Calendar(StatesGroup):
    main = State()
    read_group_name = State()
    edit_group_name = State()
    add_user = State()
    read_event_name = State()

router = Router()

start_text = """
Привет!😁✌️
Здесь ты можешь:
- создать группу людей для общего события
- создать событие для группы
При появлении нового события я тебя оповещу 🔔
"""

user_id = set()



@router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    if message.from_user.id not in user_id:
        user_id.add(message.from_user.id)
    tg_id = message.from_user.id
    username = message.from_user.username
    name = message.from_user.first_name
    last_name = message.from_user.last_name
    db.add_user(tg_id, username, name, last_name)
    # user = db.get_user(tg_id)
    await message.delete()
    await message.answer_sticker(
        "CAACAgIAAxkBAAENf2lnhzIfZHxF8nVOnbZ3Z7WiHi1NWQACjUUAAiTX0Ug4DvEOfdIqWzYE"
    )
    await message.answer(start_text, reply_markup=kb.main_ikb)
    # await message.answer(f"{user}")
    await state.set_state(Calendar.main)


# @router.message()
# async def message(message: Message) -> None:
#     await message.reply("да да, я тут🤫")
#     print(f"id -- {message.from_user.id}: {message.text}")
#     print(f"users id: {user_id}")
#     username = message.from_user.username
#     name = message.from_user.first_name
#     last_name = message.from_user.last_name
#     print(f"username : {username}, name: {name}, last_name: {last_name}")
#     print(type(message.from_user.id))

@router.callback_query(lambda query: query.data.startswith("main"))
async def main_show(callback: CallbackQuery) -> None:
    await callback.message.edit_text(text=start_text, reply_markup=kb.main_ikb)
    # await message.answer(f"{user}")
    # await state.set_state(Calendar.main)
    callback.answer("вы в меню")


@router.callback_query(lambda query: query.data.startswith("groups_"))
async def groups_show(callback: CallbackQuery) -> None:
    groups_data = callback.data.split("_")
    if groups_data[1] == "show":
        await callback.message.edit_text("Группы в которых вы состоите:", reply_markup=kb.groups_ikb(callback.from_user.id))
    elif groups_data[1] == "leave":
        group_name = groups_data[2]
        db.delete_group(group_name, callback.from_user.id)
        await callback.message.edit_text("Группы в которых вы состоите:", reply_markup=kb.groups_ikb(callback.from_user.id))

 

@router.callback_query(lambda query: query.data.startswith("group_"))
async def users_in_group(callback: CallbackQuery,state: FSMContext) -> None:
    # await callback.message.delete()
    # message_del = await callback.message.answer("Введите название группы:")
    group_data = callback.data.split("_")
    group_name = group_data[1]
    user_id = group_data[2]
    users = db.get_group_users(group_name)
    text = f'''<i>Группа</i>:
<b>{group_data[1]}</b>
    
<i>Участники:</i>'''
    k = 1
    for user in users:
        username = user[2]
        name = user[3]
        last_name = user[4]
        text += f'''\n{k}. '''
        if username:
            text += f"@{username}"
        if name:
            text += f"\n    {name}"
        if last_name:
            text += f"\n    {last_name}"
        text += "\n"
        k += 1
    await callback.message.edit_text(text=text, parse_mode="html", reply_markup=kb.users_ikb(group_name, user_id))
    # await state.update_data(created_message_id = message_del.message_id)
    await state.set_state(Calendar.main)


@router.callback_query(lambda query: query.data.startswith("create_group"))
async def create_group(callback: CallbackQuery,state: FSMContext) -> None:
    message_del = await callback.message.edit_text("Введите название группы:")
    await state.set_state(Calendar.read_group_name)
    await state.update_data(created_message_id = message_del.message_id,
                            callback_id = callback.id)



@router.callback_query(lambda query: query.data.startswith("edit_group"))
async def edit_group(callback: CallbackQuery,state: FSMContext) -> None:
    group_data = callback.data.split("_")
    group_name = group_data[2]
    message_del = await callback.message.edit_text("Введите новое название группы:")
    await state.set_state(Calendar.edit_group_name)
    await state.update_data(created_message_id = message_del.message_id,
                            group_name = group_name,
                            callback_id = callback.id,
                            user_id = callback.from_user.id)
    
@router.callback_query(lambda query: query.data.startswith("add_user"))
async def edit_group(callback: CallbackQuery,state: FSMContext) -> None:
    group_data = callback.data.split("_")
    group_name = group_data[2]
    message_del = await callback.message.edit_text("Введите username или ссылку на профиль человека:")
    await state.set_state(Calendar.add_user)
    await state.update_data(created_message_id = message_del.message_id,
                            group_name = group_name,
                            callback_id = callback.id,
                            user_id = callback.from_user.id)



@router.callback_query(lambda query: query.data.startswith("events_"))
async def events_show(callback: CallbackQuery) -> None:
    groups_data = callback.data.split("_")
    if groups_data[1] == "show":
        await callback.message.edit_text("Планируемые события:", reply_markup=kb.events_ikb(callback.from_user.id))
    elif groups_data[1] == "leave":
        # group_name = groups_data[2]
        # db.delete_group(group_name, callback.from_user.id)
        # await callback.message.edit_text("Группы в которых вы состоите:", reply_markup=kb.groups_ikb(callback.from_user.id))
        pass

@router.callback_query(lambda query: query.data.startswith("create_event"))
async def create_event(callback: CallbackQuery,state: FSMContext) -> None:
    await callback.message.edit_text("Выберите группу:", reply_markup=kb.event_groups_ikb(tg_id=callback.from_user.id))
    # await state.set_state(Calendar.read_group_name)
    # await state.update_data(created_message_id = message_del.message_id,
                            # callback_id = callback.id)
    

@router.callback_query(lambda query: query.data.startswith("event_"))
async def create_event_group(callback: CallbackQuery,state: FSMContext) -> None:
    group_data = callback.data.split("_")
    if group_data[1] == "groups":
        group_name = group_data[2]
        message_del = await callback.message.edit_text("Введите название события:")
        await state.set_state(Calendar.read_event_name)
        await state.update_data(created_message_id = message_del.message_id,
                                callback_id = callback.id,
                                group_name = group_name)
    elif group_data[1] == "group":
        event_name = group_data[2]
        group_name = group_data[3]
        text = f'''<i>Событие:</i> 
<b>{event_name}</b>

'''
        await callback.message.edit_text(text, reply_markup=kb.event_ikb(event_name=event_name, group_name=group_name), parse_mode="html")
        # await state.set_state(Calendar.read_event_name)
        # await state.update_data(created_message_id = message_del.message_id,
                                # callback_id = callback.id,
                                # group_name = group_name)

    elif group_data[1]== "date":
        state_data = await state.get_data()
        event_name = state_data.get('event_name')
        group_name = state_data.get('group_name')
        year = state_data.get('year')
        month = state_data.get('month')
        day = state_data.get('day')
        hours_start = state_data.get('hours_start')
        min_start = state_data.get('min_start')
        hours_end = state_data.get('hours_end')
        min_end = group_data[4]
        try:
            db.add_date(event_name, group_name, year, month, day, hours_start, min_start, hours_end, min_end)
            await callback.answer("Дата добавлена!")
        except Exception as e:
            print(e)
            await callback.answer("Дата не добавлена!")
        text = f'''<i>Событие:</i> 
<b>{event_name}</b>

'''
        await callback.message.edit_text(text, reply_markup=kb.event_ikb(event_name=event_name, group_name=group_name), parse_mode="html")
        


    else:
        event_name = group_data[1]
        text = f'''<i>Событие:</i> 
<b>{event_name}</b>

Группы:'''
        await callback.message.edit_text(text, parse_mode="html", reply_markup=kb.event_groups_ikb(event_name=event_name))
        # await state.set_state(Calendar.read_event_name)
        # await state.update_data(created_message_id = message_del.message_id,
                                # callback_id = callback.id,
                                # group_name = group_name)   



@router.callback_query(lambda query: query.data.startswith("add_date"))
async def add_date_group(callback: CallbackQuery,state: FSMContext) -> None:
    # print("in yare")
    group_data = callback.data.split("_")
    if group_data[2] == "year":
        print(f"callback: {callback.data}")
        print(group_data)
        event_name = group_data[3]
        group_name = group_data[4]

        # await state.set_state(Calendar.read_event_name)
        await state.update_data(event_name = event_name,
                                callback_id = callback.id,
                                group_name = group_name)
        await callback.message.edit_text("Выберите год:", reply_markup=kb.year(event_name=event_name, group_name=group_name))


    elif group_data[2] == "month":
        state_data = await state.get_data()
        event_name = state_data.get('event_name')
        group_name = state_data.get('group_name')
        year = group_data[3]

        # await state.set_state(Calendar.read_event_name)
        await state.update_data(year = year)
        await callback.message.edit_text("Выберите месяц:", reply_markup=kb.month(event_name=event_name, group_name=group_name, year=year))

    elif group_data[2] == "day":
        state_data = await state.get_data()
        event_name = state_data.get('event_name')
        group_name = state_data.get('group_name')
        year = state_data.get('year')
        month = group_data[3]

        # await state.set_state(Calendar.read_event_name)
        await state.update_data(month = month)
        await callback.message.edit_text("Выберите день:", reply_markup=kb.day(event_name=event_name, group_name=group_name, month=month))

    elif group_data[2] == "time":
        if group_data[3] == "start":
            if group_data[4] == "hour":
                state_data = await state.get_data()
                event_name = state_data.get('event_name')
                group_name = state_data.get('group_name')
                year = state_data.get('year')
                month = state_data.get('month')
                day = group_data[7]

                # await state.set_state(Calendar.read_event_name)
                await state.update_data(day = day)
                await callback.message.edit_text("Выберите час начал:", reply_markup=kb.hours_start(event_name=event_name, group_name=group_name, day=day))

            elif group_data[4] == "min":
                state_data = await state.get_data()
                event_name = state_data.get('event_name')
                group_name = state_data.get('group_name')
                year = state_data.get('year')
                month = state_data.get('month')
                day = state_data.get('day')
                hours_start = group_data[7]

                # await state.set_state(Calendar.read_event_name)
                await state.update_data(hours_start = hours_start)
                await callback.message.edit_text("Выберите минуты начала:", reply_markup=kb.min_start(event_name=event_name, group_name=group_name, hour_start=hours_start))
        
        elif group_data[3] == "end":
            if group_data[4] == "hour":
                state_data = await state.get_data()
                event_name = state_data.get('event_name')
                group_name = state_data.get('group_name')
                year = state_data.get('year')
                month = state_data.get('month')
                day = state_data.get('day')
                hours_start = state_data.get('hours_start')
                min_start = group_data[7]

                # await state.set_state(Calendar.read_event_name)
                await state.update_data(min_start = min_start)
                await callback.message.edit_text("Выберите час окончания:", reply_markup=kb.hours_end(event_name=event_name, group_name=group_name, min_start=min_start))

            elif group_data[4] == "min":
                state_data = await state.get_data()
                event_name = state_data.get('event_name')
                group_name = state_data.get('group_name')
                year = state_data.get('year')
                month = state_data.get('month')
                day = state_data.get('day')
                hours_start = state_data.get('hours_start')
                min_start = state_data.get('min_start')
                hours_end = group_data[7]

                # await state.set_state(Calendar.read_event_name)
                await state.update_data(hours_end = hours_end)
                await callback.message.edit_text("Выберите минуты окончания:", reply_markup=kb.min_end(event_name=event_name, group_name=group_name, hour_end=hours_end))



@router.message()
async def read_message(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state == Calendar.read_group_name:
        group_name = message.text
        user_data = await state.get_data()
        message_del_id = user_data.get('created_message_id')
        callback_id = user_data.get('callback_id')
   
        if message_del_id:
            await message.bot.delete_message(message.chat.id, message_del_id)
            print("deleted")
        try:
            db.add_group(group_name, message.from_user.id)

            await message.bot.answer_callback_query(callback_query_id=callback_id, text="Группа создана!")

        except Exception as e:
            print(e)
            await message.bot.answer_callback_query(callback_query_id=callback_id, text="Название уже занято!")
        
        await message.delete()    
        await message.answer("Группы в которых вы состоите:", reply_markup=kb.groups_ikb(message.from_user.id))
        await state.set_state(Calendar.main)

    elif current_state == Calendar.edit_group_name:
        new_group_name = message.text
        user_data = await state.get_data()
        message_del_id = user_data.get('created_message_id')
        group_name = user_data.get('group_name')
        callback_id = user_data.get('callback_id')

        if message_del_id:
            await message.bot.delete_message(message.chat.id, message_del_id)
        try:
            db.edit_group_name(group_name, new_group_name)

            await message.bot.answer_callback_query(callback_query_id=callback_id, text="Группа изменена!")
            group_name = new_group_name

        except Exception as e:
            print(f"error:    {e}")
            await message.bot.answer_callback_query(callback_query_id=callback_id, text="Название уже занято!")
            
        await message.delete()
        # group_data = callback.data.split("_")
        # group_name = group_data[1]
        user_data = await state.get_data()
        user_id = user_data.get('user_id')
        users = db.get_group_users(group_name)
        text = f'''<i>Группа</i>:
<b>{group_name}</b>
        
<i>Участники:</i>'''
        k = 1
        for user in users:
            username = user[2]
            name = user[3]
            last_name = user[4]
            text += f'''\n{k}. '''
            if username:
                text += f"@{username}"
            if name:
                text += f"\n    {name}"
            if last_name:
                text += f"\n    {last_name}"
            text += "\n"
            k += 1
        await message.answer(text=text, parse_mode="html", reply_markup=kb.users_ikb(group_name, user_id))
           # await state.update_data(created_message_id = message_del.message_id) 
        # await message.answer("Группы в которых вы состоите:", reply_markup=kb.groups_ikb(message.from_user.id))
        await state.set_state(Calendar.main)

    elif current_state == Calendar.add_user:
        user = message.text
        username = user
        if user[0] == "@":
            username = user[1:]
        elif user.startswith == "https://t.me/":
            username = user[13:]
            if username[-1] == "/":
                username = username[:-1]
        print(f"username: {username}")
        user_data = await state.get_data()
        message_del_id = user_data.get('created_message_id')
        group_name = user_data.get('group_name')
        callback_id = user_data.get('callback_id')
   
        if message_del_id:
            await message.bot.delete_message(message.chat.id, message_del_id)
            print("deleted")
        try:
            user_id = db.get_user_id(username)
            user_in_group = db.user_in_group(group_name, user_id)
            # print(user_in_group)
            if user_in_group:
                # await message.delete()
                await message.bot.answer_callback_query(callback_query_id=callback_id, text="Пользователь уже добавлен!")
            else:
                db.add_group(group_name, user_id)


            await message.bot.answer_callback_query(callback_query_id=callback_id, text="Пользователь добавлен!")

        except Exception as e:
            print(e)
            await message.bot.answer_callback_query(callback_query_id=callback_id, text="Пользователь не авторизован!")
            
        await message.delete()
        user_data = await state.get_data()
        user_id = user_data.get('user_id')
        users = db.get_group_users(group_name)
        text = f'''<i>Группа</i>:
<b>{group_name}</b>
        
<i>Участники:</i>'''
        k = 1
        for user in users:
            username = user[2]
            name = user[3]
            last_name = user[4]
            text += f'''\n{k}. '''
            if username:
                text += f"@{username}"
            if name:
                text += f"\n    {name}"
            if last_name:
                text += f"\n    {last_name}"
            text += "\n"
            k += 1
        await message.answer(text=text, parse_mode="html", reply_markup=kb.users_ikb(group_name, user_id))
           # await state.update_data(created_message_id = message_del.message_id) 
        # await message.answer("Группы в которых вы состоите:", reply_markup=kb.groups_ikb(message.from_user.id))
        await state.set_state(Calendar.main)

    elif current_state == Calendar.read_event_name:
        event_name = message.text
        user_data = await state.get_data()
        message_del_id = user_data.get('created_message_id')
        callback_id = user_data.get('callback_id')
        group_name = user_data.get('group_name')
        if message_del_id:
            await message.bot.delete_message(message.chat.id, message_del_id)
            print("deleted")
        try:
            db.add_event(event_name, group_name)
            await message.bot.answer_callback_query(callback_query_id=callback_id, text="Событие создано!")

        except Exception as e:
            print(e)
            await message.bot.answer_callback_query(callback_query_id=callback_id, text="Событие не создано!")
        
        await message.delete()    
        await message.answer("Планируемые события:", reply_markup=kb.events_ikb(message.from_user.id))
        await state.set_state(Calendar.main)


    elif current_state == Calendar.main:
        await message.delete()
   



# @router.message(F.text == "Группы")
# async def groups(message: Message) -> None:
#     await message.delete()
#     await message.answer(text="Группы в которых вы состоите:", reply_markup=kb.groups_ikb(message.from_user.id))
    





# @router.message()
# async def message(message: Message, state: FSMContext) -> None:
#     # await message.reply("да да, я тут🤫")
#     # print(f"id -- {message.from_user.id}: {message.text}")
#     # print(f"users id: {user_id}")
#     # username = message.from_user.username
#     # name = message.from_user.first_name
#     # last_name = message.from_user.last_name
#     # print(f"username : {username}, name: {name}, last_name: {last_name}")
#     # print(type(message.from_user.id))
#     current_state = await state.get_state()
#     if current_state == Calendar.main:
#         await message.delete()
