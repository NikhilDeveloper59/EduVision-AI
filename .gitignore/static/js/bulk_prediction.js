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

            startProcessing(file);
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

            startProcessing(file);
        }

    }

);

/* =========================================
START PROCESSING
========================================= */
async function startProcessing(file){

    const formData = new FormData();

    formData.append("file", file);

    uploadStatus.innerText =
    "Processing prediction...";

    try{

        const response = await fetch(

            "/process_bulk_prediction",

            {

                method:"POST",

                body:formData
            }
        );

        const data = await response.json();

        if(!data.success){

            alert(data.message);

            return;
        }

        /* =====================================
        SUMMARY
        ===================================== */

        document.getElementById(
        "totalStudents"
        ).innerText = data.summary.total;

        document.getElementById(
        "totalPassed"
        ).innerText = data.summary.passed;

        document.getElementById(
        "totalFailed"
        ).innerText = data.summary.failed;

        /* =====================================
        STORE CURRENT RESULT
        ===================================== */

        currentPredictionData =
        data.results;

        /* =====================================
        RECENT TABLE
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

        uploadStatus.innerText =
        "Prediction completed successfully";

        /* =====================================
        AUTO VIEW RESULT
        ===================================== */

        showPredictionResult(

            uploadData.results,

            uploadData.file
        );

    }

    catch(error){

        console.log(error);

        alert("Prediction failed");
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

    /* =====================================
    GENERATE TABLE
    ===================================== */

    results.forEach((item)=>{

        resultTableBody.innerHTML += `

            <tr>

                <td>${item.student}</td>

                <td>${item.score}</td>

                <td class="${
                    item.prediction === "PASS"
                    ? "pass"
                    : "fail"
                }">

                    ${item.prediction}

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

/* =========================================
VIEW RESULT
========================================= */
function viewResult(index){

    const upload = uploads[index];

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

    ()=>{

        /* CURRENT FILE CHECK */

        if(
            currentPredictionData.length === 0
        ){

            alert(
            "Please upload and process file first"
            );

            return;
        }

        /* SHOW CURRENT RESULT */

        showPredictionResult(

            currentPredictionData,

            fileName.innerText
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
        `${item.student},${item.score},${item.prediction}\n`;
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