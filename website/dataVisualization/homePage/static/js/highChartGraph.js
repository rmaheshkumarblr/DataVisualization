Highcharts.setOptions({
    global: {
        useUTC: false
    }
});

fieldName = ""
axisfieldName = ""

// console.log("From High Chars Library:" + specialValues)

// Calculation of the Default Equations value

// x = minimum(CO2_SensorData)
// slope1 = ((5000-390)/(4500 - x))
// int1 = (5000 - ((5000-390)/(4500 - x))

// final equation: CO2 (units ppm) = slope1*CO2_SensorData + int1
// *slope1 and int1 should be adjustable

// ________________________________________________________________
        
// x = 1/(mean(O3_SensorData))
// slope2 = ((35-0)./(x - (1/3150)))
// int2 = (35 - ((35-0)./(x - (1/3150))).*x)

// final equation: O3 (units ppb) = slope2*(1/O3_SensorData) + int2
// *slope2 and int2 should be adjustable

// _______________________________________________________________
       
// x = minimum(Fig1_SensorData);
// VOC1 = (Fig1_SensorData-x)./(4500-x);

// final equation: VOC1 (units ppm) = 20.*VOC1 + 1.8;
// *20 and 1.8 shoudl be adjustable)
        
// ________________________________________________________________

//  x = minimum(Fig2_SensorData);
// VOC2 = (poddata.Fig2 - x)./(4500 - x);

// final equation: VOC2 (units ppm) = 10.*VOC2;
// 10 should be adjustable
// _________________________________________________________________

// GPS Conversions to usable lat and long:
        
// Lat = poddata.NS.*(floor(poddata.Lat./100) +((poddata.Lat./100-(floor(poddata.Lat./100)))*100/60));
// Long = poddata.EW.*(floor(poddata.Lon./100) + ((poddata.Lon./100-(floor(poddata.Lon/100)))*100/60));

// __________________________________________________________________

// More Complex Equations: 

// Text for user: "use an equation that corrects for temperature and humidity; note you will need to input your own coefficients"

// CO2: x1*CO2_SensorData + x2*Temperature + x3*Humidity + x4 (units ppm)

// O3: x1*O3_SensorData + x2*Temperature + x3*Humidity + x4 (units ppb)

// VOC1: x1*VOC1_SensorData + x2*Temperature + x3*Humidity + x4 (units ppm)

// VOC2: x1*VOC2_SensorData + x2*Temperature + x3*Humidity + x4 (units ppm)

// In each case the user will need to input a coefficient for the sensor data, for temp, and humidity as well as an intercept (x1, x2, x3, x4)

function updateFieldName(field) {
    if (field == "O3") {
        fieldName = "e2vo3_sens"
    } else if (field == "Light VOCs") {
        fieldName = "fig210_sens"
    } else if (field == "Heavy VOCs") {
        fieldName = "fig280_sens"
    } else if (field == "CO2 (PPM)") {
        fieldName = "CO2"
    } else if (field == "O3 (PPB)") {
        fieldName = "e2vo3_sens"
    } else if (field == "Light VOCs (PPB)") {
        fieldName = "voc1_ppm"
    } else if (field == "Heavy VOCs (PPB)") {
        fieldName = "voc2_ppm"
    }
    else {
        fieldName = field
    }

    if (field == "O3") {
        axisfieldName = "O3 Electronic Signal (Voltage Equivalent)"
    } else if (field == "Light VOCs") {
        axisfieldName = "Light VOCs Electronic Signal (Voltage Equivalent)"
    } else if (field == "Heavy VOCs") {
        axisfieldName = "Heavy VOCs Electronic Signal (Voltage Equivalent)"
    } else if (field == "Temperature") {
        axisfieldName = "Temperature (deg Celsius)"
    } else if (field == "Humidity") {
        axisfieldName = "Relative Humidity (%)"
    } else if (field == "CO2") {
        axisfieldName = "CO2 Electronic Signal (Voltage Equivalent)"
    } else if (field == "CO2 (PPM)") {
        axisfieldName = "CO2 (PPM)"
    }  else if (field == "O3 (PPB)") {
        axisfieldName = "O3 (PPB)"
    }  else if (field == "Light VOCs (PPB)") {
        axisfieldName = "Light VOCs (PPB)"
    }  else if (field == "Heavy VOCs (PPB)") {
        axisfieldName = "Heavy VOCs (PPB)"
    } 
    else {
        axisfieldName = field
    }
}


fieldName1 = ""
fieldName2 = ""
axisfieldName1 = ""
axisfieldName2 = ""

