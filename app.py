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


# REGISTER FUNCTION
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Check if username is already registred in our database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists! Try different one.")
            return redirect(url_for("register"))

        register = {
            "firstname": request.form.get("firstname"),
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # Put the new user into "session" cookie
        session["user"] = request.form.get("username").lower()
        flash("You have been successfully registred!")
        return redirect(url_for("profile", username=session["user"]))
    return render_template("register.html")


# LOG IN FUNCTION
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Check if login detals match the database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # Checks hash password against user input
            if check_password_hash(
                existing_user["password"], request.form.get(
                    "password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(
                    existing_user["firstname"]), "default")
                return redirect(url_for(
                    "profile", username=session["user"]))

            else:
                # Not valid password
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # Not existing username
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


# LOG OUT FUNCTION
@app.route("/logout")
def logout():
    # remove user's session cookies
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


# GET PHOTOGRAPHERS FUNCTION
@app.route("/")
@app.route("/get_photographers")
def get_photographers():
    photographers = list(mongo.db.photographers.find())
    return render_template("photographers.html", photographers=photographers)


# ADD PHOTOGRAPHER FUNCTION
@app.route("/add_photographer", methods=["GET", "POST"])
def add_photographer():
    if request.method == "POST":
        photographer = {
            "category_name": request.form.get("category_name"),
            "photographer_name": request.form.get("photographer_name"),
            "photographer_experience": request.form.get(
                "photographer_experience"),
            "photographer_country": request.form.get(
                "photographer_country"),
            "photographer_equipment": request.form.get(
                "photographer_equipment"),
            "photographer_about": request.form.get("photographer_about"),
            "photographer_instagram": request.form.get(
                "photographer_instagram"),
            "photographer_website": request.form.get(
                "photographer_website"),
            "photographer_profile_image_URL": request.form.get(
                "photographer_profile_image_URL"),
            "photographer_image_URL2": request.form.get(
                "photographer_image_URL2"),
            "photographer_image_URL3": request.form.get(
                "photographer_image_URL3"),
            "photographer_image_URL4": request.form.get(
                "photographer_image_URL4"),
            "created_by": session["user"]
        }
        mongo.db.photographers.insert_one(photographer)
        flash("Profile Successfully Created!")
        return redirect(url_for("get_photographers"))

    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template("add_photographer.html", categories=categories)


# VIEW PHOTOGRAPHER FUNCTION
@app.route("/photographer/<photographer_id>")
def photographerprofile(photographer_id):
    photographer = mongo.db.photographers.find_one({"_id": ObjectId(
        photographer_id)})
    return render_template("photographer.html", photographer=photographer)


# EDIT PHOTOGRAPHER FUNCTION
@app.route("/edit_photographer/<photographer_id>", methods=["GET", "POST"])
def edit_photographer(photographer_id):
    if request.method == "POST":
        submit = {
            "category_name": request.form.get("category_name"),
            "photographer_name": request.form.get("photographer_name"),
            "photographer_experience": request.form.get(
                "photographer_experience"),
            "photographer_country": request.form.get(
                "photographer_country"),
            "photographer_equipment": request.form.get(
                "photographer_equipment"),
            "photographer_about": request.form.get("photographer_about"),
            "photographer_instagram": request.form.get(
                "photographer_instagram"),
            "photographer_website": request.form.get(
                "photographer_website"),
            "photographer_profile_image_URL": request.form.get(
                "photographer_profile_image_URL"),
            "photographer_image_URL2": request.form.get(
                "photographer_image_URL2"),
            "photographer_image_URL3": request.form.get(
                "photographer_image_URL3"),
            "photographer_image_URL4": request.form.get(
                "photographer_image_URL4"),
            "created_by": session["user"]
        }
        mongo.db.photographers.update({"_id": ObjectId(photographer_id)}, submit)
        flash("Profile Successfully Updated!")
        return redirect(url_for("get_photographers"))

    photographer = mongo.db.photographers.find_one({"_id": ObjectId(photographer_id)})
    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template("edit_photographer.html", photographer=photographer, categories=categories)


# DELETE PHOTOGRAPHER FUNCTION
@app.route("/delete_photographer/<photographer_id>")
def delete_photographer(photographer_id):
    mongo.db.photographers.remove({"_id": ObjectId(photographer_id)})
    flash("Profile Deleted!")
    return redirect(url_for("get_photographers"))


# GET MODELS FUNCTION
@app.route("/")
@app.route("/models")
def get_models():
    models = list(mongo.db.models.find())
    return render_template("models.html", models=models)


# ADD MODEL FUNCTION
@app.route("/add_model", methods=["GET", "POST"])
def add_model():
    if request.method == "POST":
        model = {
            "model_name": request.form.get("model_name"),
            "model_experience": request.form.get(
                "model_experience"),
            "model_country": request.form.get(
                "model_country"),
            "model_about": request.form.get("model_about"),
            "model_instagram": request.form.get(
                "model_instagram"),
            "model_website": request.form.get(
                "model_website"),
            "model_profile_image_URL": request.form.get(
                "model_profile_image_URL"),
            "model_image_URL2": request.form.get(
                "model_image_URL2"),
            "model_image_URL3": request.form.get(
                "model_image_URL3"),
            "model_image_URL4": request.form.get(
                "model_image_URL4"),
            "created_by": session["user"]
        }
        mongo.db.models.insert_one(model)
        flash("Profile Successfully Created!")
        return redirect(url_for("get_models"))

    return render_template("add_model.html")


# VIEW MODEL FUNCTION
@app.route("/model/<model_id>")
def modelprofile(model_id):
    model = mongo.db.models.find_one({"_id": ObjectId(
        model_id)})
    return render_template("model.html", model=model)


# EDIT MODEL FUNCTION
@app.route("/edit_model/<model_id>", methods=["GET", "POST"])
def edit_model(model_id):
    if request.method == "POST":
        submit = {
            "model_name": request.form.get("model_name"),
            "model_experience": request.form.get(
                "model_experience"),
            "model_country": request.form.get(
                "model_country"),
            "model_about": request.form.get("model_about"),
            "model_instagram": request.form.get(
                "model_instagram"),
            "model_website": request.form.get(
                "model_website"),
            "model_profile_image_URL": request.form.get(
                "model_profile_image_URL"),
            "model_image_URL2": request.form.get(
                "model_image_URL2"),
            "model_image_URL3": request.form.get(
                "model_image_URL3"),
            "model_image_URL4": request.form.get(
                "model_image_URL4"),
            "created_by": session["user"]
        }
        mongo.db.models.update({"_id": ObjectId(model_id)}, submit)
        flash("Profile Successfully Updated!")
        return redirect(url_for("get_models"))

    model = mongo.db.models.find_one({"_id": ObjectId(model_id)})
    return render_template("edit_model.html", model=model)


# DELETE MODEL FUNCTION
@app.route("/delete_model/<model_id>")
def delete_model(model_id):
    mongo.db.models.remove({"_id": ObjectId(model_id)})
    flash("Profile Deleted!")
    return redirect(url_for("get_models"))


# PROFILE FUNCTION
@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    if "user" in session:
        users = list(mongo.db.users.find().sort("username"))
        user_profile = []
        for user in users:
            # Check if user is logged in and matches user logged in.
            if "user" in session and (user["username"] == session["user"]):
                user_profile.append(user)
    # the session user's username from the database
        username= mongo.db.users.find_one(
            {"username": session["user"]})["username"]
        photographers = list(mongo.db.photographers.find(
                            {"created_by": session["user"]}))
        models = list(mongo.db.models.find(
                            {"created_by": session["user"]}))
        return render_template("profile.html", username=username,
                                photographers=photographers,
                                models=models)

        if session["user"]:
            return render_template("profile.html", username=username,
                                    user_profile=user_profile)
    else:
        flash("Please log in for access")
        return redirect(url_for("login", ))


# MANAGE CATEGORIES FUNCTION
@app.route("/get_categories")
def get_categories():
    categories = list(mongo.db.categories.find().sort("category_name", 1))
    return render_template("categories.html", categories=categories)


# ADD CATEGORY FUNCTION
@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    if request.method == "POST":
        category = {
            "category_name": request.form.get("category_name")
        }
        mongo.db.categories.insert_one(category)
        flash("New Category Successfully Added")
        return redirect(url_for("get_categories"))

    return render_template("add_category.html")


# EDIT CATEGORY FUNCTION
@app.route("/edit_category/<category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    if request.method == "POST":
        submit = {
            "category_name": request.form.get("category_name")
        }
        mongo.db.categories.update({"_id": ObjectId(category_id)}, submit)
        flash("Category Successfully Updated")
        return redirect(url_for("get_categories"))

    category = mongo.db.categories.find_one({"_id": ObjectId(category_id)})
    return render_template("edit_category.html", category=category)


# DELETE CATEGORY FUNCTION
@app.route("/delete_category/<category_id>")
def delete_category(category_id):
    mongo.db.categories.remove({"_id": ObjectId(category_id)})
    flash("Category Deleted!")
    return redirect(url_for("get_categories"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
