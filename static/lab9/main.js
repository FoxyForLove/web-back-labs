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
    let popup = document.createElement('div');
    popup.className = 'congrats-popup';
    popup.innerHTML = `
        <img src="/static/lab9/${present}" class="present-img">
        <p>${text}</p>
    `;

    let field = document.getElementById('field');
    field.append(popup);

    popup.style.position = 'absolute';

    let left = box.offsetLeft;
    let top = box.offsetTop;

    let popupRect = popup.getBoundingClientRect();
    let margin = 10;

    let maxLeft = field.clientWidth - popupRect.width - margin;
    let maxTop = field.clientHeight - popupRect.height - margin;

    if (left < margin) left = margin;
    if (top < margin) top = margin;
    if (left > maxLeft) left = maxLeft;
    if (top > maxTop) top = maxTop;

    popup.style.left = left + 'px';
    popup.style.top = top + 'px';

    box.classList.add('opened');
    box.onclick = null;
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
