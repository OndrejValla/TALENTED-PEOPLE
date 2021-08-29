import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

# HOME PAGE FUNCTION
@app.route("/")
@app.route("/get_home")
def get_home():
    return render_template("home.html")

# GET PHOTOGRAPHERS FUNCTION
@app.route("/")
@app.route("/get_photographers")
def get_photographers():
    photographers = mongo.db.photographers.find()
    return render_template("photographers.html", photographers=photographers)

# REGISTER FUNCTION
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username is already registred in our database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists! Try different one.")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # put the new user into "session" cookie
        session["user"] = request.form.get("username").lower()
        flash("You have been successfully registred!")
    return render_template("register.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
