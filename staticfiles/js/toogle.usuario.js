function togglePassword() {
    let passwordField = document.getElementById("password");
    let toggleIcon = document.getElementById("toggleIcon");
    if (passwordField.type === "password") {
        passwordField.type = "text";
        toggleIcon.classList.replace("bi-eye", "bi-eye-slash");
    } else {
        passwordField.type = "password";
        toggleIcon.classList.replace("bi-eye-slash", "bi-eye");
    }
}