// Get the popup
var popup = document.getElementById('reviewPopup');

// Get the button that opens the popup
var btn = document.getElementById('reviewBtn');

// Get the <span> element that closes the popup
var span = document.getElementsByClassName('close')[0];

// When the user clicks the button, open the popup
btn.onclick = function() {
    popup.style.display = 'block';
}

// When the user clicks on <span> (x), close the popup
span.onclick = function() {
    popup.style.display = 'none';
}

// When the user clicks anywhere outside of the popup, close it
window.onclick = function(event) {
    if (event.target == popup) {
        popup.style.display = 'none';
    }
}

// Form submission handling
document.getElementById('reviewForm').addEventListener('submit', function(event) {
    event.preventDefault();
    alert('Review Submitted!'); // Replace this with actual form submission logic
    popup.style.display = 'none';
});