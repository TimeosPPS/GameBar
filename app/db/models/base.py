
from sqlalchemy import(
    create_engine
)
from sqlalchemy.orm import(
    DeclarativeBase,
    sessionmaker
)



DB = "sqlite:///app.db"
User_DB = "sqlite:///users.db"

engine = create_engine(DB, echo=True)
engine_users = create_engine(User_DB, echo=True)

Session = sessionmaker(bind=engine)
Session_users = sessionmaker(bind=engine_users)

class Base(DeclarativeBase):
    ...

def create_db():
    Base.metadata.create_all(engine)
    Base.metadata.create_all(engine_users)


def fill_db(games, GameBarDB):
    session = Session()
    for game in games:
        new_game = GameBarDB(
            name=game['name'],
            description=game['description'],
            genre=game['genre'],
            rating=int(game['rating']),
            picture=game['picture']
        )
        session.add(new_game)

    session.commit()
    session.close()
def drop_db():
    Base.metadata.drop_all(engine)