# Импорт модулей

from flask import Blueprint, request, render_template, session, redirect, current_app, jsonify, abort
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash
from os import path
import re
import datetime


# Константы и настройки

rgz = Blueprint('rgz', __name__)

STUDENT_FIO = "Булыгина Елизавета Денисовна"
STUDENT_GROUP = "ФБИ-34"

RE_LOGIN_PASS = re.compile(r'^[A-Za-z0-9!"#$%&\'()*+,\-./:;<=>?@\[\]^_`{|}~]+$')


# Валидация

def validate_login_password(login: str, password: str):
    if not login or not password:
        return "Логин и пароль не должны быть пустыми"
    if not RE_LOGIN_PASS.match(login):
        return "Логин: только латиница, цифры и знаки препинания, без пробелов"
    if not RE_LOGIN_PASS.match(password):
        return "Пароль: только латиница, цифры и знаки препинания, без пробелов"
    if len(login) > 50 or len(password) > 200:
        return "Слишком длинный логин или пароль"
    return ""


def validate_name(name: str):
    if not name or name.strip() == "":
        return "Имя не должно быть пустым"
    if len(name.strip()) > 100:
        return "Имя слишком длинное"
    return ""


# Работа с базой данных

def is_postgres():
    return current_app.config.get('DB_TYPE') == 'postgres'


def db_connect():
    if is_postgres():
        conn = psycopg2.connect(
            host=current_app.config.get('PG_HOST', '127.0.0.1'),
            database=current_app.config.get('PG_DB', 'cinema'),
            user=current_app.config.get('PG_USER', 'cinema'),
            password=current_app.config.get('PG_PASSWORD', '123')
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, 'cinema.db')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    return conn, cur


def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()


# Работа с датой и временем

def now_dt():
    return datetime.datetime.now()


def parse_dt(val):
    if val is None:
        return None
    if isinstance(val, datetime.datetime):
        return val
    try:
        return datetime.datetime.strptime(str(val), "%Y-%m-%d %H:%M")
    except Exception:
        return None


# Проверка прав и текущего пользователя

def require_auth():
    if 'user_id' not in session:
        abort(401, description="Unauthorized")


def require_admin():
    require_auth()
    if not session.get('is_admin'):
        abort(403, description="Forbidden")


def get_current_user(conn, cur):
    uid = session.get('user_id')
    if not uid:
        return None

    if is_postgres():
        cur.execute("SELECT id, login, name, is_admin FROM users WHERE id=%s;", (uid,))
    else:
        cur.execute("SELECT id, login, name, is_admin FROM users WHERE id=?;", (uid,))
    return cur.fetchone()


# Страницы

@rgz.route("/rgz/")
def rgz_index():
    return render_template(
        "rgz/index.html",
        fio=STUDENT_FIO,
        group=STUDENT_GROUP,
        login=session.get('login'),
        name=session.get('name'),
        is_admin=session.get('is_admin', False)
    )


@rgz.route("/rgz/screenings/<int:screening_id>")
def rgz_screening_page(screening_id):
    return render_template(
        "rgz/screening.html",
        fio=STUDENT_FIO,
        group=STUDENT_GROUP,
        screening_id=screening_id,
        login=session.get('login'),
        name=session.get('name'),
        is_admin=session.get('is_admin', False)
    )


# Авторизация: регистрация

@rgz.route("/rgz/api/register", methods=["POST"])
def api_register():
    data = request.get_json() or {}
    name = (data.get("name") or "").strip()
    login = (data.get("login") or "").strip()
    password = data.get("password") or ""

    err = validate_name(name) or validate_login_password(login, password)
    if err:
        return jsonify({"error": err}), 400

    conn, cur = db_connect()

    if is_postgres():
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    if cur.fetchone():
        db_close(conn, cur)
        return jsonify({"error": "Логин занят"}), 400

    pw_hash = generate_password_hash(password)

    if is_postgres():
        cur.execute(
            "INSERT INTO users (login, password_hash, name, is_admin) "
            "VALUES (%s, %s, %s, FALSE) RETURNING id;",
            (login, pw_hash, name)
        )
        user_id = cur.fetchone()["id"]
    else:
        cur.execute(
            "INSERT INTO users (login, password_hash, name, is_admin) "
            "VALUES (?, ?, ?, 0);",
            (login, pw_hash, name)
        )
        user_id = cur.lastrowid

    session["user_id"] = user_id
    session["login"] = login
    session["name"] = name
    session["is_admin"] = False

    db_close(conn, cur)
    return jsonify({"result": "ok"}), 201


