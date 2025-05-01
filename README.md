# About The Project

## Group 14 Members
Sophie Chou, Elissa McDermott, Hannah Huston

## Built With
* [Python](https://www.python.org/)
* [Django](https://www.djangoproject.com/)
* [Bootstrap](https://getbootstrap.com)

## Prerequisites
Make sure you have the following installed:
* [Python 3.10+](https://www.python.org/downloads/)
* [pip](https://pip.pypa.io/en/stable/installation/)

## Installation
1. Clone and cd into the repo
   ```sh
   git clone https://github.com/sophiechou1/Group-14.git
   cd Group-14
   ```
2. (Optional) Create virtual environment
   ```sh
   python -m venv venv
   source venv/bin/activate
   ```
3. Install libraries
   ```sh
   pip install -r requirements.txt
   ```
4. Run migrations
   ```sh
   cd src
   python manage.py makemigrations CampusMart
   python manage.py migrate
   ```
6.  Start server
    ```sh
    python manage.py runserver
    ```
7. Testing the project  
   Add /CampusMart/register to view register screen  
   &nbsp; Once registered, you are prompted to the login screen  
   Add /CampusMart/login to view login screen  
   Add /admin to view admin interface + database (user: group14 pass: group14)  
   
## Folder Structure
* All necessary source files to run/start the server are located in the "src" directory.  
* The templates directory contains all html files  
Group-14/  
├── src/  
&nbsp;&nbsp;&nbsp;&nbsp;├── CourseProject/  
&nbsp;&nbsp;&nbsp;&nbsp;├── *.py files    
&nbsp;&nbsp;&nbsp;&nbsp;├── CampusMart/  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── templates/  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── migrations/  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── static/  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── *.py files  
&nbsp;&nbsp;&nbsp;&nbsp;├── manage.py  
&nbsp;&nbsp;&nbsp;&nbsp;├── db.sqlite3  
&nbsp;&nbsp;&nbsp;&nbsp;├── media    
├── README.md  
├── CONTRIBUTIONS.md  
├── Phase 1 Report - Group 14.pdf  
├── Final Report - Group 14.pdf    
└── requirements.txt  
