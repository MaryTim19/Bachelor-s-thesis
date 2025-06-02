from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
#uvicorn main:app --reload
# Дані для підключення (заміни на свої)
MYSQL_USER = "root"
MYSQL_PASSWORD = "password"
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_DB = "wedding_dresses"

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root@localhost:3306/wedding_db"


# SQLAlchemy сесія
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовий клас для моделей
Base = declarative_base()
