var numGensSlider = document.getElementById("numGensSlider");
var numGensValue = document.getElementById("numGensValue");
var numGens = document.getElementById("numGens");
numGensValue.innerHTML = numGensSlider.value;
numGens.innerHTML = numGensSlider.value;
numGensSlider.oninput = function() {
    numGensValue.innerHTML = this.value;
    numGens.innerHTML = this.value;
}

var popSizeSlider = document.getElementById("popSizeSlider");
var popSizeValue = document.getElementById("popSizeValue");
popSizeValue.innerHTML = popSizeSlider.value;
popSizeSlider.oninput = function() {
    popSizeValue.innerHTML = this.value;
}

var lifespanSlider = document.getElementById("lifespanSlider");
var lifespanValue = document.getElementById("lifespanValue");
lifespanValue.innerHTML = lifespanSlider.value;
lifespanSlider.oninput = function() {
    lifespanValue.innerHTML = this.value;
}

var numGenesSlider = document.getElementById("numGenesSlider");
var numGenesValue = document.getElementById("numGenesValue");
numGenesValue.innerHTML = numGenesSlider.value;
numGenesSlider.oninput = function() {
    numGenesValue.innerHTML = this.value;
}

var muteProbSlider = document.getElementById("muteProbSlider");
var muteProbValue = document.getElementById("muteProbValue");
muteProbValue.innerHTML = muteProbSlider.value;
muteProbSlider.oninput = function() {
    muteProbValue.innerHTML = this.value;
}

var mateProbSlider = document.getElementById("mateProbSlider");
var mateProbValue = document.getElementById("mateProbValue");
mateProbValue.innerHTML = mateProbSlider.value;
mateProbSlider.oninput = function() {
    mateProbValue.innerHTML = this.value;
}