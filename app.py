from flask import Flask, render_template
from app.routes import app
from app.db.models import base

if __name__ == '__main__':
    app.run(port=5554, debug=True)