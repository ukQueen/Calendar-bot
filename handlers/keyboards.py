from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup)

import dataBase.dataBase as bd

main_ikb = InlineKeyboardMarkup(row_width=3, 
                                inline_keyboard=[[InlineKeyboardButton(text="Группы", callback_data="groups_show")],
                                                 [InlineKeyboardButton(text="События", callback_data="events_show")]])


# groups_rkb = ReplyKeyboardMarkup(
#     keyboard=[
#         [KeyboardButton(text="Группы"), KeyboardButton(text="События")],
#     ],
#     resize_keyboard=True,
#     input_field_placeholder="Choose the button",
# )

def groups_ikb(tg_id):
    groups = bd.get_groups(tg_id)
    buttons = [
        [
            InlineKeyboardButton(
                text = group[0],
                callback_data= "group_" + group[0] + "_" + str(tg_id) ,
            )
        ]
        for group in groups
    ]
    buttons2 = [[InlineKeyboardButton(text="➕Создать новую группу", callback_data="create_group")],
                     [InlineKeyboardButton(text="🔙 Назад", callback_data="main")]]
    buttons.extend(buttons2)
    groups_ikb = InlineKeyboardMarkup(row_width=3, inline_keyboard=buttons)
    return groups_ikb


def users_ikb(group_name, tg_id):
    buttons = InlineKeyboardMarkup(row_width=3, 
                                inline_keyboard=[[InlineKeyboardButton(text="Добавить пользователя", callback_data=f"add_user_{group_name}")],
                                                 [InlineKeyboardButton(text="Изменить название", callback_data=f"edit_group_{group_name}")],
                                                 [InlineKeyboardButton(text="Выйти из группы", callback_data=f"groups_leave_{group_name}")],
                                                 [InlineKeyboardButton(text="Назад ", callback_data="groups_show")],
                                                 [InlineKeyboardButton(text="На главную", callback_data="main")]])
    return buttons
                                        



def events_ikb(tg_id):
    groups = bd.get_groups(tg_id)
    events = set()
    
    for group in groups:
        events_buf = bd.get_events(group[0])
        for event in events_buf:
            events.add(event)
        

    # events = bd.get_group(group_name)
    buttons = [
        [
            InlineKeyboardButton(
                text=event[0],
                callback_data="event_" + str(event[0]),
            )
        ]
        for event in events
    ]
    buttons2 = [[InlineKeyboardButton(text="Добавить событие ", callback_data="create_event")],
                [InlineKeyboardButton(text="🔙 Назад", callback_data="main")]]
    buttons.extend(buttons2)
    events_ikb = InlineKeyboardMarkup(row_width=3, inline_keyboard=buttons)
    return events_ikb


def event_ikb(event_name, group_name, dates):
    callback = "add_date_year_" + event_name + "_" + group_name
    print(callback)
    buttons = [[InlineKeyboardButton(text="Добавить дату", callback_data=callback)],
                [InlineKeyboardButton(text="Убрать дату", callback_data="event_deleteDate_" + event_name + "_" + group_name) if dates else None],
                [InlineKeyboardButton(text="Удалить событие из группы", callback_data="event_delete_" + event_name + "_" + group_name)],
                [InlineKeyboardButton(text="Назад ", callback_data="event_" +event_name)],
                [InlineKeyboardButton(text="На главную", callback_data="main")]]
    buttons = [button for button in buttons if button[0] is not None]
    return InlineKeyboardMarkup(row_width=3, inline_keyboard=buttons)

# event_group_ -- для  отображения групп пользователя при создании нового события
# event_groups_ -- для отображения груп в выбранно
def event_groups_ikb(tg_id=None, event_name=None):
    if tg_id:
        groups = bd.get_groups(tg_id)
        buttons = [
            [
                InlineKeyboardButton(
                    text = group[0],
                    callback_data= "event_groups_" + group[0] + "_" + str(tg_id) ,
                )
            ]
            for group in groups
        ]
    elif event_name:
        groups = bd.get_group_event(event_name)
        buttons = [
            [
                InlineKeyboardButton(
                    text = group[0],
                    callback_data= "event_group_" + event_name + "_" + group[0] ,
                )
            ]
            for group in groups
        ]
    buttons2 = [[InlineKeyboardButton(text="Назад ", callback_data="events_show")],
                [InlineKeyboardButton(text="На главную", callback_data="main")]]
    buttons.extend(buttons2)
    groups_ikb = InlineKeyboardMarkup(row_width=3, inline_keyboard=buttons)
    return groups_ikb


