from __future__ import annotations

from app import app
from flask import render_template, request, redirect, flash, url_for
from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import SignupForm, LoginForm
from app.db.models import User, Session_users
from loguru import logger

@app.route("/register/", methods=['GET', 'POST'])
def register():
    form = SignupForm()
    if form.validate_on_submit():
        with Session_users() as session:
            user = session.query(User).where(User.nickname == form.nickname.data).first()
            if user:
                logger.warning(f"User {form.nickname.data} already exists.")
                flash('User already exists!', 'danger')
                return redirect(url_for('login'))
            try:
                hashed_password = generate_password_hash(form.password.data)
                logger.info(f"Password for {form.nickname.data} has been hashed.")
                user = User(
                    nickname=form.nickname.data,
                    password=hashed_password,
                )
                session.add(user)
                session.commit()
                logger.info(f"User object created: {user.nickname}")

                login_user(user)
                logger.info(f"User {user.nickname} logged in successfully.")
                return redirect("/")
            except Exception as e:
                session.rollback()
                logger.error(f"Error during registration: {e}")
                flash(f'Error: {e}', 'danger')
                return redirect(url_for('register'))

    return render_template("form_template.html", form=form)

@app.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        with Session_users() as session:
            user = session.query(User).where(User.nickname == form.nickname.data).first()
            if user:
                if check_password_hash(user.password, form.password.data):
                    login_user(user)
                    return redirect("/")
                flash("Wrong password")
                return redirect(url_for("login"))
            flash("Wrong nickname")
            return redirect(url_for("login"))
    return render_template("form_template.html", form=form)