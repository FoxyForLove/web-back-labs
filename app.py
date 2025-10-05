from flask import Flask, url_for, request, redirect, abort, render_template, Response
import datetime
from werkzeug.exceptions import HTTPException
import sys
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3

access_log = [] 

app = Flask(__name__)

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)

@app.route('/')
@app.route('/index')
def index():
    css= url_for("static", filename="lab1/lab1.css")
    return '''
<!doctype html>
    <head>
        <link rel="stylesheet" href = "''' + css +'''">
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <header>
            НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных
        </header>

        <nav>
            <a href="/lab1">Первая лабораторная</a>
            <a href="/lab2">Вторая лабораторная</a>
            <a href="/lab3">Третья лабораторная</a>
        </nav>

        <footer>
            ФИО: Булыгина Елизавета Денисовна | Группа: ФБИ-34 | Курс: 3 | Год: 2025
        </footer>
    </body>
</html>
'''


@app.errorhandler(404)
def not_found(err):
    path2 = url_for("static", filename="lab1/kitty2.jpg")
    css = url_for("static", filename="lab1/lab1.css")
    ip = request.remote_addr
    now = datetime.datetime.now()
    url = request.url

    access_log.append((now, ip, url))
    log_text = '<br>'.join(['[ {} | пользователь: {} ] зашел на адрес: {}'.format(e[0], e[1], e[2]) for e in access_log])
   
    return '''
<!doctype html>
<html>
    <head>
        <title>Страница не найдена (404)</title>
        <link rel="stylesheet" href="''' + css + '''">
    </head>
    <body>
        <header>
            НГТУ, ФБ, WEB-программирование, часть 2
        </header>
        <div class="error404-page">
            <h1>Упс! Ошибка 404</h1>
            <img src="''' + path2 + '''">
            <p>Кажется, вы забрели не туда. Уйдите.</p>
            <p>Ваш IP: ''' + ip + '''</p>
            <p>Дата и время доступа: ''' + str(now) + '''</p>
            <a class="back-link" href="/">Вернуться на главную</a>
            <div class="access-log">
                <h2>Журнал посещений:</h2>
                ''' + log_text + '''
             </div>
        </div>
        <footer>
            ФИО: Булыгина Елизавета Денисовна | Группа: ФБИ-34 | Курс: 3 | Год: 2025
        </footer>
    </body>
</html>
''', 404


@app.errorhandler(500)
def internal_server_error(err):
    css = url_for("static", filename="lab1/lab1.css")
    return '''
<!doctype html>
    <head>
        <title>Ошибка 500</title>
        <link rel="stylesheet" href = "''' + css +'''">
    </head>
    <body>
         <header>
            НГТУ, ФБ, WEB-программирование, часть 2
        </header>
        <div class="error500">
            <h1>Внутренняя ошибка сервера (500)</h1>
            <p>Сервер сломался. Чинить я его не собираюсь</p>
        </div>
        <footer>
            ФИО: Булыгина Елизавета Денисовна | Группа: ФБИ-34 | Курс: 3 | Год: 2025
        </footer>
     </body>
</html>
''', 500


@app.errorhandler(400)
def error_400(err):
    return "400 Bad Request — Неверный запрос от клиента", 400


@app.errorhandler(401)
def error_401(err):
    return "401 Unauthorized — Необходима аутентификация", 401

class PaymentRequired(HTTPException):
    code = 402
    description = "402 Payment Required — Требуется оплата"

@app.errorhandler(PaymentRequired)
def handle_402(err):
    return err.description, err.code


@app.errorhandler(403)
def error_403(err):
    return "403 Forbidden — Доступ запрещён", 403


@app.errorhandler(405)
def error_405(err):
    return "405 Method Not Allowed — Метод не разрешён", 405


@app.errorhandler(418)
def error_418(err):
    return "418 I'm a teapot — Я - чайник", 418

  
@app.route('/400')
def route_400():
    abort(400)


@app.route('/401')
def route_401():
    abort(401)


@app.route('/402')
def route_402():
    raise PaymentRequired()


@app.route('/403')
def route_403():
    abort(403)


@app.route('/405')
def route_405():
    abort(405)


@app.route('/418')
def route_418():
    abort(418)


@app.route("/500")
def cause_error():
    return 1 / 0 