def event_dates_ikb(event_name, group_name, dates):
    # callback="delete_event" +event_name +"_"+ group_name+"_"+ date["event_name"] + "_" + date["group_name"] + "_" + date["hours_start"] + "_" + date["min_start"] + "_" + date["hours_end"] + "_" + date["min_end"],

    buttons = [
        [
            InlineKeyboardButton(
                text=f"{date["day"]}.{date["month"]}.{date["year"]} {date["hours_start"]}:{date["min_start"]} - {date["hours_end"]}:{date["min_end"]}",
                callback_data=("delete_date_" + str(index)),
            )
        ]
        for index, date in enumerate(dates)
    ]
    buttons2 = [[InlineKeyboardButton(text="Назад ", callback_data="event_group_" + event_name + "_" + group_name)],
                [InlineKeyboardButton(text="На главную", callback_data="main")]]
    buttons.extend(buttons2)
    dates_ikb = InlineKeyboardMarkup(row_width=3, inline_keyboard=buttons)
    return dates_ikb

def year(event_name, group_name, date=None):
    callback = "add_date_month_" + event_name + "_" + group_name + "_"
    buttons = InlineKeyboardMarkup(row_width=3, 
                                inline_keyboard=[[InlineKeyboardButton(text="2025", callback_data=callback + "2025"),
                                                 InlineKeyboardButton(text="2026", callback_data=callback + "2026")],
                                                 [InlineKeyboardButton(text="2027", callback_data=callback + "2027"),
                                                 InlineKeyboardButton(text="2028", callback_data=callback + "2028")],
                                                 [InlineKeyboardButton(text="Назад ", callback_data="event_group_" + event_name + "_" + group_name)],
                                                 [InlineKeyboardButton(text="На главную", callback_data="main")]])
    return buttons

def month(event_name, group_name, year, date=None):
    callback = "add_date_day_" + event_name + "_" + group_name + "_"
    back = "add_date_year_" + event_name + "_" + group_name + "_"
    buttons = InlineKeyboardMarkup(row_width=3, 
                                inline_keyboard=[[InlineKeyboardButton(text="янв", callback_data=callback + "янв"),
                                                 InlineKeyboardButton(text="февр", callback_data=callback + "февр")],
                                                 [InlineKeyboardButton(text="март", callback_data=callback + "март"),
                                                 InlineKeyboardButton(text="апр", callback_data=callback + "апр")],
                                                 [InlineKeyboardButton(text="май", callback_data=callback + "май"),
                                                 InlineKeyboardButton(text="июнь", callback_data=callback + "июнь")],
                                                 [InlineKeyboardButton(text="июнь", callback_data=callback + "июль"),
                                                 InlineKeyboardButton(text="авг", callback_data=callback + "авг")],
                                                 [InlineKeyboardButton(text="сент", callback_data=callback + "сент"),
                                                 InlineKeyboardButton(text="окт", callback_data=callback + "окт")],
                                                 [InlineKeyboardButton(text="нояб", callback_data=callback + "нояб"),
                                                 InlineKeyboardButton(text="дек", callback_data=callback + "дек")],
                                                 [InlineKeyboardButton(text="Назад ", callback_data=back + year),],
                                                 [InlineKeyboardButton(text="На главную", callback_data="main")]])
    return buttons


def day(event_name, group_name, month, date=None):
    callback = "add_date_time_start_hour_" + event_name + "_" + group_name + "_"
    back = "add_date_month_" + event_name + "_" + group_name + "_"
    buttons = InlineKeyboardMarkup(row_width=3, 
                                inline_keyboard=[[InlineKeyboardButton(text="1", callback_data=callback + "01"),
                                                 InlineKeyboardButton(text="2", callback_data=callback + "02")],
                                                 [InlineKeyboardButton(text="3", callback_data=callback + "03"),
                                                 InlineKeyboardButton(text="4", callback_data=callback + "04")],
                                                 [InlineKeyboardButton(text="Назад ", callback_data=back + month),],
                                                 [InlineKeyboardButton(text="На главную", callback_data="main")]])
    return buttons

