from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer
from sqlalchemy.sql.sqltypes import String

from watch_n_learn.database.main import Base

class User(Base):

    __tablename__ = "User"

    id_ = Column("UserId", Integer, primary_key=True)

    username = Column("Username", String, unique=True)

    password = Column("Password", String)
