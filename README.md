# Molecule-Web-Server-Application

## Description 📄
This is my first full-stack web development project that exposes me to Agile software development. This web application allows user
to insert elements and parse SDF files for molecules into a database. This web application also has the functionality to generate and displays an SVG image of the molecule.

## Language Used 🔨
![C](https://img.shields.io/badge/c-%2300599C.svg?style=for-the-badge&logo=c&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![JQuery](https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white)

## Development 🪜
- Developed a C library and implemented SWIG to generate a Python wrapper for the library.
- Used Python to develop the functionality of parsing an SDF files, inserting elements and molecules into an SQLite database, and generating an SVG image for the molecule.
- Used HTML/CSS and JQuery to communicate and send data from the client-side to a Python web server.

## Running the program 🏃
- Download python and SWIG if not yet available in your system
- Enter in command line:   
```
make  
export LD_LIBRARY_PATH=.  
python3 server 8000  
```
- Open a browser and enter: http://localhost:8000/index.html

Side note: makefile may need modifications to fit each individual's system



