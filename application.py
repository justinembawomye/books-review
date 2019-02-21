
import os

from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")


app.secret_key = 'key'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():

    return render_template('index.html', navbar=True)


@app.route("/register",methods=['GET','POST'])
def register():


    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')
        cpassword = request.form.get('cpassword')


        if not password == cpassword:
            return render_template('error.html', message='Passwords do not match')

        avail = db.execute('SELECT username FROM userdetails WHERE username=:username',
                                {'username': username}).fetchone()
        
        if avail:
            return render_template('error.html', message='Username Already Exists')

        db.execute('INSERT INTO userdetails(username, password) VALUES(:username, :password)',
         {'username': username, 'password': password})
        db.commit()


        session["username"] = username

        return redirect('/')
    
    else:
        return render_template('register.html')

@app.route("/login", methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')
        

        user = db.execute('SELECT * FROM userdetails WHERE (username=:username AND password=:password)',
                             {'username': username, 'password': password}).fetchone()

        
        if user is None:
            return render_template('error.html', message='Entered credentials not valid!')

        session["username"] = username

        return redirect('books')

    else:
        return render_template('login.html', navbar=False)

    
@app.route("/books", methods=['GET', 'POST'])
def books():

    isbn = request.form.get('isbn')
    title = request.form.get('title')
    author = request.form.get('author')

    result = db.execute('SELECT * FROM books WHERE (isbn=:isbn AND title=:title AND author=:author)',
                             {'isbn': isbn, 'title': title, 'author': author}).fetchall()

    
    return render_template('books.html')

@app.route("/result", methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
      result = request.form()
      return render_template("result.html",result = result)                     
    

