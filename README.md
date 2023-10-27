
# Bloggy - API

This project is the second part of an Integrated Final Evaluation, it consists in an API for the blog that we had to do in the first part of the evaluation. It basically has working endpoints for User, Category, Post and Commentary entities and their CRUD operations, receiving in any case the proper HTTP response. Developed for the college subject "Practicas Profesionalizantes 1 - Python"

## Technologies

 - Flask
 - Python
 - MySQL
 - Marshmallow
 - SQLAlchemy

## Set-Up

To run this project you will need an updated version of Python.
First, we will create a virtual enviroment. You can do it with
```bash
  python3 -m venv venv
```
Now, we need to activate the virtual enviroment.
On linux, just type
```bash
  source venv/bin/activate
```
on Windows,
```bash
   venv/Scripts/activate
```
Once activated, we need to install Flask and other libraries:

```bash
  pip install -r requirements.txt
```
After that, we have to run XAMP (MySQL and Apache), otherwise SQLAlchemy won't work.

Lastly, we run the proyect with:
```bash
  flask run
```

and access it through typing [localhost:5000](http://localhost:5000/) in your browser


## Author

- [@Nazareno Bucciarelli](https://github.com/nazabucciarelli)
