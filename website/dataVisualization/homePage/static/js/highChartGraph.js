// var getGraph = (function (content) {
Highcharts.setOptions({
  global: {
    useUTC: false
  }
});

function getTimeSeriesGraph(content, field) {
    // console.log('clicked' + ' ' + field)
	"use strict",
	data = []
	
    // console.log(data)
	function logArrayElements(element, index, array) {
        // console.log(element['Date'],element['Temperature'])
        dateFromPython = new Date(element['Date'])
        // console.log(dateFromPython)
        // data.push([ Date.UTC(dateFromPython.getUTCFullYear(), dateFromPython.getUTCMonth(), dateFromPython.getUTCDate(),  dateFromPython.getUTCHours(), dateFromPython.getUTCMinutes(), dateFromPython.getUTCSeconds() ), parseInt(element[field])])
        data.push([dateFromPython.getTime(), parseInt(element[field])])
	}	
	content.forEach(logArrayElements)

    // console.log(data)

	// console.log(data)
        $('#container').highcharts({
            chart: {
                zoomType: 'x',
		        width: 1032,
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
                // labels: {
                //     enabled: true
                // },
                // labels : {
                // formatter: function() {
                //     console.log(this.value)
                //     var myDate = new Date(this.value);
                //     // var newDateMs = Date.UTC(myDate.getUTCFullYear(),myDate.getUTCMonth()-1,myDate.getUTCDate());   
                    
                //     return Highcharts.dateFormat('%d-%b-%y %H:%M:%S',myDate);   

                //  } 
                // }
                

                // dateTimeLabelFormats: {
                //    day: '%d-%b-%y %H:%M:%S'    //ex- 01 Jan 2016
                // }
            },
            yAxis: {
                title: {
                    text: field
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
                    }//,
                    //threshold: null
                }
            },

            series: [{
                type: 'area',
                name: field + ' against Time',
                data: data
            }]
        
    });
};


function getScatterPlotGraph(content, field1, field2) {
    // console.log('clicked' + ' ' + field1 + ' ' + field2)
    "use strict",
    data = []
    
    function logArrayElements(element, index, array) {
        data.push([ parseFloat(element[field1]), parseInt(element[field2])])
    }   
    content.forEach(logArrayElements)

    $('#container').highcharts({
    chart: {
        type: 'scatter',
        zoomType: 'xy',
        width: 1032,
        height: 500
    },
    title: {
        text: field1 + ' Versus ' + field2
    },
    // subtitle: {
    //     text: 'Source: Heinz  2003'
    // },
    xAxis: {
        title: {
            enabled: true,
            text: field1
        },
        startOnTick: true,
        endOnTick: true,
        showLastLabel: true
    },
    yAxis: {
        title: {
            text: field2
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
        }]
        
    });
};


