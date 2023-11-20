
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
