document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('login-form');
    var button = document.getElementById('button');
    var validationMessage = document.getElementById('validation-message');

    function updateButtonState() {
        var Username = form.querySelector('#id_username').value;
        var Password = form.querySelector('#id_password').value;
        var allFilled = Array.from(form.querySelectorAll('.input-area')).every(function(input) {
            return input.value.trim() !== '';
        });
        var isValid = Password.length >= 8;

        if (allFilled && isValid) {
            button.classList.remove('disabled-button');
            button.disabled = false;
            validationMessage.textContent = 'form seems correct';
            validationMessage.classList.remove('invalid');
            validationMessage.classList.add('valid');
        } else {
            button.classList.add('disabled-button');
            button.disabled = true;
            validationMessage.textContent = 'username and password are required';
            validationMessage.classList.remove('valid');
            validationMessage.classList.add('invalid');
        }

        validationMessage.style.display = 'block';
    }

    // Update the button state when the page loads
    updateButtonState();

    // Update the button state whenever any input changes
    Array.from(form.querySelectorAll('.input-area')).forEach(function(input) {
        input.addEventListener('input', updateButtonState);
    });
});