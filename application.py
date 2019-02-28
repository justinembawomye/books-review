import os
import psycopg2

from flask import Flask, session, render_template, url_for, flash, redirect, request, Markup, jsonify
from flask_session import Session
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import scoped_session, sessionmaker
from forms import RegistrationForm, LoginForm, SearchForm
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import requests


from xml.etree import ElementTree

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"]= 'b316e2f2d8942e2315dc'
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

Session(app)



# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))



@app.route('/')
def home():
    return render_template('home.html')


	


@app.route('/register', methods=['POST', 'GET'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		db.execute("INSERT INTO users(username, email, password) VALUES(:username, :email, :password)",{"username":form.username.data, "email":form.email.data, "password":hashed_password})
		db.commit()
		flash (f"user {form.username.data} have successfully created an account! Please login", 'success')
		return redirect(url_for('login'))
	return render_template('register.html', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = db.execute("SELECT * FROM users WHERE (email=:email)",{'email': form.email.data}).fetchone()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			flash(f"Welcome start searching for your favorite books.", 'success')
			return redirect(url_for('home'))
		else:
			flash("Invalid email or password. Try again", 'danger')			
	return render_template('login.html', form=form)

#LOGOUT ROUTE
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/search', methods=['POST', 'GET'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        results = db.execute("SELECT * FROM books WHERE author LIKE  '%a%' ORDER BY id OFFSET 10 ROWS FETCH NEXT 10 ROWS ONLY ")
        print(results)
        return render_template('results.html', results=results)
		# return redirect(url_for('home'))
    return render_template('search.html', form=form)
    

#  BOOKPAGE   	

@app.route('/books/<isbn>')
def book(isbn):

    book = db.execute('SELECT * FROM books WHERE isbn=:isbn',
                      {'isbn': isbn}).fetchone()


    url = "https://www.goodreads.com/book/isbn.json", params={"key": "VbXdV8MTTSGJzdRm4z965Q", "isbns": isbn})
    res = requests.get(url)
    data = response.json
    tree = ElementTree.fromstring(res.content)

    try:
        description = tree[1][16].text
        image_url = tree[1][8].text
        review_count = tree[1][17][3].text
        avg_score = tree[1][18].text
        link = tree[1][24].text


    description_markup = Markup(description)

    return render_template('book.html', book=book, link=link, description=description_markup,
                           image_url=image_url, review_count=review_count, avg_score=avg_score)


# BOOK API
@app.route('/api/<isbn>')
def book_api(isbn):

    book = db.execute('SELECT * FROM books WHERE isbn=:isbn',
                      {'isbn': isbn}).fetchone()

    if book is None:
        api = jsonify({'error': 'This book is not available'})
        return api

    url = "https://www.goodreads.com/book/isbn.json", params={"key": "VbXdV8MTTSGJzdRm4z965Q", "isbns": isbn})
    res = requests.get(url)
    tree = ElementTree.fromstring(res.content)

    try:
        description = tree[1][16].text
        image_url = tree[1][8].text
        review_count = tree[1][17][3].text
        avg_score = tree[1][18].text
        link = tree[1][24].text

    except IndexError:
        api = jsonify({
            'title': book.title,
            'author': book.author,
            'year': book.year,
            'isbn': book.isbn,
            'link': '',
            'description': '',
            'book_cover': '',
            'review_count': '',
            'average_rating': ''
        })

        return api

    api = jsonify({
        'title': book.title,
        'author': book.author,
        'year': book.year,
        'isbn': book.isbn,
        'link': link,
        'description': description,
        'book_cover': image_url,
        'review_count': review_count,
        'average_rating': avg_score
    })

    return api
