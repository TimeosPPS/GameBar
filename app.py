from flask import Flask, render_template
from app.db.models.base import create_db, drop_db
from app.db.models.data import GameBarDB
from app.routes import app
from app.db.models import base
from loguru import logger


if __name__ == '__main__':
    logger.add("app.log", level="DEBUG", format="{time} {level} {message}", rotation="10 MB", compression="zip")
    logger.info("app started")
    create_db()
    app.run(port=5554)

