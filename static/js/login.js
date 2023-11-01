function login() {
    const userID = document.getElementById('login-id').value;
    const userPW = document.getElementById('login-pw').value;

    if (userID === '' || userPW === '') {
        alert("아이디와 비밀번호를 모두 입력해주세요.");
    } else {
        // CSRF 토큰을 직접 가져오기
        const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

        fetch('/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({
                email: userID,
                password: userPW,
            }),
        })
        .then(response => {
            if (response.status === 200) {
                return response.json();
            } else if (response.status === 401) {
                alert("잘못된 아이디 혹은 비밀번호를 입력하셨습니다.");
                throw new Error('로그인 실패');
            } else {
                throw new Error('에러 발생');
            }
        })
        .then(data => {
            if (data && data.token) {
                // 토큰을 localStorage에 저장
                localStorage.setItem('access_token', data.token);
                localStorage.setItem('expired_in', data.expired_in);
                alert("로그인 성공!");
                window.location.href = '../html/home.html';
            } else {
                console.log("로그인 실패 또는 데이터 오류");
            }
        })
        .catch(error => {
            console.log(error);
        });
    }
}