from flask import Flask, render_template, send_file, request
from src.db import insert_data_row, create_table_user, get_password_by_login
import sqlite3
from datetime import datetime

conn = sqlite3.connect("user_data.db", check_same_thread=False)
create_table_user(conn)

app = Flask(__name__)

@app.route("/signup")
def signup():
    return send_file("../templates/signup.html")

@app.route("/signup_get_form", methods=["POST"])
def signup_get_form():
    form = request.form
    insert_data_row(conn, form["login"], form["password"], form["name"], 
                    form["surname"], form["email"], datetime.now(), form["phone"])
    return "Success"

@app.route("/login")
def login():
    return send_file("../templates/login.html")

@app.route("/login_get_form", methods=["POST"])
def login_get_form():
    login = request.form["login"]
    input_password = request.form["password"]
    db_password = get_password_by_login(conn, login)
    if not db_password:
        return "No such login"
    elif input_password == db_password:
        return f"Logged in, welcome, {login}"
    else:
        return "Wrong password"