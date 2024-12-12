
const hds = document.querySelectorAll('.hidden-box');


function showInfos(curO) {
    chd = curO.querySelector(".hidden-box");
    document.body.addEventListener('mousemove', e => {
        chd.style.left = e.layerX + "px";
        chd.style.top = e.layerY + "px";
    });
}