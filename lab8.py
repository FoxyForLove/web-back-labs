from flask import Blueprint, request, render_template, session, current_app,redirect
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3 
from os import path
from db import db
from db.models import users,articles
from flask_login import login_user, login_required, current_user,logout_user
from werkzeug.utils import redirect

lab8 = Blueprint('lab8', __name__)

@lab8.route("/lab8/")
def main():
    if current_user.is_authenticated:
        return render_template("lab8/lab8.html", username=current_user.login)
    return render_template("lab8/lab8.html", username="anonymous")

@lab8.route('/lab8/register/', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')

    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if not login_form:
        return render_template('lab8/register.html',
                               error = 'Имя пользователя не должно быть пустым')
    
    if not password_form:
        return render_template('lab8/register.html',
                               error = 'Пароль не должен быть пустым')
    
    login_exists = users.query.filter_by(login = login_form).first()
    if login_exists:
        return render_template('lab8/register.html',
                               error = 'Такой пользователь уже существует')
    

    password_hash = generate_password_hash(password_form)
    new_user = users(login = login_form, password = password_hash)
    db.session.add(new_user)
    db.session.commit()


    login_user(new_user, remember=True)
    return redirect('/lab8/')


@lab8.route('/lab8/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    remember_form = request.form.get('remember')
    next_url = request.args.get('next')

    if not login_form:
        return render_template('lab8/login.html',
                               error='Логин не должен быть пустым')

    if not password_form:
        return render_template('lab8/login.html',
                               error='Пароль не должен быть пустым')

    user = users.query.filter_by(login = login_form).first()

    if user:
        if check_password_hash(user.password, password_form):
            remember = True if remember_form else False
            login_user(user, remember=remember)
            return redirect('/lab8/')
        if next_url:
            return redirect(next_url.encode('utf-8'))
        return redirect('/lab8/')
        
    return render_template('/lab8/login.html',
                           error = 'Ошибка входа: логин и/или пароль неверны')


@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')


@lab8.route('/lab8/articles/')
def article_list():
    if current_user.is_authenticated:
        all_articles = articles.query.all()
    else:
        all_articles = articles.query.filter_by(is_public=True).all()
    return render_template('lab8/articles.html', articles = all_articles)


@lab8.route('/lab8/create', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'GET':
        return render_template('lab8/create.html')

    title = request.form.get('title')
    text = request.form.get('article_text')
    is_public = request.form.get('is_public') == 'on'

    if not title:
        return render_template('lab8/create.html',
                               error='Заголовок не должен быть пустым')
    if not text:
        return render_template('lab8/create.html',
                               error='Текст статьи не должен быть пустым')

    new_article = articles(title = title, article_text=text, login_id = current_user.id, is_public=is_public)
    db.session.add(new_article)
    db.session.commit()
    return redirect('/lab8/articles/')


@lab8.route('/lab8/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_article(id):
    article = articles.query.get_or_404(id)
    if article.login_id != current_user.id:
        return "Нет доступа", 403

    if request.method == 'GET':
        return render_template('lab8/edit.html', article=article)

    title = request.form.get('title')
    text = request.form.get('article_text')

    if not title:
        return render_template('lab8/edit.html',
                               article=article,
                               error='Заголовок не должен быть пустым')
    if not text:
        return render_template('lab8/edit.html',
                               article=article,
                               error='Текст статьи не должен быть пустым')

    article.title = title
    article.article_text = text
    db.session.commit()
    return redirect('/lab8/articles/')


@lab8.route('/lab8/delete/<int:id>', methods=['POST'])
@login_required
def delete_article(id):
    article = articles.query.get_or_404(id)
    if article.login_id != current_user.id:
        return "Нет доступа", 403

    db.session.delete(article)
    db.session.commit()
    return redirect('/lab8/articles/')