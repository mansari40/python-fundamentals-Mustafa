from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import SQLAlchemyError

DATABASE_URL = "mysql+pymysql://student:student123@localhost:3306/demo_db"

engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    age = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<User {self.name}, {self.email}, {self.age}>"


SessionLocal = sessionmaker(bind=engine)


def get_session():
    return SessionLocal()


def get_all_users():
    session = get_session()
    try:
        return session.query(User).all()
    except SQLAlchemyError as e:
        print("Error:", e)
        return []
    finally:
        session.close()


def find_user_by_name(username):
    session = get_session()
    try:
        return session.query(User).filter(User.name == username).first()
    except SQLAlchemyError as e:
        print("Error:", e)
        return None
    finally:
        session.close()


def insert_user(name, email, age):
    session = get_session()
    try:
        user = User(name=name, email=email, age=age)
        session.add(user)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print("Insert failed:", e)
    finally:
        session.close()


def update_user_age(username, new_age):
    session = get_session()
    try:
        user = session.query(User).filter(User.name == username).first()
        if user:
            user.age = new_age
            session.commit()
        else:
            print("User not found")
    except SQLAlchemyError as e:
        session.rollback()
        print("Error:", e)
    finally:
        session.close()


if __name__ == "__main__":
    Base.metadata.create_all(engine)
