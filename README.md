# Bath Hub Project
## Introduction

This project is intended for the udacity backend final project. Udacity's project required an item catalog which is building a website that gives the user the option to navigate through items and run all the **CRUD** operations through an easy to use interface.

I choose to make a website that gives the user the priviledge to add entertainment descriptions and store them under certain categories.

## Project idea
The project idea was inspired by my favorite website [goodreads](https://www.goodreads.com), which is a website that helps the user store books that the user would like to read in the near future. My website is simpler form with less functionality but with all forms of media such as
-Visual(**Movies**)
-Audio(**Music**)
-Books(**Articles**)
-And so on..

## What do i need to run this project?
Here is the list of what the user needs to run this project:
- Windows users:
1- git bash (Unix based terminal)
2- Virtual Machinebox Oracle ([Link here](https://www.virtualbox.org/))
3- Python setup ([link here](https://www.python.org/downloads/))
4- Vagrant setup ([link here](https://www.vagrantup.com/downloads.html))
5- Any Text Editor, for example **Sublime Text**
- Mac and linux users
1- Everything is pre configured in Mac and linux OS 
2- You only need to download python ([linkhere](https://www.python.org/downloads/))

## Project Content
The following files are run using the Flask framework (The website), Database is run through a library called SQLalchemy that binds the project with the database.
The following folders are contained in this project:
1- Project.py (Contains the backend functionality)
2- Database.py (Contains the actual database)
3- **Templates** folder that contains the html to show the user.
4- **Static** folder that contains the css required to design the html.
5- categoires.py that populates the database.

## How to run the setup
1- open git bash or terminal.
2- place the project the vagrant directory. the vagrant directory has a folder that shares files between the virtual machine and the original OS.
3- After placing the folder, Navigate with your git bash to the vagrant folder.
4- enter "Vagrant up" **It may take a while**
5- after the setup is complete run "vagrant ssh"
6- cd into /vagrant.
7- cd into the project folder.
# ***YOU MUST RUN THESE FOLDERS IN THE ORDER SHOWN***
8- Run the Database.py folder ***python database.py***
9- Run the categories.py folder to populate the database ***python categories.py***
10- Run the python project.py
11- Then go to your favorite browser and enter "http://localhost:5000"
12- Then use the WEBSITE!!!!!

# The logic of the project
The Database.py creates the database tables. then categories.py populates then the project.py does all the backend functionality. All those folders will produce the following compiled Extentions. categorymenu.db, Database.pyc.
template and static folders are used by flask to configure the redirects and the css. 

# Bath hub
Project by **Abdulkareem Barghouthi**
All thanks to udacity for this great learning experience, the project caused some frustrations but those frustration lead me to the best things that i learned so far. Thank you for teaching me the concepts of the frameworks
