function setInitialColor(checkbox) {
    if(checkbox.checked) {
        checkbox.parentNode.style.backgroundColor = 'var(--black)';
        checkbox.parentNode.style.color = 'var(--white)';
    } else {
        checkbox.parentNode.style.backgroundColor = 'var(--white)';
        checkbox.parentNode.style.color = 'var(--gray)';
    }
}

document.querySelectorAll('.selectmultiple input[type="checkbox"]').forEach(function(checkbox){
    // Set the initial color
    setInitialColor(checkbox);

    // Add the event listener for future changes
    checkbox.addEventListener('change', function() {
        setInitialColor(checkbox);
    });
});
