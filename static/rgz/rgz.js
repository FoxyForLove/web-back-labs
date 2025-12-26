/* < Служебные функции > */

function setMsg(id, text) {
    let m = document.getElementById(id);
    if (!m) return;
    m.innerText = text || '';
}

function api(url, method, bodyObj) {
    let opts = { method: method, headers: {} };
    if (bodyObj !== undefined) {
        opts.headers["Content-Type"] = "application/json";
        opts.body = JSON.stringify(bodyObj);
    }
    return fetch(url, opts)
        .then(function(resp) {
            return resp.json().then(function(data) {
                return { ok: resp.ok, status: resp.status, data: data };
            });
        });
}


/* < Регистрация > */

function register() {
    setMsg('msg-register', '');
    let name = document.getElementById('reg-name').value;
    let login = document.getElementById('reg-login').value;
    let password = document.getElementById('reg-pass').value;

    api('/rgz/api/register', 'POST', { name: name, login: login, password: password })
        .then(function(r) {
            if (!r.ok) {
                setMsg('msg-register', r.data.error || 'Ошибка регистрации');
                return;
            }
            location.reload();
        });
}


/* < Вход > */

function login() {
    setMsg('msg-login', '');
    let login = document.getElementById('log-login').value;
    let password = document.getElementById('log-pass').value;

    api('/rgz/api/login', 'POST', { login: login, password: password })
        .then(function(r) {
            if (!r.ok) {
                setMsg('msg-login', r.data.error || 'Ошибка входа');
                return;
            }
            location.reload();
        });
}


/* < Выход > */

function logout() {
    api('/rgz/api/logout', 'POST', {})
        .then(function() {
            location.href = '/rgz/';
        });
}


/* < Удаление аккаунта > */

function deleteMe() {
    if (!confirm("Точно удалить аккаунт? Все ваши брони удалятся.")) return;

    api('/rgz/api/me', 'DELETE')
        .then(function(r) {
            if (!r.ok) {
                setMsg('msg-global', r.data.error || 'Не удалось удалить аккаунт');
                return;
            }
            location.href = '/rgz/';
        });
}


/* < Сеансы: загрузка списка > */

function loadScreenings() {
    setMsg('msg-global', '');
    fetch('/rgz/api/screenings')
        .then(resp => resp.json())
        .then(items => {
            let tbody = document.getElementById('screening-list');
            tbody.innerHTML = '';

            items.forEach(item => {
                let tr = document.createElement('tr');

                let tdFilm = document.createElement('td');
                tdFilm.innerText = item.film_title;

                let tdStart = document.createElement('td');
                tdStart.innerText = item.start_at;

                let tdStatus = document.createElement('td');
                tdStatus.innerText = item.is_past ? 'прошёл' : 'актуален';
                tdStatus.className = item.is_past ? 'rgz-past' : 'rgz-future';

                let tdActions = document.createElement('td');

                let openBtn = document.createElement('button');
                openBtn.innerText = 'Открыть';
                openBtn.className = 'rgz-btn';
                openBtn.onclick = () => location.href = '/rgz/screenings/' + item.id;
                tdActions.append(openBtn);

                let isAdmin = document.querySelector('.rgz-admin-badge') !== null;
                if (isAdmin) {
                    let delBtn = document.createElement('button');
                    delBtn.innerText = 'Удалить';
                    delBtn.className = 'rgz-btn rgz-btn-danger';
                    delBtn.disabled = item.is_past;
                    delBtn.onclick = () => deleteScreening(item.id, item.film_title);
                    tdActions.append(delBtn);
                }

                tr.append(tdFilm, tdStart, tdStatus, tdActions);
                tbody.append(tr);
            });
        });
}


/* < Сеансы: создание > */

function createScreening() {
    setMsg('msg-admin', '');
    let film = document.getElementById('new-film').value;
    let start = document.getElementById('new-start').value;

    api('/rgz/api/screenings', 'POST', { film_title: film, start_at: start })
        .then(function(r) {
            if (!r.ok) {
                setMsg('msg-admin', r.data.error || 'Не удалось создать сеанс');
                return;
            }
            document.getElementById('new-film').value = '';
            document.getElementById('new-start').value = '';
            loadScreenings();
        });
}


/* < Сеансы: удаление > */

