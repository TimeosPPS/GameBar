from flask import render_template, request
from app import app
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, func
from app.db.models.base import engine,engine_users
from app.db.models.data import GameBarDB, UserRecs
from .utils import get_sorted_query

import requests
session_db = Session(engine_users)
session = Session(engine)
@app.get("/")
def main_page():
    user = request.remote_addr
    top_games = None

    popular_genre = (
        session_db.query(UserRecs.genre)
        .filter(UserRecs.user == user)
        .group_by(UserRecs.genre)
        .order_by(func.count(UserRecs.genre).desc())
        .limit(1)
        .scalar()
    )

    if popular_genre:
        top_games = (
            session.query(GameBarDB)
            .filter(GameBarDB.genre == popular_genre)
            .order_by(GameBarDB.rating.desc())
            .limit(6)
            .all()
        )


    random_games = session.query(GameBarDB).order_by(func.random()).limit(6).all()
    top = session.query(GameBarDB).order_by(desc(GameBarDB.rating)).limit(6).all()
    return render_template("index.html", top=top, random_games=random_games, recs=top_games)


@app.get("/catalog/")
def catalog():
    sort_by = request.args.get('sort_by', '')
    filter_param = request.args.get('filter', '')
    search = request.args.get('search', '')
    games_query = session.query(GameBarDB)

    if search:
        games_query=games_query.filter(GameBarDB.name.ilike(f"%{search}%"))

    if filter_param:
        genres = filter_param.split(",")
        games_query = games_query.filter(GameBarDB.genre.in_(genres))

    games_query = get_sorted_query(games_query, sort_by)
    games = games_query.all()

    return render_template("catalog.html", games=games)

@app.get("/game/<id>/")
def game_page(id):
    game = session.query(GameBarDB).filter(GameBarDB.id == id).first()
    user = request.remote_addr
    new_user = UserRecs(user=user, genre=game.genre)
    session_db.add(new_user)
    session_db.commit()
    return render_template("game.html",
                           name=game.name,
                           description=game.description,
                           genre=game.genre,
                           rating=game.rating,
                           picture=game.picture
                           )
