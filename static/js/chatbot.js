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
            console.log(data);
        })
        .catch((error) => console.log(error));
}

function addMessage_user(message){
    var container = document.getElementById('message_container');
    var user_message = document.createElement('div');
    user_message.classList.add('user_message');

    var ask = document.createElement('p');
    ask.textContent = message;

    user_message.appendChild(ask);
    container.appendChild(user_message);

}

function addMessage_com(data){
    var container = document.getElementById('message_container');
    var com_message = document.createElement('div');
    com_message.classList.add('com_message');

    var answer = document.createElement('p');
    answer.textContent = data.best_answer;

    com_message.appendChild(answer);
    if(data.legal_info.law != null){
        var com_btn_law = document.createElement('button');
        com_btn_law.textContent = "참고 법령 - "+data.legal_info.law+"에 대해 확인하기";
        com_btn_law.classList.add('com_btn');
        com_message.appendChild(com_btn_law);
        com_btn_law.addEventListener('click', function() {
            checkLaw(data);
        });
    }
    if(data.legal_info.prec != null){
        var com_btn_prec = document.createElement('button');
        com_btn_prec.textContent = "참고 판례 - "+data.legal_info.law+"에 대해 확인하기";
        com_btn_prec.classList.add('com_btn');
        com_message.appendChild(com_btn_prec);
        com_btn_prec.addEventListener('click', function() {
            checkPrec(data);
        });
    }
    container.appendChild(com_message)
}

function addMessage_com_law(data){
    var container = document.getElementById('message_container');
    var com_message = document.createElement('div');
    com_message.classList.add('com_message');

    var answer = document.createElement('p');
    answer.textContent = data.law_content;

    com_message.appendChild(answer);
    container.appendChild(com_message)
}
function addMessage_com_prec(data){
    console.log(data);
    var container = document.getElementById('message_container');
    var com_message = document.createElement('div');
    var text_container = document.createElement("div");
    com_message.classList.add('com_message');
    
    for(const key in data){
        var text = document.createElement("p");
        text.innerHTML = '<span class="prec_bold">' + key + '</span> ' + '<span class="prec_thin">' + data[key] + '</span>';
        com_message.appendChild(text)
    };
    container.appendChild(com_message);
}

function checkLaw(data){
    var asklaw = data.textContent;
    asklaw = asklaw.replace("참고 법령 - ",'');
    asklaw = asklaw.replace("에 대해 확인하기"),'';

    fetch('/button_law/',{
        method:'POST',
        header:{
            'Content-Type':'application/json'
        },
        body:JSON.stringify({
            law : asklaw
        })
    })
    .then(response=>{
        if(response.status==200){
            return response.json();        
        }
    }).catch((error)=>console.log(error))
    .then((data)=>{
        addMessage_com_law(data.law)
    })
}

function checkPrec(data){
    var askprec = data.textContent;
    askprec = prec.replace("참고 판례 - ",'');
    askprec = prec.replace("에 대해 확인하기",'');

    fetch('/button_prec/',{
        method:'POST',
        header:{
            'Content-Type':'application/json'
        },
        body:JSON.stringify({
            prec : askprec
        })
    })
    .then(response=>{
        if(response.status==200){
            return response.json();        
        }
    }).catch((error)=>console.log(error))
    .then((data)=>{
        addMessage_com_prec(data)
    })
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}