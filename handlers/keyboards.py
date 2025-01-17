from datetime import datetime

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import dataBase.dataBase as bd
from dataBase.dataBase import month_conv, month_conv_r

main_ikb = InlineKeyboardMarkup(
    row_width=3,
    inline_keyboard=[
        [InlineKeyboardButton(text="Группы", callback_data="groups_show")],
        [InlineKeyboardButton(text="События", callback_data="events_show")],
    ],
)

day_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
if datetime.now().year % 4 == 0:
    day_month[1] = 29


def groups_ikb(tg_id):
    groups = bd.get_groups(tg_id)
    buttons = [
        [
            InlineKeyboardButton(
                text=group[0],
                callback_data="group_" + group[0] + "_" + str(tg_id),
            )
        ]
        for group in groups
    ]
    buttons2 = [
        [
            InlineKeyboardButton(
                text="Создать новую группу", callback_data="create_group"
            )
        ],
        [InlineKeyboardButton(text="Назад", callback_data="main")],
    ]
    buttons.extend(buttons2)
    ikb = InlineKeyboardMarkup(row_width=3, inline_keyboard=buttons)
    return ikb


def users_ikb(group_name, tg_id):
    buttons = InlineKeyboardMarkup(
        row_width=3,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Добавить пользователя", callback_data=f"add_user_{group_name}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Изменить название", callback_data=f"edit_group_{group_name}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Выйти из группы", callback_data=f"groups_leave_{group_name}"
                )
            ],
            [InlineKeyboardButton(text="Назад ", callback_data="groups_show")],
            [InlineKeyboardButton(text="На главную", callback_data="main")],
        ],
    )
    return buttons


def events_ikb(tg_id):
    groups = bd.get_groups(tg_id)
    events = set()

    for group in groups:
        events_buf = bd.get_events(group[0])
        for event in events_buf:
            events.add(event)

    buttons = [
        [
            InlineKeyboardButton(
                text=event[0],
                callback_data="event_" + str(event[0]),
            )
        ]
        for event in events
    ]
    buttons2 = [
        [InlineKeyboardButton(text="Добавить событие ", callback_data="create_event")],
        [InlineKeyboardButton(text="Назад", callback_data="main")],
    ]
    buttons.extend(buttons2)
    ikb = InlineKeyboardMarkup(row_width=3, inline_keyboard=buttons)
    return ikb


def event_ikb(event_name, group_name, dates):
    callback = "add_date_year_" + event_name + "_" + group_name
    print(callback)
    buttons = [
        [InlineKeyboardButton(text="Добавить дату", callback_data=callback)],
        [
            (
                InlineKeyboardButton(
                    text="Убрать дату",
                    callback_data="event_deleteDate_" + event_name + "_" + group_name,
                )
                if dates
                else None
            )
        ],
        [
            InlineKeyboardButton(
                text="Удалить событие из группы",
                callback_data="event_delete_" + event_name + "_" + group_name,
            )
        ],
        [InlineKeyboardButton(text="Назад ", callback_data="event_" + event_name)],
        [InlineKeyboardButton(text="На главную", callback_data="main")],
    ]
    buttons = [button for button in buttons if button[0] is not None]
    return InlineKeyboardMarkup(row_width=3, inline_keyboard=buttons)


# event_group_ -- для  отображения групп пользователя при создании нового события
# event_groups_ -- для отображения груп в выбранном событии
def event_groups_ikb(tg_id=None, event_name=None):
    if tg_id:
        groups = bd.get_groups(tg_id)
        buttons = [
            [
                InlineKeyboardButton(
                    text=group[0],
                    callback_data="event_groups_" + group[0] + "_" + str(tg_id),
                )
            ]
            for group in groups
        ]
    elif event_name:
        groups = bd.get_group_event(event_name)
        buttons = [
            [
                InlineKeyboardButton(
                    text=group[0],
                    callback_data="event_group_" + event_name + "_" + group[0],
                )
            ]
            for group in groups
        ]
    buttons2 = [
        [InlineKeyboardButton(text="Назад ", callback_data="events_show")],
        [InlineKeyboardButton(text="На главную", callback_data="main")],
    ]
    buttons.extend(buttons2)
    ikb = InlineKeyboardMarkup(row_width=3, inline_keyboard=buttons)
    return ikb


