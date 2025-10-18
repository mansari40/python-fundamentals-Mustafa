# db_setup.py
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    DateTime,
    func,
)
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import SQLAlchemyError

# ----------------------------------------------------
# 1️  Configure the SQLAlchemy Engine
# ----------------------------------------------------
# Use the same credentials as docker-compose.yml
DATABASE_URL = "mysql+pymysql://student:student123@localhost:3306/demo_db"

engine = create_engine(
    DATABASE_URL,
    echo=True,              # Logs SQL to console
    poolclass=QueuePool,    # Connection pooling
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
)

metadata = MetaData()

# ----------------------------------------------------
# 2️ Define Tables using SQLAlchemy Core
# ----------------------------------------------------
users_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(50), nullable=False),
    Column("email", String(100), nullable=False, unique=True),
    Column("age", Integer, nullable=False),
    Column("created_at", DateTime, server_default=func.now()),
)

# ----------------------------------------------------
# 3  Define ORM Models using Declarative Base
# ----------------------------------------------------
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    age = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<User(name='{self.name}', email='{self.email}', age={self.age})>"

# ----------------------------------------------------
# 4️ Session Setup for ORM
# ----------------------------------------------------
SessionLocal = sessionmaker(bind=engine)

def get_session():
    """Return a new SQLAlchemy session"""
    return SessionLocal()

# ----------------------------------------------------
# 5️ CRUD Utility Functions
# ----------------------------------------------------
def get_all_users() -> list[User]:
    """Retrieve all users from the database."""
    session = get_session()
    try:
        users = session.query(User).all()
        return users
    except SQLAlchemyError as e:
        print(f"Error retrieving users: {e}")
        return []
    finally:
        session.close()


def find_user_by_name(username: str) -> User | None:
    """Find a user by their name."""
    session = get_session()
    try:
        user = session.query(User).filter(User.name == username).first()
        return user
    except SQLAlchemyError as e:
        print(f"Error finding user: {e}")
        return None
    finally:
        session.close()


def insert_user(name: str, email: str, age: int) -> bool:
    """Insert a new user into the database."""
    session = get_session()
    try:
        new_user = User(name=name, email=email, age=age)
        session.add(new_user)
        session.commit()
        print(f"User '{name}' added successfully!")
        return True
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error inserting user: {e}")
        return False
    finally:
        session.close()


def update_user_age(username: str, new_age: int) -> bool:
    """Update a user's age."""
    session = get_session()
    try:
        user = session.query(User).filter(User.name == username).first()
        if not user:
            print(f"User '{username}' not found.")
            return False
        user.age = new_age
        session.commit()
        print(f"Updated '{username}' age to {new_age}.")
        return True
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error updating user: {e}")
        return False
    finally:
        session.close()

# ----------------------------------------------------
# 6 Run Test Operations
# ----------------------------------------------------
if __name__ == "__main__":
    Base.metadata.create_all(engine)  # Ensure table exists

    print("\n--- Running Database Operations ---")

    # Retrieve all users
    print("\nAll Users:")
    for u in get_all_users():
        print(u)

    # Find a user by name
    print("\nSearching for 'Alice':")
    print(find_user_by_name("Alice"))

    # Insert new user
    print("\nInserting new user 'David'...")
    insert_user("David", "david@example.com", 28)

    # Update user
    print("\nUpdating 'Bob' age to 35...")
    update_user_age("Bob", 35)

    # Show all users again
    print("\nUpdated Users:")
    for u in get_all_users():
        print(u)
