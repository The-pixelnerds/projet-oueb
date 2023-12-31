document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('password-change-form');
    var button = document.getElementById('button');
    var validationMessage = document.getElementById('validation-message');

    function updateButtonState() {
        var oldPassword = form.querySelector('#id_old_password').value;
        var newPassword1 = form.querySelector('#id_new_password1').value;
        var newPassword2 = form.querySelector('#id_new_password2').value;
        var allFilled = Array.from(form.querySelectorAll('.input-area')).every(function(input) {
            return input.value.trim() !== '';
        });
        var isValid1 = newPassword1.length >= 8;
        var isValid2 = newPassword1 === newPassword2;
        var isValid3 = newPassword1 !== oldPassword;

        if (allFilled && isValid1 && isValid2 && isValid3) {
            button.classList.remove('disabled-button');
            button.disabled = false;
            validationMessage.textContent = 'Password is valid';
            validationMessage.classList.remove('invalid');
            validationMessage.classList.add('valid');
        } else {
            button.classList.add('disabled-button');
            button.disabled = true;
            validationMessage.textContent = 'Password is not valid';
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