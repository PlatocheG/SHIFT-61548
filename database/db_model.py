from sqlalchemy import (
    create_engine, MetaData, Table, Column, ForeignKey,
    String, Integer, Float, DateTime, LargeBinary,
)

from config import DB_URL

engine = create_engine(url = DB_URL)

db_metadata = MetaData()

db_user = Table(
    "user",
    db_metadata,
    Column("id", Integer, primary_key=True),
    Column("login", String(5), unique=True),
    Column("f_name", String(20)),
    Column("l_name", String(20)),
    Column("email", String(40)),
)

db_password = Table(
    "password",
    db_metadata,
    Column("id", ForeignKey("user.id"), primary_key=True),
    Column("pwd", LargeBinary, nullable=True)
)

db_salary = Table(
    "salary",
    db_metadata,
    Column("id", ForeignKey("user.id"), primary_key=True),
    Column("amount", Float, nullable=True),
    Column("next_raise_dt", DateTime, nullable=True)
)






