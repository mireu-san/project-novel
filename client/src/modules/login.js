document.addEventListener('DOMContentLoaded', () => {
    const loginButton = document.getElementById('login-btn');
    const loginForm = document.getElementById('login-form');
    const submitLoginFormButton = document.getElementById('submit-login-btn');

    loginButton.addEventListener('click', () => {
        loginForm.style.display = 'block';
    });

    submitLoginFormButton.addEventListener('click', (e) => {
        e.preventDefault();

        const username = loginForm.querySelector('input[name="username"]').value;
        const password = loginForm.querySelector('input[name="password"]').value;

        axios.post('http://localhost:8000/api/token/', {
            username: username,
            password: password
        }).then(response => {
            console.log(response.data);
        }).catch(error => {
            console.log(error);
        });
    });
});