function updateFieldsName(field1, field2) {
    if (field1 == "O3") {
        fieldName1 = "e2vo3_sens"
    } else if (field1 == "Light VOCs") {
        fieldName1 = "fig210_sens"
    } else if (field1 == "Heavy VOCs") {
        fieldName1 = "fig280_sens"
    } else {
        fieldName1 = field1
    }

    if (field2 == "O3") {
        fieldName2 = "e2vo3_sens"
    } else if (field2 == "Light VOCs") {
        fieldName2 = "fig210_sens"
    } else if (field2 == "Heavy VOCs") {
        fieldName2 = "fig280_sens"
    } else {
        fieldName2 = field2
    }

    if (field1 == "O3") {
        axisfieldName1 = "O3 Electronic Signal (Voltage Equivalent)"
    } else if (field1 == "Light VOCs") {
        axisfieldName1 = "Light VOCs Electronic Signal (Voltage Equivalent)"
    } else if (field1 == "Heavy VOCs") {
        axisfieldName1 = "Heavy VOCs Electronic Signal (Voltage Equivalent)"
    } else if (field1 == "Temperature") {
        axisfieldName1 = "Temperature (deg Celsius)"
    } else if (field1 == "Humidity") {
        axisfieldName1 = "Relative Humidity (%)"
    } else if (field1 == "CO2") {
        axisfieldName1 = "CO2 Electronic Signal (Voltage Equivalent)"
    } else {
        axisfieldName1 = field1
    }

    if (field2 == "O3") {
        axisfieldName2 = "O3 Electronic Signal (Voltage Equivalent)"
    } else if (field2 == "Light VOCs") {
        axisfieldName2 = "Light VOCs Electronic Signal (Voltage Equivalent)"
    } else if (field2 == "Heavy VOCs") {
        axisfieldName2 = "Heavy VOCs Electronic Signal (Voltage Equivalent)"
    } else if (field2 == "Temperature") {
        axisfieldName2 = "Temperature (deg Celsius)"
    } else if (field2 == "Humidity") {
        axisfieldName2 = "Relative Humidity (%)"
    } else if (field2 == "CO2") {
        axisfieldName2 = "CO2 Electronic Signal (Voltage Equivalent)"
    } else {
        axisfieldName2 = field2
    }
}





