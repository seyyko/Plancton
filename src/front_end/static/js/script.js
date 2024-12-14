const homeworksMeter = document.querySelectorAll("#homework-meter");
homeworksMeter.forEach((homeworkMeter) => {
  const parent = homeworkMeter.parentNode;
  console.log(parent);
  const homeworkNumber = parent.querySelector(
    ".no-overflow .scroll-content .homeworks-info"
  ).children.length;

  homeworkMeter.querySelector("p").innerHTML = homeworkNumber;

  if (homeworkNumber == 0) {
    homeworkMeter.style.display = "none";
  }
});

function switchInfoDisplay(btn) {
  const courseInfo = btn.querySelector(".course-info");
  const homeworksInfo = btn.querySelector(".homeworks-info");

  courseInfo.classList.toggle("info-display-func");
  homeworksInfo.classList.toggle("info-display-func");
  btn.classList.toggle("btn-scale-func");
}
