# Flask-Basics
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
5.  Read the comments atop the `config.orig.py` file. 
6.  Make a copy of the `config.orig.py` file and name the copy `config.py`.
7.  From the home directory, initialize the database by running the `initdb` file - `python3 initdb.py`.
8.  Start the server from the home directory: `python3 app.py` or use your IDE to start the server.
9.  If all went well, you should be able to view the site: `http://127.0.0.1:5000/`.
10.  To make sure your database is working, navigate to the Companies link and create a new company. 
11.  To make sure the email config is correct, register an account and check for a verification email.

**Creating dummy data**

Beware of SSL issues on a Mac with later version of Python.  See
https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org

Get Captcha keys


