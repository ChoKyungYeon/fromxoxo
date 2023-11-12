
function showGuide() {
    var element = document.getElementById("frame-guide");
    element.style.display = "flex";
    element.style.opacity = 0;
    setTimeout(function() {
        element.style.transition = 'opacity 0.2s ease-in-out';
        element.style.opacity = 1;
    }, 10);
}

function closeGuide() {
    var element = document.getElementById("frame-guide");
    element.style.transition = 'opacity 0.4s ease-in-out';
    element.style.opacity = 0;
    setTimeout(function() {
        element.style.display = "none";
    }, 400);
}