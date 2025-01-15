import os
import sqlite3

db_path = 'dataBase/events.db'

def create_dataBase():
    if not os.path.exists(db_path):
        connection = sqlite3.connect(db_path)
        cursor=connection.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users  (               
        id_user INTEGER PRIMARY KEY,
        tg_id INTEGER UNIQUE,
        username TEXT UNIQUE,
        name TEXT,
        last_name TEXT)
        ''')

        cursor.execute('CREATE INDEX IF NOT EXISTS idx_tg_id ON Users (tg_id)')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Groups_users  (
        id_group INTEGER PRIMARY KEY,
        group_name TEXT,
        id_user INTEGER,
        FOREIGN KEY (id_user) REFERENCES Users(id_user))
        ''')

        cursor.execute('CREATE INDEX IF NOT EXISTS idx_group_name ON Groups_users (group_name)')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Events  (
        id_event INTEGER PRIMARY KEY,
        event_name TEXT,
        id_group INTEGER,
        FOREIGN KEY (id_group) REFERENCES Groups_users(id_group)
                    ON DELETE CASCADE)
        ''')

        cursor.execute('CREATE INDEX IF NOT EXISTS idx_event_name ON Events (event_name)')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Date  (
        id_date INTEGER PRIMARY KEY,
        date TEXT,
        start_time TEXT,
        end_time TEXT,
        id_event INTEGER,
        FOREIGN KEY (id_event) REFERENCES Events(id_event))
        ''')               

        cursor.execute('CREATE INDEX IF NOT EXISTS idx_date ON Date (date)')

        connection.commit()
        connection.close()
        print("База данных и таблицы успешно созданы.")




def add_user(tg_id, username=None, name=None, last_name=None):
    if not os.path.exists(db_path):
        create_dataBase()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    columns = ['tg_id']
    values = [tg_id]

    if username is not None:
        columns.append('username')
        values.append(username)

    if name is not None:    
        columns.append('name')
        values.append(name)
    
    if last_name is not None:
        columns.append('last_name')
        values.append(last_name)
    
    columns_str = ', '.join(columns)
    values_str = ', '.join(['?']*len(values))
    cursor.execute(f'''
                INSERT INTO Users ({columns_str})
                    VALUES ({values_str})
                    ''', tuple(values)) 

    connection.commit()
    connection.close()
    print("Пользователь успешно добавлен.")


def add_group(group_name, tg_ids):
    if not os.path.exists(db_path):
        create_dataBase()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    for tg_id in tg_ids:
        cursor.execute('''
                        SELECT id_user FROM Users
                        WHERE tg_id = ?
                        ''', (tg_id,))
        id_user = cursor.fetchone()[0]
        cursor.execute('''
                        INSERT INTO Groups_users (group_name, id_user)
                            VALUES (?, ?)
                        ''', 
                        (group_name, id_user))
        connection.commit()
    connection.close()
    print("Группа успешно добавлена.")


def add_event(event_name, id_group):
    if not os.path.exists(db_path):
        create_dataBase()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute('''
                INSERT INTO Events (event_name, id_group)
                    VALUES (?, ?)
                ''', (event_name, id_group))
    connection.commit()
    connection.close()
    print("Событие успешно добавлено.")


def add_date(date, start_time, end_time, id_event):
    if not os.path.exists(db_path):
        create_dataBase()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute('''
                INSERT INTO Date (date, start_time, end_time, id_event)
                    VALUES (?, ?, ?, ?)
                ''', (date, start_time, end_time, id_event))
    connection.commit()
    connection.close()
    print("Дата успешно добавлена.")

def get_user(tg_id):
    if not os.path.exists(db_path):
        create_dataBase()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute('''
                SELECT * FROM Users
                WHERE tg_id = ?
                ''', (tg_id,))
    user = cursor.fetchone()
    connection.close()
    print(user)
    return user

def get_group(group_name):
    if not os.path.exists(db_path):
        create_dataBase()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute('''
                SELECT * FROM Groups_users
                WHERE group_name = ?
                ''', (group_name,))
    group = cursor.fetchall()
    connection.close()
    print(group)
    return group
    
def get_event(event_name, group_name):
    if not os.path.exists(db_path):
        create_dataBase()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute('''
                SELECT * FROM Events
                WHERE event_name = ?
                AND id_group = (
                    SELECT id_group FROM Groups_users
                    WHERE group_name = ?
                )
                ''', (event_name, group_name))
    event = cursor.fetchall()
    connection.close()
    print(event)
    return event
    
def get_date(date, event_name, group_name):
    if not os.path.exists(db_path):
        create_dataBase()

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute('''
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
                ''', (date, event_name, group_name))
    date = cursor.fetchall()
    connection.close()
    print(date)
    return date


