document.getElementById('form-create-phonenumber').addEventListener('submit', function(event){
    const Number = this.number.value;
    const confirmation = confirm(`전화번호 ${Number} 로 인증번호를 발송합니다.`);
    if (!confirmation) {
        event.preventDefault();
    }
});

