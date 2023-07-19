
# Bloggy - Basic Blog

Website made with SQLAlchemy on Flask, it works as a social blog, but it doesn't has a properly login system. Developed for the college subject "Practicas Profesionalizantes 1 - Python"

## Technologies

 - Bootstrap
 - Flask
 - Python
 - HTML
 - CSS
 - MySQL

## Set-Up

To deploy this project you will need an updated version of Python.
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

- [@Nazareno Bucciarelli](https://github.com/nazabucciarelliITEC)
