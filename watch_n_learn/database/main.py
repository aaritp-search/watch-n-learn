from sqlalchemy.engine.create import create_engine
from sqlalchemy.orm.decl_api import declarative_base
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.session import sessionmaker

Base = declarative_base()

engine = create_engine("sqlite:///database.sqlite3", connect_args={"check_same_thread": False})

session: Session = sessionmaker(engine, autoflush=False)()
