import sqlite3


with sqlite3.connect('database.db') as conn:
    with open('schema.sql') as file:
        conn.executescript(file.read())

    cr = conn.cursor()

    cr.execute("INSERT INTO post(title, content) VALUES (?, ?)",
            ("Title1", "Content1"))
    cr.execute("INSERT INTO post(title, content) VALUES (?, ?)",
            ("Title2", "Content2"))

    conn.commit()
