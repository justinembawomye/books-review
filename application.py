import os
import psycopg2

from flask import Flask, session, render_template, url_for, flash, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from forms import RegistrationForm, LoginForm
from flask_bcrypt import Bcrypt

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"]= os.environ.get('SECRET_KEY')
bcrypt = Bcrypt(app)

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
							 



