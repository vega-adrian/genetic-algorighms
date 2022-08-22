var mainGrid = document.getElementById("grid");

function updateGrid(h, w) {
    Array.from(document.getElementsByClassName("gridItem")).forEach(gridItem => gridItem.remove());
    mainGrid.style.gridTemplateColumns = "repeat(" + w + ", 5px)";
    mainGrid.style.gridTemplateRows = "repeat(" + w + ", 5px)";
    for (let ih = 0; ih < h; ih++) {
        for (let iw = 0; iw < w; iw++) {
            var newCell = document.createElement("div");
            newCell.setAttribute("id", "cell_" + ih + "-" + iw);
            newCell.setAttribute("class", "gridItem");
            mainGrid.appendChild(newCell);
        }
    }
}

var gridH = document.forms.settingsForm.gridH;
var gridW = document.forms.settingsForm.gridW;
updateGrid(gridH.value, gridW.value);
gridH.onchange = function() {
    updateGrid(this.value, gridW.value);
}
gridW.onchange = function() {
    updateGrid(gridH.value, this.value);
}


function plotIndividuals(coordinates) {
    Array.from(document.getElementsByClassName("gridItem")).forEach(e => e.style.backgroundColor = "white");
    for (let index = 0; index < coordinates.length; index++) {
        var gridItem = document.getElementById("cell_" + coordinates[index][0] + "-" + coordinates[index][1]);
        gridItem.style.backgroundColor = stringToColour("cell_" + coordinates[index][0] + "-" + coordinates[index][1]);
    }
}

fetch(
    "update_pop_size?pop_size=" + document.forms.settingsForm.popSizeSlider.value
    + "&maxY=" + gridH.value
    + "&maxX=" + gridW.value
)
    .then(function (response) {return response.json();})
    .then(function (json_data) {plotIndividuals(json_data);});
document.forms.settingsForm.popSizeSlider.onchange = function() {
    //createIndividuals(this.value);
    fetch("update_pop_size?pop_size=" + this.value + "&maxY=" + gridH.value + "&maxX=" + gridW.value)
        .then(function (response) {return response.json();})
        .then(function (json_data) {plotIndividuals(json_data);});
}

document.getElementById("startButton").onclick = function () {
    fetch("action/start")
        .then(function (response) {return response.text();})
        .then(function (text) {console.log(text);});
    
    fetch("action/evolve")
        .then(function (response) {return response.text();})
        .then(function (text) {console.log("New message:");console.log(text);});
    
    //var source = new EventSource("action/evolve");
    //source.onmessage = function (event) {
    //    console.log(event.data);
    //}
}
