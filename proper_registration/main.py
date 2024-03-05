import os, binascii
from datetime import datetime, timedelta
from random import randint
import requests
import json

from flask import Flask, render_template, flash, redirect
from flask_login import LoginManager, login_user
from werkzeug.security import generate_password_hash, check_password_hash

from forms import SignupForm, LoginForm
from models import Session, create_db, User, Event

app = Flask(__name__)
app.config['SECRET_KEY'] = binascii.hexlify(os.urandom(24))
print(app.config['SECRET_KEY'])

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)
create_db()

@login_manager.user_loader
def user_loader(user_id):
    with Session as session:
        return session.query(User).where(User.id == user_id).first()


@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        with Session() as session:
            user = session.query(User).where(User.email == form.email.data).first()
            if user:
                flash("Email already registered")
                return redirect("login")
        pwd = generate_password_hash(form.password.data)
        user = User(
            nickname=form.email.data.split('@')[0],
            email=form.email.data,
            password=pwd,
        )
        session.add(user)
        session.commit()

        return redirect("login")
    return render_template('form_template.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        with Session() as session:
            user = session.query(User).where(User.nickname == form.nickname.data).first()
            if user:
                if check_password_hash(user.password, form.password.data):
                    login_user(user)
                    return redirect("/")
                flash("Wrong password")
                return redirect('login')
            flash("Wrong nickname")
            return redirect("login")
    return render_template('form_template.html', form=form)

@app.route('/generate_activities')
def generate_activities():
    with Session() as session:
        for item in range(5):
            event_date = datetime.today() + timedelta(days=item)
            
            for _ in range(randint(1, 4)):
                event = Event()
                req = requests.get("https://www.boredapi.com/api/activity/")
                req_content = json.loads(req.content)
                event.date = event_date
                event.header = req_content["activity"]
                event.describe = req_content["activity"]
                session.add(event)
                session.commit()
    return redirect("/")

@app.route('/')
def index():
    with Session() as session:
        events = session.query(Event).all()
        dct = {}
        for event in events:
            date = datetime.strftime(event.date, "%d %B")
            dct.setdefault(date, []).append(event.header)
    return render_template("main.html", iterable=dct)

@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(405)
@app.errorhandler(500)
def handler(e):
    return render_template("error.html", code=e.code)


if __name__ == '__main__':
    app.run()
