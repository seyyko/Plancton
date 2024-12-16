// indexeddbHandler.js

const DB_NAME = "PlanctonDB";  // Database name
const DB_VERSION = 1;          // Database version

let db;  // Database reference

// Function to initialize the database
function initializeDatabase() {
    return new Promise((resolve, reject) => {
        const request = indexedDB.open(DB_NAME, DB_VERSION);

        request.onupgradeneeded = (event) => {
            db = event.target.result;

            // Create the "homeworks" store if it doesn't exist
            if (!db.objectStoreNames.contains("homeworks")) {
                const homeworksStore = db.createObjectStore("homeworks", { keyPath: "id" });
                homeworksStore.createIndex("dayPeriod", "dayPeriod", { unique: false });  // Index for "dayPeriod"
            }

            // Create the "courses" store if it doesn't exist
            if (!db.objectStoreNames.contains("courses")) {
                const coursesStore = db.createObjectStore("courses", { keyPath: "id", autoIncrement: true });
                coursesStore.createIndex("day", "day", { unique: false });  // Index for "day"
            }
        };

        request.onsuccess = (event) => {
            db = event.target.result;
            console.log("Database initialized.");
            resolve();  // Database is ready
        };

        request.onerror = (event) => {
            console.error("Error opening database:", event.target.error);
            reject(event.target.error);
        };
    });
}

// Function to add data to the "homeworks" store
function addHomeworks(homeworksList) {
    const transaction = db.transaction(["homeworks"], "readwrite");
    const homeworksStore = transaction.objectStore("homeworks");

    // Iterate over the homework list and add each item to the database
    Object.keys(homeworksList).forEach((key) => {
        const data = {
            id: key,
            dayPeriod: key,
            tasks: homeworksList[key],  // Assign tasks to the homework item
        };
        homeworksStore.put(data);  // Store the data
    });

    transaction.oncomplete = () => {
        console.log("Homeworks added to the database.");
    };

    transaction.onerror = (event) => {
        console.error("Error adding homeworks:", event.target.error);
    };
}

// Function to add data to the "courses" store
function addCourses(coursesList) {
    const transaction = db.transaction(["courses"], "readwrite");
    const coursesStore = transaction.objectStore("courses");

    // Iterate over each day object and each course
    coursesList.forEach((dayObj) => {
        Object.keys(dayObj).forEach((day) => {
            dayObj[day].forEach((course) => {
                const data = {
                    day: day,
                    name: course.nom,           // Course name
                    room: course.salle,         // Classroom
                    time: course.heure_plate,   // Course time
                    totalClasses: course.total_classes || null,  // Total number of classes, if available
                    totalHours: course.total_heures || null,     // Total hours, if available
                };
                coursesStore.put(data);  // Store the course data
            });
        });
    });

    transaction.oncomplete = () => {
        console.log("Courses added to the database.");
    };

    transaction.onerror = (event) => {
        console.error("Error adding courses:", event.target.error);
    };
}

// Function to retrieve all data from a specified store
function getAllData(storeName) {
    const transaction = db.transaction([storeName], "readonly");
    const store = transaction.objectStore(storeName);
    const request = store.getAll();

    request.onsuccess = () => {
        console.log(`Data from ${storeName}:`, request.result);  // Log retrieved data
    };

    request.onerror = (event) => {
        console.error(`Error retrieving data from ${storeName}:`, event.target.error);
    };
}

// Function to clear all data in the database
function clearDatabase() {
    if (!db) {
        console.error("Database is not initialized.");
        return;
    }

    const transaction = db.transaction(db.objectStoreNames, "readwrite");
    transaction.oncomplete = () => {
        console.log("Database cleared.");
    };

    transaction.onerror = (event) => {
        console.error("Error clearing database:", event.target.error);
    };

    // Clear each store in the database
    Array.from(db.objectStoreNames).forEach((storeName) => {
        const store = transaction.objectStore(storeName);
        const request = store.clear();
        request.onsuccess = () => {
            console.log(`All records cleared from ${storeName}.`);
        };
    });
}
