import sqlite3

def create_table_user(conn):
    cr = conn.cursor()
    cr.execute("""
        CREATE TABLE IF NOT EXISTS user(
            id INTEGER PRIMARY KEY,
            login VARCHAR(128) UNIQUE,
            password VARCHAR(64),
            name VARCHAR(128),
            surname VARCHAR(128),
            email VARCHAR(128),
            reg_date DATETIME,
            phone VARCHAR(64)
        )
    """)
    conn.commit()


def insert_data_row(conn, login, password, name, surname, email, reg_date, phone):
    cr = conn.cursor()
    cr.execute("""
        INSERT INTO user(login, password, name, surname, email, reg_date, phone) VALUES
               (?, ?, ?, ?, ?, ?, ?)
    """, (login, password, name, surname, email, reg_date, phone))
    conn.commit()

def get_password_by_login(conn, login):
    cr = conn.cursor()
    cr.execute("SELECT password FROM user WHERE login = ?", (login,))
    data = cr.fetchone()
    return data[0] if data else None
