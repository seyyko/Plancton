let homeworkList = {};

// Function to clear the database on Mondays
function clearDatabaseOnMonday() {
  const today = new Date();
  const dayOfWeek = today.getDay(); // 0 = Sunday, 1 = Monday, ..., 6 = Saturday

  // Check if it's Monday
  if (dayOfWeek === 1) {
      const lastClearDate = localStorage.getItem("lastClearDate");
      const todayDateString = today.toISOString().split("T")[0]; // Format YYYY-MM-DD

      // If the database hasn't been cleared today
      if (lastClearDate !== todayDateString) {
          clearDatabase(); // Clear the database
          localStorage.setItem("lastClearDate", todayDateString); // Update the date
          console.log("Database cleared for the week.");
      } else {
          console.log("Database already cleared today.");
      }
  }
}

// Initialize the app on document load
document.addEventListener("DOMContentLoaded", async () => {
  try {
    await initializeDatabase();  // Wait for the database to be ready
    clearDatabaseOnMonday();     // Ensure the database is cleared on Monday
    await loadHomeworksFromDB(); // Load homework data from the database
    updateHomeworkMeter();       // Update the homework count display
  } catch (error) {
    console.error("Error during initialization:", error);
  }
});

// Load homeworks from IndexedDB
async function loadHomeworksFromDB() {
  const transaction = db.transaction(["homeworks"], "readonly");
  const store = transaction.objectStore("homeworks");

  const request = store.getAll();
  request.onsuccess = () => {
    const data = request.result;
    data.forEach((item) => {
      homeworkList[item.id] = item.tasks; // Store tasks for each course
    });
    // Update the display of homeworks without any buttons
    updateHomeworkDisplay(homeworkList);
  };

  request.onerror = (event) => {
    console.error("Error loading homeworks:", event.target.error);
  };
}

// Save the homework list to the database
function saveListToDB() {
  addHomeworks(homeworkList); // Save the homework list using the function from indexeddbHandler.js
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

  saveListToDB(); // Save homework list to DB after updating
}

// Get the number of homeworks in a course
function getHomeworkCount(homeworks) {
  return homeworks.children.length; // Return the number of child elements (homework items)
}

// Handle the plugin data (each course's homework list)
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
  const courseElement = parent.closest(".plg-data"); // Find the course element
  const courseName = courseElement.classList[4];     // Get the course name from the class
  const courseId = courseElement.id;                 // Get the course ID

  // Prompt the user to enter the homework
  const homework = prompt(`Add a homework for: ${courseName}`);

  if (homework) {
    // Create new elements to display the homework
    div = createHomeworkElement(homework);
    homeworks.appendChild(div); // Add the new homework to the course

    // Ensure the course has an entry in the homeworkList
    if (!homeworkList[courseId]) {
      homeworkList[courseId] = [];
    }
    homeworkList[courseId].push(homework); // Add the homework to the list
    updateHomeworkMeter();                 // Update the homework count display
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
        div = createHomeworkElement(homework);
        homeworksContainer.appendChild(div);
      });
    }
  });

  updateHomeworkMeter(); // Update the homework count display
}

// Remove a homework from the course
function removeHomework(button) {
  const parent = button.parentNode;
  const courseElement = parent.closest(".plg-data");        // Find the course element
  const courseId = courseElement.id;                        // Get the course ID
  const homeworkText = button.querySelector("p").innerHTML; // Get the homework text

  // Remove the homework from the homework list
  if (courseId in homeworkList) {
    homeworkList[courseId] = homeworkList[courseId].filter(
      (homework) => homework !== homeworkText
    );
  }

  parent.removeChild(button); // Remove the homework item from the UI
  updateHomeworkMeter();      // Update the homework count display
}
