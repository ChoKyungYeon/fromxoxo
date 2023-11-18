function confirmAction(id, text) {
    if (confirm(text)) {
        document.getElementById(id).submit();
    }
}