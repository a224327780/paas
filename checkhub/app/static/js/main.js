document.addEventListener('DOMContentLoaded', function() {
    console.log('CheckHub initialized');
});

window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = 'none';
    }
};
