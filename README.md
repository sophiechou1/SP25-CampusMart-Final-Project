# About The Project

## Group 14 Members
Sophie Chou, Elissa McDermott, Hannah Huston

## Built With
* [Python](https://www.python.org/)
* [Django](https://www.djangoproject.com/)
* [Bootstrap](https://getbootstrap.com)

### Prerequisites
Make sure you have the following installed:
* [Python 3.10+](https://www.python.org/downloads/)
* [pip](https://pip.pypa.io/en/stable/installation/)

### Installation
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
   cd CourseProject
   python manage.py migrate
   ```
6.  Start server
    ```sh
    python manage.py runserver
    ```

### Folder Structure
Group-14/  
├── CourseProject/
&nbsp;&nbsp;&nbsp;&nbsp;├── CourseProject/
&nbsp;&nbsp;&nbsp;&nbsp;├── manage.py
&nbsp;&nbsp;&nbsp;&nbsp;├── db.sqlite3
&nbsp;&nbsp;&nbsp;&nbsp;├── CampusMart/
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── templates/
├── README.md  
├── CONTRIBUTIONS.md  
└── requirements.txt  
