
from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import dataBase.dataBase as db

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
    await message.answer(start_text)
    # await message.answer(f"{user}")
    await message.answer_sticker(
        "CAACAgIAAxkBAAENf2lnhzIfZHxF8nVOnbZ3Z7WiHi1NWQACjUUAAiTX0Ug4DvEOfdIqWzYE"
    )


@router.message()
async def message(message: Message) -> None:
    await message.reply("да да, я тут🤫")
    print(f"id -- {message.from_user.id}: {message.text}")
    print(f"users id: {user_id}")
    username = message.from_user.username
    name = message.from_user.first_name
    last_name = message.from_user.last_name
    print(f"username : {username}, name: {name}, last_name: {last_name}")
    print(type(message.from_user.id))
