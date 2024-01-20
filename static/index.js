document.addEventListener('DOMContentLoaded', function() {

    let form = document.getElementById("file-form");
    form.addEventListener('submit', () => {
        event.preventDefault();

        let filed = document.getElementById("file-input");
        const file = filed.files[0];
        console.log(file)

        showLoader();

        const formData = new FormData();
        formData.append("file", file);

        fetch("http://127.0.0.1:5000/verify", {
            method: 'POST',
            body: formData,
            // headers: {
            //     'Content-Type': 'multipart/form-data'
            // }

        })
            .then(response => response.blob())
            .then(blob => {
                hideLoader();

                document.querySelector('#loader-text').innerHTML =
                    "Your Verified email File will start downloading Automatically";

                const link = document.createElement('a');
                link.href = URL.createObjectURL(blob);
                link.download = 'processed_file.txt';
                document.body.appendChild(link);

                link.click();
                document.body.removeChild(link);

            })
            .catch(error => {
                console.error(error);
            });

    })

    function showLoader() {
        document.querySelector('#loader').style.display = 'flex';
    }

    function hideLoader() {
        document.querySelector('#loader').style.display = 'none';
    }


    let loginButton = document.querySelector('#login-button');
    loginButton.addEventListener('click', () => {
        event.preventDefault();
        document.getElementById('signup-segment').style.display = 'none';
        document.getElementById('login-segment').style.display = 'block';
    });

    let cancelLoginButton = document.querySelector('#cancel-login');
    cancelLoginButton.addEventListener("click", () => {
        document.getElementById('login-segment').style.display = 'none';
    });

    let cancelSignupButton = document.querySelector('#cancel-signup');
    cancelSignupButton.addEventListener("click", () => {
        document.getElementById('signup-segment').style.display = 'none';
    });

    let mainSignupButton = document.querySelector('#straight-signup');
    mainSignupButton.addEventListener("click", () => {
        document.getElementById('signup-segment').style.display = 'block';
    });

    let getStartedButton = document.querySelector('#get-started');
    getStartedButton.addEventListener("click", () => {
        document.getElementById('signup-segment').style.display = 'block';
    });

    let mainLoginButton = document.querySelector('#straight-login');
    mainLoginButton.addEventListener("click", () => {
        document.getElementById('login-segment').style.display = 'block';
    });



    const signup = document.getElementById('submit-signup');
    signup.addEventListener('click', () => {

        event.preventDefault()
        const username = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const number = document.getElementById('phone-number').value;
        const password = document.getElementById('password').value;

        fetch('http://localhost:5000/signup', {
            method: 'POST',
            body: JSON.stringify({username, email, number, password}),
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then(res => res.json())
            .then(resObj => {
                console.log(resObj)

            })
            .catch(error => {
                console.log(error);
            })

    })






});
