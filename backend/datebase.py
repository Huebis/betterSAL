import sqlite3


def creatTableUser():
    conn = sqlite3.connect('datebase.db')
    cursor = conn.cursor()
    cursor_obj.execute("DROP TABLE IF EXISTS user")
    table_creation_query = """
    CREATE TABLE user (
        userid TEXT NOT NULL PRIMARY KEY,
        username TEXT NOT NULL PRIMARY KEY,
        password TEXT NOT NULL,
        class TEXT NOT NULL,
        major TEXT NOT NULL
    );
    """
    cursor_obj.execute(table_creation_query)
    conn.commit()
    return True


def creatTableGrade():
    conn = sqlite3.connect('datebase.db')
    cursor = conn.cursor()
    cursor_obj.execute("DROP TABLE IF EXISTS grade")
    table_creation_query = """
    CREATE TABLE grade (
        userid TEXT NOT NULL,
        grade INT NOT NULL,
        subject TEXT NOT NULL,
        date TEXT NOT NULL,
        name TEXT NOT NULL,
        change TEXT NOT NULL,
        message TEXT
    );
    """
    cursor_obj.execute(table_creation_query)
    conn.commit()
    return True

def creatTableAbsence():
    conn = sqlite3.connect('datebase.db')
    cursor = conn.cursor()
    cursor_obj.execute("DROP TABLE IF EXISTS absence")
    table_creation_query = """
    CREATE TABLE absence (
        userid TEXT NOT NULL,
        subject TEXT NOT NULL,
        date TEXT NOT NULL,
        starttime TEXT NOT NULL,
        endtime TEXT NOT NULL,
        excused INT not NULL
    );
    """
    cursor_obj.execute(table_creation_query)
    conn.commit()
    return True


def creatTableSchedule(): #CHANGE NOT FINISHED
    conn = sqlite3.connect('datebase.db')
    cursor = conn.cursor()
    cursor_obj.execute("DROP TABLE IF EXISTS schedule")
    table_creation_query = """
    CREATE TABLE schedule (
        lesson TEXT NOT NULL,
        subject TEXT NOT NULL,
        date TEXT NOT NULL,
        starttime TEXT NOT NULL,
        endtime TEXT NOT NULL,
        change INT not NULL
    );
    """
    cursor_obj.execute(table_creation_query)
    conn.commit()
    return True






# Execute the table creation query
cursor_obj.execute(table_creation_query)
    conn.commit()
    return True



def creatNewUser(benutzername, password):
    return True
