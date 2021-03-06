import sqlite3

ADMIN_USER="hackbright"
ADMIN_PASSWORD=5980025637247534551
CONN = None
DB = None

def authenticate(username, password): 
    # if user is in the database, confirm 'yes'
    # then, get the password associated with the username and assign to DB_password
    # if hashed(DB_password) is the same as hashed(input password), you're gravy.
    # otherwise fuck you.
    try:
        user_id = get_user_by_name(username)
        db_password = get_password(username)
        if hash(db_password) == hash(password):
            return user_id
    except TypeError:
        return None


def get_user_by_name(username):
    query = """SELECT id FROM Users WHERE username == ?"""
    DB.execute(query, (username,))
    user_id_tup = DB.fetchone()
    if user_id_tup == None:
        return None
    else:
        return user_id_tup[0]

def get_password(username):
    query = """SELECT password FROM Users WHERE username == ?"""
    DB.execute(query, (username,))
    DB_password_tup = DB.fetchone()
    DB_password = DB_password_tup[0]
    return DB_password

def get_username_by_id(user_id):
    query = """SELECT username FROM Users WHERE id == ?"""
    DB.execute(query, (user_id,))
    DB_username_tup = DB.fetchone()
    DB_username = DB_username_tup[0]
    return DB_username

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect('thewall.db')
    DB = CONN.cursor()

def create_new_post(owner_id, author_id, content):
    query = """INSERT INTO Wall_posts (owner_id, author_id, content) VALUES (?,?,?)"""
    DB.execute(query, (owner_id, author_id, content))
    CONN.commit()
    return (author_id, owner_id, content)

def get_user_posts(username):
    user_id = get_user_by_name(username)
    query = """SELECT Wall_posts.content
    FROM Users JOIN Wall_posts ON (Users.id=Wall_posts.author_id) WHERE Users.id == ?"""
    DB.execute(query, (user_id,))
    posts = DB.fetchall()
    return posts

def create_new_account(username, password):
    connect_to_db()
    query = """INSERT INTO Users (username, password) VALUES (?, ?)"""
    password = hash(password)
    DB.execute(query, (username, password))
    CONN.commit()
    return (username, password)

