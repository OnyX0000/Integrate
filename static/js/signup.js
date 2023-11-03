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
        .then(response=>{
            if(response.statur==200){
                return response.json;
            }
            else if(response.status==400){
                alert("이미 가입된 이메일 입니다.");
            }else{
                throw new Error('에러 발생');
            }
        }).catch((error)=>console.log(error))
        .then((data)=>{
            if(data.message=='회원가입 성공'){
                alert('회원가입이 완료되었습니다.')
                window.location.href='../html/login.html'
            }
        })
    }
}