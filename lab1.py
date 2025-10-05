from flask import Blueprint, url_for, request, redirect, Response
import datetime
from werkzeug.exceptions import HTTPException
import sys

lab1 = Blueprint('lab1',__name__)

access_log = [] 

@lab1.route('/lab1')
def lab():
    css= url_for("static", filename="lab1/lab1.css")
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


@lab1.route('/lab1/web')
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


@lab1.route('/lab1/author')
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


@lab1.route('/lab1/image')
def image():
    path = url_for("static",filename="lab1/kitty.png")
    css = url_for("static",filename="lab1/lab1.css")
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

@lab1.route('/lab1/counter')
def counter():
    global count
    count +=1
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr 
    css = url_for("static",filename="lab1/lab1.css")

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


@lab1.route('/lab1/clean_counter')
def clean_counter():
    global count
    count = 0
    css = url_for("static",filename="lab1/lab1.css")
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


@lab1.route('/lab1/info')
def info():
    return redirect("/lab1/author")


@lab1.route('/lab1/created')
def created():
    css = url_for("static",filename="lab1/lab1.css")
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
