// ===============================
// PASSWORD SHOW / HIDE
// ===============================

const eyeIcon = document.querySelector(".eye-icon");
const passwordInput = document.querySelector('input[type="password"]');

if (eyeIcon && passwordInput) {

    eyeIcon.addEventListener("click", () => {

        if (passwordInput.type === "password") {

            passwordInput.type = "text";

            eyeIcon.classList.remove("fa-eye");

            eyeIcon.classList.add("fa-eye-slash");

        } else {

            passwordInput.type = "password";

            eyeIcon.classList.remove("fa-eye-slash");

            eyeIcon.classList.add("fa-eye");

        }

    });

}

// ===============================
// TAB SWITCHING
// ===============================

const tabs = document.querySelectorAll(".tab");

tabs.forEach((tab) => {

    tab.addEventListener("click", () => {

        tabs.forEach((btn) => {
            btn.classList.remove("active");
        });

        tab.classList.add("active");

    });

});

// ===============================
// INPUT FOCUS EFFECT
// ===============================

const inputBoxes = document.querySelectorAll(".input-box");

inputBoxes.forEach((box) => {

    const input = box.querySelector("input, select");

    input.addEventListener("focus", () => {

        box.style.borderColor = "#1f64ff";
        box.style.boxShadow = "0 0 10px rgba(31,100,255,0.2)";

    });

    input.addEventListener("blur", () => {

        box.style.borderColor = "#e2e6f0";
        box.style.boxShadow = "none";

    });

});

// ===============================
// BUTTON CLICK ANIMATION
// ===============================

const loginBtn = document.querySelector(".login-btn");

if (loginBtn) {

    loginBtn.addEventListener("click", () => {

        loginBtn.innerHTML = "Please Wait...";

        setTimeout(() => {

            loginBtn.innerHTML = "Login";

        }, 2000);

    });

}