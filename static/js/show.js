
function showZoom(counter) {
    var element = document.getElementById("frame-zoom"+ counter);
    element.style.display = "flex";
    element.style.opacity = 0;
    setTimeout(function() {
        element.style.transition = 'opacity 0.2s ease-in-out';
        element.style.opacity = 1;
    }, 10);
}


function closeZoom(counter) {
    var element = document.getElementById("frame-zoom"+ counter);
    element.style.transition = 'opacity 0.4s ease-in-out';
    element.style.opacity = 0;
    setTimeout(function() {
        element.style.display = "none";
    }, 400);
}


function reloadZoom(counter) {
    var element = document.getElementById("frame-zoom"+ counter);
    element.style.display = "flex";
    element.style.opacity = 0;

    setTimeout(function() {
        element.style.transition = 'opacity 0.2s ease-in-out';
        element.style.opacity = 1;
    }, 10);

    location.reload();
}

function showSlide(slideNumber) {
    for (let i = 1; i <= 6; i++) {
        const btn = document.querySelector(`#btn-slide${i}`);
        const slide = document.querySelector(`#slide${i}`);

        if (i === slideNumber) {
            btn.classList.add('btn-touched');
            btn.classList.remove('btn-untouched');
            slide.style.display = 'block';
        } else {
            btn.classList.add('btn-untouched');
            btn.classList.remove('btn-touched');
            slide.style.display = 'none';
        }
    }
}
showSlide(1);



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