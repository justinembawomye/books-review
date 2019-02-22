# import os

# from flask import Flask, session
# from flask_session import Session
# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker

# app = Flask(__name__)

# # Check for environment variable
# if not os.getenv("DATABASE_URL"):
#     raise RuntimeError("DATABASE_URL is not set")

# # Configure session to use filesystem
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

# # Set up database
# engine = create_engine(os.getenv("DATABASE_URL"))
# db = scoped_session(sessionmaker(bind=engine))


# @app.route("/")
# def index():
#     return "Project 1: TODO



# my routes




from flask import Flask, flash, request, session, redirect, render_template, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)

engine = create_engine("mysql+pymysql://bartix997:zxszxs321@localhost:3306/project1")
db = scoped_session(sessionmaker(engine))

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)





@app.route('/register', methods=['POST', 'GET'])
def register():
            return render_template("register.html")
            if request.method == "POST":
                username = request.form.get("username")
                pass1 = request.form.get("pass")
                pass2 = request.form.get("pass2")

            if pass1 != pass2 or pass1 is None or pass2 is None:
                flash("Password don't match")
            return redirect(url_for('register'), "303")

            hash = pbkdf2_sha256.hash(pass1)
            db.execute("INSERT INTO users (username, password) VALUES (:name, :hash)",
                   {"name": username, "hash": hash})
            db.commit()
            flash("Register successful")
            return redirect(url_for('register'), "303")

        

