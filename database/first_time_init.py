from datetime import datetime

from sqlalchemy import insert, text

from auth.auth_tools import create_pwd_hash
from database.db_model import db_metadata, engine, db_user

# ---------------------------------------------------------------------------------------------------------------------------------------
# базовая инициализация данных:

db_metadata.create_all(engine)

with engine.connect() as conn:
    try:
        conn.execute(
            insert(db_user),
            [
                {"login": "e0001", "f_name": "Rick", "l_name": "Sanchez", "email": "Rick@me.com"},
                {"login": "e0002", "f_name": "Morty", "l_name": "Smith", "email": "Morty@smith.com"},
                {"login": "e0003", "f_name": "Jerry", "l_name": "Smith", "email": "Jerry@live.com"}
            ]
        )
        conn.execute(
            text("INSERT INTO password values ( (select id from user where login = :login), :pwd )"),
            [
                {"login": "Rick@me.com", "pwd": create_pwd_hash("1")},
                {"login": "Morty@smith.com", "pwd": create_pwd_hash("2")},
                {"login": "Jerry@live.com", "pwd": create_pwd_hash("3")},
            ]
        )
        conn.execute(
            text("INSERT INTO salary values ( (select id from user where login = :login), :wage, :inc_dt )"),
            [
                {"login": "Rick@me.com", "wage": 1, "inc_dt": datetime.fromisoformat('2027-01-01T00:00:00')},
                {"login": "Morty@smith.com", "wage": 10237.99, "inc_dt": datetime.fromisoformat('2024-09-01T00:00:00')}
            ]
        )
    except Exception as exp:
        # print(exp)    # можно использовать при отладке
        pass
    else:
        conn.commit()
# ---------------------------------------------------------------------------------------------------------------------------------------