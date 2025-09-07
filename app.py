from flask import Flask, url_for, request, redirect
import datetime
app = Flask(__name__)

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
        <div class="lab-text">
            Flask — фреймворк для создания веб-приложений на языке программирования Python, использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2. Относится к категории так называемых микрофреймворков — минималистичных каркасов веб-приложений, сознательно предоставляющих лишь самые базовые возможности.
        </div>
        <a class="back-link" href="/">Вернуться на главную</a>
    </body>
</html>
'''

@app.route('/lab1/web')
def web():
    return """<!doctype html>
        <html> 
           <body> 
                <h1>Web-сервес на flask </h1> 
                <a href="/author">author</a>
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
                <a href="/web">web</a>
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
        <h1> Грустный котик (Я) </h1>
        <img src="''' + path +'''">
    </body> 
</html>
'''

count = 0 

@app.route('/lab1/counter')
def counter():
    global count
    count +=1
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr 

    return '''
<!doctype html>
<html> 
    <body> 
        Вы сюда заходили: ''' + str(count) + ''' раз 
        <hr>
        Дата и время: ''' + str(time) + '''<br>
        Запрошенный адрес: ''' + url + '''<br>
        Ваш IP-адрес: ''' + client_ip + '''<br>
        <a href="/clean_counter">Очистить счётчик</a>

    </body> 
</html>
'''

@app.route('/lab1/clean_counter')
def clean_counter():
    global count
    count = 0
    return '''
<!doctype html>
<html> 
    <body> 
        <h1>Счётчик успешно сброшен!</h1>
        <a href="/counter">Вернуться к счётчику</a>
    </body> 
</html>
'''

@app.route('/lab1/info')
def info():
    return redirect("/lab1/author")

@app.route('/lab1/created')
def created():
    return '''
<!doctype html>
<html> 
    <body> 
        <h1>Создано успешно</h1>
        <div><i>что-то создано...</i></div>
    </body> 
</html>
''',201

@app.errorhandler(404)
def not_found(err):
    return "Нет тут такой страницы",404