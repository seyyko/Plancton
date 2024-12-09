
# IUT Planning App

This project aims to recreate the IUT planning website with a modern interface, featuring the ability to add homework, evaluations, and grades for each course. The app will be built using HTML, CSS, and JavaScript for the front-end and Python for the back-end, including a web scraping script to fetch the timetable.

## Features
- Modern user interface for viewing the schedule.
- Ability to add homework, evaluations, and grades to courses.
- Web scraping script to fetch the timetable from the existing IUT website.
- Backend API using Python for data management.

## Technologies
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Flask
- **Web Scraping**: Python
- **Client-Side Storage**: IndexedDB / localStorage

## Installation
To run this project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/seyyko/Plancton.git
   cd https://github.com/seyyko/Plancton.git
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the backend server:
   ```bash
   python src/back_end/app.py
   ```

5. Open the front-end in your browser:
   - The app will be available at `http://localhost:5000`.

## License
This project is open-source and available under the MIT License. See the LICENSE file for more information.
