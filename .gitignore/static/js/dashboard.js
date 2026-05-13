// =========================
// SIDEBAR
// =========================

function toggleSidebar(){

    document
    .getElementById("sidebar")
    .classList
    .toggle("active");

}

// =========================
// THEME TOGGLE
// =========================

function toggleTheme(){

    document.body.classList.toggle("light-mode");

    // SAVE

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


function openNotificationReply(el){

    // GET DATA

    const username = el.dataset.user;

    const message = el.dataset.message;

    const time = el.dataset.time;

    // SHOW PANEL

    document
    .getElementById("replyPanel")
    .classList
    .add("active");

    // SET DATA

    document
    .getElementById("replyUser")
    .innerText = username;

    document
    .getElementById("replyMessage")
    .innerText = message;

    document
    .getElementById("replyTime")
    .innerText = time;

    // HIDDEN INPUT

    document
    .getElementById("replyStudentUsername")
    .value = username;

    // DEBUG

    console.log("USERNAME SET:", username);

}


function toggleReplyPanel(element){

    // =========================
    // GET PANEL
    // =========================

    const panel =
    document.getElementById("replyPanel");

    // =========================
    // GET DATA
    // =========================

    const username =
    element.getAttribute("data-user");

    const message =
    element.getAttribute("data-message");

    const time =
    element.getAttribute("data-time");

    // =========================
    // SHOW PANEL
    // =========================

    panel.classList.add("active");

    // =========================
    // SET DATA
    // =========================

    document.getElementById(
        "replyUser"
    ).innerText = username;

    document.getElementById(
        "replyMessage"
    ).innerText = message;

    document.getElementById(
        "replyTime"
    ).innerText = time;

    // =========================
    // VERY IMPORTANT
    // SET HIDDEN INPUT
    // =========================

    document.getElementById(
        "replyStudentUsername"
    ).value = username;

    // =========================
    // DEBUG
    // =========================

    console.log(
        "Username Set:",
        username
    );

}

function closeReplyPanel(){

    document
    .getElementById("replyPanel")
    .classList
    .remove("active");

}