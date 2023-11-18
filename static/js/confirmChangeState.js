function confirmChangeState(id, text) {
  event.preventDefault(); // Prevent the default link behavior

  const btnUpdateState = document.getElementById(id);

  if (confirm(text)) {
    window.location.href = btnUpdateState.href;
    }
}