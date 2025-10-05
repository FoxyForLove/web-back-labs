from flask import Blueprint, request, render_template, Response, make_response, redirect 
lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name') or 'Анон'
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age') or 'только бог знает'
    return render_template("lab3/lab3.html", name = name, name_color = name_color, age=age)


@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp


@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Liza', max_age = 5)
    resp.set_cookie('age', '21')
    resp.set_cookie('name_color', 'Orange')
    return resp


@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user') 
    if user == '': 
        errors['user'] = 'Заполните поле' 
    
    age = request.args.get('age') 
    if age == '': 
        errors['age'] = 'Заполните поле'

    sex = request.args.get('sex')
    
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors = errors)


@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')


@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')

    if drink == 'cofee':
        price = 120
    elif drink == 'red-tea':
        price = 80
    else:
        price = 70
    
    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10
    return render_template('lab3/pay.html', price=price)


@lab3.route('/lab3/success')
def success():
    price = request.args.get('price')
    return render_template('lab3/success.html', price=price)


@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    bgcolor = request.args.get('bgcolor')
    fontsize = request.args.get('fontsize')
    style = request.args.get('style')

    if any([color, bgcolor, fontsize, style]):
        resp = make_response(redirect('/lab3/settings'))
        if color:
            resp.set_cookie('color', color)
        if bgcolor:
            resp.set_cookie('bgcolor', bgcolor)
        if fontsize:
            resp.set_cookie('fontsize', fontsize)
        if style:
            resp.set_cookie('style', style)
        return resp

    color = request.cookies.get('color')
    bgcolor = request.cookies.get('bgcolor')
    fontsize = request.cookies.get('fontsize')
    style = request.cookies.get('style')

    return render_template('lab3/settings.html',
                           color=color,
                           bgcolor=bgcolor,
                           fontsize=fontsize,
                           style=style)


@lab3.route('/lab3/clear-cookies')
def clear_cookies():
    resp = make_response(redirect('/lab3/settings'))
    resp.delete_cookie('color')
    resp.delete_cookie('bgcolor')
    resp.delete_cookie('fontsize')
    resp.delete_cookie('style')
    return resp


@lab3.route('/lab3/train')
def train():
    return render_template('lab3/train.html')


@lab3.route('/lab3/ticket')
def ticket():
    name = request.args.get('name')
    shelf = request.args.get('shelf')
    bedding = request.args.get('bedding') == 'on'
    luggage = request.args.get('luggage') == 'on'
    age = int(request.args.get('age'))
    from_city = request.args.get('from_city')
    to_city = request.args.get('to')
    date = request.args.get('date')
    insurance = request.args.get('insurance') == 'on'

    price = 700 if age < 18 else 1000
    if shelf in ['нижняя', 'нижняя боковая']:
        price += 100
    if bedding:
        price += 75
    if luggage:
        price += 250
    if insurance:
        price += 150

    return render_template('lab3/ticket.html', name=name, age=age, shelf=shelf,
                        bedding=bedding, luggage=luggage, from_city=from_city, to=to_city,
                        date=date, insurance=insurance, price=price)

