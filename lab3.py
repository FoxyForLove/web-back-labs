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

