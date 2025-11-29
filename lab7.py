from flask import Blueprint, request, render_template, session, current_app, abort
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
import jsonify
from os import path

lab7 = Blueprint('lab7', __name__)

@lab7.route("/lab7/")
def main():
    return render_template("lab7/index.html")

films = [
    {
        "title": "Taxi",
        "title_ru": "Такси",
        "year": 1998,
        "description": "Французский комедийный боевик о талантливом водителе такси в Марселе,"
        "который вынужден помочь неуклюжему полицейскому‑инспектору поймать банду "
        "профессиональных грабителей банков. Этот фильм стал первой частью успешной франшизы."
    },
    {
        "title": "Léon: The Professional",
        "title_ru": "Леон",
        "year": 1994,
        "description": "Криминальный боевик‑драма режиссёра Люка Бессона, "
        "рассказывающий историю профессионального наёмного убийцы Леона, который "
        "берёт под свою защиту 12‑летнюю девочку Матильду после того, как её семья "
        "была уничтожена коррумпированными полицейскими. Он учит её искусству выживания, "
        "и между ними зарождается нестандартная связь."
    },
    {
        "title": "Resident Evil",
        "title_ru": "Обитель зла",
        "year": 2002,
        "description": "Британско‑американский фантастический боевик‑хоррор, первая "
        "экранизация одноимённой серии видеоигр. Фильм рассказывает о героине Алисе и"
        "группе спецназовцев, пытающихся остановить вспышку вируса T и предотвратить"
        " зомби‑апокалипсис в засекреченном комплексе корпорации Umbrella. "

    },
    {
        "title": "Intouchables",
        "title_ru": "1+1",
        "year": 2011,
        "description": "Трогательная французская комедийная драма, основанная на реальной"
        " истории: богатый аристократ Филипп, ставший инвалидом после несчастного случая, "
        "нанимает себе нянечку/помощника — бывшего мелкого правонарушителя Дрисса. "
        "Между ними развиваются искренняя дружба и взаимное уважение, несмотря на социальные "
        "и расовые различия."
    },
    {
        "title": "Green Book",
        "title_ru": "Зелёная книга",
        "year": 2018,
        "description": "Биографическая драма‑дружба, основанная на реальных событиях:"
        " чернокожий джазовый пианист Дон Ширли нанимает водителя Тони Валлелонгу для "
        "турне по южным штатам США. В поездке они сталкиваются с расизмом и предрассудками, "
        "но по ходу путешествия между ними возникает глубокая дружба."
    }
]


@lab7.route("/lab7/rest-api/films/", methods=['GET'])
def get_films():
    return films


@lab7.route("/lab7/rest-api/films/<int:id>", methods=['GET'])
def get_film(id):
    if id < 0 or id >= len(films):
        abort(404,description="Films not found")
    return films[id]


@lab7.route("/lab7/rest-api/films/<int:id>", methods=['DELETE'])
def del_film(id):
    if id < 0 or id >= len(films):
        abort(404, description="Film not found")
    del films[id]
    return '', 204
   

@lab7.route("/lab7/rest-api/films/<int:id>", methods=['PUT'])
def put_films(id):
    if id < 0 or id >= len(films):
        abort(404, description="Film not found")

    film = request.get_json()
    films[id] = film 
    return films[id], 200


@lab7.route("/lab7/rest-api/films/", methods=['POST'])
def add_film():
    film = request.get_json()
    films.append(film)

    new_id = len(films) - 1
    film_with_id = films[new_id]
    film_with_id["id"] = new_id 

    return film_with_id, 201