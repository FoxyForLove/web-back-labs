function clearMessage() {
    document.getElementById('message').innerText = '';
}

function setMessage(text) {
    document.getElementById('message').innerText = text;
}

function updateRemaining(n) {
    document.getElementById('remaining').innerText = n;
}

function showCongrats(box, text, present) {
    box.innerHTML = '';

    let div = document.createElement('div');
    div.className = 'congrats-popup';

    let img = document.createElement('img');
    img.src = `/static/lab9/${present}`;
    img.className = 'present-img';

    let p = document.createElement('p');
    p.innerText = text;

    div.append(img);
    div.append(p);

    box.classList.add('opened');
    box.onclick = null;

    box.append(div);
}

function handleBoxClick(box) {
    if (box.classList.contains('opened'))
        return;

    clearMessage();

    let id = box.dataset.id;

    fetch('/lab9/open', {
        method: 'POST',
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({box_id: id})
    })
    .then(resp => resp.json())
    .then(data => {
        if (data.error) {
            setMessage(data.error);
            return;
        }

        showCongrats(box, data.congrats, data.present);
        updateRemaining(data.remaining);
    });
}

function initBoxes() {
    document.querySelectorAll('.box').forEach(box => {
        box.onclick = () => handleBoxClick(box);
    });
}

function initResetButton() {
    let resetBtn = document.getElementById('reset-session');
    resetBtn.onclick = function() {
        fetch('/lab9/reset', {method: 'POST'})
        .then(() => location.reload());
    };
}

document.addEventListener('DOMContentLoaded', function() {
    initBoxes();
    initResetButton();
});
