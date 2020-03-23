function tryRes(foodname){

    $.ajax({
        type: 'GET',
        url: 'http://localhost:8000/api/food/'+foodname,
        async: false,
        error: function(xhr, status, error){
            alert('등록되지 않은 메뉴입니다.');
            flag = false;
        },
        success: function(xhr){
            flag = true;
        },
    });
    return flag;
}

function foodCheck(){
       var res = tryRes(document.getElementById('foodname').value);
       return res;
}

function goFood(){
    if(tryRes(document.getElementById('gowithfoodname').value)){
        redirect_url = "http://localhost:8000/food/menu/" + document.getElementById('gowithfoodname').value;
        window.location.href = redirect_url;
    }
}