# Авторизация: вход

@rgz.route("/rgz/api/login", methods=["POST"])
def api_login():
    data = request.get_json() or {}
    login = (data.get("login") or "").strip()
    password = data.get("password") or ""

    err = validate_login_password(login, password)
    if err:
        return jsonify({"error": err}), 400

    conn, cur = db_connect()

    if is_postgres():
        cur.execute(
            "SELECT id, login, password_hash, name, is_admin "
            "FROM users WHERE login=%s;",
            (login,)
        )
    else:
        cur.execute(
            "SELECT id, login, password_hash, name, is_admin "
            "FROM users WHERE login=?;",
            (login,)
        )

    user = cur.fetchone()

    if not user:
        db_close(conn, cur)
        return jsonify({"error": "Неверный логин и/или пароль"}), 400

    password_ok = False

    try:
        if check_password_hash(user["password_hash"], password):
            password_ok = True
    except Exception:
        pass

    if not password_ok and is_postgres():
        cur.execute(
            "SELECT crypt(%s, %s) = %s AS ok;",
            (password, user["password_hash"], user["password_hash"])
        )
        row = cur.fetchone()
        if row and row["ok"]:
            password_ok = True

    if not password_ok:
        db_close(conn, cur)
        return jsonify({"error": "Неверный логин и/или пароль"}), 400

    session["user_id"] = user["id"]
    session["login"] = user["login"]
    session["name"] = user["name"]
    session["is_admin"] = bool(user["is_admin"])

    db_close(conn, cur)
    return jsonify({"result": "ok"}), 200


# Авторизация: выход

@rgz.route("/rgz/api/logout", methods=["POST"])
def api_logout():
    session.pop("user_id", None)
    session.pop("login", None)
    session.pop("name", None)
    session.pop("is_admin", None)
    return jsonify({"result": "ok"}), 200


# Текущий пользователь

@rgz.route("/rgz/api/me", methods=["GET"])
def api_me_get():
    if "user_id" not in session:
        return jsonify({"is_auth": False}), 200

    return jsonify({
        "is_auth": True,
        "login": session.get("login"),
        "name": session.get("name"),
        "is_admin": bool(session.get("is_admin"))
    }), 200


@rgz.route("/rgz/api/me", methods=["DELETE"])
def api_me_delete():
    require_auth()

    conn, cur = db_connect()
    user = get_current_user(conn, cur)
    if not user:
        db_close(conn, cur)
        abort(401, description="Unauthorized")

    uid = user["id"]

    if is_postgres():
        cur.execute("DELETE FROM bookings WHERE user_id=%s;", (uid,))
        cur.execute("DELETE FROM users WHERE id=%s;", (uid,))
    else:
        cur.execute("DELETE FROM bookings WHERE user_id=?;", (uid,))
        cur.execute("DELETE FROM users WHERE id=?;", (uid,))

    db_close(conn, cur)

    session.pop("user_id", None)
    session.pop("login", None)
    session.pop("name", None)
    session.pop("is_admin", None)

    return jsonify({"result": "ok"}), 200


# Сеансы: список

@rgz.route("/rgz/api/screenings", methods=["GET"])
def api_screenings_list():
    conn, cur = db_connect()

    if is_postgres():
        cur.execute("SELECT id, film_title, start_at FROM screenings ORDER BY start_at;")
    else:
        cur.execute("SELECT id, film_title, start_at FROM screenings ORDER BY start_at;")

    rows = cur.fetchall()
    db_close(conn, cur)

    result = []
    now = now_dt()

    for r in rows:
        start = parse_dt(r["start_at"])
        result.append({
            "id": r["id"],
            "film_title": r["film_title"],
            "start_at": start.strftime("%Y-%m-%d %H:%M") if start else str(r["start_at"]),
            "is_past": True if (start and start < now) else False
        })

    return jsonify(result), 200


# Сеансы: создание

