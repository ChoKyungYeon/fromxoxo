function copyLetterUrl(text) {
    // Get the URL from the data-url attribute of the touched button
    var url = event.currentTarget.getAttribute('data-url');  // Using the event object to get the touched element

    // Create a new temporary input element
    var input = document.createElement('input');
    input.setAttribute('value', url);
    document.body.appendChild(input);

    // Select and copy the URL
    input.select();
    document.execCommand('copy');
    document.body.removeChild(input);

    // Show an alert to confirm that the URL has been copied
    alert(text);
}