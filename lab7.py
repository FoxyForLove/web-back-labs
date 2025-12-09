from flask import Blueprint, request, render_template, abort, current_app
import psycopg2
import sqlite3
from psycopg2.extras import RealDictCursor
import datetime
from os import path

lab7 = Blueprint('lab7', __name__)

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='liza_bulygina',
            user='liza_bulygina',
            password='123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, 'database.db')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@lab7.route("/lab7/")
def main():
    return render_template("lab7/index.html")

def validate_film(film):
    errors = {}

    if not film.get('title_ru') or film['title_ru'].strip() == '':
        errors['title_ru'] = 'Русское название обязательно'

    if (not film.get('title') or film['title'].strip() == '') and (not film.get('title_ru') or film['title_ru'].strip() == ''):
        errors['title'] = 'Укажите хотя бы одно название (русское или оригинальное)'

    try:
        year = int(film.get('year', 0))
        current_year = datetime.datetime.now().year
        if year < 1895 or year > current_year:
            errors['year'] = f'Год должен быть от 1895 до {current_year}'
    except ValueError:
        errors['year'] = 'Год должен быть числом'

    if not film.get('description') or film['description'].strip() == '':
        errors['description'] = 'Заполните описание'
    elif len(film['description']) > 2000:
        errors['description'] = 'Описание не должно превышать 2000 символов'

    return errors

@lab7.route("/lab7/rest-api/films/", methods=['GET'])
def get_films():
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM films ORDER BY year")
    else:
        cur.execute("SELECT * FROM films ORDER BY year")

    films = cur.fetchall()
    db_close(conn, cur)
    
    return films

@lab7.route("/lab7/rest-api/films/<int:id>", methods=['GET'])
def get_film(id):
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM films WHERE id=%s", (id,))
    else:
        cur.execute("SELECT * FROM films WHERE id=?", (id,))

    film = cur.fetchone()
    db_close(conn, cur)

    if not film:
        abort(404, description="Film not found")

    return film

@lab7.route("/lab7/rest-api/films/<int:id>", methods=['DELETE'])
def del_film(id):
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("DELETE FROM films WHERE id=%s", (id,))
    else:
        cur.execute("DELETE FROM films WHERE id=?", (id,))

    db_close(conn, cur)
    return '', 204

@lab7.route("/lab7/rest-api/films/<int:id>", methods=['PUT'])
def put_films(id):
    conn, cur = db_connect()

    if id < 0:
        abort(404, description="Film not found")

    film = request.get_json()
    errors = validate_film(film)

    if film['title'] == '' and film['title_ru'] != '':
        film['title'] = film['title_ru']

    if errors:
        return errors, 400

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("""
            UPDATE films
            SET title=%s, title_ru=%s, year=%s, description=%s
            WHERE id=%s
        """, (film['title'], film['title_ru'], film['year'], film['description'], id))
    else:
        cur.execute("""
            UPDATE films
            SET title=?, title_ru=?, year=?, description=?
            WHERE id=?
        """, (film['title'], film['title_ru'], film['year'], film['description'], id))

    db_close(conn, cur)
    return film, 200

@lab7.route("/lab7/rest-api/films/", methods=['POST'])
def add_film():
    film = request.get_json()
    errors = validate_film(film)

    if film['title'] == '' and film['title_ru'] != '':
        film['title'] = film['title_ru']

    if errors:
        return errors, 400

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("""
            INSERT INTO films (title, title_ru, year, description)
            VALUES (%s, %s, %s, %s) RETURNING id
        """, (film['title'], film['title_ru'], film['year'], film['description']))
        new_id = cur.fetchone()['id']
    else:
        cur.execute("""
            INSERT INTO films (title, title_ru, year, description)
            VALUES (?, ?, ?, ?)
        """, (film['title'], film['title_ru'], film['year'], film['description']))
        new_id = cur.lastrowid

    film_with_id = film
    film_with_id["id"] = new_id

    db_close(conn, cur)
    return film_with_id, 201