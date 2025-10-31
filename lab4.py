from flask import Blueprint, request, render_template,redirect, session

lab4 = Blueprint('lab4',__name__)

@lab4.route("/lab4/")
def lab():
    return render_template("lab4/lab4.html")


@lab4.route("/lab4/div-form")
def div_form():
    return render_template("lab4/div-form.html")


@lab4.route("/lab4/div", methods = ['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
            return render_template('lab4/div.html', error='Оба поля должны быть заполнены!')
    if x2 == '0':
        return render_template('lab4/div.html', error='На ноль делить нельзя!')
    x1 = int(x1)
    x2 = int(x2)
    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)


@lab4.route("/lab4/sum-form")
def sum_form():
    return render_template("lab4/sum-form.html")


@lab4.route("/lab4/sum", methods=['POST'])
def summation():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if x1 == '':
        x1 = '0'
    if x2 == '':
        x2 = '0'

    result = int(x1) + int(x2)
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)


@lab4.route("/lab4/mul-form")
def mul_form():
    return render_template("lab4/mul-form.html")


@lab4.route("/lab4/mul", methods=['POST'])
def mul():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if x1 == '':
        x1 = '1'
    if x2 == '':
        x2 = '1'

    result = int(x1) * int(x2)
    return render_template('lab4/mul.html', x1=x1, x2=x2, result=result)


@lab4.route("/lab4/sub-form")
def sub_form():
    return render_template("lab4/sub-form.html")


@lab4.route("/lab4/sub", methods=['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if x1 == '' or x2 == '':
        return render_template('lab4/sub.html', error='Оба поля должны быть заполнены!')

    result = int(x1) - int(x2)
    return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)


@lab4.route("/lab4/pow-form")
def pow_form():
    return render_template("lab4/pow-form.html")


@lab4.route("/lab4/pow", methods=['POST'])
def pow_():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if x1 == '' or x2 == '':
        return render_template('lab4/pow.html', error='Оба поля должны быть заполнены!')

    if x1 == '0' and x2 == '0':
        return render_template('lab4/pow.html', error='0 в степени 0 не определено!')

    result = int(x1) ** int(x2)
    return render_template('lab4/pow.html', x1=x1, x2=x2, result=result)

tree_count = 0
max_trees = 25

@lab4.route("/lab4/tree", methods= ['GET', 'POST'])
def tree():
    global tree_count, max_trees
    if request.method == 'GET':
        return render_template("lab4/tree.html", tree_count=tree_count, max_trees=max_trees)
    
    operation = request.form.get('operation')

    if operation == 'cut' and tree_count > 0:
        tree_count -= 1
    elif operation == 'plant' and tree_count < max_trees:
        tree_count += 1

    return redirect('/lab4/tree')

users = [
    {'login': 'alex', 'password': '123', 'name': 'Алексей', 'gender': 'муж'},
    {'login': 'bob', 'password': '555', 'name': 'Боб', 'gender': 'муж'},
    {'login': 'cat', 'password': '666', 'name': 'Кэтрин', 'gender': 'жен'},
    {'login': 'bird', 'password': '234', 'name': 'Бёрд', 'gender': 'муж'},
    {'login': 'dog', 'password': '345', 'name': 'Дог', 'gender': 'муж'}
]

@lab4.route("/lab4/login", methods = ['GET','POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            login = session['login']
            for user in users:
                if user['login'] == login:
                    name = user.get('name', login)
                    break
            return render_template("lab4/login.html", authorized=authorized, name=name, login='')
        else:
            authorized = False
            return render_template("lab4/login.html", authorized=authorized, login='', error='')

    login = request.form.get('login', '')
    password = request.form.get('password', '')

    if not login:
        error = 'Не введён логин'
        return render_template("lab4/login.html", error=error, authorized=False, login='')

    if not password:
        error = 'Не введён пароль'
        return render_template("lab4/login.html", error=error, authorized=False, login=login)

    for user in users:
        if login == user['login'] and password == user['password']:
            session['login'] = login
            return redirect('/lab4/login')

    error = 'Неверные логин и/или пароль'
    return render_template("lab4/login.html", error=error, authorized=False, login=login)


@lab4.route("/lab4/logout", methods = ['POST'])
def logout():
    session.pop('login',None)
    return redirect('/lab4/login')


@lab4.route("/lab4/fridge", methods = ['GET','POST'])
def fridge():
    if request.method == 'GET':
        return render_template("lab4/fridge.html", result='', temperature='')

    temp_raw = request.form.get('temperature', '')

    if 'reset' in request.form:
        return render_template("lab4/fridge.html", result='', temperature='')
    
    if temp_raw == '':
        result = 'Ошибка: не задана температура'
        return render_template("lab4/fridge.html", result=result, temperature='')

    try:
        temp = int(temp_raw)
    except ValueError:
        result = 'Ошибка: неверный формат температуры'
        return render_template("lab4/fridge.html", result=result, temperature=temp_raw)

    if temp < -12:
        result = 'Не удалось установить температуру — слишком низкое значение'
        return render_template("lab4/fridge.html", result=result, temperature=temp)
    if temp > -1:
        result = 'Не удалось установить температуру — слишком высокое значение'
        return render_template("lab4/fridge.html", result=result, temperature=temp)

    snowflakes = 0
    if -12 <= temp <= -9:
        snowflakes = 3
    elif -8 <= temp <= -5:
        snowflakes = 2
    elif -4 <= temp <= -1:
        snowflakes = 1

    result = f'Установлена температура: {temp}°С'
    return render_template("lab4/fridge.html", result=result, temperature=temp, snowflakes=snowflakes)

PRICES = {
        'Ячмень': 12000,
        'Овёс': 8500,
        'Пшеница': 9000,
        'Рожь': 15000
    }


@lab4.route("/lab4/grain_order", methods=['GET', 'POST'])
def grain_order():

    if request.method == 'GET':
        return render_template("lab4/grain_order.html", result='', grain='', weight='')

    if 'reset' in request.form:
        return render_template("lab4/grain_order.html", result='', grain='', weight='')

    grain = request.form.get('grain', '')
    weight_raw = request.form.get('weight', '')

    if weight_raw == '':
        result = 'Ошибка: не указан вес'
        return render_template("lab4/grain_order.html", result=result, grain=grain, weight='')

    weight = float(weight_raw)

    if weight <= 0:
        result = 'Ошибка: вес должен быть больше 0'
        return render_template("lab4/grain_order.html", result=result, grain=grain, weight=weight_raw)

    if weight > 100:
        result = 'Ошибка: такого объёма сейчас нет в наличии'
        return render_template("lab4/grain_order.html", result=result, grain=grain, weight=weight_raw)

    price_per_t = PRICES[grain]
    total = weight * price_per_t
    discount = 0.0
    discount_msg = ''

    if weight > 10:
        discount = 0.10  
        discount_amount = total * discount
        total_after = total - discount_amount
        discount_msg = f'Применена скидка за большой объём: {int(discount*100)}% ({int(discount_amount)} руб)'
        total = total_after
    else:
        discount_amount = 0

    total_int = int(round(total))

    result = (f'Заказ успешно сформирован. Вы заказали {grain}. Вес: {weight} т. '
              f'Сумма к оплате: {total_int} руб.')
    if discount_msg:
        result = result + ' ' + discount_msg

    return render_template("lab4/grain_order.html", result=result, grain=grain, weight=weight)