@rgz.route("/rgz/api/screenings", methods=["POST"])
def api_screenings_create():
    require_admin()

    data = request.get_json() or {}
    film_title = (data.get("film_title") or "").strip()
    start_at = (data.get("start_at") or "").strip()

    if not film_title:
        return jsonify({"error": "Название фильма не должно быть пустым"}), 400
    if len(film_title) > 200:
        return jsonify({"error": "Название фильма слишком длинное"}), 400

    try:
        dt = datetime.datetime.strptime(start_at, "%Y-%m-%d %H:%M")
    except Exception:
        return jsonify({"error": "Дата/время: формат должен быть YYYY-MM-DD HH:MM"}), 400

    if dt < now_dt():
        return jsonify({"error": "Нельзя создать сеанс в прошлом"}), 400

    conn, cur = db_connect()

    if is_postgres():
        cur.execute(
            "INSERT INTO screenings (film_title, start_at) VALUES (%s, %s) RETURNING id;",
            (film_title, dt)
        )
        new_id = cur.fetchone()["id"]
    else:
        cur.execute(
            "INSERT INTO screenings (film_title, start_at) VALUES (?, ?);",
            (film_title, start_at)
        )
        new_id = cur.lastrowid

    db_close(conn, cur)
    return jsonify({"result": "ok", "id": new_id}), 201


# Сеансы: удаление

@rgz.route("/rgz/api/screenings/<int:screening_id>", methods=["DELETE"])
def api_screenings_delete(screening_id):
    require_admin()

    conn, cur = db_connect()

    if is_postgres():
        cur.execute("SELECT start_at FROM screenings WHERE id=%s;", (screening_id,))
    else:
        cur.execute("SELECT start_at FROM screenings WHERE id=?;", (screening_id,))
    row = cur.fetchone()

    if not row:
        db_close(conn, cur)
        abort(404, description="Not found")

    start = parse_dt(row["start_at"])
    if start and start < now_dt():
        db_close(conn, cur)
        return jsonify({"error": "Сеанс в прошлом — удалять нельзя"}), 400

    if is_postgres():
        cur.execute("DELETE FROM bookings WHERE screening_id=%s;", (screening_id,))
        cur.execute("DELETE FROM screenings WHERE id=%s;", (screening_id,))
    else:
        cur.execute("DELETE FROM bookings WHERE screening_id=?;", (screening_id,))
        cur.execute("DELETE FROM screenings WHERE id=?;", (screening_id,))

    db_close(conn, cur)
    return jsonify({"result": "ok"}), 200


# Места: список мест и информация о сеансе

@rgz.route("/rgz/api/screenings/<int:screening_id>/seats", methods=["GET"])
def api_seats_list(screening_id):
    conn, cur = db_connect()

    if is_postgres():
        cur.execute("SELECT id, film_title, start_at FROM screenings WHERE id=%s;", (screening_id,))
    else:
        cur.execute("SELECT id, film_title, start_at FROM screenings WHERE id=?;", (screening_id,))
    scr = cur.fetchone()

    if not scr:
        db_close(conn, cur)
        abort(404, description="Not found")

    start = parse_dt(scr["start_at"])
    now = now_dt()
    is_past = True if (start and start < now) else False

    if is_postgres():
        cur.execute(
            """
            SELECT b.seat_no, u.name, u.login
            FROM bookings b
            JOIN users u ON u.id = b.user_id
            WHERE b.screening_id = %s
            ORDER BY b.seat_no;
            """,
            (screening_id,)
        )
    else:
        cur.execute(
            """
            SELECT b.seat_no, u.name, u.login
            FROM bookings b
            JOIN users u ON u.id = b.user_id
            WHERE b.screening_id = ?
            ORDER BY b.seat_no;
            """,
            (screening_id,)
        )

    booked = cur.fetchall()
    db_close(conn, cur)

    seats = []
    map_booked = {
        int(x["seat_no"]): {"name": x["name"], "login": x["login"]}
        for x in booked
    }

    for seat_no in range(1, 31):
        occ = map_booked.get(seat_no)
        seats.append({
            "seat_no": seat_no,
            "is_booked": True if occ else False,
            "user_name": occ["name"] if occ else "",
            "user_login": occ["login"] if occ else ""
        })

    return jsonify({
        "screening": {
            "id": scr["id"],
            "film_title": scr["film_title"],
            "start_at": start.strftime("%Y-%m-%d %H:%M") if start else str(scr["start_at"]),
            "is_past": is_past
        },
        "seats": seats,
        "me": {
            "is_auth": True if session.get("user_id") else False,
            "login": session.get("login") or "",
            "is_admin": bool(session.get("is_admin", False))
        }
    }), 200


