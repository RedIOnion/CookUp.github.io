from flask import Flask, render_template, redirect, request, url_for
from flask_login import current_user, LoginManager, login_user, logout_user, login_required

from models import db, User, Food, Review, Notification
from search import Search, CleanedIngredientsList
from appConfig import CreateApp
from loginHelper import StringChecker, UsedEmails, UsedUsernames, AddUser, UserByEmail, UserByID

from datetime import datetime

import os;

base_folder = os.getcwd()

staticPath = os.path.join(base_folder, "static")
templatePath = os.path.join(base_folder, "templates")    

app = Flask(__name__,
    template_folder= templatePath,
    static_folder= staticPath
)

app.config["SECRET_KEY"] = "very secret key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite"

db.init_app(app)

with app.app_context():
    db.create_all()

login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def Home():
    return render_template("index.html", user = current_user)

@app.route("/browse", methods = ["GET", "POST"])
def Browse():
    if request.method == "POST":
        ingredients = request.form["ingredients"]
        sort = request.form["sort"]
        time = request.form["time"]
        ingredients = CleanedIngredientsList(ingredients)

        foods = Search(ingredients, sort, time)

        return render_template("browse.html", user = current_user, foods = foods, ingredients = ingredients, sort = sort, time = time)

    return render_template("browse.html", user = current_user, foods = Search(None, "top", ""), ingredients = [])

@app.route("/login", methods = ["GET", "POST"])
def Login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = UserByEmail(email)
        if user == None: return render_template("login.html", error = "Invalid User")
        if not user.password == password: return render_template("login.html", error = "Invalid Passwrod")

        login_user(user)
        return redirect(url_for("Profile", userID = current_user.id))

    return render_template("login.html", error = "")

@app.route("/register", methods = ["GET", "POST"])
def Register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirmPassword = request.form["confirmPassword"]

        error = StringChecker(username, "Username", 4, 20, True, UsedUsernames())
        if not error == None: return render_template("register.html", error = error)

        error = StringChecker(email, "Email", 0, 100, True, UsedEmails())
        if not error == None: return render_template("register.html", error = error)

        error = StringChecker(password, "Password", 8, 20, False, None)
        if not error == None: return render_template("register.html", error = error)

        if not confirmPassword == password:
            return render_template("register.html", error = "Please Confirm Password Correctly")
        
        newUser = User(
            email = email,
            username = username,
            password = password
        )

        AddUser(newUser)
        login_user(newUser)

        return redirect(url_for("Profile", userID = current_user.id))

    return render_template("register.html", error = "")

@login_required
@app.route("/profile/<int:userID>")
def Profile(userID):
    user = UserByID(userID)
    return render_template("profile.html", profileUser = user, user = current_user)

@login_required
@app.route("/logout")
def Logout():
    logout_user()
    return redirect(url_for("Login"))

@login_required
@app.route("/settings")
def Settings():
    return render_template("settings.html", user = current_user)

@app.route("/changeUsername", methods = ["GET", "POST"])
def ChangeUsername():
    username = request.form["username"]

    error = StringChecker(username, "Username", 4, 20, True, UsedUsernames())
    if not error == None:
        return render_template("settings.html", user = current_user, usernameError = error)
    
    current_user.username = username
    db.session.commit()

    return render_template("settings.html", user=current_user, usernameError = "Success!")

@app.route("/changePassword", methods = ["GET", "POST"])
def ChangePassword():
    password = request.form["password"]

    error = StringChecker(password, "Password", 8, 20, False, None)
    if not error == None:
        return render_template("settings.html", user = current_user, passwordError = error)
    
    current_user.password = password
    db.session.commit()
    
    return render_template("settings.html", user=current_user, passwordError = "Success!")

@app.route("/changeProfilePicture", methods = ["GET", "POST"])
def ChangeProfilePicture():
    profilePicture = request.files["profilePicture"]

    acceptedFileTypes = ["png", "jpg"]
    goodFormat = False
    for fileType in acceptedFileTypes:
        if profilePicture.filename.lower().endswith("." + fileType):
            goodFormat = True
    if not goodFormat:
        return render_template("settings.html", user=current_user, profilePictureError = "Wrong Format.")
    
    imgPath = os.path.join(staticPath, profilePicture.filename)
    profilePicture.save(imgPath)

    current_user.profilePic = profilePicture.filename
    db.session.commit()
    
    return render_template("settings.html", user=current_user, profilePictureError = "Success!")

