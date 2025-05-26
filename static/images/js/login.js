function togglePassword() {
    const passwordInput = document.getElementById("password");
    const toggleButton = event.currentTarget;

    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        toggleButton.textContent = "Hide";
    } else {
        passwordInput.type = "password";
        toggleButton.textContent = "Show";
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("loginForm");
    form.addEventListener("submit", function (e) {
        e.preventDefault();

        const formData = new FormData(form);
        const spinnerOverlay = document.getElementById("spinnerOverlay");
        spinnerOverlay.style.display = "block";

        fetch("/login_view/", {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: formData,
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.success) {

            }})
            .catch((error) => {
                toastr.error("Error:", error);
            })
            .finally(() => {
                spinnerOverlay.style.display = "none";
            });
    });
});
