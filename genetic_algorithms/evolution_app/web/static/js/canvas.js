var mainCanvas = document.getElementById("grid");

var numFires = 0;
var numInds = -1;

mainCanvas.addEventListener("click", clickOnCanvas, false);

function clickOnCanvas(event) {
    const rect = this.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    document.getElementById("posX").innerHTML = x;
    document.getElementById("posY").innerHTML = y;
    createFire(this, x, y);
}

function createFire(x, y) {
    var newFire = document.createElement("div");
    newFire.innerHTML = "🔥";
    newFire.setAttribute("id", "fire" + numFires);
    newFire.setAttribute("class", "fires");
    mainCanvas.appendChild(newFire);
    newFire.style.left = (x - 20) + 'px';
    newFire.style.top = (y - 20) + 'px';
    newFire.style.zIndex = numFires + 1;
    numFires += 1;

    //Communicate python that another fire has been created.
}

function createIndividual(id) {
    var newInd = document.createElement("div");
    newInd.innerHTML = "🚶🏻";
    newInd.setAttribute("id", "ind" + id);
    newInd.setAttribute("class", "inds");
    mainCanvas.appendChild(newInd);
    var mainRect = mainCanvas.getBoundingClientRect();
    newInd.style.left = (Math.random() * (mainRect.width - 20)) + 'px';
    newInd.style.top = (Math.random() * (mainRect.height - 25)) + 'px';
}

function updateIndividuals(selectedNumInds) {
    numInds = selectedNumInds;
    var inds = Array.from(document.getElementsByClassName("inds"));
    if (inds.length > 0) {
        console.log("hola");
        console.log(inds);
        inds.forEach(ind => {
            ind.remove();
        });
    }
    for (let i = 0; i < selectedNumInds; i++) {
        createIndividual(i);
    }
}

function drawRect(canvas, x, y) {
    var height = 20;
    var width = 20;

    var ctx = canvas.getContext("2d");
    ctx.font = "30px Arial";
    //ctx.beginPath();
    //ctx.rect(x - width/2, y - height/2, height, width);
    //ctx.stroke();
    ctx.fillText("🔥", x-20, y+5);
}