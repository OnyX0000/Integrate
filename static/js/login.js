function login() {
    const userID = document.getElementById('login-id').value;
    const userPW = document.getElementById('login-pw').value;

    if (userID === '' || userPW === '') {
        alert("아이디와 비밀번호를 모두 입력해주세요.");
    } else {
        const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

        fetch('/login/', { // /api/login/
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
                // 'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({
                email: userID,
                password: userPW, // "둘 다 따옴표 안에 수정"
            }),
        })
        .then(response => {
            if (response.status === 200) {
                return response.json();
            } else if (response.status === 401) {
                alert(data.error); 
                console.log('Login Fail')
            } else {
                throw new Error('ERROR');
            }
        })
        .then(data => {
            console.log(data)
            if (data && data.access_token) {
                console.log("Login Success");
                localStorage.setItem('access_token', data.access_token);
                localStorage.setItem('expired_in', data.access_token_expires);
                alert("Login SUCCESS !");
                window.location.href = '/home/';
            } else {
                console.log("Login Fail or Data error");
            }
        })
        .catch(error => {
            console.log(error);
        });
    }
}