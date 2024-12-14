let homeworksList = {};
getList();

function saveList() {
  fetch("/saveList", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ list: homeworksList }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Server response:", data);
    })
    .catch((error) => {
      console.error("Query error:", error);
    });
}

async function getList() {
  try {
    const response = await fetch("/getList");
    const data = await response.json();

    if (data.list) {
      homeworksList = data.list;
      addHomeworkWObtn(homeworksList);
    } else {
      console.log("No list found.");
      return null;
    }
  } catch (error) {
    console.error("Error retrieving list:", error);
    return null;
  }
}

function loadHomeworkMeter() {
  const homeworksMeter = document.querySelectorAll("#homework-meter");
  homeworksMeter.forEach((homeworkMeter) => {
    const parent = homeworkMeter.parentNode;
    const homeworks = parent.querySelector(
      ".no-overflow .scroll-content .homeworks-info .homeworks"
    );
    const homeworkNumber = getHomeworkNumber(homeworks);

    homeworkMeter.querySelector("p").innerHTML = homeworkNumber;
    if (homeworkNumber == 0) {
      homeworkMeter.style.display = "none";
    } else {
      homeworkMeter.style.display = "flex";
    }
  });

  saveList();
}

function getHomeworkNumber(homeworks) {
  return homeworks.children.length;
}

const plgDatas = document.querySelectorAll(".plg-data");
plgDatas.forEach((data) => {
  const scrollContent = data.querySelector(".no-overflow .scroll-content");
  const addHomeworkBtn = data.querySelector(
    ".no-overflow .scroll-content .homeworks-info #add-homework"
  );

  data.addEventListener("click", (e) => {
    if (e.target.parentNode == addHomeworkBtn) {
      addHomework(addHomeworkBtn);
    } else if (e.target.id == "del-homework") {
      delHomework(e.target.parentNode);
    } else {
      switchInfoDisplay(scrollContent);
    }
  });
});

function switchInfoDisplay(btn) {
  const courseInfo = btn.querySelector(".course-info");
  const homeworksInfo = btn.querySelector(".homeworks-info");

  courseInfo.classList.toggle("info-display-func");
  homeworksInfo.classList.toggle("info-display-func");
  btn.classList.toggle("btn-scale-func");
}

function addHomework(btn) {
  const parent = btn.parentNode;
  const homeworks = parent.querySelector(".homeworks");
  const firstParent = parent.parentNode.parentNode.parentNode;
  const courseName = firstParent.classList[4];
  const courseId = firstParent.id;

  const homework = prompt(`Add a homework : ${courseName}`);

  if (homework) {
    const div = document.createElement("div");
    const span = document.createElement("span");
    const p = document.createElement("p");

    p.innerText = homework;
    span.id = "del-homework";
    span.innerHTML = "x";

    div.appendChild(p);
    div.appendChild(span);

    homeworks.appendChild(div);
    if (!homeworksList[courseId]) {
      homeworksList[courseId] = [];
    }
    homeworksList[courseId].push(homework);
    loadHomeworkMeter();
  }
  // else {
  //   console.log("canceled");
  // }
}

function addHomeworkWObtn(lst) {
  const plgDatas = document.querySelectorAll(".plg-data");

  plgDatas.forEach((data) => {
    if (data.id in lst) {
      homeworks = data.querySelector(
        ".no-overflow .scroll-content .homeworks-info .homeworks"
      );

      homeworksList[data.id].forEach((hw) => {
        const div = document.createElement("div");
        const span = document.createElement("span");
        const p = document.createElement("p");

        p.innerText = hw;
        span.id = "del-homework";
        span.innerHTML = "x";

        div.appendChild(p);
        div.appendChild(span);
        homeworks.appendChild(div);

        loadHomeworkMeter();
      });
    }
  });
}

function delHomework(btn) {
  const parent = btn.parentNode;
  const firstParent = parent.parentNode.parentNode.parentNode.parentNode;
  const courseId = firstParent.id;
  const hwText = btn.querySelector("p").innerHTML;

  if (courseId in homeworksList) {
    for (let i = 0; i < homeworksList[courseId].length; i++) {
      if (homeworksList[courseId][i] == hwText) {
        homeworksList[courseId].splice(i, 1);
        break;
      }
    }
  }

  parent.removeChild(btn);
  loadHomeworkMeter();
}

document.addEventListener("DOMContentLoaded", () => {
  addHomeworkWObtn(homeworksList);
  loadHomeworkMeter();
});
