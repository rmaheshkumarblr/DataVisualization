function lineGraph(data) 
{
	// console.log("Inside lineGraph")
	var margin = {top: 20, right: 20, bottom: 30, left: 50},
	    width = 960 - margin.left - margin.right,
	    height = 500 - margin.top - margin.bottom;
	
	// 2016-8-5 20:27:46
	var parseTime = d3.timeParse("%Y-%m-%d %H:%M:%S");
	
	// var data = {{ displayContent | safe }}
	
	data.forEach(function (d) {
	    d.date = parseTime(d.date);
	    // console.log(d.date)
	    d.temperature = d.temperature;
	    return d;
	});
	
	var x = d3.scaleTime()
	    .range([0, width]);
	
	var y = d3.scaleLinear()
	    .range([height, 0]);
	
	var line = d3.line()
	    .x(function(d) { return x(d.date); })
	    .y(function(d) { return y(d.temperature); });
	
	
	var svg = d3.select("body").selectAll("div.graph").append("svg")
	// append('div').attr('class', 'container').append("svg")
	    .attr("width", width + margin.left + margin.right)
	    .attr("height", height + margin.top + margin.bottom)
	  .append("g")
	    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
	
	(function() {
	
	  x.domain(d3.extent(data, function(d) { return d.date; }));
	  y.domain(d3.extent(data, function(d) { return d.temperature; }));
	
	  svg.append("g")
	      .attr("class", "axis axis--x")
	      .attr("transform", "translate(0," + height + ")")
	      .call(d3.axisBottom(x));
	
	  svg.append("g")
	      .attr("class", "axis axis--y")
	      .call(d3.axisLeft(y))
	    .append("text")
	      .attr("class", "axis-title")
	      .attr("transform", "rotate(-90)")
	      .attr("y", 6)
	      .attr("dy", ".71em")
	      .style("text-anchor", "end")
	      .text("Price ($)");
	
	  svg.append("path")
	      .datum(data)
	      .attr("class", "line")
	      .attr("d", line);
	// })
	})();
}
