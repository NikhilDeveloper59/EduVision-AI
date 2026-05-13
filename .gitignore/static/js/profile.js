// =========================
// THEME TOGGLE
// =========================

function toggleTheme(){

    document.body.classList.toggle("light-mode");

    // SAVE THEME

    if(document.body.classList.contains("light-mode")){

        localStorage.setItem("theme", "light");
    }

    else{

        localStorage.setItem("theme", "dark");
    }
}

// =========================
// LOAD SAVED THEME
// =========================

document.addEventListener("DOMContentLoaded", function(){

    const savedTheme =
    localStorage.getItem("theme");

    if(savedTheme === "light"){

        document.body.classList.add("light-mode");
    }

    else{

        document.body.classList.remove("light-mode");
    }
});