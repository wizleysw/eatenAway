var regExp = /^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{2,3}$/i;

var check = function() {
  if (document.getElementById('password').value == document.getElementById('password2').value) {
		document.getElementById('message').style.color = 'green';
		document.getElementById('message').innerHTML = '패스워드가 일치합니다.';
  } else {
	document.getElementById('message').style.color = 'red';
	document.getElementById('message').innerHTML = '패스워드가 올바르지 않습니다.';
  }
 }

function checkRecap(){
	var v = grecaptcha.getResponse();
	if(v.length==0){
		alert('로봇이 아닌지 판단하기 위한 캡차를 진행해주시기 바랍니다.');
		return false;
	}
	else{
		return true;
	}
}

function checkUsername(){
	id = document.getElementById('username').value;
	if(id.length<1){
		alert('아이디를 입력하세요.');
		return false;
	}
	else{
		$.ajax({
		    type: 'GET',
		    url: 'http://localhost:8000/api/accounts/verify/' + id,
    	    error: function(xhr, status, error){
    	        alert("이미 사용중인 아이디입니다.");
    		    return false;
    	    },
    	    success: function(xhr, status){
    	        alert("사용가능한 아이디입니다.");
        		return true;
        	},
	    });
	}
}

function checkEmail(){
	email = document.getElementById('email').value;
	var csrf_token = $('[name=csrfmiddlewaretoken]').val();
   	if (regExp.test(email)){
   		$.ajax({
    	    type: 'POST',
    	    url: 'http://localhost:8000/api/accounts/verify/',
    	    data : {
        	    email: email,
        	    csrfmiddlewaretoken: csrf_token,
        	},
    	    error: function(xhr, status, error){
    	        alert("이미 사용중인 이메일입니다.")
    		    return false;
    	    },
    	    success: function(xhr){
        		alert("사용 가능한 이메일입니다.");
        		return true;
        	},
	    });
	}
	else{
		alert('잘못된 이메일 형식입니다');
	};
}

function lastCheck(){
	id = document.getElementById('username').value;
	if(id.length<1){
		alert('아이디를 다시 확인해주세요.');
		return false;
	}

	if(document.getElementById('password').value != document.getElementById('password2').value){
		alert('패스워드를 다시 확인해주세요.');
		return false;
	}

	if(document.getElementById('password').value.length < 8){
		alert('패스워드 최소길이는 8글자입니다.');
		return false;
	}

	email = document.getElementById('email').value;
	if(!(regExp.test(email))){
		alert('이메일을 다시 확인해주세요.');
		return false;
	}

	if(!checkRecap()){
		return false;
	}

    function tryRes(){
	    var queryString = $("form[name=registerForm]").serialize();

        $.ajax({
            type: 'POST',
            url: 'http://localhost:8000/api/accounts/',
            data : queryString,
            dataType : 'json',
            async: false,
            success: function(xhr, status, success){
                alert('회원가입 신청이 완료되었습니다.');
                flag = true;
            },
            error: function(xhr, status, error){
                alert('정보를 다시 확인해주세요.');
                grecaptcha.reset();
                flag = false;
            },
        });

        return flag;
       }

       var res = tryRes();
       return res;
}