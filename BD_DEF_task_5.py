
import psycopg2

# 1.Функция, создающая структуру БД (таблицы)
def create_bd_client_phone(conn):
    with conn.cursor() as cur:
        # удаление таблиц
        cur.execute("""
        DROP TABLE phone;
        DROP TABLE client;
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS client(
            id SERIAL PRIMARY KEY, 
            name VARCHAR(40) NOT NULL,
            last_name VARCHAR(60) NOT NULL,
            email VARCHAR(50) UNIQUE NOT NULL,
            phones VARCHAR(30) 
            );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS phone(
            id SERIAL PRIMARY KEY,
            number_phone VARCHAR(30),
            client_id INTEGER REFERENCES client(id)
            );            
        """)
        
    # 2.Функция, позволяющая добавить нового клиента
def add_client(conn, name, last_name, email, phones = None):
    with conn.cursor() as cur:
        cur.execute(f"""
        INSERT INTO client(name, last_name, email, phones)
        VALUES('{name}', '{last_name}', '{email}', '{phones}') RETURNING id, name, last_name, email, phones;
        """)
        print(cur.fetchone())
    
 # 3.Функция, позволяющая добавить телефон для существующего клиента
def add_phone(conn, number_phone, client_id):
    with conn.cursor() as cur:
        cur.execute(f"""
        INSERT INTO phone(number_phone, client_id)
        VALUES ('{number_phone}', '{client_id}') RETURNING number_phone, client_id; 
        """)
        print(cur.fetchall())
        
# 4.Функция, позволяющая изменить данные о клиенте
def change_client(conn, id, new_name=None, new_last_name=None, new_email=None, new_phones=None):
    with conn.cursor() as cur:
        cur.execute(f"""
                UPDATE client
            set name = '{new_name}', last_name = '{new_last_name}', email = '{new_email}', phones = '{new_phones}'
                WHERE id = '{id}';
                """)
        
# 5.Функция, позволяющая удалить телефон для существующего клиента
def delete_phone(conn, id, number_phone=None):
    with conn.cursor() as cur:
        cur.execute(f"""
                DELETE from phone
                WHERE client_id = '{id}' and number_phone = '{number_phone}';
                """)
        
# 6.Функция, позволяющая удалить существующего клиента
def delete_client(conn, id):
    with conn.cursor() as cur:
        cur.execute(f"""
                DELETE from client
                WHERE id = '{id}';
                """)

# 7.Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у или телефону)
def find_clients(conn, search_by, str):
    with conn.cursor() as cur:
        cur.execute(f"""
                    SELECT c.id, name, last_name, email, phones FROM client c
                    WHERE {search_by} = '{str}';
                    """)
        print(f"Информация о клиенте {cur.fetchall()}") # Хотел здесь через if , но они у меня не работают
        find_phone(conn, search_by, str)
        # Ответьте пожалуйста почему эта часть кода с if не работает
        # if cur.fetchall() == ( ):
        #     print(f"Дополнительный номер телефона клиента {cur.fetchall()}")
        # if cur.fetchall() != ( ):
        #     find_phone(conn, search_by, str)
               
        
def find_phone(conn, search_by, str):
    with conn.cursor() as cur:
        cur.execute(f"""
                    SELECT c.id, name, last_name, email, phones, number_phone FROM client c
                    JOIN phone p ON c.id = p.client_id
                    WHERE {search_by} = '{str}';
                    """)
        print(f"Информация о клиенте c дополнительным номером телефона клиента {cur.fetchall()}")
        # Ответьте пожалуйста всё таки почему эта часть кода с if не работает, ну только конкретно        
        # if find_phone != None:
        #     print(f"Дополнительный номер телефона клиента {cur.fetchall()}")
        # if find_phone == None:
        #     print('if-2')
        #     find_clients(conn, search_by, str)
            
        

conn = psycopg2.connect(database="netology_db", user="postgres", password="happy1228")
with conn.cursor() as cur:
    
    # 1.Вызов функции, создающей структуру БД (таблицы)
    create_bd = create_bd_client_phone(conn)
    print("База данных создана")
     
    # 2.Вызов функции, позволяющей добавить нового клиента
    add_client(conn, 'Aram', 'Darbinayan', 'aramiusfilm@yandex.ru')
    print('Новый клиент Арам добавлен')
    add_client(conn, 'Oleg', 'Krapiva', 'okrap@mail.ru', '89004002233')
    print('Новый клиент Олег, добавлен')
    add_client(conn, 'Olya', 'Krasivaya', 'olkras@mail.ru', '89004004455')
    print('Новый клиент Оля, добавлен') 
    add_client(conn, 'Gor', 'Darbinayan', 'albrus@yandex.ru')
    print('Новый клиент Арам добавлен')
    
    # 3.Вызов функции позволяющей добавить телефон для существующего клиента
    add_phone(conn, 89649156228, 1)
    print('Новый номер телефона добавлен на 1')
    add_phone(conn, 89284021118, 2)
    print('Новый номер телефона добавлен на 2')
    add_phone(conn, 89281002233, 4)
    print('Новый номер телефона добавлен на 4')    
    # add_phone(conn, 89283334455, 3)
    # print('Новый номер телефона добавлен на 3')
 
    # 4.Вызов функции позволяющей изменить данные о клиенте
    change_client(conn, 2, 'Женя', 'Харламов', 'gehar@mail.ru')
    print('Дынные о клиенте 2 обновлены')
    
    # 5.Вызов функции позволяющей удалить телефон для существующего клиента
    delete_phone(conn, 1, '89004004455') 
    print('Телефон клиента 1 удалён')
    
    # 6.Вызов функции позволяющей удалить существующего клиента
    delete_client(conn, 3)
    print('Клиент 3 удалён')
     
    # 7.Вызов функции позволяющей найти клиента по его данным (имени, фамилии, email-у или телефону) 
    find_clients(conn, 'last_name', 'Харламов')
    print('Клиент 22222 найден')
        


conn.close()
