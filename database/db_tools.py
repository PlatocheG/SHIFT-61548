from sqlalchemy import text

from database.db_model import engine


def db_get_user_pwd(login: str) -> dict | None:
    login = login.lower()
    stmt = text("SELECT p.pwd FROM user u, password p WHERE u.id = p.id and lower(u.login) = :login")
    with engine.connect() as conn:
        result = conn.execute(stmt, [{"login": login}]).fetchone()
    if not result:
        return None
    return {"pwd": result[0]}

def db_get_salary_info(login: str) -> dict | None:
    login = login.lower()
    stmt = text("SELECT s.amount, s.next_raise_dt FROM user u, salary s WHERE u.id = s.id and lower(u.login) = :login")
    with engine.connect() as conn:
        result = conn.execute(stmt, [{"login": login}]).fetchone()
    if not result:
        return None
    return {"amnt": result[0], "next_raise_dt": result[1]}