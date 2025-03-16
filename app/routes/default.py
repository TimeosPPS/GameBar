from flask import render_template, request
from app import app
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, func
from app.db.models.base import engine
from app.db.models.data import GameBarDB
from .utils import get_sorted_query

import requests

session = Session(engine)
@app.get("/")
def main_page():
    random_games = session.query(GameBarDB).order_by(func.random()).limit(6).all()
    top = session.query(GameBarDB).order_by(desc(GameBarDB.rating)).limit(6).all()
    return render_template("index.html", top=top, random_games=random_games)


@app.get("/catalog/")
def games_list():
    sort_by = request.args.get('sort_by', '')
    games = session.query(GameBarDB)
    games = get_sorted_query(games, sort_by)
    return render_template("catalog.html", games=games.all())


@app.get("/catalog/filter=<filter>/")
def catalog_filter(filter):
    genres = filter.split(",")
    sort_by = request.args.get('sort_by', '')
    filtered = session.query(GameBarDB).filter(GameBarDB.genre.in_(genres))
    filtered = get_sorted_query(filtered, sort_by)

    return render_template("catalog.html", games=filtered.all())

@app.get("/game/<id>/")
def game_page(id):
    game = session.query(GameBarDB).filter(GameBarDB.id == id).first()
    return render_template("game.html",
                           name=game.name,
                           description=game.description,
                           genre=game.genre,
                           rating=game.rating,
                           picture=game.picture
                           )
