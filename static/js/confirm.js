function confirmAction(event, text, formId) {
    if (confirm(text)) {
        document.getElementById(formId).submit();
    } else {
        event.preventDefault();
    }
}
function confirmDelete(id, text) {
    if (confirm(text)) {
        document.getElementById(id).submit();
    }
}

function confirmChangeState(id, text) {
  event.preventDefault(); // Prevent the default link behavior

  const btnUpdateState = document.getElementById(id);

  if (confirm(text)) {
    window.location.href = btnUpdateState.href;
    }
}
document.getElementById('form-create-verification').addEventListener('submit', function(event){
    const phonenumber = this.phonenumber.value;
    const confirmation = confirm(`전화번호 ${phonenumber} 로 인증번호를 발송합니다.`);
    if (!confirmation) {
        event.preventDefault();
    }
});

