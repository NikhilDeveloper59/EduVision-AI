// bulk_prediction.js

const body = document.body;
let currentUploadedFile = null;

const fileInput =
document.getElementById("fileInput");

const uploadBox =
document.getElementById("dropArea");

const totalRecords =
document.querySelector(".blue .summary-flex span");

const passedRecords =
document.querySelector(".green .summary-flex span");

const failedRecords =
document.querySelector(".red .summary-flex span");

const recentTableBody =
document.getElementById("recentTableBody");

const resultSection =
document.getElementById("resultSection");

const resultTableBody =
document.getElementById("resultTableBody");

const closeResultBtn =
document.getElementById("closeResultBtn");

const currentResultFile =
document.getElementById("currentResultFile");

const downloadCurrentBtn =
document.getElementById("downloadCurrentBtn");

const viewUploadsBtn =
document.getElementById("viewUploadsBtn");

const fileName =
document.getElementById("fileName");

const uploadStatus =
document.getElementById("uploadStatus");

const fileMeta =
document.getElementById("fileMeta");

const uploadIcon =
document.getElementById("uploadIcon");

const removeBtn =
document.getElementById("removeBtn");

const chooseBtn =
document.getElementById("chooseBtn");

const topViewBtn =
document.getElementById("topViewBtn");

const topDownloadBtn =
document.getElementById("topDownloadBtn");

let currentPredictionData = [];
let predictionCompleted = false;

/* =========================================
THEME
========================================= */

function applyTheme(mode){

    if(mode === "light"){

        body.classList.add("light-mode");

    }else{

        body.classList.remove("light-mode");
    }
}

if(localStorage.getItem("theme") === "light"){

    applyTheme("light");
}

/* =========================================
LOCAL STORAGE
========================================= */

let uploads =
JSON.parse(
    localStorage.getItem("bulkUploads")
) || [];

/* =========================================
SAVE UPLOADS
========================================= */

function saveUploads(){

    localStorage.setItem(

        "bulkUploads",

        JSON.stringify(uploads)

    );
}

/* =========================================
LOAD RECENT UPLOADS
========================================= */

function loadUploads(){

    recentTableBody.innerHTML = "";

    if(uploads.length === 0){

        recentTableBody.innerHTML = `

            <tr>

                <td colspan="6"
                class="no-data">

                    No recent uploads available

                </td>

            </tr>

        `;

        return;
    }

    uploads.slice(0,5).forEach(

        (item,index)=>{

        recentTableBody.innerHTML += `

            <tr>

                <td>${item.file}</td>

                <td>${item.by}</td>

                <td>${item.date}</td>

                <td>${item.records}</td>

                <td>

                    <span class="status">

                        Completed

                    </span>

                </td>

                <td>

                    <div class="action-group">

                        <button
                        class="table-btn"
                        onclick="viewResult(${index})">

                            👁

                        </button>

                        <button
                        class="table-btn"
                        onclick="nextResult(${index})">

                            ⬇

                        </button>

                        <button
                        class="table-btn delete"
                        onclick="deleteUpload(${index})">

                            🗑

                        </button>

                    </div>

                </td>

            </tr>

        `;
    });

}

loadUploads();

/* =========================================
OPEN FILE PICKER
========================================= */

chooseBtn.addEventListener(

    "click",

    (e)=>{

        e.stopPropagation();

        fileInput.click();
    }

);

uploadBox.addEventListener(

    "click",

    (e)=>{

        if(
            e.target !== removeBtn
        ){

            fileInput.click();
        }
    }

);

/* =========================================
FILE CHANGE
========================================= */

fileInput.addEventListener(

    "change",

    function(){

        const file =
        this.files[0];

        if(file){

            const sizeMB = (

                file.size /
                (1024 * 1024)

            ).toFixed(2);

            fileName.innerText =
            file.name;

            uploadStatus.innerText =
            "File uploaded successfully";

            fileMeta.innerText =
            `${sizeMB} MB`;

            uploadIcon.innerText =
            "✅";

            removeBtn.style.display =
            "block";

            currentUploadedFile = file;

            uploadStatus.innerText =
            "File selected. Click View Predicted Result to start processing.";
        }

    }

);

