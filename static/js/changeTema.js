document.addEventListener('DOMContentLoaded', function() {
    var bodyTema = document.getElementById('bodyTema');
    var temaField = document.getElementById('temaField');

    temaField.addEventListener('change', function() {
        // Define a function to update the tema classes
        function updateTemaClasses(element) {
            // Remove all tema-related classes
            element.classList.remove('tema-blue', 'tema-pink', 'tema-gray', 'tema-yellow', 'tema-green', 'tema-purple');

            // Add the selected tema class
            var selectedTema = 'tema-' + temaField.value;
            element.classList.add(selectedTema);
        }

        // Update classes for both elements
        updateTemaClasses(bodyTema);
    });
});
