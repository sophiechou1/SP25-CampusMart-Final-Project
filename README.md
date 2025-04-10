# About The Project

## Group 14 Members
Sophie Chou, Elissa McDermott, Hannah Huston

## Built With
* [Python](https://www.python.org/)
* [Django](https://www.djangoproject.com/)
* [Bootstrap](https://getbootstrap.com)

### Prerequisites
Make sure you have the following installed:
* [Python 3.10+]((https://www.python.org/downloads/)
* [pip](https://pip.pypa.io/en/stable/installation/)
* [npm (for Bootstrap or optional frontend)](https://www.npmjs.com/get-npm)
* Install `npm` (if needed):
```sh
npm install npm@latest -g
```

### Installation
1. Clone the repo
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
    ├── CampusMart/
      ├── templates/
    ├── manage.py/
    ├── db.sqlite3
├── README.md
├── CONTRIBUTIONS.md
└── requirements.txt
