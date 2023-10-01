import sqlite3 as sq

cursor=None
connection=None

async def db_start():
  global cursor,connection
  connection=sq.connect('resourses/users.db')
  cursor=connection.cursor()
  cursor.execute('''CREATE TABLE if not exists clients (
     "tel_number"    TEXT NOT NULL UNIQUE,
     "name"    INTEGER NOT NULL,
     "master"    TEXT,
     FOREIGN KEY("master") REFERENCES "masters"("tel_number"),
     PRIMARY KEY("tel_number")
 )  ''')
  cursor.execute('''CREATE TABLE if not exists masters (
    "tel_number"    TEXT NOT NULL UNIQUE,
    "name"    TEXT NOT NULL,
    "status"    INTEGER DEFAULT 1,
    "rate"    INTEGER DEFAULT 10,
    "image"    TEXT NOT NULL,
    PRIMARY KEY("tel_number")
) ''')
  connection.commit()
async def create_client(client:dict)->None:
      tel_number_client=client['tel']
      result=cursor.execute(f'Select 1 from clients where tel_number=={tel_number_client}').fetchone()
      if not result:
        cursor.execute(f'Insert into clients values({client["tel"]},{client["name"]},{client["master"]})')
        connection.commit()

async def get_client(telephone_number,cursor)->bool:
    result = cursor.execute(f'Select 1 from clients where tel_number=={telephone_number}').fetchone()
    return len(result)>0

async def get_masters(cursor)->tuple:
    result = cursor.execute(f'Select * from masters where status=1').fetchall()#получим список кортежей
    return result

