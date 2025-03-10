from flask import render_template
from app import app
import requests

@app.route("/")
def hello_world():
    return "Welcome!"