# Места: проверка, что сеанс не в прошлом

def check_screening_not_past(conn, cur, screening_id):
    if is_postgres():
        cur.execute("SELECT start_at FROM screenings WHERE id=%s;", (screening_id,))
    else:
        cur.execute("SELECT start_at FROM screenings WHERE id=?;", (screening_id,))
    row = cur.fetchone()

    if not row:
        abort(404, description="Not found")

    start = parse_dt(row["start_at"])
    if start and start < now_dt():
        return False
    return True


# Места: бронирование

@rgz.route("/rgz/api/screenings/<int:screening_id>/seats/<int:seat_no>", methods=["POST"])
def api_seat_book(screening_id, seat_no):
    require_auth()

    if not (1 <= seat_no <= 30):
        return jsonify({"error": "Место должно быть от 1 до 30"}), 400

    conn, cur = db_connect()

    if not check_screening_not_past(conn, cur, screening_id):
        db_close(conn, cur)
        return jsonify({"error": "Сеанс в прошлом — бронировать нельзя"}), 400

    uid = session["user_id"]

    if is_postgres():
        cur.execute(
            "SELECT id FROM bookings WHERE screening_id=%s AND seat_no=%s;",
            (screening_id, seat_no)
        )
    else:
        cur.execute(
            "SELECT id FROM bookings WHERE screening_id=? AND seat_no=?;",
            (screening_id, seat_no)
        )
    if cur.fetchone():
        db_close(conn, cur)
        return jsonify({"error": "Место уже занято"}), 400

    if is_postgres():
        cur.execute(
            "SELECT COUNT(*) AS c FROM bookings WHERE screening_id=%s AND user_id=%s;",
            (screening_id, uid)
        )
        c = cur.fetchone()["c"]
    else:
        cur.execute(
            "SELECT COUNT(*) AS c FROM bookings WHERE screening_id=? AND user_id=?;",
            (screening_id, uid)
        )
        c = cur.fetchone()["c"]

    if int(c) >= 5:
        db_close(conn, cur)
        return jsonify({"error": "Нельзя занять больше 5 мест на один сеанс"}), 400

    if is_postgres():
        cur.execute(
            "INSERT INTO bookings (screening_id, seat_no, user_id, created_at) "
            "VALUES (%s, %s, %s, NOW());",
            (screening_id, seat_no, uid)
        )
    else:
        cur.execute(
            "INSERT INTO bookings (screening_id, seat_no, user_id, created_at) "
            "VALUES (?, ?, ?, ?);",
            (screening_id, seat_no, uid, now_dt().strftime("%Y-%m-%d %H:%M:%S"))
        )

    db_close(conn, cur)
    return jsonify({"result": "ok"}), 200


# Места: снятие брони

@rgz.route("/rgz/api/screenings/<int:screening_id>/seats/<int:seat_no>", methods=["DELETE"])
def api_seat_unbook(screening_id, seat_no):
    require_auth()

    if not (1 <= seat_no <= 30):
        return jsonify({"error": "Место должно быть от 1 до 30"}), 400

    conn, cur = db_connect()

    if not check_screening_not_past(conn, cur, screening_id):
        db_close(conn, cur)
        return jsonify({"error": "Сеанс в прошлом — снимать бронь нельзя"}), 400

    uid = session["user_id"]
    is_admin_user = bool(session.get("is_admin", False))

    if is_postgres():
        cur.execute(
            "SELECT id, user_id FROM bookings WHERE screening_id=%s AND seat_no=%s;",
            (screening_id, seat_no)
        )
    else:
        cur.execute(
            "SELECT id, user_id FROM bookings WHERE screening_id=? AND seat_no=?;",
            (screening_id, seat_no)
        )
    booking = cur.fetchone()

    if not booking:
        db_close(conn, cur)
        return jsonify({"error": "Это место не занято"}), 400

    if (not is_admin_user) and (int(booking["user_id"]) != int(uid)):
        db_close(conn, cur)
        return jsonify({"error": "Нельзя снять чужую бронь"}), 403

    if is_postgres():
        cur.execute("DELETE FROM bookings WHERE id=%s;", (booking["id"],))
    else:
        cur.execute("DELETE FROM bookings WHERE id=?;", (booking["id"],))

    db_close(conn, cur)
    return jsonify({"result": "ok"}), 200
