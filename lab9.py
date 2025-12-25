from flask import Blueprint, render_template, request, session, jsonify
import random

lab9 = Blueprint('lab9', __name__)

BOX_COUNT = 10

congrats = [
    "С Новым годом! Пусть сбудутся мечты!",
    "Счастья и тепла в новом году!",
    "Пусть год принесёт удачу!",
    "Здоровья и радости!",
    "Пусть всё получится!",
    "Улыбок и вдохновения!",
    "Пусть год будет ярким!",
    "Тепла и уюта!",
    "Пусть будет много побед!",
    "Исполнения желаний!"
]

gifts = [f"gift{i}.png" for i in range(1, 11)]
presents = [f"present{i}.png" for i in range(1, 11)]

GLOBAL_BOX_STATE = [False] * BOX_COUNT


def random_position(size, field_w, field_h, padding, existing):
    gap = 10
    min_left, max_left = padding, field_w - size - padding
    min_top, max_top = padding, field_h - size - padding

    for _ in range(2000):
        left = random.randint(min_left, max_left)
        top = random.randint(min_top, max_top)

        if all(
            abs(pos["left"] - left) >= size + gap or
            abs(pos["top"] - top) >= size + gap
            for pos in existing
        ):
            return {"left": left, "top": top}

    return {"left": min_left, "top": min_top}


@lab9.route("/lab9/")
def index():
    session.setdefault("opened", 0)

    if "positions" not in session:
        positions = []
        for _ in range(BOX_COUNT):
            positions.append(random_position(100, 700, 550, 15, positions))
        session["positions"] = positions

    remaining = GLOBAL_BOX_STATE.count(False)

    return render_template(
        "lab9/index.html",
        box_ids=range(BOX_COUNT),
        box_state=GLOBAL_BOX_STATE,
        positions=session["positions"],
        remaining=remaining
    )


@lab9.route("/lab9/open", methods=['POST'])
def open_box():
    global GLOBAL_BOX_STATE

    data = request.get_json()
    box_id = data.get("box_id")

    try:
        box_id = int(box_id)
    except:
        return jsonify({"error": "Некорректный номер коробки"})

    if not 0 <= box_id < BOX_COUNT:
        return jsonify({"error": "Некорректный номер коробки"})

    if session["opened"] >= 3:
        return jsonify({"error": "Вы уже открыли 3 коробки"})

    if GLOBAL_BOX_STATE[box_id]:
        return jsonify({"error": "Эта коробка уже открыта"})

    GLOBAL_BOX_STATE[box_id] = True
    session["opened"] += 1

    remaining = GLOBAL_BOX_STATE.count(False)

    return jsonify({
        "congrats": congrats[box_id],
        "gift": gifts[box_id],
        "present": presents[box_id],
        "remaining": remaining
    })


@lab9.route("/lab9/reset", methods=['POST'])
def reset():
    global GLOBAL_BOX_STATE

    GLOBAL_BOX_STATE = [False] * BOX_COUNT
    session["opened"] = 0

    positions = []
    for _ in range(BOX_COUNT):
        positions.append(random_position(100, 700, 550, 15, positions))
    session["positions"] = positions

    return {}
