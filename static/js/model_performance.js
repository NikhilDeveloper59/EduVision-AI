/* ===================================================== */
/* THEME */
/* ===================================================== */

const savedTheme = localStorage.getItem(
    "theme"
);

if(savedTheme === "light"){

    document.body.classList.add(
        "light-mode"
    );
}

/* ===================================================== */
/* COLORS */
/* ===================================================== */

const darkMode = !document.body.classList.contains(
    'light-mode'
);

const textColor = darkMode
? '#ffffff'
: '#111827';

const gridColor = darkMode
? 'rgba(255,255,255,0.08)'
: 'rgba(0,0,0,0.08)';

/* ===================================================== */
/* REGRESSION CHART */
/* ===================================================== */

new Chart(

    document.getElementById(
        'regressionChart'
    ),

    {

        type:'scatter',

        data:{

            datasets:[{

                label:'Actual vs Predicted',

                data:regressionChartData,

                backgroundColor:'#3b82f6'

            }]

        },

        options:{

            responsive:true,

            maintainAspectRatio:false,

            plugins:{

                legend:{

                    labels:{

                        color:textColor
                    }
                }
            },

            scales:{

                x:{

                    ticks:{

                        color:textColor
                    },

                    grid:{

                        color:gridColor
                    }
                },

                y:{

                    ticks:{

                        color:textColor
                    },

                    grid:{

                        color:gridColor
                    }
                }
            }
        }
    }

);

/* ===================================================== */
/* PASS FAIL CHART */
/* ===================================================== */

new Chart(

    document.getElementById(
        'passChart'
    ),

    {

        type:'doughnut',

        data:{

            labels:[

                'PASS',
                'FAIL'

            ],

            datasets:[{

                data:passChartData,

                backgroundColor:[

                    '#22c55e',
                    '#ef4444'

                ]

            }]

        },

        options:{

            responsive:true,

            maintainAspectRatio:false,

            plugins:{

                legend:{

                    labels:{

                        color:textColor
                    }
                }
            }
        }
    }

);

/* ===================================================== */
/* GRADE CHART */
/* ===================================================== */

new Chart(

    document.getElementById(
        "gradeChart"
    ),

    {

        type:"bar",

        data:{

            labels:gradeChartLabels,

            datasets:[{

                label:"Students",

                data:gradeChartValues,

                borderRadius:10,

                backgroundColor:[

                    "#22c55e",
                    "#3b82f6",
                    "#8b5cf6",
                    "#f59e0b",
                    "#ef4444"

                ]

            }]
        },

        options:{

            responsive:true,

            maintainAspectRatio:false,

            plugins:{

                legend:{

                    labels:{

                        color:"#ffffff"
                    }
                }
            },

            scales:{

                x:{

                    ticks:{
                        color:"#ffffff"
                    },

                    grid:{
                        color:"rgba(255,255,255,0.08)"
                    }
                },

                y:{

                    beginAtZero:true,

                    ticks:{
                        color:"#ffffff"
                    },

                    grid:{
                        color:"rgba(255,255,255,0.08)"
                    }
                }
            }
        }
    }
);

/* ===================================================== */
/* MODEL COMPARISON */
/* ===================================================== */

new Chart(

    document.getElementById(
        'comparisonChart'
    ),

    {

        type:'bar',

        data:{

            labels:[

                'Regression',
                'Pass/Fail',
                'Grade'

            ],

            datasets:[{

                label:'Model Accuracy %',

                data:comparisonChartData,

                backgroundColor:[

                    '#3b82f6',
                    '#22c55e',
                    '#8b5cf6'

                ],

                borderRadius:12,

                borderSkipped:false

            }]

        },

        options:{

            responsive:true,

            maintainAspectRatio:false,

            plugins:{

                legend:{

                    labels:{

                        color:textColor,

                        font:{

                            size:14
                        }
                    }
                }
            },

            scales:{

                x:{

                    ticks:{

                        color:textColor,

                        font:{

                            size:13
                        }
                    },

                    grid:{

                        color:gridColor
                    }
                },

                y:{

                    beginAtZero:true,

                    max:100,

                    ticks:{

                        color:textColor,

                        callback:function(value){

                            return value + "%";
                        }
                    },

                    grid:{

                        color:gridColor
                    }
                }
            }
        }
    }

);

/* ===================================================== */
/* EXPORT PDF */
/* ===================================================== */

function downloadPDF(){

    const element =
    document.getElementById(
        'performancePage'
    );

    html2pdf()

    .set({

        margin:0.5,

        filename:'Model_Performance_Report.pdf',

        image:{
            type:'jpeg',
            quality:1
        },

        html2canvas:{
            scale:2
        },

        jsPDF:{
            unit:'in',
            format:'a3',
            orientation:'portrait'
        }

    })

    .from(element)

    .save();

}