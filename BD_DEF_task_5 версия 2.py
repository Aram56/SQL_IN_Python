
import psycopg2

# Удаление таблиц
def delete_tables(cur):
    cur.execute("""
        DROP TABLE phone;
        DROP TABLE client;
        """)



# 1.Функция, создающая структуру БД (таблицы)
def create_bd_client_phone(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS client(
        id SERIAL PRIMARY KEY, 
        name VARCHAR(40) NOT NULL,
        last_name VARCHAR(60) NOT NULL,
        email VARCHAR(50) UNIQUE NOT NULL
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
def add_client(cur, name, last_name, email):    
    cur.execute(
        """INSERT INTO client(name, last_name, email) 
    VALUES(%s,%s,%s) RETURNING id, name, last_name, email;"""
    , (name, last_name, email)
    )
    print(cur.fetchall()) 
    
    
 # 3.Функция, позволяющая добавить телефон для существующего клиента
def add_phone(cur, number_phone, client_id):
    cur.execute("""
    INSERT INTO phone(number_phone, client_id)
    VALUES (%s,%s) RETURNING number_phone, client_id; 
    """, (number_phone, client_id))
    print(cur.fetchall())
        
# 4.Функция, позволяющая изменить данные о клиенте
def change_client(cur, id , dic):
    for k, v in dic.items():
        cur.execute(f"""
                UPDATE client
            set {k}=%s 
            WHERE id = %s RETURNING id, name, last_name, email;
                """, (v, id))
    print(cur.fetchall())  
    
# 5.Функция, позволяющая удалить телефон для существующего клиента
def delete_phone(cur, id, number_phone=None):
    cur.execute("""
            DELETE from phone
            WHERE client_id = %s and number_phone = %s;
            """, (id, number_phone))
        
# 6.Функция, позволяющая удалить существующего клиента
def delete_client(cur, id):
    cur.execute("""
                DELETE from phone
                WHERE client_id = %s;
                """, (id,))
    cur.execute("""
            DELETE from client
            WHERE id = %s;
            """, (id,))
    
# 7.Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у или телефону)
def find_clients(cur, filds_dict):
    str = ' and '.join([f"{x} = '{y}'" for x, y in filds_dict.items() if y != None])
    cur.execute("""SELECT name, last_name, email, p.number_phone FROM client c 
     LEFT JOIN phone p ON c.id = p.client_id WHERE """ + str)      
    print(f"Информация о клиенте {cur.fetchall()}")        
        
        
        
if __name__ == "__main__":
    
    with psycopg2.connect(database="netology_db", user="postgres", password="happy1228") as conn:
        with conn.cursor() as cur:
           
            # Удаление таблиц.
            delete_tables(cur)
            print('Все таблицы удалены')
            
            # 1.Вызов функции, создающей структуру БД (таблицы)
            create_bd = create_bd_client_phone(cur)
            print("База данных создана")
            
            # 2.Вызов функции, позволяющей добавить нового клиента
            add_client(cur, 'Aram', 'Darbinayan', 'aramiusfilm@yandex.ru')
            print('Новый клиент Арам добавлен')
            add_client(cur, 'Oleg', 'Krapiva', 'okrap@mail.ru')
            print('Новый клиент Олег, добавлен')
            add_client(cur, 'Olya', 'Krasivaya', 'olkras@mail.ru')
            print('Новый клиент Оля, добавлен') 
            add_client(cur, 'Gor', 'Darbinayan', 'albrus@yandex.ru')
            print('Новый клиент Гор добавлен')
            
            # 3.Вызов функции позволяющей добавить телефон для существующего клиента
            add_phone(cur, 89649156228, 1)
            print('Новый номер телефона добавлен на 1')
            add_phone(cur, 89284021118, 2)
            print('Новый номер телефона добавлен на 2')
            add_phone(cur, 89281002233, 4)
            print('Новый номер телефона добавлен на 4') 
            add_phone(cur, 89004004455, 1)
            print('Новый номер телефона добавлен на 1')   
            add_phone(cur, 89283334455, 3)
            print('Новый номер телефона добавлен на 3')
        
            # 4.Вызов функции позволяющей изменить данные о клиенте
            change_client(cur, 2, {'name': 'Jon'})
            print('Дынные о клиенте 2 обновлены снова')
            change_client(cur, 2, {'last_name': 'Харламов'})
            print('Дынные о клиенте 2 обновлены снова')
            
            # 5.Вызов функции позволяющей удалить телефон для существующего клиента
            delete_phone(cur, 1, '89004004455') 
            print('Телефон клиента 1 удалён')
            
            # 6.Вызов функции позволяющей удалить существующего клиента
            delete_client(cur, 3)
            print('Клиент 3 удалён')
            
            # 7.Вызов функции позволяющей найти клиента по его данным (имени, фамилии, email-у или телефону) 
            find_clients(cur, {'number_phone': '89284021118'})
            print('Нужный клиент найден')
            
            find_clients(cur, {'last_name': 'Darbinayan'})
            print('Нужный клиент найден')
            
            find_clients(cur, {'last_name': 'Darbinayan', 'name': 'Gor'})
            print('Нужный клиент найден')
        
     
            

    