def hours_start(event_name, group_name, day, date=None):
    callback = "add_date_time_start_min_" + event_name + "_" + group_name + "_"
    back = "add_date_day_" + event_name + "_" + group_name + "_"

    buttons = InlineKeyboardMarkup(row_width=3, 
                                inline_keyboard=[[InlineKeyboardButton(text="1", callback_data=callback + "01"),
                                                 InlineKeyboardButton(text="2", callback_data=callback + "02")],
                                                 [InlineKeyboardButton(text="3", callback_data=callback + "03"),
                                                 InlineKeyboardButton(text="4", callback_data=callback + "04")],
                                                 [InlineKeyboardButton(text="Назад ", callback_data=back + day),],
                                                 [InlineKeyboardButton(text="На главную", callback_data="main")]])
    return buttons

def min_start(event_name, group_name, hour_start, date=None):
    callback = "add_date_time_end_hour_" + event_name + "_" + group_name + "_"
    back = "add_date_time_start_hour_" + event_name + "_" + group_name + "_"

    buttons = InlineKeyboardMarkup(row_width=3, 
                                inline_keyboard=[[InlineKeyboardButton(text="00", callback_data=callback + "00"),
                                                 InlineKeyboardButton(text="05", callback_data=callback + "05"),
                                                 InlineKeyboardButton(text="10", callback_data=callback + "10")],
                                                 [InlineKeyboardButton(text="15", callback_data=callback + "15"),
                                                 InlineKeyboardButton(text="20", callback_data=callback + "20"),
                                                 InlineKeyboardButton(text="25", callback_data=callback + "25")],
                                                 [InlineKeyboardButton(text="30", callback_data=callback + "30"),
                                                 InlineKeyboardButton(text="35", callback_data=callback + "35"),
                                                 InlineKeyboardButton(text="40", callback_data=callback + "40")],
                                                 [InlineKeyboardButton(text="Назад ", callback_data=back + hour_start)],
                                                 [InlineKeyboardButton(text="На главную", callback_data="main")]])
    return buttons


def hours_end(event_name, group_name,min_start, date=None):
    callback = "add_date_time_end_min_" + event_name + "_" + group_name + "_"
    back = "add_date_time_start_min_" + event_name + "_" + group_name + "_"
    buttons = InlineKeyboardMarkup(row_width=3, 
                          inline_keyboard=[[InlineKeyboardButton(text="1", callback_data=callback + "01"),
                                                 InlineKeyboardButton(text="2", callback_data=callback + "02")],
                                                 [InlineKeyboardButton(text="3", callback_data=callback + "03"),
                                                 InlineKeyboardButton(text="4", callback_data=callback + "04")],
                                                 [InlineKeyboardButton(text="Назад ", callback_data=back + min_start),],
                                                 [InlineKeyboardButton(text="На главную", callback_data="main")]])
    return buttons

def min_end(event_name, group_name,hour_end, date=None):
    callback = "event_date_" + event_name + "_" + group_name + "_"
    back = "add_date_time_end_hour_" + event_name + "_" + group_name + "_"
    buttons = InlineKeyboardMarkup(row_width=3, 
                                inline_keyboard=[[InlineKeyboardButton(text="00", callback_data=callback + "00"),
                                                 InlineKeyboardButton(text="05", callback_data=callback + "05"),
                                                 InlineKeyboardButton(text="10", callback_data=callback + "10")],
                                                 [InlineKeyboardButton(text="15", callback_data=callback + "15"),
                                                 InlineKeyboardButton(text="20", callback_data=callback + "20"),
                                                 InlineKeyboardButton(text="25", callback_data=callback + "25")],
                                                 [InlineKeyboardButton(text="30", callback_data=callback + "30"),
                                                 InlineKeyboardButton(text="35", callback_data=callback + "35"),
                                                 InlineKeyboardButton(text="40", callback_data=callback + "40")],
                                                 [InlineKeyboardButton(text="Назад ", callback_data=back + hour_end)],
                                                 [InlineKeyboardButton(text="На главную", callback_data="main")]])
    return buttons