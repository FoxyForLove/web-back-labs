from flask import Blueprint, url_for, request, redirect, abort, render_template, Response
import datetime
from werkzeug.exceptions import HTTPException
import sys

lab2 = Blueprint('lab2',__name__)

@lab2.route("/lab2/")
def lab2_home():
    return render_template("lab2_menu.html")


@lab2.route('/lab2/a')
def a():
    return 'Без слэша'


@lab2.route('/lab2/a/')
def a2():
    return 'Со слэшем'


flower_list = [
    {"name": "Черная роза", "price": 150},
    {"name": "Орхидея", "price": 200},
    {"name": "Лотос", "price": 180},
    {"name": "Кадупул", "price": 300}
]


@lab2.route('/lab2/flowers', endpoint ='all_flowers')
def all_flowers():
    return render_template('flowers.html', flowers=flower_list)


@lab2.route('/lab2/flowers/<int:flower_id>')
def flower_detail(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    flower = flower_list[flower_id]
    return render_template('flower_detail.html', flower=flower, flower_id=flower_id)


@lab2.route('/lab2/add_flower', methods=['POST'])
def add_flower():
    name = request.form.get('name')
    price = int(request.form.get('price', 0))  

    if price < 0:
        return redirect(url_for('lab2.all_flowers', error="Цена не может быть отрицательной"))
    
    flower_list.append({"name": name, "price": price})
    return redirect(url_for('lab2.all_flowers'))


@lab2.route('/lab2/delete_flower/<int:flower_id>')
def delete_flower(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    flower_list.pop(flower_id)
    return redirect(url_for('lab2.all_flowers'))


@lab2.route('/lab2/clear_flowers')
def clear_flowers():
    flower_list.clear()
    return redirect(url_for('lab2.all_flowers'))


@lab2.route('/lab2/example')
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


@lab2.route('/lab2/template')
def lab():
    return render_template('lab2.html')


@lab2.route('/lab2/filters') 
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase = phrase)

sys.set_int_max_str_digits(1000000) 

@lab2.route('/lab2/calc/<int:a>/<int:b>')
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


@lab2.route('/lab2/calc/')
def calc_default():
    return redirect(url_for('lab2.calc', a=1, b=1))


@lab2.route('/lab2/calc/<int:a>')
def calc_single(a):
    return redirect(url_for('lab2.calc', a=a, b=1))


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


@lab2.route('/lab2/books')
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


@lab2.route("/lab2/cats")
def show_cats():
    return render_template("cats.html", cats=cats)


@lab2.route('/lab2/add_flower_example')
def add_flower_example():
    flower_list.append({"name": "Пример", "price": 100})
    return redirect(url_for('lab2.all_flowers'))