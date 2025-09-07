from flask import Flask, url_for, request, redirect
import datetime
app = Flask(__name__)

@app.route('/')
@app.route('/web')
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

@app.route('/author')
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

@app.route('/image')
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

@app.route('/counter')
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
    </body> 
</html>
'''

@app.route('/info')
def info():
    return redirect("/author")

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