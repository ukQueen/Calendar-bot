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
            username TEXT,
            name TEXT,
            last_name TEXT
        );''')

        cursor.execute('CREATE INDEX IF NOT EXISTS idx_tg_id ON Users (tg_id)')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Groups  (
            id_group INTEGER PRIMARY KEY,
            group_name TEXT UNIQUE
        );''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Groups_users  (
            id_group_users INTEGER PRIMARY KEY,
            id_group INTEGER,
            id_user INTEGER,
            FOREIGN KEY (id_group) REFERENCES Groups(id_group),
            FOREIGN KEY (id_user) REFERENCES Users(id_user),
            UNIQUE (id_group, id_user)
        );''')


        cursor.execute('CREATE INDEX IF NOT EXISTS idx_id_group ON Groups_users (id_group)')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Events  (
            id_event INTEGER PRIMARY KEY,
            event_name TEXT,
            id_group INTEGER,
            FOREIGN KEY (id_group) REFERENCES Groups(id_group)
                        ON DELETE CASCADE
        );''')

        cursor.execute('CREATE INDEX IF NOT EXISTS idx_event_name ON Events (event_name)')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Date  (
            id_date INTEGER PRIMARY KEY,
            date TEXT,
            start_time TEXT,
            end_time TEXT,
            id_event INTEGER,
            FOREIGN KEY (id_event) REFERENCES Events(id_event)
        );''')               

        cursor.execute('CREATE INDEX IF NOT EXISTS idx_date ON Date (date)')

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


def add_group(group_name, tg_id):
    if not os.path.exists(db_path):
        create_dataBase()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute('''
                   SELECT id_group FROM Groups 
                   WHERE group_name = ?              
                   ''', (group_name,))
    group = cursor.fetchone()

    cursor.execute('''
                        SELECT id_user FROM Users
                        WHERE tg_id = ?
                        ''', (tg_id,))
    user = cursor.fetchone()

    if not group:        
        cursor.execute('''
                        INSERT INTO Groups (group_name)
                            VALUES (?)
                        ''', (group_name,))
        connection.commit()
        cursor.execute('''
                    SELECT id_group FROM Groups
                        WHERE group_name = ?
                        ''', (group_name,))
        group = cursor.fetchone()


    id_user = user[0]
    id_group = group[0]
    cursor.execute('''
                   SELECT * FROM Groups_users   
                   WHERE id_group = ? AND id_user = ?
                     ''', (id_group, id_user))
    group_user = cursor.fetchone()


    
    if group_user:
        # print(f"Группа с именем {group_name} уже существует.")
        raise Exception(f"Группа с именем {group_name} уже существует.")
    
    else:
        

        cursor.execute('''
                        INSERT INTO Groups_users (id_group, id_user)
                            VALUES (?, ?)
                        ''', 
                        (id_group, id_user))
        connection.commit()
    connection.close()
    print("Группа успешно добавлена.")


def add_event(event_name, group_name):
    if not os.path.exists(db_path):
        create_dataBase()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute('''
                     SELECT id_group FROM Groups
                        WHERE group_name = ?
                        ''', (group_name,))
    id_group = cursor.fetchone()[0]

    cursor.execute('''
                   SELECT * FROM Events
                     WHERE event_name = ? AND id_group = ?
                        ''', (event_name, id_group))
    event = cursor.fetchone()
    if event:
        raise Exception(f"Событие с именем {event_name} уже существует.")
    else:

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
def get_user_id(username):
    if not os.path.exists(db_path):
        create_dataBase()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute('''
                SELECT tg_id FROM Users
                WHERE username = ?
                ''', (username,))
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

    cursor.execute('''
                SELECT id_group FROM Groups
                WHERE group_name = ?
                ''', (group_name,))
    id_group = cursor.fetchone()[0]
    
    cursor.execute('''
                SELECT * FROM Groups_users
                WHERE id_group = ?
                ''', (id_group,))
    group = cursor.fetchall()
    connection.close()
    print(group)
    return group

