const studentBtn =
document.querySelectorAll(".type-btn")[0];

const teacherBtn =
document.querySelectorAll(".type-btn")[1];

const studentForm =
document.getElementById("studentForm");

const teacherForm =
document.getElementById("teacherForm");

function showStudent(){

    studentBtn.classList.add("active");

    teacherBtn.classList.remove("active");

    studentForm.classList.remove("hidden");

    teacherForm.classList.add("hidden");

}

function showTeacher(){

    teacherBtn.classList.add("active");

    studentBtn.classList.remove("active");

    teacherForm.classList.remove("hidden");

    studentForm.classList.add("hidden");

}


const password =
document.getElementById("password");

password.addEventListener("keyup", function(){

    const value = password.value;

    // LOWERCASE
    if(/[a-z]/.test(value)){

        lower.classList.add("valid");
        lower.innerHTML = "✅ Lowercase Letter";

    }else{

        lower.classList.remove("valid");
        lower.innerHTML = "❌ Lowercase Letter";
    }

    // UPPERCASE
    if(/[A-Z]/.test(value)){

        upper.classList.add("valid");
        upper.innerHTML = "✅ Uppercase Letter";

    }else{

        upper.classList.remove("valid");
        upper.innerHTML = "❌ Uppercase Letter";
    }

    // NUMBER
    if(/[0-9]/.test(value)){

        number.classList.add("valid");
        number.innerHTML = "✅ Number";

    }else{

        number.classList.remove("valid");
        number.innerHTML = "❌ Number";
    }

    // SYMBOL
    if(/[@$!%*?&]/.test(value)){

        symbol.classList.add("valid");
        symbol.innerHTML = "✅ Special Symbol";

    }else{

        symbol.classList.remove("valid");
        symbol.innerHTML = "❌ Special Symbol";
    }

    // LENGTH
    if(value.length >= 8){

        length.classList.add("valid");
        length.innerHTML = "✅ Minimum 8 Characters";

    }else{

        length.classList.remove("valid");
        length.innerHTML = "❌ Minimum 8 Characters";
    }

});