/* =========================================
DRAG DROP
========================================= */

uploadBox.addEventListener(

    "dragover",

    (e)=>{

        e.preventDefault();

        uploadBox.style.borderColor =
        "#1f64ff";
    }

);

uploadBox.addEventListener(

    "dragleave",

    ()=>{

        uploadBox.style.borderColor =
        "rgba(31,100,255,0.4)";
    }

);

uploadBox.addEventListener(

    "drop",

    (e)=>{

        e.preventDefault();

        uploadBox.style.borderColor =
        "rgba(31,100,255,0.4)";

        const file =
        e.dataTransfer.files[0];

        if(file){

            fileInput.files =
            e.dataTransfer.files;

            const sizeMB = (

                file.size /
                (1024 * 1024)

            ).toFixed(2);

            fileName.innerText =
            file.name;

            uploadStatus.innerText =
            "File uploaded successfully";

            fileMeta.innerText =
            `${sizeMB} MB`;

            uploadIcon.innerText =
            "✅";

            removeBtn.style.display =
            "block";

            currentUploadedFile = file;

            uploadStatus.innerText =
            "File selected. Click View Predicted Result to start processing.";
        }

    }

);

/* =========================================
START PROCESSING
========================================= */
async function startProcessing(file){

    console.log("START PROCESSING CALLED");

    if(!file){
        alert("No file selected");
        return;
    }

    const loader =
    document.getElementById("uploadLoader");

    const formData =
    new FormData();

    formData.append(
        "file",
        file
    );

    uploadStatus.innerText =
    "Processing prediction... Please wait";

    if(loader){

        loader.style.display =
        "flex";
    }

    topViewBtn.disabled = true;
    topDownloadBtn.disabled = true;

    try{

        console.log("SENDING REQUEST...");

        const response =
        await fetch(
            "/process_bulk_prediction",
            {
                method:"POST",
                body:formData
            }
        );

        console.log(
            "RESPONSE STATUS:",
            response.status
        );

        const data =
        await response.json();

        console.log(
            "SERVER DATA:",
            data
        );

        if(loader){

            loader.style.display =
            "none";
        }

        topViewBtn.disabled = false;
        topDownloadBtn.disabled = false;

        if(!data.success){

            alert(
                data.message ||
                "Prediction failed"
            );

            return;
        }

        currentPredictionData =
        data.results;

        predictionCompleted =
        true;

        /* =====================================
        SAVE IN RECENT UPLOADS
        ===================================== */

        const uploadData = {

            file:file.name,

            by:"Teacher",

            date:new Date()
            .toLocaleString(),

            records:data.summary.total,

            results:data.results

        };

        uploads.unshift(uploadData);

        saveUploads();

        loadUploads();

        /* =====================================
        UPDATE SUMMARY
        ===================================== */

        uploadStatus.innerText =
        "Prediction completed successfully";

        document.getElementById(
            "totalStudents"
        ).innerText =
        data.summary.total;

        document.getElementById(
            "totalPassed"
        ).innerText =
        data.summary.passed;

        document.getElementById(
            "totalFailed"
        ).innerText =
        data.summary.failed;

        /* =====================================
        SHOW RESULT
        ===================================== */

        showPredictionResult(
            data.results,
            file.name
        );

    }
    catch(error){

        console.error(
            "FETCH ERROR:",
            error
        );

        if(loader){

            loader.style.display =
            "none";
        }

        topViewBtn.disabled = false;
        topDownloadBtn.disabled = false;

        alert(
            "Error: " +
            error.message
        );
    }
}

/* =========================================
SHOW PREDICTION RESULT
========================================= */

