var mainGrid = document.getElementById("grid");
var gridH = document.forms.settingsForm.gridH;
var gridW = document.forms.settingsForm.gridW;

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

function plotIndividuals(individuals) {
    Array.from(document.getElementsByClassName("gridItem")).forEach(e => e.style.backgroundColor = "white");
    for (let index = 0; index < individuals.length; index++) {
        var coordX = individuals[index].coords[0];
        var coordY = individuals[index].coords[1];
        var color = individuals[index].color;
        var gridItem = document.getElementById("cell_" + coordX + "-" + coordY);
        gridItem.style.backgroundColor = stringToColor(color);
    }
}

function update_population() {
    fetch(
        "/update_population"
        + "?pop_size=" + popSizeSlider.value
        + "&lifespan=" + lifespanSlider.value
        + "&worldY=" + gridH.value
        + "&worldX=" + gridW.value
        + "&num_genes=" + numGenesSlider.value
    )
    .then(function (response) {return response.json();})
    .then(function (json_data) {plotIndividuals(json_data);});
}

function evolve() {
    for (let generationIdx = 0; generationIdx < 100; generationIdx++) {
        for (let stepIdx = 0; stepIdx < 60; stepIdx++) {
            fetch(
                "/evolve_step"
                + "?generationIdx=" + generationIdx
                + "&stepIdx=" + stepIdx
            )
            .then(function (response) {return response.json();})
            .then(function (json_data) {
                plotIndividuals(json_data);
            })
        }
    }
}



updateGrid(gridH.value, gridW.value);
gridH.onchange = function() {updateGrid(this.value, gridW.value);}
gridW.onchange = function() {updateGrid(gridH.value, this.value);}


var popSizeSlider = document.forms.settingsForm.popSizeSlider
var lifespanSlider = document.forms.settingsForm.lifespanSlider
var numGenesSlider = document.forms.settingsForm.numGenesSlider
update_population();
popSizeSlider.onchange = function() {update_population();};
lifespanSlider.onchange = function() {
    fetch("/update_lifespan?lifespan=" + lifespanSlider.value)
    .then()
};
numGenesSlider.onchange = function() {
    fetch("/update_num_genes?num_genes=" + numGenesSlider.value)
    .then(function (response) {return response.json();})
    .then(function (json_data) {plotIndividuals(json_data);});
};

document.getElementById("startButton").onclick = function () {evolve();};
