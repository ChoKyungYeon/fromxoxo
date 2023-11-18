document.getElementById('form-create-phonenumber').addEventListener('submit', function(event){
    const phonenumber = this.phonenumber.value;
    const confirmation = confirm(`전화번호 ${phonenumber} 로 인증번호를 발송합니다.`);
    if (!confirmation) {
        event.preventDefault();
    }
});

