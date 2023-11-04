function login() {
    const userID = document.getElementById('login-id').value;
    const userPW = document.getElementById('login-pw').value;

    if (userID === '' || userPW === '') {
        alert("아이디와 비밀번호를 모두 입력해주세요.");
    } else {
        const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

        fetch('/api/login/', {
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
                alert("Wrong Email or Password");
                console.log('Login Fail')
            } else {
                throw new Error('new ERROR');
            }
        })
        .then(data => {
            console.log(data)
            if (data && data.access_token) {
                localStorage.setItem('access_token', data.access_token);
                localStorage.setItem('expired_in', data.access_token_expires);
                alert("Login Success");
                window.location.href = '/home/';
            } else {
                console.log("Login Fail or Data Error");
            }
        })
        .catch(error => {
            console.log(error);
        });
    }
}