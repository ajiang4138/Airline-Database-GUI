# Information
This is the phase IV project for CS 4400: Intro to Databases, created by Allen Jiang and Jonathan Liang. We created a python GUI that is connected to a MySQL database capable of running custom queries, running built in procedures, and displaying tables and views from the database.

# Packages
- tkinter
- mypysql

# Package installation instructions

### On Windows
- tkinter should already be installed by default with python3
    - If not installed, run python -m tkinter
        - Or python3 -m tkinter
- pip install pymysql

### On macos
```
- pip install python-tk
- pip install pymysql
```

OR
``` 
- brew install python-tk
- brew install pymysql
```

# HOW TO RUN
- Download a python IDE (preferably VSCode)
- Install required packages
- Run `airline_database_gui.py`

# Notes
- Make sure to change the connection method to your database, otherwise it will not work.
    - Like password, host, port, etc...
- Color palettes appear to be different between Windows and Mac
    - Keep this in mind when adding and changing colors.

# Technologies Used
- In our project, we used two python libraries: Tkinter and pymysql. Tkinter is a built-in GUI that comes with python, and it supports the buttons/text fields used in our project. pymysql is a library for python that allows us to connect to a running MySQL server, and allows us to access the database, views, and procedures.

# Work distribution
- Allen worked on the procedures portion of the GUI, while Jonathan worked on the custom query page and the views portion of the GUI. Remaining work was divided roughly by half between the two of us.
