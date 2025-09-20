from flask import Flask, url_for, request, redirect, abort, render_template
import datetime
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

access_log = [] 

@app.route('/')
@app.route('/index')
def index():
    css= url_for("static", filename="lab1.css")
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
        </nav>

        <footer>
            ФИО: Булыгина Елизавета Денисовна | Группа: ФБИ-34 | Курс: 3 | Год: 2025
        </footer>
    </body>
</html>
'''

@app.route('/lab1')
def lab1():
    css= url_for("static", filename="lab1.css")
    return '''
<!doctype html>
    <head>
        <title>Лабораторная №1</title>
        <link rel="stylesheet" href = "''' + css +'''">
    </head>
    <body>
     <header>
            НГТУ, ФБ, WEB-программирование, часть 2
        </header>

        <div class="lab-text">
            Flask — фреймворк для создания веб-приложений на языке программирования Python, использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2. Относится к категории так называемых микрофреймворков — минималистичных каркасов веб-приложений, сознательно предоставляющих лишь самые базовые возможности.
        </div>
        <ul>
            <li><a href="/lab1/web">/lab1/web</a></li>
            <li><a href="/lab1/author">/lab1/author</a></li>
            <li><a href="/lab1/image">/lab1/image</a></li>
            <li><a href="/lab1/counter">/lab1/counter</a></li>
            <li><a href="/lab1/clean_counter">/lab1/clean_counter</a></li>
            <li><a href="/lab1/info">/lab1/info</a></li>
            <li><a href="/lab1/created">/lab1/created</a></li>
        </ul>

        <h2>Список маршрутов ошибок</h2>
        <ul>
            <li><a href="/400">/400</a></li>
            <li><a href="/401">/401</a></li>
            <li><a href="/402">/402</a></li>
            <li><a href="/403">/403</a></li>
            <li><a href="/405">/405</a></li>
            <li><a href="/418">/418</a></li>
            <li><a href="/500">/500</a></li>
        </ul>

        <a class="back-link" href="/">Вернуться на главную</a>

        <footer>
            ФИО: Булыгина Елизавета Денисовна | Группа: ФБИ-34 | Курс: 3 | Год: 2025
        </footer>
    </body>
</html>
'''

@app.route('/lab1/web')
def web():
    return """<!doctype html>
        <html> 
           <body> 
                <h1>Web-сервес на flask </h1> 
                <a href="/lab1/author">author</a>
           </body> 
        </html>""",200, {
            'X-Server': 'sample',
            'Content-Type': 'text/plain; charset=utf-8'
        }

@app.route('/lab1/author')
def author():
    name = "Булыгина Елизавета Денисовна"
    group = "ФБИ-34"
    faculty = "ФБ"

    return """<!doctype html>
        <html> 
           <body> 
                <P>Студент: """ + name + """</p> 
                <P>Группа: """ + group + """</p> 
                <P>Факультет: """ + faculty+ """</p> 
                <a href="/lab1/web">web</a>
           </body> 
        </html>"""

@app.route('/lab1/image')
def image():
    path = url_for("static",filename="kitty.png")
    css = url_for("static",filename="lab1.css")
    return '''
<!doctype html>
<html> 
    <head> 
        <link rel="stylesheet" href = "''' + css +'''">
    </head>
    <body> 
        <header>
            НГТУ, ФБ, WEB-программирование, часть 2
        </header>
        <h1> Грустный котик (Я) </h1>
        <img src="''' + path +'''">
        <footer>
            ФИО: Булыгина Елизавета Денисовна | Группа: ФБИ-34 | Курс: 3 | Год: 2025
        </footer>
    </body> 
</html> ''',200, {
            'Content-Language': 'ru',
            'X-Developer': 'Liza',                   
            'X-Life': 'Repeating the same action over and over and expecting change is the definition of insanity'
        }
        

count = 0 

@app.route('/lab1/counter')
def counter():
    global count
    count +=1
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr 
    css = url_for("static",filename="lab1.css")

    return '''
<!doctype html>
<html> 
    <link rel="stylesheet" href = "''' + css +'''">
    <body> 
        <header>
            НГТУ, ФБ, WEB-программирование, часть 2
        </header>
        <div class="main-content">
        Вы сюда заходили: ''' + str(count) + ''' раз 
        <hr>
        Дата и время: ''' + str(time) + '''<br>
        Запрошенный адрес: ''' + url + '''<br>
        Ваш IP-адрес: ''' + client_ip + '''<br>
        </div>
        <a href="/lab1/clean_counter">Очистить счётчик</a>
        <footer>
            ФИО: Булыгина Елизавета Денисовна | Группа: ФБИ-34 | Курс: 3 | Год: 2025
        </footer>

    </body> 
</html>
'''

@app.route('/lab1/clean_counter')
def clean_counter():
    global count
    count = 0
    css = url_for("static",filename="lab1.css")
    return '''
<!doctype html>
<html> 
    <link rel="stylesheet" href = "''' + css +'''">
    <body> 
        <header>
            НГТУ, ФБ, WEB-программирование, часть 2
        </header>
        <h1>Счётчик успешно сброшен!</h1>
        <a href="/lab1/counter">Вернуться к счётчику</a>
        <footer>
            ФИО: Булыгина Елизавета Денисовна | Группа: ФБИ-34 | Курс: 3 | Год: 2025
        </footer>
    </body> 
</html>
'''

@app.route('/lab1/info')
def info():
    return redirect("/lab1/author")

@app.route('/lab1/created')
def created():
    css = url_for("static",filename="lab1.css")
    return '''
<!doctype html>
<html> 
    <link rel="stylesheet" href = "''' + css +'''">
    <body> 
        <header>
            НГТУ, ФБ, WEB-программирование, часть 2
        </header>
        <h1>Создано успешно</h1>
        <div><i>что-то создано...</i></div>
        <footer>
            ФИО: Булыгина Елизавета Денисовна | Группа: ФБИ-34 | Курс: 3 | Год: 2025
        </footer>
    </body> 
</html>
''',201 

@app.errorhandler(404)
def not_found(err):
    path2 = url_for("static", filename="kitty2.jpg")
    css = url_for("static", filename="lab1.css")
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
    path2 = url_for("static",filename="kitty2.jpg")
    css = url_for("static",filename="lab1.css")
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


#Lab 2

@app.route('/lab2/a')
def a():
    return 'Без слэша'

@app.route('/lab2/a/')
def a2():
    return 'Со слэшем'

flower_list = ['Черная роза','Орхидея','Лотос','Кадупул']

@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    else: 
        return "Цветок:" + flower_list[flower_id]

@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.append(name)
    return f''' 
<!doctype html>
<html> 
    <body> 
        <h1>Добавлен новый цветок!</h1>
        <p>Название нового цветка: {name}</p>
        <p>Всего цветков: {len(flower_list)}</p>
        <p>Полный список: {flower_list}</p>
    </body> 
</html>
'''

@app.route('/lab2/example')
def example():
    name, lab_num, group, course = 'Елизавета Булыгина', '№2', 'ФБИ-34', '3 курс'
    fruits = [
    {"name": "Яблоки", "price": 150},
    {"name": "Нектарины", "price": 220},
    {"name": "Лимоны", "price": 90},
    {"name": "Мандарины", "price": 130},
    {"name": "Помело", "price": 270}
    ]
    return render_template('example.html', 
                           name=name, 
                           lab_num=lab_num, 
                           group=group, 
                           course=course,
                           fruits = fruits)

@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')