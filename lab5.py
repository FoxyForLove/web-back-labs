from flask import Blueprint, request, render_template,redirect, session
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash

lab5 = Blueprint('lab5',__name__)

@lab5.route("/lab5/")
def lab():
    return render_template("lab5/lab5.html", login=session.get('login'))


def db_connect():
    conn = psycopg2.connect(
        host = '127.0.0.1',
        database = 'liza_bulygina',
        user = 'liza_bulygina',
        password = '123'
    )
    cur = conn.cursor(cursor_factory= RealDictCursor)

    return conn, cur

def db_close(conn,cur):
    conn.commit()
    cur.close()
    conn.close()


@lab5.route("/lab5/register", methods = ['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template("lab5/register.html")
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template("lab5/register.html", error='Заполните оба поля')
    
    conn, cur = db_connect()

    cur.execute(f"select login from users where login='{login}';")
    if cur.fetchone():
        db_close(conn, cur)
        return render_template("lab5/register.html",
                               error='Такой пользователь уже существует')
    
    password_hash = generate_password_hash(password)
    cur.execute(f"insert into users (login, password) values ('{login}', '{password_hash}');")

    db_close(conn, cur)
    return render_template("lab5/success.html", login=login)

@lab5.route("/lab5/login", methods = ['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template("lab5/login.html")
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template("lab5/register.html", error='Заполните оба поля')
    
    conn, cur = db_connect()

    cur.execute(f"select * from users where login='{login}';")
    user = cur.fetchone()

    if not user:
        db_close(conn, cur)
        return render_template("lab5/login.html", 
                               error='Логин и/или пароль неверны')
    
    if not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template("lab5/login.html", 
                               error='Логин и/или пароль неверны')
    
    session['login'] = login
    db_close(conn, cur)
    return render_template("lab5/success_login.html", login=login)
