
from sqlalchemy import(
    create_engine
)
from sqlalchemy.orm import(
    DeclarativeBase,
    sessionmaker
)



DB = "sqlite:///app.db"
USERSTORY_DB = "sqlite:///users_story.db"
USER_DB = "sqlite:///users.db"

engine = create_engine(DB, echo=True)
engine_users_story = create_engine(USERSTORY_DB, echo=True)
engine_users = create_engine(USER_DB, echo=True)

Session = sessionmaker(bind=engine)
Session_users_story = sessionmaker(bind=engine_users_story)
Session_users = sessionmaker(bind=engine_users)

class Base(DeclarativeBase):
    ...

def create_db():
    Base.metadata.create_all(engine)
    Base.metadata.create_all(engine_users_story)
    Base.metadata.create_all(engine_users)

def drop_db():
    Base.metadata.drop_all(engine)