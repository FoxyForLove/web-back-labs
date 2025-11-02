from flask import Blueprint, request, render_template,redirect, session, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3 
from os import path

lab5 = Blueprint('lab5',__name__)

@lab5.route("/lab5/")
def lab():
    return render_template("lab5/lab5.html", login=session.get('login'))


def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host = '127.0.0.1',
            database = 'liza_bulygina',
            user = 'liza_bulygina',
            password = '123'
        )
        cur = conn.cursor(cursor_factory= RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path,'database.db')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

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
    real_name = request.form.get('real_name')

    if not (login and password and real_name):
        return render_template("lab5/register.html", error='Заполните все поля')
    
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute("SELECT login FROM users WHERE login=?;", (login, ))

    if cur.fetchone():
        db_close(conn, cur)
        return render_template("lab5/register.html",
                               error='Такой пользователь уже существует')
    
    password_hash = generate_password_hash(password)

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO users (login, password, real_name) VALUES (%s, %s, %s);",
                    (login, password_hash, real_name))
    else:
        cur.execute("INSERT INTO users (login, password, real_name) VALUES (?, ?, ?);",
                    (login, password_hash, real_name))

    db_close(conn, cur)
    return render_template("lab5/success.html", login=login)


@lab5.route("/lab5/login", methods = ['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template("lab5/login.html")
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template("lab5/login.html", error='Заполните оба поля')
    
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("select * from users where login=%s;", (login, ))
    else:
        cur.execute("select * from users where login=?;", (login, ))

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


@lab5.route("/lab5/create_article", methods = ['GET', 'POST'])
def create():
    login=session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    if request.method == 'GET':
        return render_template('lab5/create_article.html')

    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_public = request.form.get('is_public') == 'on' 

    conn, cur = db_connect()

    if not title or not article_text:
        db_close(conn, cur)
        return render_template('lab5/create_article.html',
                           error='Заполните оба поля: заголовок и текст статьи')

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login, ))

    user_id = cur.fetchone()["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO articles (user_id, title, article_text, is_favorite, is_public) \
                     VALUES (%s, %s, %s, FALSE, %s);", (user_id, title, article_text, is_public))
    else:
        cur.execute("INSERT INTO articles (user_id, title, article_text, is_favorite, is_public) \
                     VALUES (?, ?, ?, 0, ?);", (user_id, title, article_text, int(is_public)))
    
    db_close(conn, cur)
    return redirect('/lab5')


@lab5.route("/lab5/list")
def list():
    login = session.get('login')

    conn, cur = db_connect()

    if login:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
        else:
            cur.execute("SELECT id FROM users WHERE login=?;", (login,))
        user_id = cur.fetchone()['id']

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                SELECT * FROM articles 
                WHERE user_id = %s OR is_public = TRUE 
                ORDER BY is_favorite DESC, id DESC;
            """, (user_id,))
        else:
            cur.execute("""
                SELECT * FROM articles 
                WHERE user_id = ? OR is_public = 1 
                ORDER BY is_favorite DESC, id DESC;
            """, (user_id,))
    else:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                SELECT * FROM articles 
                WHERE is_public = TRUE 
                ORDER BY is_favorite DESC, id DESC;
            """)
        else:
            cur.execute("""
                SELECT * FROM articles 
                WHERE is_public = 1 
                ORDER BY is_favorite DESC, id DESC;
            """)

    articles = cur.fetchall()
    db_close(conn, cur)

    if not articles:
        return render_template('lab5/articles.html',
                               message='У вас пока нет ни одной статьи')

    return render_template('lab5/articles.html', articles=articles)


@lab5.route("/lab5/logout")
def logout():
    session.pop('login', None)
    return redirect('/lab5/')


@lab5.route("/lab5/edit_article/<int:article_id>", methods=['GET', 'POST'])
def edit_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE id=%s;", (article_id,))
    else:
        cur.execute("SELECT * FROM articles WHERE id=?;", (article_id,))

    article = cur.fetchone()

    if request.method == 'GET':
        db_close(conn, cur)
        return render_template('lab5/edit_article.html', article=article)

    title = request.form.get('title')
    article_text = request.form.get('article_text')

    if not title or not article_text:
        db_close(conn, cur)
        return render_template('lab5/edit_article.html',
                               article=article,
                               error='Заполните оба поля')

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("UPDATE articles SET (title, article_text) = (%s, %s) \
                 WHERE id = %s;", (title, article_text, article_id))
    else:   
        cur.execute("UPDATE articles SET (title, article_text) = (?, ?) \
                 WHERE id = ?;", (title, article_text, article_id))

    db_close(conn, cur)
    return redirect('/lab5/list')


@lab5.route("/lab5/delete_article/<int:article_id>", methods=['POST'])
def delete_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("DELETE FROM articles WHERE id=%s;", (article_id,))
    else:
        cur.execute("DELETE FROM articles WHERE id=?;", (article_id,))

    db_close(conn, cur)
    return redirect('/lab5/list')


@lab5.route('/lab5/users')
def users_list():

    conn, cur = db_connect()

    cur.execute("SELECT login, real_name FROM users;")

    users = cur.fetchall()

    db_close(conn, cur)
    return render_template('lab5/users_list.html', users=users)


@lab5.route('/lab5/update_profile', methods=['GET', 'POST'])
def update_profile():
    if 'login' not in session:
        return redirect('/lab5/login')

    if request.method == 'POST':
        real_name = request.form['real_name']
        password = request.form['password']
        confirm = request.form['confirm']

        if not real_name or not password or not confirm:
            return render_template('lab5/update_profile.html',
                                   error="Пожалуйста, заполните все поля")
        
        if password != confirm:
            return render_template('lab5/update_profile.html', error="Пароли не совпадают")

        conn, cur = db_connect()
        password_hash = generate_password_hash(password)

        login = session['login']

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
        else:
            cur.execute("SELECT id FROM users WHERE login=?;", (login,))

        user_id = cur.fetchone()["id"]

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE users SET (real_name, password) = (%s, %s) WHERE id = %s;", 
                        (real_name, password_hash, user_id))
        else:   
            cur.execute("UPDATE users SET (real_name, password) = (?, ?) WHERE id = ?;", 
                        (real_name, password_hash, user_id))

        conn.commit()
        db_close(conn, cur)
        return redirect('/lab5/users')

    return render_template('lab5/update_profile.html')


@lab5.route("/lab5/favorite/<int:article_id>", methods=['GET', 'POST'])
def mark_favorite(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("UPDATE articles SET is_favorite = TRUE WHERE id = %s;", (article_id,))
    else:
        cur.execute("UPDATE articles SET is_favorite = 1 WHERE id = ?;", (article_id,))

    conn.commit()
    db_close(conn, cur)
    return redirect('/lab5/list')


@lab5.route("/lab5/unfavorite/<int:article_id>", methods=['POST'])
def unmark_favorite(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("UPDATE articles SET is_favorite = FALSE WHERE id = %s;", (article_id,))
    else:
        cur.execute("UPDATE articles SET is_favorite = 0 WHERE id = ?;", (article_id,))

    conn.commit()
    db_close(conn, cur)
    return redirect('/lab5/list')