books = [
    {"author": "Донато Карризи", "title": "Девушка в тумане", "genre": "Детектив, триллер", "pages": 416, "price": 650, "publisher": "Эксмо"},
    {"author": "Донато Карризи", "title": "Потерянные девушки Рима", "genre": "Детектив", "pages": 512, "price": 720, "publisher": "АСТ"},
    {"author": "Донато Карризи", "title": "Дом голосов", "genre": "Триллер, драма", "pages": 384, "price": 580, "publisher": "Эксмо"},
    {"author": "Андреас Грубер", "title": "Смерть приходит по записи", "genre": "Детектив, триллер", "pages": 512, "price": 690, "publisher": "АСТ"},
    {"author": "Андреас Грубер", "title": "Смерть по подписке", "genre": "Детектив, криминал", "pages": 544, "price": 740, "publisher": "Эксмо"},
    {"author": "Андреас Грубер", "title": "Смерть как ремесло", "genre": "Психологический триллер", "pages": 576, "price": 780, "publisher": "АСТ"},
    {"author": "Себастьян Фитцек", "title": "Терапия", "genre": "Психологический триллер", "pages": 320, "price": 560, "publisher": "Эксмо"},
    {"author": "Себастьян Фитцек", "title": "Пассажир 23", "genre": "Детектив, триллер", "pages": 352, "price": 610, "publisher": "АСТ"},
    {"author": "Себастьян Фитцек", "title": "Посылка", "genre": "Психологический триллер", "pages": 368, "price": 590, "publisher": "Эксмо"},
    {"author": "Франк Тилье", "title": "Лес теней", "genre": "Детектив, триллер", "pages": 448, "price": 670, "publisher": "АСТ"},
    {"author": "Франк Тилье", "title": "Синдром Е", "genre": "Детектив, триллер", "pages": 512, "price": 730, "publisher": "Эксмо"},
    {"author": "Франк Тилье", "title": "Головоломка", "genre": "Психологический триллер", "pages": 416, "price": 640, "publisher": "АСТ"},
    {"author": "Ю Несбё", "title": "Снеговик", "genre": "Криминал", "pages": 480, "price": 710, "publisher": "Азбука"},
    {"author": "Ю Несбё", "title": "Призрак", "genre": "Детектив", "pages": 512, "price": 750, "publisher": "Азбука"},
    {"author": "Ю Несбё", "title": "Полиция", "genre": "Триллер", "pages": 544, "price": 770, "publisher": "Азбука"},
    {"author": "Питер Джеймс", "title": "Убийственно просто", "genre": "Детектив", "pages": 432, "price": 690, "publisher": "Эксмо"},
    {"author": "Питер Джеймс", "title": "Мёртвая простота", "genre": "Триллер", "pages": 480, "price": 720, "publisher": "АСТ"},
    {"author": "Питер Джеймс", "title": "Простая месть", "genre": "Криминальный роман", "pages": 512, "price": 740, "publisher": "Эксмо"},
    {"author": "Питер Джеймс", "title": "Простая правда", "genre": "Психологический триллер", "pages": 400, "price": 670, "publisher": "АСТ"},
    {"author": "Донато Карризи", "title": "Игра снов", "genre": "Психологический детектив", "pages": 448, "price": 700, "publisher": "АСТ"},
    {"author": "Донато Карризи", "title": "Мастер теней", "genre": "Триллер", "pages": 496, "price": 750, "publisher": "Эксмо"},
]

@lab3.route('/lab3/books')
def book_search():
    min_price = request.args.get('min_price') or request.cookies.get('min_price')
    max_price = request.args.get('max_price') or request.cookies.get('max_price')

    min_price = int(min_price) if min_price else None
    max_price = int(max_price) if max_price else None

    if min_price is not None and max_price is not None and min_price > max_price:
        min_price, max_price = max_price, min_price

    prices = [book['price'] for book in books]
    min_possible = min(prices)
    max_possible = max(prices)

    filtered_books = [
        book for book in books
        if (min_price is None or book['price'] >= min_price) and
            (max_price is None or book['price'] <= max_price)
        ] if min_price is not None or max_price is not None else []


    show_results = bool(min_price or max_price)

    resp = make_response(render_template('lab3/books.html',
                                         books=filtered_books,
                                         count=len(filtered_books),
                                         min_price=min_price,
                                         max_price=max_price,
                                         min_possible=min_possible,
                                         max_possible=max_possible,
                                         show_results=show_results))

    if min_price is not None:
        resp.set_cookie('min_price', str(min_price))
    if max_price is not None:
        resp.set_cookie('max_price', str(max_price))

    return resp


@lab3.route('/lab3/books/reset')
def reset_books():
    resp = make_response(redirect('/lab3/books'))
    resp.delete_cookie('min_price')
    resp.delete_cookie('max_price')
    return resp
