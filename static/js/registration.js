document.addEventListener("DOMContentLoaded", function () {
    // === Elements ===
    const form = document.getElementById("voterForm");

    const userPhotoInput = document.getElementById("userPhotoUpload");
    const userPhotoPreview = document.getElementById("userPhotoPreview");

    const photoDropArea = document.getElementById("drop-area");
    const clickToBrowse = document.getElementById("clickToBrowse");

    // === Constants ===
    const MAX_FILE_SIZE = 2 * 1024 * 1024; // 2MB

    // === Utility Functions ===
    function isEmailValid(email) {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(email);
    }

    function showImagePreview(fileInput, previewImg) {
        const file = fileInput.files[0];
        if (!file) return;

        if (!file.type.startsWith("image/")) {
            toastr.error("Please upload a valid image.");
            fileInput.value = "";
            return;
        }

        if (file.size > MAX_FILE_SIZE) {
            toastr.error("File size should be less than 2MB.");
            fileInput.value = "";
            return;
        }

        const reader = new FileReader();
        reader.onload = function (e) {
            previewImg.src = e.target.result;
            previewImg.style.display = "block";
        };
        reader.readAsDataURL(file);
    }

    // === Click to Browse ===
    if (clickToBrowse) {
        clickToBrowse.addEventListener("click", () => userPhotoInput.click());
    }

    // === Image Preview on Change ===
    userPhotoInput.addEventListener("change", () => showImagePreview(userPhotoInput, userPhotoPreview));

    // === Drag and Drop ===
    if (photoDropArea) {
        photoDropArea.addEventListener("dragover", (e) => {
            e.preventDefault();
            photoDropArea.classList.add("border-primary");
        });

        photoDropArea.addEventListener("dragleave", () => {
            photoDropArea.classList.remove("border-primary");
        });

        photoDropArea.addEventListener("drop", (e) => {
            e.preventDefault();
            photoDropArea.classList.remove("border-primary");

            const file = e.dataTransfer.files[0];
            if (file) {
                userPhotoInput.files = e.dataTransfer.files;
                showImagePreview(userPhotoInput, userPhotoPreview);
            }
        });
    }

    // === Form Validation ===
    form.addEventListener("submit", function (e) {
        e.preventDefault();

        // Clear previous error messages
        const errorElements = form.querySelectorAll(".error-message");
        errorElements.forEach((el) => (el.textContent = ""));
        const inputs = form.querySelectorAll("input");
        inputs.forEach((input) => input.classList.remove("is-invalid"));

        const firstName = document.getElementById("firstName");
        const middleName = document.getElementById("middleName");
        const lastName = document.getElementById("lastName");
        const username = document.getElementById("username");
        const email = document.getElementById("email");
        const dob = document.getElementById("dob");

        let isValid = true;

        function showError(input, message) {
            const errorSpan = input.parentElement.querySelector(".error-message");
            if (errorSpan) {
                errorSpan.textContent = message;
                input.classList.add("is-invalid");
                isValid = false;
            }
        }

        if (!firstName.value.trim()) showError(firstName, "First name is required.");
        if (!lastName.value.trim()) showError(lastName, "Last name is required.");
        if (!username.value.trim() || username.value.trim().length < 3)
            showError(username, "Username must be at least 3 characters.");
        if (!email.value.trim() || !isEmailValid(email.value.trim()))
            showError(email, "A valid email is required.");
        

        if (!userPhotoInput.files.length) showError(userPhotoInput, "User photo is required.");

        if (!isValid) return;

        const spinnerOverlay = document.getElementById("spinnerOverlay");
        spinnerOverlay.style.display = "block";

        const formData = new FormData();
        formData.append("csrfmiddlewaretoken", document.querySelector("[name=csrfmiddlewaretoken]").value);
        formData.append("firstName", firstName.value.trim());
        formData.append("middleName", middleName.value.trim());
        formData.append("lastName", lastName.value.trim());
        formData.append("username", username.value.trim());
        formData.append("email", email.value.trim());
        formData.append("userPhotoUpload", userPhotoInput.files[0]);

        fetch("/user-registration/", {
            method: "POST",
            body: formData,
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.status === "success") {
                    toastr.success(data.message);
                    setTimeout(() => {
                        window.location.href = data.redirect_url;
                    }, 2000); // Delay to show toast
                } else {
                    toastr.error(data.message || "An error occurred.");
                }
            })
            .catch((error) => {
                toastr.error("Something went wrong.");
                console.error("Error:", error);
            })
            .finally(() => {
                spinnerOverlay.style.display = "none";
            });
    });
});
