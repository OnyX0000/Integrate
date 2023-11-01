const textarea = document.getElementById("message_input");
const sendbtn = document.getElementById('message_btn');

textarea.addEventListener("input", function () {
    this.style.height = "auto";

    const lineHeight = parseFloat(getComputedStyle(this).lineHeight);
    const minRows = 3;

    const scrollHeight = this.scrollHeight;
    const maxScrollHeight = minRows * lineHeight;

    if (scrollHeight >= maxScrollHeight) {
        this.style.overflowY = "auto";
    } else {
        this.style.height = scrollHeight + "px";
    }
});

textarea.style.height = "auto";
sendbtn.addEventListener("click", () => {
    addMessage_user(textarea.value);
    submit(textarea.value);
    textarea.value = '';
    textarea.rows = '1';
});
textarea.addEventListener("keydown", (e) => {
    if (e.keyCode == '13') {
        if (!e.shiftKey) {
            addMessage_user(textarea.value);
            submit(textarea.value);
            textarea.value = '';
            textarea.rows = '1';
        }
    }
});

function getCSRFToken() {
    const csrfToken = getCookie('csrftoken');
    return csrfToken;
}

function submit(message) {
    fetch('/messages/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken() // CSRF 토큰 추가
        },
        body: JSON.stringify({
            user_input: message
        }),
    })
        .then(response => {
            if (response.status == 200) {
                return response.json();
            } else if (response.status == 405) {
                throw new Error('Method Not Allowed (405)');
            } else {
                throw new Error('에러 발생');
            }
        })
        .then((data) => {
            addMessage_com(data);
        })
        .catch((error) => console.log(error));
}

function addMessage_user(message) {
    var container = document.getElementById('message_container');
    var user_message = document.createElement('div');
    user_message.classList.add('user_message');

    var ask = document.createElement('p');
    ask.textContent = message;

    user_message.appendChild(ask);
    container.appendChild(user_message);
}

function addMessage_com(data) {
    var container = document.getElementById('message_container');
    var com_message = document.createElement('div');
    com_message.classList.add('com_message');

    var answer = document.createElement('p');
    answer.textContent = data.messages;

    com_message.appendChild(answer);
    if (data.legal_info.law != '') {
        var com_btn = document.createElement('button');
        com_btn.textContent = "참고 법령 - " + data.legal_info.law + "에 대해 확인하기";
        com_btn.classList.add('com_btn');
        com_message.appendChild(com_btn);
    }
    if (data.legal_info.prec != '') {
        var com_btn = document.createElement('button');
        com_btn.textContent = "참고 판례 - " + data.legal_info.prec + "에 대해 확인하기";
        com_btn.classList.add('com_btn');
        com_message.appendChild(com_btn);
    }
    container.appendChild(com_message);
}

function checkLaw(data) {
    var law = data.textContent;
    law = law.replace("참고 법령 - ", '');
    law = law.replace("에 대해 확인하기", '');
}

function checkPrec(data) {
    var prec = data.textContent;
    prec = prec.replace("참고 판례 - ", '');
    prec = prec.replace("에 대해 확인하기", '');
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}