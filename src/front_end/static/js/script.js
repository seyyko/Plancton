let homeworkList = JSON.parse(localStorage.getItem('homeworkList')) || {};

document.getElementById("plg-form").addEventListener("submit", async function (event) {
  // event.preventDefault();

  const formData = new FormData(event.target);
  const response = await fetch("/plg", {
      method: "POST",
      body: formData
  });

  if (response.ok) {
      const data = await response.text();
      console.log(data);
  }
});

// Clear the homework list from localStorage
function clearList() {
  localStorage.removeItem('homeworkList');
  console.log("List has been removed successfully!");
}

// Save the homework list to localStorage and sync with the server
function saveList() {
  localStorage.setItem("homeworkList", JSON.stringify(homeworkList));
  homeworkList = JSON.parse(localStorage.getItem('homeworkList'));
  console.log("List has been saved successfully!");
  syncWithServer(); // Sync with the server after saving
}

// Clear the database on Mondays
function clearListOnMonday() {
  const today = new Date();
  const dayOfWeek = today.getDay(); // 0 = Sunday, 1 = Monday, ..., 6 = Saturday

  if (dayOfWeek === 1) { // Check if it's Monday
    const lastClearDate = localStorage.getItem("lastClearDate");
    const todayDateString = today.toISOString().split("T")[0]; // Format YYYY-MM-DD

    if (lastClearDate !== todayDateString) { // If not cleared today
      clearList();
      localStorage.setItem("lastClearDate", todayDateString); // Update the clear date
      console.log("Data cleared for the week.");
    } else {
      console.log("Data already cleared today.");
    }
  }
}

// Synchronize localStorage with the server
async function syncWithServer() {
  try {
    const response = await fetch('/sync', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(homeworkList), // Send the current homework list
    });

    const result = await response.json();
    if (response.ok) {
      console.log(result.message);
    } else {
      console.error("Error syncing with server:", result.message);
    }
  } catch (error) {
    console.error("Error during syncWithServer:", error);
  }
}

// Load data from server to localStorage
async function loadFromServer() {
  try {
    const response = await fetch('/load');
    if (response.ok) {
      const data = await response.json();
      homeworkList = data || {}; // Load data into homeworkList
      localStorage.setItem('homeworkList', JSON.stringify(homeworkList)); // Save to localStorage
      updateHomeworkDisplay(homeworkList); // Update UI
      console.log("Data loaded from server successfully.");
    } else {
      console.error("Error loading from server:", await response.text());
    }
  } catch (error) {
    console.error("Error during loadFromServer:", error);
  }
}

// Initialize the app on document load
document.addEventListener("DOMContentLoaded", async () => {
  try {
    clearListOnMonday();   // Clear the database on Mondays
    await loadFromServer(); // Load data from server on page load

    // Synchronize every 5 minutes (300000ms)
    setInterval(async () => {
      await syncWithServer();
    }, 300000); // 5 minutes
  } catch (error) {
    console.error("Error during initialization:", error);
  }
});

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('plg-form');

  // Fonction pour restaurer les données du localStorage dans le formulaire
  function restoreFormData() {
      const savedData = localStorage.getItem('plgFormData');
      if (savedData) {
          const formData = JSON.parse(savedData);
          Object.keys(formData).forEach(key => {
              const input = document.querySelector(`#plg-form [name="${key}"]`);
              if (input) {
                  input.value = formData[key];
              }
          });
      }
  }

  // Écouteur sur le formulaire pour sauvegarder les données lors de la soumission
  form.addEventListener('submit', () => {
      const formData = {
          semester: form.querySelector('[name="semester"]').value,
          group: form.querySelector('[name="group"]').value,
          group_week: form.querySelector('[name="group_week"]').value
      };
      localStorage.setItem('plgFormData', JSON.stringify(formData));
  });

  // Restaurer les données au chargement de la page
  restoreFormData();
});


// Get the number of homeworks in a course
function getHomeworkCount(homeworks) {
  return homeworks.children.length; // Return the number of child elements (homework items)
}