function showPredictionResult(results,fileName){

    resultSection.style.display =
    "block";

    currentResultFile.innerText =
    `Current File: ${fileName}`;

    resultTableBody.innerHTML = "";

    /* =====================================
    SAVE CURRENT DATA
    ===================================== */

    currentPredictionData = results;

    // GENERATE TABLE

  results.forEach((item)=>{

    resultTableBody.innerHTML += `

        <tr>

            <td>${item.student_id}</td>

            <td>${item.predicted_score}</td>

            <td class="${
                item.result === "PASS"
                ? "pass"
                : "fail"
            }">

                ${item.result}

            </td>

        </tr>

    `;
});

    /* =====================================
    SCROLL TO RESULT
    ===================================== */

    window.scrollTo({

        top:
        resultSection.offsetTop - 120,

        behavior:"smooth"
    });
}


function viewResult(index){

    const upload =
    uploads[index];

    showPredictionResult(

        upload.results,

        upload.file

    );
}

/* =========================================
NEXT RESULT
========================================= */

function nextResult(index){

    if(index + 1 < uploads.length){

        viewResult(index + 1);

    }else{

        alert(
        "No more upload results available"
        )
        
    }
}

/* =========================================
DELETE RESULT
========================================= */

function deleteUpload(index){

    const confirmDelete =
    confirm(
    "Delete this upload record?"
    );

    if(confirmDelete){

        uploads.splice(index,1);

        saveUploads();

        loadUploads();

        if(uploads.length === 0){

            resultSection.style.display =
            "none";
        }
    }
}

/* =========================================
REMOVE FILE
========================================= */

removeBtn.addEventListener(

    "click",

    function(e){

        e.stopPropagation();

        fileInput.value = "";

        predictionCompleted = false;
        currentPredictionData = [];
        currentUploadedFile = null;

        fileName.innerText =
        "No file selected";

        uploadStatus.innerText =
        "Upload CSV or Excel file";

        fileMeta.innerText =
        "Supported: .csv .xlsx .xls";

        uploadIcon.innerText =
        "📂";

        removeBtn.style.display =
        "none";

        resultSection.style.display =
        "none";

        totalRecords.innerText = 0;
        passedRecords.innerText = 0;
        failedRecords.innerText = 0;
    }

);

/* =========================================
TOP VIEW BUTTON
========================================= */
topViewBtn.addEventListener(

    "click",

    async ()=>{

        if(!currentUploadedFile){

            alert(
                "Please choose a file first"
            );

            return;
        }

        // Already predicted
        if(predictionCompleted){

            showPredictionResult(
                currentPredictionData,
                currentUploadedFile.name
            );

            return;
        }

        await startProcessing(
            currentUploadedFile
        );

    }
);

/* =========================================
DOWNLOAD CSV
========================================= */

function downloadCSV(){

    if(
        currentPredictionData.length === 0
    ){

        alert(
        "Please view prediction first"
        );

        return;
    }

    let csvContent =
    "Name,Marks,Prediction\n";

    currentPredictionData.forEach(

        (item)=>{

       csvContent +=
`${item.student_id},${item.predicted_score},${item.result}\n`;
    });

    const blob = new Blob(

        [csvContent],

        {
            type:"text/csv"
        }

    );

    const url =
    window.URL.createObjectURL(blob);

    const a =
    document.createElement("a");

    a.href = url;

    a.download =
    "predicted_result.csv";

    document.body.appendChild(a);

    a.click();

    document.body.removeChild(a);

    window.URL.revokeObjectURL(url);
}

topDownloadBtn.addEventListener(

    "click",

    ()=>{

        downloadCSV();
    }

);

downloadCurrentBtn.addEventListener(

    "click",

    ()=>{

        downloadCSV();
    }

);

/* =========================================
CLOSE RESULT
========================================= */

closeResultBtn.addEventListener(

    "click",

    ()=>{

        resultSection.style.display =
        "none";
    }

);

/* =========================================
VIEW ALL UPLOADS
========================================= */

viewUploadsBtn.addEventListener(

    "click",

    ()=>{

        document.querySelector(".table-wrapper")
        .scrollIntoView({

            behavior:"smooth"
        });
    }

);