def event_dates_ikb(event_name, group_name, dates):
    buttons = [
        [
            InlineKeyboardButton(
                text=f"{date["day"]}.{date["month"]}.{date["year"]} {date["hours_start"]}:{date["min_start"]} - {date["hours_end"]}:{date["min_end"]}",
                callback_data=("delete_date_" + str(index)),
            )
        ]
        for index, date in enumerate(dates)
    ]
    buttons2 = [
        [
            InlineKeyboardButton(
                text="Назад ",
                callback_data="event_group_" + event_name + "_" + group_name,
            )
        ],
        [InlineKeyboardButton(text="На главную", callback_data="main")],
    ]
    buttons.extend(buttons2)
    ikb = InlineKeyboardMarkup(row_width=3, inline_keyboard=buttons)
    return ikb


def year(event_name, group_name, date=None):
    current_time = datetime.now()
    year = current_time.year
    callback = "add_date_month_" + event_name + "_" + group_name + "_"

    buttons = []
    k = 0
    for i in range(3):
        buttons.append([])
        for j in range(2):
            buttons[i].append(
                InlineKeyboardButton(
                    text=str(year + k), callback_data=callback + str(year + k)
                )
            )
            k += 1

    buttons2 = [
        [
            InlineKeyboardButton(
                text="Назад ",
                callback_data="event_group_" + event_name + "_" + group_name,
            )
        ],
        [InlineKeyboardButton(text="На главную", callback_data="main")],
    ]
    buttons.extend(buttons2)
    return InlineKeyboardMarkup(row_width=3, inline_keyboard=buttons)


def month(event_name, group_name, year):
    current_time = datetime.now()
    month = current_time.month
    if int(year) > current_time.year:
        month = 1
    callback = "add_date_day_" + event_name + "_" + group_name + "_"
    back = "add_date_year_" + event_name + "_" + group_name + "_"

    buttons = []
    k = 0
    while month < 13:
        buttons.append([])
        buttons[k].append(
            InlineKeyboardButton(
                text=month_conv_r[str(month).zfill(2)],
                callback_data=callback + month_conv_r[str(month).zfill(2)],
            )
        )
        month += 1
        if month > 12:
            break
        buttons[k].append(
            InlineKeyboardButton(
                text=month_conv_r[str(month).zfill(2)],
                callback_data=callback + month_conv_r[str(month).zfill(2)],
            )
        )
        month += 1
        k += 1

    buttons2 = [
        [
            InlineKeyboardButton(text="Назад ", callback_data=back + year),
        ],
        [InlineKeyboardButton(text="На главную", callback_data="main")],
    ]
    buttons.extend(buttons2)
    return InlineKeyboardMarkup(row_width=3, inline_keyboard=buttons)


def day(event_name, group_name, year, month):
    current_time = datetime.now()
    current_month = current_time.month
    day = current_time.day
    days_count = day_month[int(month) - 1]
    if (int(month) > current_time.month and int(year) == current_time.year) or (
        int(year) > current_time.year
    ):
        day = 1

    callback = "add_date_time_start_hour_" + event_name + "_" + group_name + "_"
    back = "add_date_month_" + event_name + "_" + group_name + "_"

    print(f"day_count: {days_count}")
    buttons = []
    k = 0
    while day <= days_count:
        buttons.append([])
        buttons[k].append(
            InlineKeyboardButton(
                text=str(day), callback_data=callback + str(day).zfill(2)
            )
        )
        day += 1
        if day > days_count:
            break
        buttons[k].append(
            InlineKeyboardButton(
                text=str(day), callback_data=callback + str(day).zfill(2)
            )
        )
        day += 1
        if day > days_count:
            break
        buttons[k].append(
            InlineKeyboardButton(
                text=str(day), callback_data=callback + str(day).zfill(2)
            )
        )
        day += 1
        if day > days_count:
            break
        buttons[k].append(
            InlineKeyboardButton(
                text=str(day), callback_data=callback + str(day).zfill(2)
            )
        )
        day += 1
        k += 1

    buttons2 = [
        [
            InlineKeyboardButton(text="Назад ", callback_data=back + year),
        ],
        [InlineKeyboardButton(text="На главную", callback_data="main")],
    ]
    buttons.extend(buttons2)
    return InlineKeyboardMarkup(row_width=4, inline_keyboard=buttons)