@app.route("/createPost", methods = ["POST", "GET"])
def CreateFood():
    if request.method == "POST":
        name = request.form["foodName"]
        image = request.files["image"]
        ingredients = request.form["ingredients"]
        description = request.form["description"]
        duration = request.form["duration"]

        if not duration.isdigit():
            return render_template("createPost.html", user = current_user, error = "Invalid Duration")
        
        acceptedFileTypes = ["png", "jpg"]
        goodFormat = False
        for fileType in acceptedFileTypes:
            if image.filename.lower().endswith("." + fileType):
                goodFormat = True

        if not goodFormat:
            return render_template("createPost.html", user =current_user, error = "Wrong image format")

        imgPath = os.path.join(staticPath, image.filename)
        image.save(imgPath)

        duration = int(duration)

        food = Food(
            name = name,
            img = image.filename,
            ingredients = ingredients,
            description = description,
            duration = duration,
            postDate = datetime.now(),

            posterID = current_user.id
        )

        db.session.add(food)
        db.session.commit()

        return redirect(url_for("FoodPage", foodID = food.id))

    return render_template("createPost.html", user = current_user)

@app.route("/food/<int:foodID>", methods = ["POST", "GET"])
def FoodPage(foodID):
    food = Food.query.filter_by(id = foodID).first()

    if current_user.is_authenticated and not food.HasUserReviewed(current_user.id) and not food.posterID == current_user.id and request.method == "POST":

        content = request.form["content"]
        rating = float(request.form["rating"])

        review = Review(
            posterID = current_user.id,
            foodID = foodID,
            content = content,
            rating = rating,
            postDate = datetime.now()
        )

        notification = Notification(
            userToID = Food.query.filter_by(id = foodID).first().posterID,
            userFromID = current_user.id,
            content = f"{User.query.filter_by(id = current_user.id).first().username} has left a {rating} star review!",
            link = url_for('FoodPage', foodID=foodID)
        )

        db.session.add(review)
        db.session.add(notification)
        db.session.commit()

    return render_template("post.html", food = food, user = current_user)

@app.route("/SavePost/<int:foodID>")
def SavePost(foodID):
    if current_user.HasSavedFood(foodID):
        return redirect(url_for("FoodPage", foodID = foodID))
    
    current_user.savedFoodIds = current_user.savedFoodIds + ", " + str(foodID) 

    notification = Notification(
        userToID = Food.query.filter_by(id = foodID).first().posterID,
        userFromID = current_user.id,
        content = f"{User.query.filter_by(id = current_user.id).first().username} has saved your post!",
        link = url_for('FoodPage', foodID=foodID)
    )

    if not notification.userToID == current_user.id:
        db.session.add(notification)
    db.session.commit()
    
    return redirect(url_for("FoodPage", foodID = foodID))

@app.route("/UnsavePost/<int:foodID>")
def UnsavePost(foodID):
    if not current_user.HasSavedFood(foodID):
        return redirect(url_for("FoodPage", foodID = foodID))
    
    current_user.savedFoodIds = current_user.savedFoodIds.replace(", " + str(foodID), "") 
    db.session.commit()
    
    return redirect(url_for("FoodPage", foodID = foodID))

@app.route("/DeleteNotification/<int:notificationID>")
def DeleteNotification(notificationID):
    notfication = Notification.query.get(notificationID)

    if notfication: db.session.delete(notfication)
    db.session.commit()

    return redirect(url_for("Home"))

@app.route("/DeleteFood/<int:foodID>")
def DeleteFood(foodID):
    food = Food.query.get(foodID)

    for review in food.Reviews():
        if review: db.session.delete(review)

    if food: db.session.delete(food)
    db.session.commit()
    return redirect(url_for("Browse"))

@app.route("/pantry")
def Pantry():
    return render_template("savedFoods.html", user = current_user)

@app.route("/follow/<int:userID>")
def Follow(userID):
    user = User.query.filter_by(id = userID).first()

    if current_user in user.Followers():
        return redirect(url_for("Profile", userID = userID))
    current_user.followingIDs = current_user.followingIDs + ", " + str(userID)
    db.session.commit()

    return redirect(url_for("Profile", userID = userID))

@app.route("/unfollow/<int:userID>")
def Unfollow(userID):
    user = User.query.filter_by(id = userID).first()

    if not current_user in user.Followers():
        return redirect(url_for("Profile", userID = userID))
     
    current_user.followingIDs = current_user.followingIDs.replace(", " + str(userID), "")
    db.session.commit()

    return redirect(url_for("Profile", userID = userID))


if __name__ == "__main__":
    app.run(debug=True)