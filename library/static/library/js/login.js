document.addEventListener("DOMContentLoaded", function() {
    const passwordRegex = /^(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$/;
    const emailRegex = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const signInButton = document.getElementById('sign_in_btn');
    
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

    // Validate all form fields
    function validateForm() {
        const emailValid = validateInput(emailInput, emailRegex);
        const passwordValid = validateInput(passwordInput, passwordRegex);

        signInButton.disabled = !(emailValid && passwordValid);
    }

    emailInput.addEventListener('blur', function() {
        validateInput(emailInput, emailRegex);
        validateForm();
    });

    passwordInput.addEventListener('blur', function() {
        validateInput(passwordInput, passwordRegex);
        validateForm();
    });

    validateForm();
});
