from flask import Flask, url_for, request, redirect, abort, render_template, Response
import datetime
from werkzeug.exceptions import HTTPException
import sys

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
            <a href="/lab2">Вторая лабораторная</a>
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
    css = url_for("static", filename="lab1.css")
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

@app.route("/lab2/")
def lab2_home():
    return render_template("lab2_menu.html")

@app.route('/lab2/a')
def a():
    return 'Без слэша'

@app.route('/lab2/a/')
def a2():
    return 'Со слэшем'

flower_list = [
    {"name": "Черная роза", "price": 150},
    {"name": "Орхидея", "price": 200},
    {"name": "Лотос", "price": 180},
    {"name": "Кадупул", "price": 300}
]

@app.route('/lab2/flowers')
def all_flowers():
    return render_template('flowers.html', flowers=flower_list)

@app.route('/lab2/flowers/<int:flower_id>')
def flower_detail(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    flower = flower_list[flower_id]
    return render_template('flower_detail.html', flower=flower, flower_id=flower_id)

@app.route('/lab2/add_flower', methods=['POST'])
def add_flower():
    name = request.form.get('name')
    price = int(request.form.get('price', 0))  

    if price < 0:
        return redirect(url_for('all_flowers', error="Цена не может быть отрицательной"))
    
    flower_list.append({"name": name, "price": price})
    return redirect(url_for('all_flowers'))

@app.route('/lab2/delete_flower/<int:flower_id>')
def delete_flower(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    flower_list.pop(flower_id)
    return redirect(url_for('all_flowers'))

@app.route('/lab2/clear_flowers')
def clear_flowers():
    flower_list.clear()
    return redirect(url_for('all_flowers'))


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

@app.route('/lab2/template')
def lab2():
    return render_template('lab2.html')

@app.route('/lab2/filters') 
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase = phrase)

sys.set_int_max_str_digits(1000000) 

@app.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    try:
        summ = a + b
        diff = a - b
        prod = a * b
        div = a / b if b != 0 else "∞"
        sup = a ** b

        sup_str = str(sup)
        if len(sup_str) > 20:
            sup_display = f"{sup_str[:20]}... (всего {len(sup_str)} цифр)"
        else:
            sup_display = sup_str
    except Exception as e:
        return f"Ошибка: {e}"

    return render_template(
        "calc.html",
        a=a,
        b=b,
        summ=summ,
        diff=diff,
        prod=prod,
        div=div,
        sup_display=sup_display
    )

@app.route('/lab2/calc/')
def calc_default():
    return redirect(url_for('calc', a=1, b=1))

@app.route('/lab2/calc/<int:a>')
def calc_single(a):
    return redirect(url_for('calc', a=a, b=1))

books = [
    {"author": "Донато Карризи", "title": "Девушка в тумане", "genre": "Детектив, триллер", "pages": 416},
    {"author": "Донато Карризи", "title": "Потерянные девушки Рима", "genre": "Детектив", "pages": 512},
    {"author": "Донато Карризи", "title": "Дом голосов", "genre": "Триллер, драма", "pages": 384},
    {"author": "Андреас Грубер", "title": "Смерть приходит по записи", "genre": "Детектив, триллер", "pages": 512},
    {"author": "Андреас Грубер", "title": "Смерть по подписке", "genre": "Детектив, криминал", "pages": 544},
    {"author": "Андреас Грубер", "title": "Смерть как ремесло", "genre": "Психологический триллер", "pages": 576},
    {"author": "Себастьян Фитцек", "title": "Терапия", "genre": "Психологический триллер", "pages": 320},
    {"author": "Себастьян Фитцек", "title": "Пассажир 23", "genre": "Детектив, триллер", "pages": 352},
    {"author": "Себастьян Фитцек", "title": "Посылка", "genre": "Психологический триллер", "pages": 368},
    {"author": "Франк Тилье", "title": "Лес теней", "genre": "Детектив, триллер", "pages": 448},
    {"author": "Франк Тилье", "title": "Синдром Е", "genre": "Детектив, триллер", "pages": 512},
    {"author": "Франк Тилье", "title": "Головоломка", "genre": "Психологический триллер", "pages": 416},
]

@app.route('/lab2/books')
def show_books():
    return render_template("books.html", books=books)

cats = [
    {"name": "Сиамский", "desc": "Элегантный, стройный, голубоглазый", "img": "siamese.jpg"},
    {"name": "Мейн-кун", "desc": "Огромный пушистый, добродушный", "img": "maine_coon.jpg"},
    {"name": "Британский", "desc": "Короткая шерсть, плюшевый вид", "img": "british.jpg"},
    {"name": "Персидский", "desc": "Длинная шерсть, спокойный характер", "img": "persian.jpg"},
    {"name": "Бенгальский", "desc": "Пятнистый, активный", "img": "bengal.jpg"},
    {"name": "Русская голубая", "desc": "Серая шерсть, зелёные глаза", "img": "russian_blue.jpg"},
    {"name": "Сфинкс", "desc": "Без шерсти, дружелюбный", "img": "sphinx.jpg"},
    {"name": "Сноу-шу", "desc": "Мягкая шерсть, белый с тёмными пятнами", "img": "snow_shoe.jpg"},
    {"name": "Экзотическая короткошерстная", "desc": "Плюшевый котик, спокойный", "img": "exotic.jpg"},
    {"name": "Абиссинский", "desc": "Активный, рыжевато-коричневый", "img": "abyssinian.jpg"},
    {"name": "Балинезийский", "desc": "Сиамская порода с длинной шерстью", "img": "balinese.jpg"},
    {"name": "Бурманский", "desc": "Коренастый, дружелюбный", "img": "burmese.jpg"},
    {"name": "Тойгер", "desc": "Похож на тигра", "img": "toyger.jpg"},
    {"name": "Селкирк рекс", "desc": "Кудрявая шерсть", "img": "selkirk.jpg"},
    {"name": "Сибирский", "desc": "Пушистый, выносливый, добродушный", "img": "siberian.jpg"},
    {"name": "Ориентальная", "desc": "Стройная, грациозная", "img": "oriental.jpg"},
    {"name": "Рэгдолл", "desc": "Очень крупный, мягкий характер", "img": "ragdoll.jpg"},
    {"name": "Саванне", "desc": "Пятнистый, высокий рост", "img": "savannah.jpg"},
    {"name": "Тонкинский", "desc": "Средний размер, активный", "img": "tonkinese.jpg"},
    {"name": "Хайленд фолд", "desc": "Сложенные ушки, пушистый", "img": "highland_fold.jpg"},
]

@app.route("/lab2/cats")
def show_cats():
    return render_template("cats.html", cats=cats)

@app.route('/lab2/add_flower_example')
def add_flower_example():
    flower_list.append({"name": "Пример", "price": 100})
    return redirect(url_for('all_flowers'))