def get_groups(tg_id):
    if not os.path.exists(db_path):
        create_dataBase()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute('''SELECT id_user FROM Users WHERE tg_id = ?''', (tg_id,))
    id_user = cursor.fetchone()[0]
    cursor.execute('''
                SELECT group_name FROM Groups
                JOIN Groups_users as gu ON Groups.id_group = gu.id_group
                WHERE gu.id_user = ?
                ''', (id_user,))
    groups = cursor.fetchall()
    connection.close()
    print(groups)
    return groups

def get_group_event(event_name):
    if not os.path.exists(db_path):
        create_dataBase()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute('''
                SELECT group_name FROM Events
                JOIN Groups as g ON Events.id_group = g.id_group
                WHERE event_name = ?
                ''', (event_name,))
    event = cursor.fetchall()
    connection.close()
    print(event)
    return event

def get_events(group_name):
    if not os.path.exists(db_path):
        create_dataBase()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute('''SELECT id_group FROM Groups WHERE group_name = ?''', (group_name,))
    id_group = cursor.fetchone()[0]
    cursor.execute('''
                SELECT event_name FROM Events
                WHERE id_group = ?
                
                ''', (id_group,))
    events = cursor.fetchall()
    connection.close()
    print(events)
    return events
    
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

def user_in_group(group_name, tg_id):
    if not os.path.exists(db_path):
        create_dataBase()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute('''
                   SELECT * FROM Groups_users
                   WHERE id_group = (
                       SELECT id_group FROM Groups
                       WHERE group_name = ?
                   )
                   AND id_user = (
                        SELECT id_user FROM Users
                        WHERE tg_id = ?)
                   ''', (group_name, tg_id))
    user = cursor.fetchall()
    connection.close()
    # print(user)
    return user

def get_group_users(group_name):
    if not os.path.exists(db_path):
        create_dataBase()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute('''
                   SELECT id_group FROM Groups
                   WHERE group_name = ?
                   ''', (group_name,))
    id_group = cursor.fetchone()[0]

    cursor.execute('''
                SELECT * FROM Users
                WHERE id_user IN (
                    SELECT id_user FROM Groups_users
                    WHERE id_group = ?
                )
                ''', (id_group,))
    users = cursor.fetchall()
    connection.close()
    print(users)
    return users

def edit_group_name(group_name, new_group_name):
    if not os.path.exists(db_path):
        create_dataBase()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute('''
                SELECT id_group FROM Groups
                WHERE group_name = ?
                ''', (new_group_name,))
    id_group = cursor.fetchone()
    if id_group:
        raise Exception(f"Группа с именем {group_name} уже существует.")
    else:
        cursor.execute('''
                    UPDATE Groups
                    SET group_name = ?
                    WHERE group_name = ?
                    ''', (new_group_name, group_name))
        connection.commit()
        connection.close()
        print("Имя группы успешно изменено.")

def delete_group(group_name, tg_id):
    if not os.path.exists(db_path):
        create_dataBase()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute(''' 
                   SELECT id_user FROM Users
                   WHERE tg_id = ?
                   ''', (tg_id,))
    id_user = cursor.fetchone()[0]

    cursor.execute('''
                   SELECT id_group FROM Groups
                   WHERE group_name = ?
                   ''', (group_name,))
    id_group = cursor.fetchone()[0]               

    cursor.execute('''
                   DELETE  FROM Groups_users
                   WHERE id_group = ? AND id_user = ?
                    ''', (id_group,id_user))
    
    connection.commit()

    cursor.execute('''
                   SELECT * FROM Groups_users
                   WHERE id_group = ?
                   ''', (id_group,))
    exist_group = cursor.fetchall()
    if exist_group == []:
        cursor.execute('''
                       DELETE FROM Groups
                       WHERE group_name = ?
                       ''', (group_name,))
        connection.commit()
    connection.close()
    print("Группа успешно удалена.")