function deleteScreening(id, title) {
    if (!confirm('Удалить сеанс: ' + title + '?')) return;

    api('/rgz/api/screenings/' + id, 'DELETE')
        .then(function(r) {
            if (!r.ok) {
                setMsg('msg-admin', r.data.error || 'Не удалось удалить');
                return;
            }
            loadScreenings();
        });
}


/* < Места: загрузка и логика бронирования > */

function loadSeats(screeningId) {
    setMsg('msg-seats', '');

    fetch('/rgz/api/screenings/' + screeningId + '/seats')
        .then(resp => resp.json())
        .then(data => {

            let info = document.getElementById('screening-info');
            info.innerHTML = `<b>${data.screening.film_title}</b> | ${data.screening.start_at}` +
                             (data.screening.is_past ? ' <span class="rgz-past">(прошёл)</span>' : '');

            let grid = document.getElementById('seat-grid');
            grid.innerHTML = '';

            let freeCount = 0;
            let bookedCount = 0;

            let rows = [[], [], [], []];
            let seatsPerRow = Math.ceil(data.seats.length / 4);

            data.seats.forEach((s, i) => {
                rows[Math.floor(i / seatsPerRow)].push(s);
            });

            rows.forEach((row, index) => {
                let rowDiv = document.createElement('div');
                rowDiv.className = 'rgz-seat-row';

                let label = document.createElement('div');
                label.className = 'rgz-row-label';
                label.innerText = 'Ряд ' + (index + 1);
                rowDiv.append(label);

                row.forEach(s => {
                    if (s.is_booked) bookedCount++;
                    else freeCount++;

                    let btn = document.createElement('button');
                    btn.className = 'rgz-seat ' + (s.is_booked ? 'booked' : 'free');
                    btn.innerText = s.is_booked ? s.seat_no + ' ✖' : s.seat_no;

                    btn.title = s.is_booked
                        ? 'Занял: ' + s.user_name + ' (' + s.user_login + ')'
                        : 'Свободно';

                    btn.onclick = function() {

                        if (data.screening.is_past) {
                            alert('Сеанс в прошлом — только просмотр');
                            return;
                        }

                        if (s.is_booked) {
                            if (data.me.is_auth && (data.me.is_admin || data.me.login === s.user_login)) {
                                if (!confirm('Снять бронь с места ' + s.seat_no + '?')) return;

                                api(`/rgz/api/screenings/${screeningId}/seats/${s.seat_no}`, 'DELETE')
                                    .then(r => {
                                        if (!r.ok) {
                                            setMsg('msg-seats', r.data.error || 'Не удалось снять бронь');
                                            return;
                                        }
                                        loadSeats(screeningId);
                                    });
                                return;
                            }

                            alert('Место занял: ' + s.user_name + ' (' + s.user_login + ')');
                            return;
                        }

                        if (!data.me.is_auth) {
                            alert('Нужно войти, чтобы занять место');
                            return;
                        }

                        if (data.me.selected_count >= 5) {
                            setMsg('msg-seats', 'Вы уже выбрали 5 мест');
                            return;
                        }

                        api(`/rgz/api/screenings/${screeningId}/seats/${s.seat_no}`, 'POST')
                            .then(r => {
                                if (!r.ok) {
                                    setMsg('msg-seats', r.data.error || 'Не удалось занять место');
                                    return;
                                }
                                loadSeats(screeningId);
                            });
                    };

                    rowDiv.append(btn);
                });

                grid.append(rowDiv);
            });

            const header = document.querySelector('.rgz-card h2');
            if (header) {
                header.innerText = `Места: свободно ${freeCount}, занято ${bookedCount}`;
            }
        });
}


/* < Форматирование даты > */

function rgz_format_datetime_input(el) {
    let v = el.value.replace(/\D/g, "");

    if (v.length > 4) v = v.slice(0,4) + "-" + v.slice(4);
    if (v.length > 7) v = v.slice(0,7) + "-" + v.slice(7);
    if (v.length > 10) v = v.slice(0,10) + " " + v.slice(10);
    if (v.length > 13) v = v.slice(0,13) + ":" + v.slice(13);

    el.value = v;
}


/* < Инициализация > */

document.addEventListener("DOMContentLoaded", () => {
    if (typeof loadScreenings === "function") {
        loadScreenings();
    }
});
