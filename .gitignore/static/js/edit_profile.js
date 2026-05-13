// THEME

function toggleTheme(){

    document.body.classList.toggle("light-mode");

    if(document.body.classList.contains("light-mode")){

        localStorage.setItem("theme","light");

    }

    else{

        localStorage.setItem("theme","dark");

    }
}

// LOAD THEME

document.addEventListener("DOMContentLoaded", function(){

    const theme =
    localStorage.getItem("theme");

    if(theme === "light"){

        document.body.classList.add("light-mode");
    }
});

// IMAGE PREVIEW

const imageInput =
document.getElementById("profile_image");

if(imageInput){

    imageInput.addEventListener("change", function(e){

        const file =
        e.target.files[0];

        if(file){

            const reader =
            new FileReader();

            reader.onload =
            function(event){

                document.getElementById(
                "previewImage"
                ).src = event.target.result;

                const preview =
                document.querySelector(
                ".preview-profile"
                );

                if(preview){

                    preview.src =
                    event.target.result;
                }
            };

            reader.readAsDataURL(file);
        }
    });
}