// Update the homework meter for each course (display homework count)
function updateHomeworkMeter() {
  const homeworkMeters = document.querySelectorAll("#homework-meter");
  homeworkMeters.forEach((homeworkMeter) => {
    const parent = homeworkMeter.parentNode;
    const homeworks = parent.querySelector(
      ".no-overflow .scroll-content .homeworks-info .homeworks"
    );
    const homeworkCount = getHomeworkCount(homeworks); // Get the number of homeworks

    homeworkMeter.querySelector("p").innerHTML = homeworkCount; // Display the count
    homeworkMeter.style.display = homeworkCount == 0 ? "none" : "flex"; // Hide if no homework
  });

  saveList(); // Save homework list to localStorage
}

// Handle the planning data (each course's homework list)
const planningDataElements = document.querySelectorAll(".plg-data");
planningDataElements.forEach((data) => {
  const scrollContent = data.querySelector(".no-overflow .scroll-content");
  const addHomeworkBtn = data.querySelector(
    ".no-overflow .scroll-content .homeworks-info #add-homework"
  );

  data.addEventListener("click", (e) => {
    if (e.target.parentNode == addHomeworkBtn) {
      addHomework(addHomeworkBtn); // Add homework when button is clicked
    } else if (e.target.id == "del-homework") {
      removeHomework(e.target.parentNode); // Remove homework when delete button is clicked
    } else {
      toggleInfoDisplay(scrollContent); // Toggle display of course/homework info
    }
  });
});

// Toggle the visibility of course and homework info
function toggleInfoDisplay(button) {
  const courseInfo = button.querySelector(".course-info");
  const homeworksInfo = button.querySelector(".homeworks-info");

  courseInfo.classList.toggle("info-display-func");     // Toggle course info visibility
  homeworksInfo.classList.toggle("info-display-func");  // Toggle homework info visibility
  button.classList.toggle("btn-scale-func");            // Animate the button scaling
}

function createHomeworkElement(homework) {
  const div = document.createElement("div");
  const span = document.createElement("span");
  const p = document.createElement("p");

  p.innerText = homework; // Set the homework text
  span.id = "del-homework";
  span.innerHTML = "x"; // Set the delete button

  div.appendChild(p);     // Append the homework text
  div.appendChild(span);  // Append the delete button
  return div;
}

// Add a new homework to the course
function addHomework(button) {
  const parent = button.parentNode;
  const homeworks = parent.querySelector(".homeworks");
  const courseElement = parent.closest(".plg-data");
  const courseName = courseElement.classList[4];
  const courseId = courseElement.id;

  const homework = prompt(`Add a homework for: ${courseName}`);
  if (homework) {
    const div = createHomeworkElement(homework);
    homeworks.appendChild(div);

    if (!homeworkList[courseId]) {
      homeworkList[courseId] = [];
    }
    homeworkList[courseId].push(homework);

    updateHomeworkMeter();
    syncWithServer(); // Sync with server after adding homework
  }
}

// Update the homework display (for courses without buttons)
function updateHomeworkDisplay(list) {
  const planningDataElements = document.querySelectorAll(".plg-data");

  planningDataElements.forEach((data) => {
    if (data.id in list) {
      const homeworksContainer = data.querySelector(
        ".no-overflow .scroll-content .homeworks-info .homeworks"
      );

      list[data.id].forEach((homework) => {
        const div = createHomeworkElement(homework);
        homeworksContainer.appendChild(div);
      });
    }
  });

  updateHomeworkMeter(); // Update the homework count display
}

// Remove a homework from the course
function removeHomework(button) {
  const parent = button.parentNode;
  const courseElement = parent.closest(".plg-data");
  const courseId = courseElement.id;
  const homeworkText = button.querySelector("p").innerHTML;

  if (courseId in homeworkList) {
    homeworkList[courseId] = homeworkList[courseId].filter(
      (homework) => homework !== homeworkText
    );
  }

  parent.removeChild(button);
  updateHomeworkMeter();
  syncWithServer(); // Sync with server after removing homework
}