def hours_start(event_name, group_name, year, month, day):
    current_time = datetime.now()
    current_hour = current_time.hour
    if (
        int(day) > current_time.day
        and int(month) == current_time.month
        and int(year) == current_time.year
    ) or (int(month) > current_time.month and int(year) >= current_time.year):
        current_hour = 0

    callback = "add_date_time_start_min_" + event_name + "_" + group_name + "_"
    back = "add_date_day_" + event_name + "_" + group_name + "_"

    buttons = []
    k = 0
    while current_hour < 24:
        buttons.append([])
        buttons[k].append(
            InlineKeyboardButton(
                text=str(current_hour).zfill(2),
                callback_data=callback + str(current_hour).zfill(2),
            )
        )
        current_hour += 1
        if current_hour >= 24:
            break
        buttons[k].append(
            InlineKeyboardButton(
                text=str(current_hour).zfill(2),
                callback_data=callback + str(current_hour).zfill(2),
            )
        )
        current_hour += 1
        if current_hour >= 24:
            break
        buttons[k].append(
            InlineKeyboardButton(
                text=str(current_hour).zfill(2),
                callback_data=callback + str(current_hour).zfill(2),
            )
        )
        current_hour += 1
        k += 1

    buttons2 = [
        [
            InlineKeyboardButton(
                text="Назад ", callback_data=back + month_conv_r[month]
            ),
        ],
        [InlineKeyboardButton(text="На главную", callback_data="main")],
    ]
    buttons.extend(buttons2)
    return InlineKeyboardMarkup(row_width=3, inline_keyboard=buttons)


def min_start(event_name, group_name, year, month, day, hour_start):
    current_time = datetime.now()
    min = current_time.minute
    min = min + 5 - min % 5

    if (
        int(hour_start) > current_time.hour
        and int(day) == current_time.day
        and int(month) == current_time.month
        and int(year) == current_time.year
    ) or (
        int(day) > current_time.day
        and int(month) >= current_time.month
        and int(year) >= current_time.year
    ):
        min = 0

    callback = "add_date_time_end_hour_" + event_name + "_" + group_name + "_"
    back = "add_date_time_start_hour_" + event_name + "_" + group_name + "_"

    buttons = []
    k = 0
    while min < 60:
        buttons.append([])
        buttons[k].append(
            InlineKeyboardButton(
                text=str(min).zfill(2), callback_data=callback + str(min).zfill(2)
            )
        )
        min += 5
        if min >= 60:
            break
        buttons[k].append(
            InlineKeyboardButton(
                text=str(min).zfill(2), callback_data=callback + str(min).zfill(2)
            )
        )
        min += 5
        k += 1

    buttons2 = [
        [InlineKeyboardButton(text="Назад ", callback_data=back + day)],
        [InlineKeyboardButton(text="На главную", callback_data="main")],
    ]
    buttons.extend(buttons2)
    return InlineKeyboardMarkup(row_width=3, inline_keyboard=buttons)


def hours_end(event_name, group_name, year, month, day, hour_start, min_start):
    hour = int(hour_start)

    callback = "add_date_time_end_min_" + event_name + "_" + group_name + "_"
    back = "add_date_time_start_min_" + event_name + "_" + group_name + "_"

    buttons = []
    k = 0
    while hour < 24:
        buttons.append([])
        buttons[k].append(
            InlineKeyboardButton(
                text=str(hour).zfill(2), callback_data=callback + str(hour).zfill(2)
            )
        )
        hour += 1
        if hour >= 24:
            break
        buttons[k].append(
            InlineKeyboardButton(
                text=str(hour).zfill(2), callback_data=callback + str(hour).zfill(2)
            )
        )
        hour += 1
        if hour >= 24:
            break
        buttons[k].append(
            InlineKeyboardButton(
                text=str(hour).zfill(2), callback_data=callback + str(hour).zfill(2)
            )
        )
        hour += 1
        k += 1

    buttons2 = [
        [
            InlineKeyboardButton(text="Назад ", callback_data=back + hour_start),
        ],
        [InlineKeyboardButton(text="На главную", callback_data="main")],
    ]
    buttons.extend(buttons2)
    return InlineKeyboardMarkup(row_width=3, inline_keyboard=buttons)


def min_end(event_name, group_name, year, month, day, hour_start, min_start, hour_end):

    min = int(min_start)
    min = min + 5 - min % 5

    if int(hour_end) > int(hour_start):
        min = 0

    callback = "event_date_" + event_name + "_" + group_name + "_"
    back = "add_date_time_end_hour_" + event_name + "_" + group_name + "_"

    buttons = []
    k = 0
    while min < 60:
        buttons.append([])
        buttons[k].append(
            InlineKeyboardButton(
                text=str(min).zfill(2), callback_data=callback + str(min).zfill(2)
            )
        )
        min += 5
        if min >= 60:
            break
        buttons[k].append(
            InlineKeyboardButton(
                text=str(min).zfill(2), callback_data=callback + str(min).zfill(2)
            )
        )
        min += 5
        k += 1

    buttons2 = [
        [InlineKeyboardButton(text="Назад ", callback_data=back + min_start)],
        [InlineKeyboardButton(text="На главную", callback_data="main")],
    ]
    buttons.extend(buttons2)
    return InlineKeyboardMarkup(row_width=3, inline_keyboard=buttons)
