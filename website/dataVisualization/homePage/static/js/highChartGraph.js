// var getGraph = (function (content) {
function getTimeSeriesGraph(content, field) {
    console.log('clicked' + ' ' + field)
	"use strict",
	data = []
	
    // console.log(data)
	function logArrayElements(element, index, array) {
        // console.log(element['Date'],element['Temperature'])
        dateFromPython = new Date(element['Date'])
        data.push([ Date.UTC(dateFromPython.getUTCFullYear(), dateFromPython.getUTCMonth(), dateFromPython.getUTCDate(),  dateFromPython.getUTCHours(), dateFromPython.getUTCMinutes(), dateFromPython.getUTCSeconds() ), parseInt(element[field])])
	}	
	content.forEach(logArrayElements)

	// console.log(data)
        $('#container').highcharts({
            chart: {
                zoomType: 'x',
		width: 1032,
		height: 400
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
                enabled: false
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
                    },
                    threshold: null
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
    console.log('clicked' + ' ' + field1 + ' ' + field2)
    "use strict",
    data = []
    
    function logArrayElements(element, index, array) {
        data.push([ parseFloat(element[field1]), parseInt(element[field2])])
    }   
    content.forEach(logArrayElements)

    $('#container').highcharts({
    chart: {
        type: 'scatter',
        zoomType: 'xy'
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


function getBoxPlotGraph(content) {
    console.log('clicked')
    "use strict",
    data = []


    // dictContent['Temperature'] = splitLine[5]
    //             dictContent['Humidity'] = splitLine[6]
    //             dictContent['CO2'] = splitLine[7]
    //             dictContent['fig210_sens'] = splitLine[19]
    //             dictContent['fig280_sens'] = splitLine[21]
    //             dictContent['e2vo3_sens'] = splitLine[25]

    Temperature = [];
    Humidity = [];
    CO2 = [];
    fig210_sens = [];
    fig280_sens = [];
    e2vo3_sens = [];

    function logArrayElements(element, index, array) {
        Temperature.push([parseFloat(element['Temperature'])])
        Humidity.push([parseFloat(element['Humidity'])])
        CO2.push([parseFloat(element['CO2'])])
        fig210_sens.push([parseFloat(element['fig210_sens'])])
        fig280_sens.push([parseFloat(element['fig280_sens'])])
        e2vo3_sens.push([parseFloat(element['e2vo3_sens'])])
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
        boxValues.push(getPercentile(data, 25)[0]);
        boxValues.push(getPercentile(data, 50)[0]);
        boxValues.push(getPercentile(data, 75)[0]);
        boxValues.push(Math.max.apply(Math,data));
        return boxValues;
    }

    data.push(getBoxValues(Temperature));
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
            type: 'boxplot'
        },
    
        title: {
            text: 'Box Plot for different pollutants'
        },
    
        legend: {
            enabled: false
        },
    
        xAxis: {
            categories: ['Temperature'],//, 'Humidity', 'CO2', 'fig210_sens', 'fig280_sens', 'e2vo3_sens'],
            title: {
                text: 'Pollutant'
            }
        },
    
        yAxis: {
            title: {
                text: 'Observations'
            },
            plotLines: [{
                value: 932,
                color: 'red',
                width: 1,
                label: {
                    text: 'Theoretical mean: 932',
                    align: 'center',
                    style: {
                        color: 'gray'
                    }
                }
            }]
        },
    
        series: [{
            name: 'Observations',
            data: data,
            tooltip: {
                headerFormat: '<em>Experiment No {point.key}</em><br/>'
            }
        // }, {
        //     name: 'Outlier',
        //     color: Highcharts.getOptions().colors[0],
        //     type: 'scatter',
        //     data: [ // x, y positions where 0 is the first category
        //         [0, 644],
        //         [4, 718],
        //         [4, 951],
        //         [4, 969]
        //     ],
        //     marker: {
        //         fillColor: 'white',
        //         lineWidth: 1,
        //         lineColor: Highcharts.getOptions().colors[0]
        //     },
        //     tooltip: {
        //         pointFormat: 'Observation: {point.y}'
        //     }
        }]
    
    });
};

