document.addEventListener('DOMContentLoaded', () => {
    const signupButton = document.getElementById('signup-btn');
    const signupForm = document.getElementById('signup-form');
    const submitSignupFormButton = document.getElementById('submit-signup-btn');

    signupButton.addEventListener('click', () => {
        signupForm.style.display = 'block';
    });

    submitSignupFormButton.addEventListener('click', () => {
        const username = signupForm.querySelector('input[name="username"]').value;
        const password = signupForm.querySelector('input[name="password"]').value;
        const email = signupForm.querySelector('input[name="email"]').value;
        const first_name = signupForm.querySelector('input[name="first_name"]').value;
        const last_name = signupForm.querySelector('input[name="last_name"]').value;

        axios.post('http://localhost:8000/users/', {
            username: username,
            password: password,
            email: email,
            first_name: first_name,
            last_name: last_name
        }).then(response => {
            console.log(response.data);
        }).catch(error => {
            console.log(error);
        });
    });
});
