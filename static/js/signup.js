function checkBlank(word){
    if(word == '') return false;
    return true;
}
function signUp(){
    const userName = document.getElementById('input-name').value;
    const userID = document.getElementById('input-id').value;
    const userPW = document.getElementById('input-pw').value;
    const confirmPW = document.getElementById('input-pw-cf').value;

    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value; // 수정

    token = localStorage.getItem('access_token');

    if(userPW!=confirmPW){
        alert("비밀번호가 일치하지 않습니다.")
    }else if(checkBlank(userID)!=true){
        alert("사용할 이메일을 입력해주세요.")
    }
    else if(checkBlank(userName)!=true){
        alert("사용할 이름을 입력해주세요.")
    }
    else if(checkBlank(userPW)!=true){
        alert("사용할 비밀번호를 입력해주세요.")
    }
    else if(checkBlank(confirmPW)!=true){
        alert("비밀번호를 확인해주세요.")
    }
    else{
        const formData = new FormData();
        fetch('/register/',{ // member/register/ -> /regiseter/ 수정
            method:"POST",
            headers:{
                'Content-Type': 'application/JSON',
                'X-CSRFToken': csrfToken // 수정
            },
            body: JSON.stringify({
                username: userName,
                password: userPW,
                email: userID
            })
        })
        .then(response => {
    if (response.status === 201) {
        return response.json();
    } else if (response.status === 403) {
        // Handle CSRF token length error 수정
        alert("CSRF 토큰의 길이가 잘못되었습니다.");
    } else if (response.status === 401) {
        alert("잘못된 아이디 혹은 비밀번호를 입력하셨습니다.");
    } else {
        throw new Error('에러 발생');
    }
})
.catch(error => {
    console.log(error);
})
.then(data => {
    if (data && data.message === '로그인 성공') {
        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('expired_in', data.expired_in);
        alert("로그인 성공!");
        window.location.href = '../html/login.html';
    } else {
        console.error('로그인 실패 또는 잘못된 응답');
    }
});

    }
}