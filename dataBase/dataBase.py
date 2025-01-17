import os
import sqlite3
from datetime import datetime

month_conv = {
    "янв": "01",
    "февр": "02",
    "март": "03",
    "апр": "04",
    "май": "05",
    "июнь": "06",
    "июль": "07",
    "авг": "08",
    "сент": "09",
    "окт": "10",
    "нояб": "11",
    "дек": "12",
}
month_conv_r = {
    "01": "янв",
    "02": "февр",
    "03": "март",
    "04": "апр",
    "05": "май",
    "06": "июнь",
    "07": "июль",
    "08": "авг",
    "09": "сент",
    "10": "окт",
    "11": "нояб",
    "12": "дек",
}

db_path = "dataBase/events.db"


def create_dataBase():
    if not os.path.exists(db_path):
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS Users  (               
            id_user INTEGER PRIMARY KEY,
            tg_id INTEGER UNIQUE,
            username TEXT,
            name TEXT,
            last_name TEXT
        );"""
        )

        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tg_id ON Users (tg_id)")

        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS Groups  (
            id_group INTEGER PRIMARY KEY,
            group_name TEXT UNIQUE
        );"""
        )
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS Groups_users  (
            id_group_users INTEGER PRIMARY KEY,
            id_group INTEGER,
            id_user INTEGER,
            FOREIGN KEY (id_group) REFERENCES Groups(id_group),
            FOREIGN KEY (id_user) REFERENCES Users(id_user),
            UNIQUE (id_group, id_user)
        );"""
        )

        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_id_group ON Groups_users (id_group)"
        )

        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS Events  (
            id_event INTEGER PRIMARY KEY,
            event_name TEXT,
            id_group INTEGER,
            FOREIGN KEY (id_group) REFERENCES Groups(id_group)
                        ON DELETE CASCADE
        );"""
        )

        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_event_name ON Events (event_name)"
        )

        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS Date  (
            id_date INTEGER PRIMARY KEY,
            date TEXT,
            start_time TEXT,
            end_time TEXT,
            id_event INTEGER,
            FOREIGN KEY (id_event) REFERENCES Events(id_event)
        );"""
        )

        cursor.execute("CREATE INDEX IF NOT EXISTS idx_date ON Date (date)")

        connection.commit()
        connection.close()
        print("База данных и таблицы успешно созданы.")


def add_user(tg_id, username=None, name=None, last_name=None):
    if not os.path.exists(db_path):
        create_dataBase()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Users WHERE tg_id = ?", (tg_id,))
    existing_user = cursor.fetchone()

    if existing_user:
        print(f"Пользователь с tg_id {tg_id} уже существует.")
        return

    columns = ["tg_id"]
    values = [tg_id]

    if username is not None:
        columns.append("username")
        values.append(username)

    if name is not None:
        columns.append("name")
        values.append(name)

    if last_name is not None:
        columns.append("last_name")
        values.append(last_name)

    columns_str = ", ".join(columns)
    values_str = ", ".join(["?"] * len(values))
    cursor.execute(
        f"""
                INSERT INTO Users ({columns_str})
                    VALUES ({values_str})
                    """,
        tuple(values),
    )

    connection.commit()
    connection.close()
    print("Пользователь успешно добавлен.")


def add_group(group_name, tg_id):
    if not os.path.exists(db_path):
        create_dataBase()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute(
        """
                   SELECT id_group FROM Groups 
                   WHERE group_name = ?              
                   """,
        (group_name,),
    )
    group = cursor.fetchone()

    cursor.execute(
        """
                        SELECT id_user FROM Users
                        WHERE tg_id = ?
                        """,
        (tg_id,),
    )
    user = cursor.fetchone()

    if not group:
        cursor.execute(
            """
                        INSERT INTO Groups (group_name)
                            VALUES (?)
                        """,
            (group_name,),
        )
        connection.commit()
        cursor.execute(
            """
                    SELECT id_group FROM Groups
                        WHERE group_name = ?
                        """,
            (group_name,),
        )
        group = cursor.fetchone()
    else:
        raise Exception(f"Группа с именем {group_name} уже существует.")

    id_user = user[0]
    id_group = group[0]
    cursor.execute(
        """
                   SELECT * FROM Groups_users   
                   WHERE id_group = ? AND id_user = ?
                     """,
        (id_group, id_user),
    )
    group_user = cursor.fetchone()

    if group_user:
        # print(f"Группа с именем {group_name} уже существует.")
        raise Exception(f"Группа с именем {group_name} уже существует.")

    else:

        cursor.execute(
            """
                        INSERT INTO Groups_users (id_group, id_user)
                            VALUES (?, ?)
                        """,
            (id_group, id_user),
        )
        connection.commit()
    connection.close()
    print("Группа успешно добавлена.")


def add_event(event_name, group_name):
    if not os.path.exists(db_path):
        create_dataBase()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute(
        """
                     SELECT id_group FROM Groups
                        WHERE group_name = ?
                        """,
        (group_name,),
    )
    id_group = cursor.fetchone()[0]

    cursor.execute(
        """
                   SELECT * FROM Events
                     WHERE event_name = ? AND id_group = ?
                        """,
        (event_name, id_group),
    )
    event = cursor.fetchone()
    if event:
        raise Exception(f"Событие с именем {event_name} уже существует.")
    else:

        cursor.execute(
            """
                    INSERT INTO Events (event_name, id_group)
                        VALUES (?, ?)
                    """,
            (event_name, id_group),
        )
        connection.commit()
        connection.close()
        print("Событие успешно добавлено.")


def add_date(date, start_time, end_time, id_event):
    if not os.path.exists(db_path):
        create_dataBase()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute(
        """
                INSERT INTO Date (date, start_time, end_time, id_event)
                    VALUES (?, ?, ?, ?)
                """,
        (date, start_time, end_time, id_event),
    )
    connection.commit()
    connection.close()
    print("Дата успешно добавлена.")


def get_user(tg_id):
    if not os.path.exists(db_path):
        create_dataBase()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute(
        """
                SELECT * FROM Users
                WHERE tg_id = ?
                """,
        (tg_id,),
    )
    user = cursor.fetchone()
    connection.close()
    print(user)
    return user


def get_user_id(username):
    if not os.path.exists(db_path):
        create_dataBase()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute(
        """
                SELECT tg_id FROM Users
                WHERE username = ?
                """,
        (username,),
    )
    tg_id = cursor.fetchone()
    if tg_id == None:
        raise Exception(f"Пользователь с именем {username} не найден.")
    else:
        tg_id = tg_id[0]
    connection.close()
    # print(tg_id)
    return tg_id


def get_group(group_name):
    if not os.path.exists(db_path):
        create_dataBase()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute(
        """
                SELECT id_group FROM Groups
                WHERE group_name = ?
                """,
        (group_name,),
    )
    id_group = cursor.fetchone()[0]

    cursor.execute(
        """
                SELECT * FROM Groups_users
                WHERE id_group = ?
                """,
        (id_group,),
    )
    group = cursor.fetchall()
    connection.close()
    print(group)
    return group


def get_groups(tg_id):
    if not os.path.exists(db_path):
        create_dataBase()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute("""SELECT id_user FROM Users WHERE tg_id = ?""", (tg_id,))
    id_user = cursor.fetchone()[0]
    cursor.execute(
        """
                SELECT group_name FROM Groups
                JOIN Groups_users as gu ON Groups.id_group = gu.id_group
                WHERE gu.id_user = ?
                """,
        (id_user,),
    )
    groups = cursor.fetchall()
    connection.close()
    print(groups)
    return groups


def get_group_event(event_name):
    if not os.path.exists(db_path):
        create_dataBase()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute(
        """
                SELECT group_name FROM Events
                JOIN Groups as g ON Events.id_group = g.id_group
                WHERE event_name = ?
                """,
        (event_name,),
    )
    event = cursor.fetchall()
    connection.close()
    print(event)
    return event


def get_events(group_name):
    if not os.path.exists(db_path):
        create_dataBase()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute(
        """SELECT id_group FROM Groups WHERE group_name = ?""", (group_name,)
    )
    id_group = cursor.fetchone()[0]
    cursor.execute(
        """
                SELECT event_name FROM Events
                WHERE id_group = ?
                
                """,
        (id_group,),
    )
    events = cursor.fetchall()
    connection.close()
    print(events)
    return events


def get_event(event_name, group_name):
    if not os.path.exists(db_path):
        create_dataBase()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute(
        """
                SELECT * FROM Events
                WHERE event_name = ?
                AND id_group = (
                    SELECT id_group FROM Groups_users
                    WHERE group_name = ?
                )
                """,
        (event_name, group_name),
    )
    event = cursor.fetchall()
    connection.close()
    print(event)
    return event


def get_date(date, event_name, group_name):
    if not os.path.exists(db_path):
        create_dataBase()

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute(
        """
                SELECT * FROM Date
                WHERE date = ?
                AND id_event = (
                    SELECT id_event FROM Events
                    WHERE event_name = ?
                    AND id_group = (
                        SELECT id_group FROM Groups_users
                        WHERE group_name = ?
                    )
                )
                """,
        (date, event_name, group_name),
    )
    date = cursor.fetchall()
    connection.close()
    print(date)
    return date


def user_in_group(group_name, tg_id):
    if not os.path.exists(db_path):
        create_dataBase()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute(
        """
                   SELECT * FROM Groups_users
                   WHERE id_group = (
                       SELECT id_group FROM Groups
                       WHERE group_name = ?
                   )
                   AND id_user = (
                        SELECT id_user FROM Users
                        WHERE tg_id = ?)
                   """,
        (group_name, tg_id),
    )
    user = cursor.fetchall()
    connection.close()
    # print(user)
    return user


def get_group_users(group_name):
    if not os.path.exists(db_path):
        create_dataBase()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute(
        """
                   SELECT id_group FROM Groups
                   WHERE group_name = ?
                   """,
        (group_name,),
    )
    id_group = cursor.fetchone()[0]

    cursor.execute(
        """
                SELECT * FROM Users
                WHERE id_user IN (
                    SELECT id_user FROM Groups_users
                    WHERE id_group = ?
                )
                """,
        (id_group,),
    )
    users = cursor.fetchall()
    connection.close()
    print(users)
    return users


def edit_group_name(group_name, new_group_name):
    if not os.path.exists(db_path):
        create_dataBase()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute(
        """
                SELECT id_group FROM Groups
                WHERE group_name = ?
                """,
        (new_group_name,),
    )
    id_group = cursor.fetchone()
    if id_group:
        raise Exception(f"Группа с именем {group_name} уже существует.")
    else:
        cursor.execute(
            """
                    UPDATE Groups
                    SET group_name = ?
                    WHERE group_name = ?
                    """,
            (new_group_name, group_name),
        )
        connection.commit()
        connection.close()
        print("Имя группы успешно изменено.")


def delete_group(group_name, tg_id):
    if not os.path.exists(db_path):
        create_dataBase()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute(
        """ 
                   SELECT id_user FROM Users
                   WHERE tg_id = ?
                   """,
        (tg_id,),
    )
    id_user = cursor.fetchone()[0]

    cursor.execute(
        """
                   SELECT id_group FROM Groups
                   WHERE group_name = ?
                   """,
        (group_name,),
    )
    id_group = cursor.fetchone()[0]

    cursor.execute(
        """
                   DELETE  FROM Groups_users
                   WHERE id_group = ? AND id_user = ?
                    """,
        (id_group, id_user),
    )

    connection.commit()

    cursor.execute(
        """
                   SELECT * FROM Groups_users
                   WHERE id_group = ?
                   """,
        (id_group,),
    )
    exist_group = cursor.fetchall()
    if exist_group == []:
        cursor.execute(
            """
                       DELETE FROM Groups
                       WHERE group_name = ?
                       """,
            (group_name,),
        )
        connection.commit()
    connection.close()
    print("Группа успешно удалена.")


def add_date(
    event_name, group_name, year, month, day, start_hour, start_min, end_hour, end_min
):
    if not os.path.exists(db_path):
        create_dataBase()

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    start_time = f"{start_hour}:{start_min}"
    end_time = f"{end_hour}:{end_min}"
    date = f"{year}.{month_conv[month]}.{day}"

    cursor.execute(
        """
                SELECT id_event FROM Events
                WHERE event_name = ?
                AND id_group = (
                    SELECT id_group FROM Groups
                    WHERE group_name = ?
                )
                """,
        (event_name, group_name),
    )
    id_event = cursor.fetchone()[0]

    cursor.execute(
        """
                SELECT * FROM Date
                    WHERE date = ?
                    AND id_event = ?
                    AND start_time = ?
                    AND end_time = ?
                """,
        (date, id_event, start_time, end_time),
    )

    existing_date = cursor.fetchone()
    if existing_date:
        raise Exception(f"Дата {date} уже существует.")

    else:
        cursor.execute(
            """
                    INSERT INTO Date (date, start_time, end_time, id_event)
                        VALUES (?, ?, ?, ?)
                    """,
            (date, start_time, end_time, id_event),
        )
        connection.commit()
        connection.close()
        print("Дата успешно добавлена.")


def get_dates_groups(event_name):
    current_time = datetime.now().time()
    current_date = datetime.now().date()

    date = current_date.strftime("%Y.%m.%d")
    time = current_time.strftime("%H:%M")

    if not os.path.exists(db_path):
        create_dataBase()

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute(
        """
                SELECT date, start_time, end_time, g.group_name FROM Date as d
                    JOIN Events as e ON d.id_event = e.id_event
                    JOIN Groups as g ON  e.id_group = g.id_group
                    WHERE e.event_name = ?
                    AND date >= ?
                    AND start_time >= ?
                    GROUP BY date, start_time, end_time, g.group_name
                """,
        (event_name, date, time),
    )
    dates = cursor.fetchall()

    connection.close()
    print(dates)
    return dates


def get_dates(event_name, group_name):
    current_time = datetime.now().time()
    current_date = datetime.now().date()

    date = current_date.strftime("%Y.%m.%d")
    time = current_time.strftime("%H:%M")

    if not os.path.exists(db_path):
        create_dataBase()

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute(
        """
                SELECT date, start_time, end_time FROM Date as d
                JOIN Events as e ON d.id_event = e.id_event
                JOIN Groups as g ON  e.id_group = g.id_group
                WHERE g.group_name = ? 
                AND e.event_name = ?
                AND date >= ?
                AND start_time >= ?
                GROUP BY date, start_time, end_time, g.group_name
                """,
        (group_name, event_name, date, time),
    )
    dates = cursor.fetchall()

    connection.close()
    print(dates)
    return dates


def get_dates_all(tg_id):
    current_time = datetime.now().time()
    current_date = datetime.now().date()

    date = current_date.strftime("%Y.%m.%d")
    time = current_time.strftime("%H:%M")

    if not os.path.exists(db_path):
        create_dataBase()

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute(
        """
                SELECT date, start_time, end_time, g.group_name, e.event_name FROM Date as d
                JOIN Events as e ON d.id_event = e.id_event
                JOIN Groups as g ON  e.id_group = g.id_group
                JOIN Groups_users as gu ON  g.id_group = gu.id_group
                JOIN Users as u ON gu.id_user = u.id_user
                WHERE u.tg_id = ?
                AND date >= ?
                AND start_time >= ?
                GROUP BY date, start_time, end_time, g.group_name
                """,
        (tg_id, date, time),
    )
    dates = cursor.fetchall()

    connection.close()
    print(dates)
    return dates


def delete_date(event_name, group_name, date, start_time, end_time):
    if not os.path.exists(db_path):
        create_dataBase()

    print(date, start_time, end_time)
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute(
        """
                SELECT id_event FROM Events
                WHERE event_name = ?
                AND id_group = (
                    SELECT id_group FROM Groups
                    WHERE group_name = ?
                )
                """,
        (event_name, group_name),
    )
    id_event = cursor.fetchone()[0]

    cursor.execute(
        """
                DELETE FROM Date
                WHERE date = ?
                AND start_time = ?
                AND end_time = ?
                AND id_event = ?
                """,
        (date, start_time, end_time, id_event),
    )
    connection.commit()
    connection.close()
    print("Дата успешно удалена.")


def delete_event(event_name, group_name):
    if not os.path.exists(db_path):
        create_dataBase()

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute(
        """
                SELECT id_group FROM Groups
                WHERE group_name = ?
                """,
        (group_name,),
    )
    id_group = cursor.fetchone()[0]

    cursor.execute(
        """
                DELETE FROM Events
                WHERE event_name = ?
                AND id_group = ?
                """,
        (event_name, id_group),
    )
    connection.commit()
    connection.close()
    print("Событие успешно удалено.")


def get_notification_list(date, time):
    if not os.path.exists(db_path):
        create_dataBase()

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute(
        """
SELECT date, start_time, end_time, g.group_name, e.event_name, u.tg_id FROM Date as d
JOIN Events as e ON d.id_event = e.id_event
JOIN Groups as g ON  e.id_group = g.id_group
JOIN Groups_users as gu ON gu.id_group = g.id_group
JOIN Users as u ON u.id_user = gu.id_user
WHERE d.date = ? AND d.start_time = ?
                   """,
        (date, time),
    )
    dates = cursor.fetchall()
    return dates
