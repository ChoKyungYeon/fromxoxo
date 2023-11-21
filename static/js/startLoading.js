function showLoading(counter, event, alert) {
  event.preventDefault(); // Prevent the default link behavior

  const saveButton = document.getElementById('btn-loading' + counter);
  const loadingIndicator = document.getElementById('loading');

  if (alert) {
    if (confirm(alert)) {
      loadingIndicator.style.display = 'block';

      // Delay the navigation
      setTimeout(function() {
        window.location.href = saveButton.href;
      }, 1000);
    }
  } else {
    loadingIndicator.style.display = 'block';

    setTimeout(function() {
        window.location.href = saveButton.href;
      }, 1000);
  }
}