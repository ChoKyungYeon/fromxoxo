function copyLetterUrl() {
    // Get the URL from the data-url attribute of the clicked button
    var url = event.currentTarget.getAttribute('data-url');  // Using the event object to get the clicked element

    // Create a new temporary input element
    var input = document.createElement('input');
    input.setAttribute('value', url);
    document.body.appendChild(input);

    // Select and copy the URL
    input.select();
    document.execCommand('copy');
    document.body.removeChild(input);

    // Show an alert to confirm that the URL has been copied
    alert('편지 링크가 복사되었습니다! 자유롭게 공유해 보세요');
}