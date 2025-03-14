from flask import render_template
from app import app
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from app.db.models.base import engine
from app.db.models.data import GameBarDB

import requests

session = Session(engine)
@app.route("/")
def main_page():
    random_games = session.query(GameBarDB).order_by(func.random()).limit(6).all()
    top = session.query(GameBarDB).order_by(desc(GameBarDB.rating)).limit(6).all()
    return render_template("index.html", top=top, random_games=random_games)