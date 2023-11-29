 function alertAuthentication(element) {
    alert('로그인이 필요한 서비스입니다.');
    window.location.href = element.getAttribute('href');
}

function alertMessage(text) {
    alert(text);
}