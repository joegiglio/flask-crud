**Flask-CRUD**

A Python Flask CRUD application template with mySQL, Bootstrap, modal dialogs, Font Awesome icons,
flask-migrate, authentication, sessions and SQLAlchemy. 

__Why start from scratch?__  

---
**Tech stack:**
Python 3.7, Flask, Pip, MySQL
---
**Author:**
Joe Giglio
---

**Installation:**

1.  Clone project using git
2.  From project home directory (where app.py sits), create a virtual environment for dependencies.  Use https://flask.palletsprojects.com/en/1.1.x/installation/ as a reference.  I recommend naming it `venv`, which has already been added to the .gitignore file.  
3.  Activate the virtual environment directory.  
4.  Use `pip install -r requirements.txt` to install all dependencies. 
5.  Make a copy of the `config.orig.py` file and name the copy `config.py`.
6.  Set the configuration values in config.py file.  **NOTE:  This file holds sensitive information such
as passwords and keys.  It is excluded from the default .gitignore file.  Keep this file secure!**
7.  From the home directory, initialize the database by running the `initdb` file - `python3 initdb.py`.
8.  Start the server from the home directory: `python3 app.py` or use your IDE to start the server.
9.  If all went well, you should be able to view the site: `http://127.0.0.1:5000/`.
10.  To make sure your database is working, navigate to the View Dogs link.  You should see an entry for Romeo.

**Coming soon in future versions:**
(Feel free to create a branch if you want to contribute!)
1.  Send email through a form
2.  Authentication system
3.  Custom decorators to check for logged in user and user level
4.  Code cleanup into modules


