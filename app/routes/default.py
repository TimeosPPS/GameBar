from flask import render_template, request, redirect, make_response, url_for, flash
from app import app
from flask_login import login_required, logout_user, current_user
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, func
from app.db.models.base import engine, engine_users_story
from app.db.models.data import GameBarDB, UserRecs
from .utils import get_sorted_query
from loguru import logger

import requests

session_db = Session(engine_users_story)
session = Session(engine)


@app.get("/")
def main_page():
    logger.info("main page loaded")
    user = current_user.nickname if current_user.is_authenticated else None

    popular_genre = None
    top_games = None

    if user:
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
    else: top_games = (session.query(GameBarDB).order_by(desc(GameBarDB.rating)).limit(6).all())

    random_games = session.query(GameBarDB).order_by(func.random()).limit(6).all()
    top = session.query(GameBarDB).order_by(desc(GameBarDB.rating)).limit(6).all()

    return render_template("index.html", top=top, random_games=random_games, recs=top_games, user=user)


@app.get("/catalog/")
def catalog():
    logger.info("catalog loaded")
    user = current_user.nickname if current_user.is_authenticated else None
    sort_by = request.args.get('sort_by', '')
    filter_param = request.args.get('filter', '')
    search = request.args.get('search', '')
    games_query = session.query(GameBarDB)

    if search:
        games_query = games_query.filter(GameBarDB.name.ilike(f"%{search}%"))

    if filter_param:
        genres = filter_param.split(",")
        games_query = games_query.filter(GameBarDB.genre.in_(genres))

    games_query = get_sorted_query(games_query, sort_by)
    games = games_query.all()

    return render_template("catalog.html", games=games, user=user)


@app.get("/game/<id>/")
def game_page(id):
    game = session.query(GameBarDB).filter(GameBarDB.id == id).first()
    user = current_user.nickname if current_user.is_authenticated else None
    if user:
        new_user = UserRecs(user=user, genre=game.genre)
        session_db.add(new_user)
        session_db.commit()

    return render_template(
        "game.html",
        user=user,
        name=game.name,
        description=game.description,
        genre=game.genre,
        rating=game.rating,
        picture=game.picture,
        id=id
    )


@app.post("/game/<id>/save/")
def save_game(id):
    game = session.query(GameBarDB).filter(GameBarDB.id == id).first()
    user = current_user.nickname if current_user.is_authenticated else None

    logger.info(f"{user} saved game")

    if user:
        existing_rec = session_db.query(UserRecs).filter(
            UserRecs.user == user, UserRecs.favourite == game.name
        ).first()

        if not existing_rec:
            new_user = UserRecs(user=user, favourite=game.name)
            session_db.add(new_user)
            session_db.commit()

        return redirect(f"/game/{id}/")
    flash("You must login first")
    return redirect(f"/game/{id}/")


@app.post("/game/<id>/delete/")
def delete_game(id):
    game = session.query(GameBarDB).filter(GameBarDB.id == id).first()
    user = current_user.nickname if current_user.is_authenticated else None

    if user:
        existing_rec = session_db.query(UserRecs).filter(
            UserRecs.user == user, UserRecs.favourite == game.name
        ).first()

        if existing_rec:
            session_db.delete(existing_rec)
            session_db.commit()

        return redirect("/favourite/")
    return flash("You must login first")


@app.get("/favourite/")
def get_favourite():
    user = current_user.nickname if current_user.is_authenticated else None

    fav_games = session_db.query(UserRecs.favourite).filter(UserRecs.user == user).all()
    favourite_game_names = [game[0] for game in fav_games if game[0]]

    games = session.query(GameBarDB).filter(GameBarDB.name.in_(favourite_game_names)).all()

    return render_template("favourite.html", games=games, user=user)

@app.get("/news/")
def news_page():
    URL = "https://api.gnews.io/v4/search"
    PARAMS = {
        "q": "video games industry",
        "lang": "en",
        "apiKey": "YOUR_API_KEY"
    }

    response = requests.get(URL, params=PARAMS)
    data = response.json()

    articles = data.get("articles", [])[:12]
    return render_template("news.html", articles=articles)
    return render_template("news.html", articles=articles)

@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('catalog'))