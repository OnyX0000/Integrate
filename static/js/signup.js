function checkBlank(word){
    if(word == '') return false;
    return true;
}
function signUp(){
    const userName = document.getElementById('input-name').value;
    const userID = document.getElementById('input-id').value;
    const userPW = document.getElementById('input-pw').value;
    const confirmPW = document.getElementById('input-pw-cf').value;

    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

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
        fetch('/api/register/',{
            method:"POST",
            headers:{
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                username: userName,
                password: userPW,
                email: userID
            })
        })
        .then(response=>{
            if(response.status==200){
                return response.json();
            }
            else if(response.status==400){
                alert("Already Registerd Email.");
            }else{
                throw new Error('에러 발생');
            }
        }).catch((error)=>console.log(error))
        .then((data)=>{
            console.log(data);
            if(data.message=='Register Success'){
                alert('Register Success.')
                window.location.href='../html/login.html'
            } else if (data.error === 'Already Registered Email') {
                alert('Already Registered Email.');
            }
        });
    }
}