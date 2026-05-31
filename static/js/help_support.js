// help_support.js

const faqItems =
document.querySelectorAll(".faq-item");

/* FAQ TOGGLE */

faqItems.forEach((item)=>{

    const question =
    item.querySelector(".faq-question");

    question.addEventListener("click",()=>{

        item.classList.toggle("active");

        const icon =
        item.querySelector(".faq-icon");

        if(item.classList.contains("active")){

            icon.innerText = "−";

        }else{

            icon.innerText = "+";
        }
    });
});

/* THEME SUPPORT */

const body = document.body;

function applyTheme(mode){

    if(mode === "light"){

        body.classList.add("light-mode");

    }else{

        body.classList.remove("light-mode");
    }
}

/* AUTO MATCH DASHBOARD THEME */

if(localStorage.getItem("theme") === "light"){

    applyTheme("light");
}