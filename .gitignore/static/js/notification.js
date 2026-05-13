// ========================================
// TOGGLE DROPDOWN
// ========================================

function toggleNotifications(){

    const dropdown = document.getElementById(
        "notificationDropdown"
    );

    dropdown.classList.toggle("active");
}

// ========================================
// REPLY PANEL
// ========================================

function toggleReplyPanel(item){

    const panel = document.getElementById(
        "replyPanel"
    );

    const dropdown = document.getElementById(
        "notificationDropdown"
    );

    // =====================================
    // SAME CLICK CLOSE
    // =====================================

    if(item.classList.contains("active-item")){

        item.classList.remove("active-item");

        panel.classList.remove("active");

        dropdown.classList.remove(
            "reply-open"
        );

        return;
    }

    // =====================================
    // REMOVE OLD ACTIVE
    // =====================================

    document.querySelectorAll(
        ".notification-item"
    ).forEach(el=>{

        el.classList.remove("active-item");
    });

    // =====================================
    // ACTIVE CURRENT ITEM
    // =====================================

    item.classList.add("active-item");

    panel.classList.add("active");

    dropdown.classList.add("reply-open");

    // =====================================
    // MARK READ
    // =====================================

    fetch(
        "/mark-read/" + item.dataset.id
    );

    // =====================================
    // REMOVE BLUE DOT
    // =====================================

    const dot = item.querySelector(
        ".unread-dot"
    );

    if(dot){

        dot.remove();

        // ===============================
        // ADD DELETE BUTTON
        // ===============================

        if(!item.querySelector(".delete-btn")){

            const id = item.dataset.id;

            const btn = document.createElement(
                "button"
            );

            btn.className = "delete-btn";

            btn.innerHTML =
            '<i class="fa-solid fa-trash"></i>';

            btn.onclick = function(event){

                deleteNotification(
                    event,
                    id
                );
            };

            item.appendChild(btn);
        }
    }

    // =====================================
    // DYNAMIC TITLE
    // =====================================

    const type = item.dataset.type;

    let title = "Support Message";

    if(type === "message"){

        title = "Email Message";
    }

    else if(type === "feedback"){

        title = "Feedback Message";
    }

    else if(type === "issue"){

        title = "Report Issue";
    }

    else if(type === "reply"){

        title = "Reply Message";
    }

    document.getElementById(
        "replyTitle"
    ).innerText = title;

    // =====================================
    // SET DATA
    // =====================================

    document.getElementById(
        "replyUser"
    ).innerText = item.dataset.user;

    const fullMessage =
    item.dataset.message;

    document.getElementById(
        "replyMessage"
    ).innerText = fullMessage;

    // ======================================
    // FILE PREVIEW
    // ======================================

    const file =
    item.dataset.file;

    const filePreview =
    document.getElementById(
        "replyFilePreview"
    );

    const fileLink =
    document.getElementById(
        "replyFileLink"
    );

    const fileName =
    document.getElementById(
        "replyFileName"
    );

    if(file && file !== ""){

        filePreview.style.display =
        "flex";

        fileLink.href =
        "/static/uploads/" + file;

        fileName.innerText =
        file;

    }else{

        filePreview.style.display =
        "none";
    }

    document.getElementById(
        "replyTime"
    ).innerText = item.dataset.time;
    
    document.getElementById(
    "replyStudentUsername"
    ).value = item.dataset.user;

}


// ========================================
// CLOSE PANEL
// ========================================

function closeReplyPanel(){

    const panel = document.getElementById(
        "replyPanel"
    );

    const dropdown = document.getElementById(
        "notificationDropdown"
    );

    panel.classList.remove("active");

    dropdown.classList.remove("reply-open");

    document.querySelectorAll(
        ".notification-item"
    ).forEach(el=>{

        el.classList.remove("active-item");
    });
}

// ========================================
// CLICK OUTSIDE
// ========================================

window.addEventListener("click", function(e){

    const wrapper = document.querySelector(
        ".notification-wrapper"
    );

    if(!wrapper.contains(e.target)){

        document.getElementById(
            "notificationDropdown"
        ).classList.remove("active");

        closeReplyPanel();
    }
});

// ========================================
// DELETE NOTIFICATION
// ========================================

function deleteNotification(event, id){

    event.stopPropagation();

    if(confirm("Delete this notification?")){

        window.location.href =
        "/delete-notification/" + id;
    }
}