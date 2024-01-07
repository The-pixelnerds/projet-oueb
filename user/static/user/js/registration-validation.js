document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('registration-form');
    var button = document.getElementById('button');
    var validationMessage = document.getElementById('validation-message');

    function updateButtonState() {
        var Password1 = form.querySelector('#id_password1').value;
        var Password2 = form.querySelector('#id_password2').value;
        var allFilled = Array.from(form.querySelectorAll('.input-area')).every(function(input) {
            return input.value.trim() !== '';
        });
        var isValid1 = Password1.length >= 8;
        var isValid2 = Password1 === Password2;

        if (allFilled && isValid1 && isValid2) {
            button.classList.remove('disabled-button');
            button.disabled = false;
            validationMessage.textContent = 'form seems correct';
            validationMessage.classList.remove('invalid');
            validationMessage.classList.add('valid');
        } else {
            button.classList.add('disabled-button');
            button.disabled = true;
            validationMessage.textContent = 'form is incomplete or invalid';
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