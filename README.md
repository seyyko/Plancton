
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
- **Storage**:
   - IndexedDB (client-side) : save preferences of a user.
   - Flask-SQLAlchemy (MySQL, server-side) : save the planning week for a class.

## Installation
To run this project locally, follow these steps:

1. Clone the repository:
   
   ```bash
   git clone https://github.com/seyyko/Plancton.git
   cd Plancton
   ```

2. Create a virtual environment:
   
   - linux:
     
      ```bash
      python3 -m venv venv
      source venv/bin/activate  (linux)
      ```
   - windows:
     
     ```bash
      python -m venv venv
      .\venv\Scripts\Activate.ps1 (windows)
      ```
     

3. Install the required dependencies:
   
   ```bash
   pip install -r requirements.txt
   ```

You might need to do this to install Playwright's web browser:

   ```bash
   playwright install
   ```

4. Run the backend server:
   
   ```bash
   python src/back_end/app.py
   ```

5. Open the front-end in your browser:
   
   - The application will be available on all addresses (0.0.0.0:80)
   - in particular on:
      - http://127.0.0.1:80
      - and your ip address.

## License
This project is open-source and available under the MIT License. See the LICENSE file for more information.
