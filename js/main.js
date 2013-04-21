// vim: et sw=2

// STUB: generate a random data set
function generateData() {
  var data = new Array();
  var gen1 = d3.random.normal(10, 5);
  var gen2 = d3.random.normal(20, 7);
  var gen3 = d3.random.normal(20, 5);
  var gen4 = d3.random.normal(5, 30);
  for (var i=0; i<25; ++i) {
    data.push({x: gen1(), 
        y: gen2(), 
        c: "Class A",
        t: Math.random() > 0.7});
  }
  for (var i=0; i<25; ++i) {
    data.push({x: gen3(), 
        y: gen4(), 
        c: "Class B",
        t: Math.random() > 0.6});
  }
  return data;
}

function drawVisual(data, viewport) {
  $(viewport).empty();

  var margin = {top: 20, right: 20, bottom: 30, left: 40},
      width = $(viewport).width() - margin.left - margin.right,
      height = $(viewport).height() - margin.top - margin.bottom;

  var x = d3.scale.linear()
    .range([0, width]);

  var y = d3.scale.linear()
    .range([height, 0]);

  var color = d3.scale.category10();

  var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

  var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left");

  var svg = d3.select(viewport)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  x.domain(d3.extent(data, function(d) { return d.x; })).nice();
  y.domain(d3.extent(data, function(d) { return d.y; })).nice();

  // X axis
  svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis)
    .append("text")
    .attr("class", "label")
    .attr("x", width)
    .attr("y", -6)
    .style("text-anchor", "end")
    .text("X");

  // Y axis
  svg.append("g")
    .attr("class", "y axis")
    .call(yAxis)
    .append("text")
    .attr("class", "label")
    .attr("transform", "rotate(-90)")
    .attr("y", 6)
    .attr("dy", ".71em")
    .style("text-anchor", "end")
    .text("Y")

    // Points
    svg.selectAll(".dot")
    .data(data)
    .enter().append("path")
    .attr("class", "dot")
    .attr("transform", function(d) { return "translate(" + x(d.x) + "," + y(d.y) + ")"; })
    .attr("d", d3.svg.symbol()
        .type(function(d) { return d.t? "triangle-up" : "circle"; })
        .size(function(d) { return d.t? 150 : 50; }))
    .style("fill", function(d) { return color(d.c); });

  // Legend
  var legend = svg.selectAll(".legend")
    .data(color.domain())
    .enter().append("g")
    .attr("class", "legend")
    .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

  // Color box
  legend.append("rect")
    .attr("x", width - 18)
    .attr("width", 18)
    .attr("height", 18)
    .style("fill", color);

  // Item label
  legend.append("text")
    .attr("x", width - 24)
    .attr("y", 9)
    .attr("dy", ".35em")
    .style("text-anchor", "end")
    .text(function(d) { return d; });
}

function updateViewport() {
  var viewport = $("#viewport")[0];
  fullSize = $(viewport).parent().width();
  $(viewport)
    .width(fullSize)
    .height(fullSize);
  drawVisual(pracData, viewport);
}


// Achtung: global variables!
var pracData = generateData();

// Initialization
$(window).load(updateViewport);
$(window).resize(updateViewport);
