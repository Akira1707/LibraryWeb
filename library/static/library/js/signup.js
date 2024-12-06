document.addEventListener("DOMContentLoaded", function() {
    const phoneRegex = /^(?:\+?\d{1,3})?[-.\s]?\(?\d{2,3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$/;
    const passwordRegex = /^(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$/;
    const emailRegex = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

    const phoneInput = document.getElementById('phone');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const passwordRepeatInput = document.getElementById('password-repeat');
    const signUpButton = document.getElementById('sign_up_btn');
    
    // Function to check and show error on the input field
    function validateInput(input, regex) {
        const isValid = regex.test(input.value);
        const helperText = input.parentNode.querySelector('.helper-text');
        const errorMessage = input.getAttribute('data-error');

        if (isValid) {
            input.classList.remove('invalid');
            input.classList.add('valid');
            input.setCustomValidity('');
            if (helperText) helperText.textContent = ''; 
        } else {
            input.classList.remove('valid');
            input.classList.add('invalid');
            input.setCustomValidity(errorMessage); 
            if (helperText) helperText.textContent = errorMessage; 
        }
        return isValid;
    }

    function validateForm() {
        const phoneValid = validateInput(phoneInput, phoneRegex);
        const emailValid = validateInput(emailInput, emailRegex);
        const passwordValid = validateInput(passwordInput, passwordRegex);
        const passwordsMatch = passwordInput.value === passwordRepeatInput.value;

        if (passwordsMatch) {
            passwordRepeatInput.classList.remove('invalid');
            passwordRepeatInput.classList.add('valid');
            passwordRepeatInput.setCustomValidity('');
            const helperText = passwordRepeatInput.parentNode.querySelector('.helper-text');
            if (helperText) helperText.textContent = ''; 
        } else {
            passwordRepeatInput.classList.remove('valid');
            passwordRepeatInput.classList.add('invalid');
            passwordRepeatInput.setCustomValidity('Passwords do not match.');
            const helperText = passwordRepeatInput.parentNode.querySelector('.helper-text');
            if (helperText) helperText.textContent = 'Passwords do not match.'; 
        }

        signUpButton.disabled = !(phoneValid && emailValid && passwordValid && passwordsMatch);
    }

    phoneInput.addEventListener('blur', function() {
        validateInput(phoneInput, phoneRegex);
        validateForm();
    });

    emailInput.addEventListener('blur', function() {
        validateInput(emailInput, emailRegex);
        validateForm();
    });

    passwordInput.addEventListener('blur', function() {
        validateInput(passwordInput, passwordRegex);
        validateForm();
    });

    passwordRepeatInput.addEventListener('blur', function() {
        if (passwordRepeatInput.value !== passwordInput.value) {
            passwordRepeatInput.classList.remove('valid');
            passwordRepeatInput.classList.add('invalid');
            passwordRepeatInput.setCustomValidity('Passwords do not match.');
            const helperText = passwordRepeatInput.parentNode.querySelector('.helper-text');
            if (helperText) helperText.textContent = 'Passwords do not match.'; 
        } else {
            passwordRepeatInput.classList.remove('invalid');
            passwordRepeatInput.classList.add('valid');
            passwordRepeatInput.setCustomValidity('');
            const helperText = passwordRepeatInput.parentNode.querySelector('.helper-text');
            if (helperText) helperText.textContent = ''; 
        }
        validateForm();
    });

    validateForm();
});