function getDoubleYAxisPlotGraph(content,field1,field2)
{
    "use strict",
    data1 = []
    data2 = []
    function logArrayElements(element, index, array) {
        dateFromPython = new Date(element['Date']) //.valueOf()
        data1.push( [dateFromPython.getTime(),parseFloat(element[field1])])
        data2.push( [dateFromPython.getTime(),parseFloat(element[field2])])
    }   
    content.forEach(logArrayElements)
    // console.log(data1)
    // console.log(data2)

    $('#container').highcharts({
        chart: {
            zoomType: 'xy',
            width: 1032,
            height: 500
        },
        title: {
            text: 'Pollutant Information from the Pod : ' + field1 + " and " + field2
        },
        subtitle: {
            text: 'UPOD Data'
        },
        // xAxis: [{
        //     categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        //         'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        //     crosshair: true
        // }],
        xAxis: {
                type: 'datetime'
            },
        yAxis: [{ // Primary yAxis
            labels: {
                // format: '{value}°C',
                style: {
                    color: Highcharts.getOptions().colors[1]
                }
            },
            title: {
                text: field2 ,
                style: {
                    color: Highcharts.getOptions().colors[1]
                }
            },
            opposite: true

        }, 
        { // Tertiary yAxis
            gridLineWidth: 0,
            title: {
                text: field1 ,
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
        }
         ],
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
        series: [
         {
            name: field1 ,
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
            name: field2 ,
            type: 'spline',
            yAxis: 0,
            data: data2,
            // tooltip: {
            //     valueSuffix: ' grams per cubic meter'
            // }
        }]
    });
}


function getBoxPlotGraph(content,field) {
    // console.log('clicked')
    "use strict",
    data = []


    // dictContent['Temperature'] = splitLine[5]
    //             dictContent['Humidity'] = splitLine[6]
    //             dictContent['CO2'] = splitLine[7]
    //             dictContent['fig210_sens'] = splitLine[19]
    //             dictContent['fig280_sens'] = splitLine[21]
    //             dictContent['e2vo3_sens'] = splitLine[25]

    // Temperature = [];
    // Humidity = [];
    // CO2 = [];
    // fig210_sens = [];
    // fig280_sens = [];
    // e2vo3_sens = [];

    Field = [];

    function logArrayElements(element, index, array) {
        // Temperature.push([parseFloat(element['Temperature'])])
        // Humidity.push([parseFloat(element['Humidity'])])
        // CO2.push([parseFloat(element['CO2'])])
        // fig210_sens.push([parseFloat(element['fig210_sens'])])
        // fig280_sens.push([parseFloat(element['fig280_sens'])])
        // e2vo3_sens.push([parseFloat(element['e2vo3_sens'])])
        Field.push([parseFloat(element[field])])
    }   
    content.forEach(logArrayElements)  



    //get any percentile from an array
    function getPercentile(data, percentile) {
        data.sort(numSort);
        var index = (percentile/100) * data.length;
        var result;
        if (Math.floor(index) == index) {
             result = (data[(index-1)] + data[index])/2;
        }
        else {
            result = data[Math.floor(index)];
        }
        return result;
    }
    //because .sort() doesn't sort numbers correctly
    function numSort(a,b) { 
        return a - b; 
    } 


    //wrap the percentile calls in one method
    function getBoxValues(data) {
        var boxValues = [];
        boxValues.push(Math.min.apply(Math,data));
        boxValues.push(getPercentile(data, 25));
        boxValues.push(getPercentile(data, 50));
        boxValues.push(getPercentile(data, 75));
        boxValues.push(Math.max.apply(Math,data));
        return boxValues;
    }
    console.log(getBoxValues(Field))
    data.push(getBoxValues(Field));
    // data.push(getBoxValues(Humidity));
    // data.push(getBoxValues(CO2));
    // data.push(getBoxValues(fig210_sens));
    // data.push(getBoxValues(fig280_sens));
    // data.push(getBoxValues(e2vo3_sens));

    // data.push(temperatureBoxPlot)
    // console.log(temperatureBoxPlot, humidityBoxPlot, co2BoxPlot, fig210_sensBoxPlot, fig280_sensBoxPlot, e2vo3_sensBoxPlot)
    

        
    // console.log(data)
    


    // console.log(data)
    $('#container').highcharts(
    {
        chart: {
            type: 'boxplot',
            width: 1032,
            height: 500
        },
    
        title: {
            text: 'Box Plot for ' + field
        },
    
        legend: {
            enabled: false
        },
    
        xAxis: {
            categories: field, //['Temperature'],//, 'Humidity', 'CO2', 'fig210_sens', 'fig280_sens', 'e2vo3_sens'],
            title: {
                text: 'Pollutant'
            }
        },
    
        yAxis: {
            title: {
                text: 'Observations'
            }
            //,
            // plotLines: [{
            //     value: 932,
            //     color: 'red',
            //     width: 1,
            //     label: {
            //         text: 'Theoretical mean: 932',
            //         align: 'center',
            //         style: {
            //             color: 'gray'
            //         }
            //     }
            // }]
        },
    
        series: [{
            name: 'Observations',
            data: data,
            // tooltip: {
            //     headerFormat: '<em>Experiment No {point.key}</em><br/>'
            // }
        }]
    
    });
};


function getCompareTimeSeriesGraph(content1,content2, field) {
    // console.log('clicked' + ' ' + field)
    "use strict",
    data1 = []
    data2 = []
    
    // console.log(data)
    function logArrayElements1(element, index, array) {
        // console.log(element['Date'],element['Temperature'])
        dateFromPython = new Date(element['Date'])
        // data1.push([ Date.UTC(dateFromPython.getUTCFullYear(), dateFromPython.getUTCMonth(), dateFromPython.getUTCDate(),  dateFromPython.getUTCHours(), dateFromPython.getUTCMinutes(), dateFromPython.getUTCSeconds() ), parseInt(element[field])])
        data1.push([dateFromPython.getTime(),parseInt(element[field])])
    } 
    function logArrayElements2(element, index, array) {
        // console.log(element['Date'],element['Temperature'])
        dateFromPython = new Date(element['Date'])
        // data2.push([ Date.UTC(dateFromPython.getUTCFullYear(), dateFromPython.getUTCMonth(), dateFromPython.getUTCDate(),  dateFromPython.getUTCHours(), dateFromPython.getUTCMinutes(), dateFromPython.getUTCSeconds() ), parseInt(element[field])])
        data2.push([dateFromPython.getTime(),parseInt(element[field])])
    }   
    content1.forEach(logArrayElements1)
    content2.forEach(logArrayElements2)

    // console.log(data1[0])
    // console.log(data2[0])
    // console.log(data1)
    // console.log(data2)

    // console.log(data1)
    // console.log(data2)
    // console.log(data1)
    // console.log(data)
    //     $('#container').highcharts({
    //     chart: {
    //         type: 'spline'
    //     },
    //     title: {
    //         text: field + ' against Time'
    //     },
    //     subtitle: {
    //         text: 'Comparing the pollutant ' + field + ' between two PODS'
    //     },
    //     xAxis: {
    //         type: 'datetime',
    //         // dateTimeLabelFormats: { // don't display the dummy year
    //         //     month: '%e. %b',
    //         //     year: '%b'
    //         // },
    //         title: {
    //             text: 'Date'
    //         }
    //     },
    //     yAxis: {
    //         title: {
    //             text: 'Temperature (C)'
    //         },
    //         min: 0
    //     },
    //     tooltip: {
    //         headerFormat: '<b>{series.name}</b><br>',
    //         pointFormat: '{point.x:%e. %b}: {point.y:.2f} m'
    //     },

    //     plotOptions: {
    //         spline: {
    //             marker: {
    //                 enabled: true
    //             }
    //         }
    //     },

    //     series: [{
    //         name: 'First Pod',
    //         // Define the data points. All series have a dummy year
    //         // of 1970/71 in order to be compared on the same x axis. Note
    //         // that in JavaScript, months start at 0 for January, 1 for February etc.
    //         data: data1
    //     }
    //     , {
    //         name: 'Second Pod',
    //         data: data2
    //     } 
    //     ]
    // });
$('#container').highcharts({
            chart: {
                zoomType: 'x',
                width: 1032,
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
                    text: field
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
                // area1: {
                //     fillColor: {
                //         linearGradient: {
                //             x1: 0,
                //             y1: 0,
                //             x2: 0,
                //             y2: 1
                //         },
                //         stops: [
                //             [0, Highcharts.getOptions().colors[1]],
                //             [1, Highcharts.Color(Highcharts.getOptions().colors[1]).setOpacity(0).get('rgba')]
                //         ]
                //     },
                //     marker: {
                //         radius: 2
                //     },
                //     lineWidth: 1,
                //     states: {
                //         hover: {
                //             lineWidth: 1
                //         }
                //     },
                //     threshold: null
                // }
            },

            series: [{
                type: 'area',
                name: field + ' against Time' + " for POD1",
                data: data1,
                color: Highcharts.getOptions().colors[8],
                fillColor : {
                                linearGradient : [0, 0, 0, 100],
                                stops : [
                                            [0, Highcharts.getOptions().colors[8]],
                                            [1, Highcharts.Color(Highcharts.getOptions().colors[8]).setOpacity(0.3).get('rgba')]
                                        ]
                            }
                    },
            {
                type: 'area',
                name: field + ' against Time' + " for POD2",
                data: data2,
                color: Highcharts.getOptions().colors[2],
                fillColor : {
                                linearGradient : [0, 0, 0, 100],
                                stops : [
                                            [0, Highcharts.getOptions().colors[2]],
                                            [1, Highcharts.Color(Highcharts.getOptions().colors[2]).setOpacity(0.3).get('rgba')]
                                        ]
                            }
            }
            ]
        
    });
};

function getCompareScatterPlotGraph(content1, content2, field1, field2) {
    // console.log('clicked' + ' ' + field1 + ' ' + field2)
    "use strict",
    data1 = []
    data2 = []

    function logArrayElements1(element, index, array) {
        data1.push([ parseFloat(element[field1]), parseInt(element[field2])])
    }   
    content1.forEach(logArrayElements1)
    function logArrayElements2(element, index, array) {
        data2.push([ parseFloat(element[field1]), parseInt(element[field2])])
    }   
    content2.forEach(logArrayElements2)

    $('#container').highcharts({
    chart: {
        type: 'scatter',
        zoomType: 'xy',
        width: 1032,
        height: 500
    },
    title: {
        text: field1 + ' Versus ' + field2
    },
    // subtitle: {
    //     text: 'Source: Heinz  2003'
    // },
    xAxis: {
        title: {
            enabled: true,
            text: field1
        },
        startOnTick: true,
        endOnTick: true,
        showLastLabel: true
    },
    yAxis: {
        title: {
            text: field2
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
        },
        {
        name: field1 + ' Versus ' + field2 + ' for POD2',
        color: Highcharts.getOptions().colors[2],
        data: data2
        }

        ]
        
    });
};



function getCompareBoxPlotGraph(content1,content2,field) {
    // console.log('clicked')
    "use strict",
    data1 = []
    data2 = []

    // dictContent['Temperature'] = splitLine[5]
    //             dictContent['Humidity'] = splitLine[6]
    //             dictContent['CO2'] = splitLine[7]
    //             dictContent['fig210_sens'] = splitLine[19]
    //             dictContent['fig280_sens'] = splitLine[21]
    //             dictContent['e2vo3_sens'] = splitLine[25]

    // Temperature1 = [];
    // Humidity1 = [];
    // CO21 = [];
    // fig210_sens1 = [];
    // fig280_sens1 = [];
    // e2vo3_sens1 = [];


    // Temperature2 = [];
    // Humidity2 = [];
    // CO22 = [];
    // fig210_sens2 = [];
    // fig280_sens2 = [];
    // e2vo3_sens2 = [];

    Field1 = [];
    Field2 = [];

    function logArrayElements1(element, index, array) {
        Field1.push(parseFloat(element[field]))
        // Temperature1.push([parseFloat(element['Temperature'])])
        // Humidity1.push([parseFloat(element['Humidity'])])
        // CO21.push([parseFloat(element['CO2'])])
        // fig210_sens1.push([parseFloat(element['fig210_sens'])])
        // fig280_sens1.push([parseFloat(element['fig280_sens'])])
        // e2vo3_sens1.push([parseFloat(element['e2vo3_sens'])])
    }   
    content1.forEach(logArrayElements1)  

    function logArrayElements2(element, index, array) {
        Field2.push(parseFloat(element[field]))
        // Temperature2.push([parseFloat(element['Temperature'])])
        // Humidity2.push([parseFloat(element['Humidity'])])
        // CO22.push([parseFloat(element['CO2'])])
        // fig210_sens2.push([parseFloat(element['fig210_sens'])])
        // fig280_sens2.push([parseFloat(element['fig280_sens'])])
        // e2vo3_sens2.push([parseFloat(element['e2vo3_sens'])])
    }   
    content2.forEach(logArrayElements2)  

    //get any percentile from an array
    // function getPercentile(data, percentile) {
    //     data.sort(numSort);
    //     var index = (percentile/100) * data.length; 
    //     var result;
    //     if (Math.floor(index) == index) {
    //         // console.log("Inside If: " + index ) 
    //          // console.log((data[(index-1)][0] + data[index][0]))
    //          result = [(data[(index-1)][0] + data[index][0])/2];
    //     }
    //     else {
    //         result = data[Math.floor(index)];
    //     }
    //     // console.log(result)
    //     return result;
    // }


    function getPercentile(data, percentile) {
        data.sort(numSort);
        var index = (percentile/100) * data.length;
        var result;
        if (Math.floor(index) == index) {
             result = (data[(index-1)] + data[index])/2;
        }
        else {
            result = data[Math.floor(index)];
        }
        return result;
    }

    //because .sort() doesn't sort numbers correctly
    function numSort(a,b) { 
        return a - b; 
    } 


    //wrap the percentile calls in one method
    function getBoxValues(data) {
        var boxValues = [];
        boxValues.push(Math.min.apply(Math,data));
        boxValues.push(getPercentile(data, 25));
        // console.log("Median",getPercentile(data, 50)[0] ) 
        boxValues.push(getPercentile(data, 50));
        boxValues.push(getPercentile(data, 75));
        boxValues.push(Math.max.apply(Math,data));
        return boxValues;
    }

    data1.push(getBoxValues(Field1));
    // console.log(data1)
    data2.push(getBoxValues(Field2));
    // console.log(data2)
    // data.push(getBoxValues(Humidity));
    // data.push(getBoxValues(CO2));
    // data.push(getBoxValues(fig210_sens));
    // data.push(getBoxValues(fig280_sens));
    // data.push(getBoxValues(e2vo3_sens));

    // data.push(temperatureBoxPlot)
    // console.log(temperatureBoxPlot, humidityBoxPlot, co2BoxPlot, fig210_sensBoxPlot, fig280_sensBoxPlot, e2vo3_sensBoxPlot)
    

        
    // console.log(data)
    


    // console.log(data)
    $('#container').highcharts(
    {
        chart: {
            type: 'boxplot',
            width: 1032,
            height: 500
        },
    
        title: {
            text: 'Box Plot for the pollutant ' + field
        },
    
        legend: {
            enabled: false
        },
    
        xAxis: {
            categories: [field],//['Temperature'],//, 'Humidity', 'CO2', 'fig210_sens', 'fig280_sens', 'e2vo3_sens'],
            title: {
                text: 'Pollutant'
            }
        },
    
        yAxis: {
            title: {
                text: 'Observations'
            }
            //,
            // plotLines: [{
            //     value: 932,
            //     color: 'red',
            //     width: 1,
            //     label: {
            //         text: 'Theoretical mean: 932',
            //         align: 'center',
            //         style: {
            //             color: 'gray'
            //         }
            //     }
            // }]
        },
    
        series: [{
            name: 'POD1',
            data: data1,
            // tooltip: {
            //     headerFormat: '<em>Experiment No {point.key}</em><br/>'
            // }
        },
        {
            name: 'POD2',
            data: data2,
            // tooltip: {
            //     headerFormat: '<em>Experiment No {point.key}</em><br/>'
            // }
        }

        ]
    
    });
};

