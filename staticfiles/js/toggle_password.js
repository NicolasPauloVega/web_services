document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".toggle-password").forEach(function (eyeIcon) {
        eyeIcon.addEventListener("click", function () {
            let target = document.getElementById(this.getAttribute("data-target"));
            if (target.type === "password") {
                target.type = "text";
                this.innerHTML = '<i class="fa-solid fa-eye-slash"></i>'; // Ojo cerrado
            } else {
                target.type = "password";
                this.innerHTML = '<i class="fa-solid fa-eye-slash"></i>'; // Ojo abierto
            }
        });
    });
});