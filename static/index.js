document.addEventListener('DOMContentLoaded', function() {
    // Your JavaScript code here


    let form = document.getElementById("form");
    form.addEventListener('submit', () => {
        event.preventDefault();

        let file = document.getElementById("file-input");
        const filed = file.files[0];

        showLoader();

       setTimeout(() => {
        const formData = new FormData();
        formData.append('file', filed);  // Assuming filed is a valid file object

        fetch("http://127.0.0.1:5000/start", {

            method: 'POST',
            body: formData,
            headers: {
                'Content-Type': 'application/json; charset=UTF-8'
            }

        })
            .then(response => response.blob())
            .then(blob => {
                hideLoader();
                document.querySelector('#loader-text').innerHTML = "Your Verified email File is ready for download";

                const link = document.createElement('a');
                link.href = URL.createObjectURL(blob);
                link.download = 'processed_file.txt';
                document.body.appendChild(link);

                link.click();
                document.body.removeChild(link);

            }).catch(error => {
                console.error(error);
            });

    }, 3000);

    })

    // let downloadButton = document.querySelector("#download");
    // downloadButton.addEventListener('submit', () => {
    //     event.preventDefault();
    //     console.log("Downlaod Button was Click")
    //     document.querySelector('#loader-text').innerHTML = "";
    //
    //     showLoader();
    //     result.
    //
    //
    // });

    function showLoader() {
        document.querySelector('#loader').style.display = 'flex';
    }

    function hideLoader() {
        document.querySelector('#loader').style.display = 'none';
    }

});
