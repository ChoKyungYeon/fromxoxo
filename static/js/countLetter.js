document.addEventListener('DOMContentLoaded', function() {
    // Function to restrict input to English and Korean characters
    function restrictInput(event) {
    var regex = /^[a-zA-Zㄱ-ㅎㅏ-ㅣ가-힣0-9]*$/;
    var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
    if (!regex.test(key)) {
        event.preventDefault();
        return false;
        }
    }

    // Function to count characters
    function countCharacters() {
        var text = document.getElementById('field-wordanswer').value; // Get the value of the input
        var totalCount = (text.match(/[ㄱ-ㅎㅏ-ㅣ가-힣a-zA-Z0-9]/g) || []).length;

        // Update the counts on the page
        document.getElementById('total-count').textContent = '현재 ' + totalCount + '글자';
    }

    // Get the input element by ID
    var answerInput = document.getElementById('field-wordanswer');

    // Add event listeners for the input and keypress events
    answerInput.addEventListener('input', countCharacters);
    answerInput.addEventListener('keypress', restrictInput);

    // Call countCharacters on page load to handle pre-filled values
    countCharacters();
});