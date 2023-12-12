document.addEventListener('DOMContentLoaded', function() {

    let form = document.getElementById("form");
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

    function handleResponse(data) {
        document.getElementById('output').innerHTML = data.processed_file;
}

    function showLoader() {
        document.querySelector('#loader').style.display = 'flex';
    }

    function hideLoader() {
        document.querySelector('#loader').style.display = 'none';
    }

});