function getTimeSeriesGraph(content, field) {
    "use strict",
    data = []
    updateFieldName(field)

    // console.log(field + " " + fieldName)
    function logArrayElements(element, index, array) {
        dateFromPython = new Date(element['Date'])
        data.push([dateFromPython.getTime(), parseFloat(element[fieldName])])
    }
    content.forEach(logArrayElements)

    // console.log(data)
    $('#container').highcharts({
        chart: {
            zoomType: 'x',
            width: 950,
            height: 500
        },
        title: {
            text: field + ' against Time'
        },
        subtitle: {
            text: document.ontouchstart === undefined ?
                'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
        },
        xAxis: {
            type: 'datetime',
            title: {
                text: "Time"
            }
        },
        yAxis: {
            title: {
                text: axisfieldName
            }
        },
        legend: {
            enabled: true
        },
        plotOptions: {
            area: {
                fillColor: {
                    linearGradient: {
                        x1: 0,
                        y1: 0,
                        x2: 0,
                        y2: 1
                    },
                    stops: [
                        [0, Highcharts.getOptions().colors[0]],
                        [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                    ]
                },
                marker: {
                    radius: 2
                },
                lineWidth: 1,
                states: {
                    hover: {
                        lineWidth: 1
                    }
                }
            }
        },

        series: [{
            type: 'area',
            name: field + ' against Time',
            data: data
        }],
        exporting: {
            buttons: {
                contextButton: {
                    text: 'Download'
                }
            }
        }

    });
};


// This Time Series is graph is for the Default Equations which have 2 extra parameters which are modifiableby the user
function getTimeSeriesGraphWithExtraParameters(content, field, slope, intercept) {

    "use strict",
    data = []
    updateFieldName(field)

    // console.log("From Time Series with patameters: " + field + " " + slope + " " + intercept + " " + fieldName)
    function logArrayElements(element, index, array) {
        dateFromPython = new Date(element['Date'])
        if(field == "CO2 (PPM)"){
            data.push([dateFromPython.getTime(), ( parseFloat(slope) * parseFloat(element[fieldName]) ) + parseFloat(intercept)] )
        } else if (field == "O3 (PPB)"){
            data.push([dateFromPython.getTime(), ( parseFloat(slope) * (1/parseFloat(element[fieldName])) ) + parseFloat(intercept)] )
        } else if (field == "Light VOCs (PPM)"){
            data.push([dateFromPython.getTime(), ( parseFloat(slope) * parseFloat(element[fieldName]) ) + parseFloat(intercept)] )
        } else if (field == "High VOCs (PPM)"){
            data.push([dateFromPython.getTime(), ( parseFloat(slope) * parseFloat(element[fieldName]) )] )
        } 
    }
    content.forEach(logArrayElements)
    // console.log(data)
    $('#container').highcharts({
        chart: {
            zoomType: 'x',
            width: 950,
            height: 500
        },
        title: {
            text: field + ' against Time'
        },
        subtitle: {
            text: document.ontouchstart === undefined ?
                'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
        },
        xAxis: {
            type: 'datetime',
            title: {
                text: "Time"
            }
        },
        yAxis: {
            title: {
                text: axisfieldName
            }
        },
        legend: {
            enabled: true
        },
        plotOptions: {
            area: {
                fillColor: {
                    linearGradient: {
                        x1: 0,
                        y1: 0,
                        x2: 0,
                        y2: 1
                    },
                    stops: [
                        [0, Highcharts.getOptions().colors[0]],
                        [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                    ]
                },
                marker: {
                    radius: 2
                },
                lineWidth: 1,
                states: {
                    hover: {
                        lineWidth: 1
                    }
                }
            }
        },

        series: [{
            type: 'area',
            name: field + ' against Time',
            data: data
        }],
        exporting: {
            buttons: {
                contextButton: {
                    text: 'Download'
                }
            }
        }

    });
};


function getScatterPlotGraph(content, field1, field2) {
    "use strict",
    data = []

    updateFieldsName(field1, field2)

    function logArrayElements(element, index, array) {
        data.push([parseFloat(element[fieldName1]), parseFloat(element[fieldName2])])
    }
    content.forEach(logArrayElements)

    $('#container').highcharts({
        chart: {
            type: 'scatter',
            zoomType: 'xy',
            width: 950,
            height: 500
        },
        title: {
            text: field1 + ' Versus ' + field2
        },
        xAxis: {
            title: {
                enabled: true,
                text: axisfieldName1
            },
            startOnTick: true,
            endOnTick: true,
            showLastLabel: true
        },
        yAxis: {
            title: {
                text: axisfieldName2
            }
        },
        legend: {
            layout: 'vertical',
            align: 'left',
            verticalAlign: 'top',
            x: 100,
            y: 70,
            floating: true,
            backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF',
            borderWidth: 1
        },
        plotOptions: {
            scatter: {
                marker: {
                    radius: 5,
                    states: {
                        hover: {
                            enabled: true,
                            lineColor: 'rgb(100,100,100)'
                        }
                    }
                },
                states: {
                    hover: {
                        marker: {
                            enabled: false
                        }
                    }
                },
                tooltip: {
                    headerFormat: '<b>{series.name}</b><br>',
                    pointFormat: '{point.x} cm, {point.y} kg'
                }
            }
        },
        series: [{
            name: field1 + ' Versus ' + field2,
            color: 'rgba(119, 152, 191, .5)',
            data: data
        }],
        exporting: {
            buttons: {
                contextButton: {
                    text: 'Download'
                }
            }
        }

    });
};


function getDoubleYAxisPlotGraph(content, field1, field2) {
    "use strict",
    data1 = []
    data2 = []

    updateFieldsName(field1, field2)

    function logArrayElements(element, index, array) {
        dateFromPython = new Date(element['Date'])
        data1.push([dateFromPython.getTime(), parseFloat(element[fieldName1])])
        data2.push([dateFromPython.getTime(), parseFloat(element[fieldName2])])
    }
    content.forEach(logArrayElements)

    $('#container').highcharts({
        chart: {
            zoomType: 'xy',
            width: 950,
            height: 500
        },
        title: {
            text: 'Pollutant Information from the Pod : ' + field1 + " and " + field2
        },
        subtitle: {
            text: 'UPOD Data'
        },
        xAxis: {
            type: 'datetime'
        },
        yAxis: [{
            labels: {
                // format: '{value}°C',
                style: {
                    color: Highcharts.getOptions().colors[1]
                }
            },
            title: {
                text: axisfieldName2,
                style: {
                    color: Highcharts.getOptions().colors[1]
                }
            },
            opposite: true

        }, { // Tertiary yAxis
            gridLineWidth: 0,
            title: {
                text: axisfieldName1,
                style: {
                    color: Highcharts.getOptions().colors[0]
                }
            },
            labels: {
                // format: '{value} grams per cubic meter',
                style: {
                    color: Highcharts.getOptions().colors[0]
                }
            },
            opposite: true
        }],
        tooltip: {
            shared: true
        },
        legend: {
            layout: 'vertical',
            align: 'left',
            x: 80,
            verticalAlign: 'top',
            y: 55,
            floating: true,
            backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'
        },
        series: [{
            name: field1,
            type: 'spline',
            yAxis: 1,
            data: data1,
            marker: {
                enabled: false
            },
            dashStyle: 'shortdot',
            // tooltip: {
            //     valueSuffix: ' °C'
            // }

        }, {
            name: field2,
            type: 'spline',
            yAxis: 0,
            data: data2,
            // tooltip: {
            //     valueSuffix: ' grams per cubic meter'
            // }
        }],
        exporting: {
            buttons: {
                contextButton: {
                    text: 'Download'
                }
            }
        }
    });
}


function getBoxPlotGraph(content, field) {
    // console.log('clicked')
    "use strict",
    data = []

    updateFieldName(field)

    Field = [];

    function logArrayElements(element, index, array) {
        Field.push([parseFloat(element[fieldName])])
    }
    content.forEach(logArrayElements)



    //get any percentile from an array
    function getPercentile(data, percentile) {
        data.sort(numSort);
        var index = (percentile / 100) * data.length;
        var result;
        if (Math.floor(index) == index) {
            result = (data[(index - 1)] + data[index]) / 2;
        } else {
            result = data[Math.floor(index)];
        }
        return result;
    }
    //because .sort() doesn't sort numbers correctly
    function numSort(a, b) {
        return a - b;
    }


    //wrap the percentile calls in one method
    function getBoxValues(data) {
        var boxValues = [];
        boxValues.push(Math.min.apply(Math, data));
        boxValues.push(getPercentile(data, 25));
        boxValues.push(getPercentile(data, 50));
        boxValues.push(getPercentile(data, 75));
        boxValues.push(Math.max.apply(Math, data));
        return boxValues;
    }
    console.log(getBoxValues(Field))
    data.push(getBoxValues(Field));

    $('#container').highcharts({
        chart: {
            type: 'boxplot',
            width: 950,
            height: 500
        },

        title: {
            text: 'Box Plot for ' + field
        },

        legend: {
            enabled: false
        },

        xAxis: {
            categories: field,
            title: {
                text: 'Pollutant'
            }
        },

        yAxis: {
            title: {
                text: 'Observations'
            }
        },

        series: [{
            name: 'Observations',
            data: data
        }],
        exporting: {
            buttons: {
                contextButton: {
                    text: 'Download'
                }
            }
        }

    });
};


function getCompareTimeSeriesGraph(content1, content2, field) {
    "use strict",
    data1 = []
    data2 = []

    updateFieldName(field)

    function logArrayElements1(element, index, array) {
        dateFromPython = new Date(element['Date'])
        data1.push([dateFromPython.getTime(), parseFloat(element[fieldName])])
    }

    function logArrayElements2(element, index, array) {
        dateFromPython = new Date(element['Date'])
        data2.push([dateFromPython.getTime(), parseFloat(element[fieldName])])
    }
    content1.forEach(logArrayElements1)
    content2.forEach(logArrayElements2)

    $('#container').highcharts({
        chart: {
            zoomType: 'x',
            width: 950,
            height: 500
        },
        title: {
            text: field + ' against Time'
        },
        subtitle: {
            text: document.ontouchstart === undefined ?
                'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
        },
        xAxis: {
            type: 'datetime'
        },
        yAxis: {
            title: {
                text: axisfieldName
            }
        },
        legend: {
            enabled: true
        },
        tooltip: {
            headerFormat: '<b>{series.name}</b><br>',
            pointFormat: '{point.x:%e. %b}: {point.y:.2f} m'
        },
        plotOptions: {
            area: {
                marker: {
                    radius: 2
                },
                lineWidth: 1,
                states: {
                    hover: {
                        lineWidth: 1
                    }
                },
                threshold: null
            }
        },

        series: [{
            type: 'area',
            name: field + ' against Time' + " for POD1",
            data: data1,
            color: Highcharts.getOptions().colors[8],
            fillColor: {
                linearGradient: [0, 0, 0, 100],
                stops: [
                    [0, Highcharts.getOptions().colors[8]],
                    [1, Highcharts.Color(Highcharts.getOptions().colors[8]).setOpacity(0.3).get('rgba')]
                ]
            }
        }, {
            type: 'area',
            name: field + ' against Time' + " for POD2",
            data: data2,
            color: Highcharts.getOptions().colors[2],
            fillColor: {
                linearGradient: [0, 0, 0, 100],
                stops: [
                    [0, Highcharts.getOptions().colors[2]],
                    [1, Highcharts.Color(Highcharts.getOptions().colors[2]).setOpacity(0.3).get('rgba')]
                ]
            }
        }],
        exporting: {
            buttons: {
                contextButton: {
                    text: 'Download'
                }
            }
        }

    });
};

function getCompareScatterPlotGraph(content1, content2, field1, field2) {

    "use strict",
    data1 = []
    data2 = []

    updateFieldsName(field1, field2)

    function logArrayElements1(element, index, array) {
        data1.push([parseFloat(element[fieldName1]), parseFloat(element[fieldName2])])
    }
    content1.forEach(logArrayElements1)

    function logArrayElements2(element, index, array) {
        data2.push([parseFloat(element[fieldName1]), parseFloat(element[fieldName2])])
    }
    content2.forEach(logArrayElements2)

    $('#container').highcharts({
        chart: {
            type: 'scatter',
            zoomType: 'xy',
            width: 950,
            height: 500
        },
        title: {
            text: field1 + ' Versus ' + field2
        },
        xAxis: {
            title: {
                enabled: true,
                text: axisfieldName1
            },
            startOnTick: true,
            endOnTick: true,
            showLastLabel: true
        },
        yAxis: {
            title: {
                text: axisfieldName2
            }
        },
        legend: {
            layout: 'vertical',
            align: 'left',
            verticalAlign: 'top',
            x: 100,
            y: 70,
            floating: true,
            backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF',
            borderWidth: 1
        },
        plotOptions: {
            scatter: {
                marker: {
                    radius: 5,
                    states: {
                        hover: {
                            enabled: true,
                            lineColor: 'rgb(100,100,100)'
                        }
                    }
                },
                states: {
                    hover: {
                        marker: {
                            enabled: false
                        }
                    }
                },
                tooltip: {
                    headerFormat: '<b>{series.name}</b><br>',
                    pointFormat: '{point.x} cm, {point.y} kg'
                }
            }
        },
        series: [{
                name: field1 + ' Versus ' + field2 + ' for POD1',
                color: Highcharts.getOptions().colors[8],
                data: data1
            }, {
                name: field1 + ' Versus ' + field2 + ' for POD2',
                color: Highcharts.getOptions().colors[2],
                data: data2
            }

        ],
        exporting: {
            buttons: {
                contextButton: {
                    text: 'Download'
                }
            }
        }

    });
};



function getCompareBoxPlotGraph(content1, content2, field) {
    "use strict",
    data1 = []
    data2 = []

    Field1 = [];
    Field2 = [];

    updateFieldName(field)

    function logArrayElements1(element, index, array) {
        Field1.push(parseFloat(element[fieldName]))
    }
    content1.forEach(logArrayElements1)

    function logArrayElements2(element, index, array) {
        Field2.push(parseFloat(element[fieldName]))
    }
    content2.forEach(logArrayElements2)

    function getPercentile(data, percentile) {
        data.sort(numSort);
        var index = (percentile / 100) * data.length;
        var result;
        if (Math.floor(index) == index) {
            result = (data[(index - 1)] + data[index]) / 2;
        } else {
            result = data[Math.floor(index)];
        }
        return result;
    }

    //because .sort() doesn't sort numbers correctly
    function numSort(a, b) {
        return a - b;
    }


    //wrap the percentile calls in one method
    function getBoxValues(data) {
        var boxValues = [];
        boxValues.push(Math.min.apply(Math, data));
        boxValues.push(getPercentile(data, 25));
        // console.log("Median",getPercentile(data, 50)[0] ) 
        boxValues.push(getPercentile(data, 50));
        boxValues.push(getPercentile(data, 75));
        boxValues.push(Math.max.apply(Math, data));
        return boxValues;
    }

    data1.push(getBoxValues(Field1));
    data2.push(getBoxValues(Field2));

    $('#container').highcharts({
        chart: {
            type: 'boxplot',
            width: 950,
            height: 500
        },

        title: {
            text: 'Box Plot for the pollutant ' + field
        },

        legend: {
            enabled: false
        },

        xAxis: {
            categories: [field],
            title: {
                text: 'Pollutant'
            }
        },

        yAxis: {
            title: {
                text: 'Observations'
            }
        },

        series: [{
                name: 'POD1',
                data: data1
            }, {
                name: 'POD2',
                data: data2
            }

        ],
        exporting: {
            buttons: {
                contextButton: {
                    text: 'Download'
                }
            }
        }

    });
};