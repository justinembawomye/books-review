import os



from flask import Flask, session, render_template, url_for, flash, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from forms import RegistrationForm, LoginForm
from flask_bcrypt import Bcrypt


app = Flask(__name__)

engine = create_engine("mysql+pymysql://bartix997:zxszxs321@localhost:3306/project1")
db = scoped_session(sessionmaker(engine))

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"]= os.environ.get('SECRET_KEY')
bcrypt = Bcrypt(app)

Session(app)




# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
>>>>>>> ad1414d9cf870944f64073d83e6d8cce9dc90cce

@app.route('/')
def home():
    if not session.get("logged_in"):
        return render_template("welcome.html")
    else:
        return render_template("home.html", username=session["user_name"])


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "GET":
        if session.get("logged_in"):
            flash("You are already logged in")
            return redirect(url_for('home'), "303")
        else:
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


@app.route('/login', methods=["POST", "GET"])
def login():
        
    return render_template(('login.html'))

