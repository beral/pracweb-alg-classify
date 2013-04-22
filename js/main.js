// vim: et si sw=2

function btnClear_do() {
  var $input = $("#inputData");
  $input.val("");
  $input.change();
}

function btnRandom_do() {
  var $input = $("#inputData");
  var text = "";
  var data = generateData();
  for (var i=0; i<data.length; ++i) {
    var item = data[i];
    text += item.x.toFixed(1) + " " 
          + item.y.toFixed(1) + " " 
          + item.c + " " 
          + (item.t?1:0) + "\n";
  }
  $input.val(text);
  $input.change();
}

function parseInput(text) {
  var comment = /^\s*(?:\/\/.*)?$/;
  var object = /^\s*(\S+)\s+(\S+)\s+(\S+)\s+([01])\s*$/;
  var lines = text.split("\n");
  var data = Array();
  for (var i=0; i<lines.length; ++i) {
    if (comment.test(lines[i]))
      continue;
    var match = object.exec(lines[i]);
    var broken = false;
    if (match) {
      match[1] = +match[1];
      match[2] = +match[2];
      match[4] = +match[4];
      if (!isNaN(match[1]) && !isNaN(match[2])) {
        data.push({
          line: i,
          valid: true,
          x: match[1],
          y: match[2],
          c: match[3],
          t: match[4]
        });
      }
      else
        broken = true;
    } // if (match)
    else
      broken = true;
    if (broken) {
      data.push({
        line: i,
        valid: false,
        text: lines[i]
      });
    }
  }
  return data;
}

// STUB: generate a random data set
function generateData() {
  var data = new Array();
  var gen1 = d3.random.normal(10, 5);
  var gen2 = d3.random.normal(20, 7);
  var gen3 = d3.random.normal(25, 5);
  var gen4 = d3.random.normal(5, 30);
  for (var i=0; i<25; ++i) {
    data.push({x: gen1(), 
        y: gen2(), 
        c: "first",
        t: Math.random() > 0.7});
  }
  for (var i=0; i<25; ++i) {
    data.push({x: gen3(), 
        y: gen4(), 
        c: "second",
        t: Math.random() > 0.6});
  }
  return data;
}

function smartExtent(data, accessor) {
  if (!data.length)
    return [0, 1];
  if (data.length == 1)
  {
    var d = accessor(data[0]);
    return [d-1, d+1];
  }
  var extent = d3.extent(data, accessor);
  var med = (extent[0] + extent[1]) / 2;
  var delta = 0.1 * (med - extent[0]);
  extent[0] -= delta;
  extent[1] += delta;
  return extent;
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

  x.domain(smartExtent(data, function(d) { return d.x; })).nice();
  y.domain(smartExtent(data, function(d) { return d.y; })).nice();

  // X axis
  svg.selectAll("#xAxis")
    .data([width]).enter()
    .append("g")
    .attr("id", "xAxis")
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
  svg.selectAll("#yAxis")
    .data([height]).enter()
    .append("g")
    .attr("id", "yAxis")
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
    .filter(function(d) { return d.valid; })
    .data(data)
    .enter().append("path")
    .attr("class", "dot")
    .attr("transform", function(d) { return "translate(" + x(d.x) + "," + y(d.y) + ")"; })
    .attr("d", d3.svg.symbol()
        .type(function(d) { return d.t? "triangle-up" : "circle"; })
        .size(50))
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

function drawObjTable(data) {
  var table = d3.select("#objTable tbody");
  
  var object = table.selectAll(".object").data(data);

  object.enter().append("tr")
    .attr("class", "object");

  object.each(function(d) {
    var object = d3.select(this),
        line = d.line + 1;
    if (d.valid)
      object
        .classed("error", false)
        .html("<td>" + line + "</td>"
          + "<td>" + d.x + "</td>"
          + "<td>" + d.y + "</td>"
          + "<td>" + d.c + "</td>"
          + "<td>" + d.t + "</td>");
    else
      object
        .classed("error", true)
        .html("<td>" + line + "</td>"
          + "<td colspan=4><span class=\"label label-important\">Синтаксическая ошибка</span>" 
          + "<pre>" + d.text + "</pre></td>");
  });

  object.exit().remove();
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
var pracData = [];

// Initialization
$(window).load(function() {
  updateViewport();
  $("#inputData").change();
});
$("#inputData").keyup(function() {
  $("#inputData").change();
});
$("#inputData").change(function() {
  pracData = parseInput($("#inputData").val());
  drawVisual(pracData, $("#viewport")[0]);
  drawObjTable(pracData);
});
//$(window).resize(updateViewport);