import os, binascii
from flask import Flask, render_template, flash, redirect
from flask_login import LoginManager, login_user
from werkzeug.security import generate_password_hash, check_password_hash

from forms import SignupForm, LoginForm
from models import Session, create_db, User

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


if __name__ == '__main__':
    app.run()
