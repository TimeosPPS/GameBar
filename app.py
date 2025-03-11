from flask import Flask, render_template
from app.db.models.base import fill_db, create_db, drop_db
from app.db.models.data import GameBarDB
from app.routes import app
from app.db.models import base


if __name__ == '__main__':
    create_db()
    app.run(port=5554)
