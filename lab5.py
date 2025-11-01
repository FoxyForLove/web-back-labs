from flask import Blueprint, request, render_template,redirect, session
import psycopg2

lab5 = Blueprint('lab5',__name__)

@lab5.route("/lab5/")
def lab():
    return render_template("lab5/lab5.html")


@lab5.route("/lab5/register", methods = ['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template("lab5/register.html")
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template("lab5/register.html", error='Заполните оба поля')
    
    conn = psycopg2.connect(
        host = '127.0.0.1',
        database = 'liza_bulygina',
        user = 'liza_bulygina',
        password = '123'
    )
    cur = conn.cursor()

    cur.execute(f"select login from users where login='{login}';")
    if cur.fetchone():
        cur.close()
        conn.close()
        return render_template("lab5/register.html",
                               error='Такой пользователь уже существует')
    
    cur.execute(f"insert into users (login, password) values ('{login}', '{password}');")
    conn.commit()
    cur.close()
    conn.close()
    return render_template("lab5/success.html", login=login)
    