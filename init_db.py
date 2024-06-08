import os
from models import Base, engine, User, SessionLocal
from sqlalchemy import select


def init_db():
    # Создание таблиц
    Base.metadata.create_all(bind=engine)
    print('database created!')

    session = SessionLocal()

    query = select(User).limit(1)
    result = session.execute(query)
    if result.fetchone() is not None:
        session.close()
        return

    # Получение пользователей из переменных окружения
    default_users = os.getenv("DEFAULT_USERS")
    if default_users:
        print(f'Users found in env!')
        users = [user.split(":") for user in default_users.split(",")]
        for username, password in users:
            db_user = User(username=username, password=password)
            session.add(db_user)
            print(f'user {username} created!')

    session.commit()
    session.close()


if __name__ == "__main__":
    init_db()
