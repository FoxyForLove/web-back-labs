from flask import Blueprint, request, render_template, session, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path

lab6 = Blueprint('lab6', __name__)

@lab6.route("/lab6/")
def main():
    return render_template("lab6/lab6.html")

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


@lab6.route("/lab6/json-rpc-api/", methods=['POST'])
def api():
    data = request.json
    id = data['id']
    login = session.get('login')

    conn, cur = db_connect()

    if data['method'] == 'info':
        cur.execute("SELECT number, tenant, price FROM offices ORDER BY number;")
        offices = cur.fetchall()

        offices_list = []
        total = 0
        for office in offices:
            number = office['number']
            tenant = office['tenant']
            price = office['price']
            offices_list.append({"number": number, "tenant": tenant, "price": price})
            if login and tenant == login:
                total += price

        db_close(conn, cur)
        return {
            'jsonrpc': '2.0',
            'result': {
                'offices': offices_list,
                'total': f'Общая стоимость аренды: {total}' if login else ''
            },
            'id': id
        }

    if not login:
        db_close(conn, cur)
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 1,
                'message': 'Unauthorized'
            },
            'id': id
        }

    if data['method'] == 'booking':
        office_number = data['params']
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT tenant FROM offices WHERE number=%s;", (office_number,))
        else:
            cur.execute("SELECT tenant FROM offices WHERE number=?;", (office_number,))
        office = cur.fetchone()

        tenant = office['tenant']

        if tenant:
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 2, 
                    'message': 'Already booked'
                },
                'id': id
            }

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE offices SET tenant=%s WHERE number=%s;", (login, office_number))
        else:
            cur.execute("UPDATE offices SET tenant=? WHERE number=?;", (login, office_number))
        
        db_close(conn, cur)

        return {
            'jsonrpc': '2.0', 
            'result': 'success', 
            'id': id
        }

    if data['method'] == 'cancelation':
        office_number = data['params']
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT tenant FROM offices WHERE number=%s;", (office_number,))
        else:
            cur.execute("SELECT tenant FROM offices WHERE number=?;", (office_number,))
        office = cur.fetchone()

        tenant = office['tenant']

        if not tenant:
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 3, 
                    'message': 'Office not booked'
                },
                'id': id
            }
        
        if tenant != login:
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 4, 
                    'message': 'Not your booking'
                },
                'id': id
            }

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE offices SET tenant=%s WHERE number=%s;", ('', office_number))
        else:
            cur.execute("UPDATE offices SET tenant=? WHERE number=?;", ('', office_number))

        db_close(conn, cur)

        return {
            'jsonrpc': '2.0', 
            'result': 'success', 
            'id': id
        }

    db_close(conn, cur)

    return {
        'jsonrpc': '2.0',
        'error': {
            'code': -32601,
            'message': 'Method not found'
        },
        'id': id
    }