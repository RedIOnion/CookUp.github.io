from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

from datetime import datetime

db = SQLAlchemy()
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique = True, nullable = False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    profilePic = db.Column(db.String(200), default = "pfp.jpg")
    savedFoodIds = db.Column(db.String(300), default = "")
    followingIDs = db.Column(db.String(300), default = "")

    def Notifications(self):
        return Notification.query.filter_by(userToID = self.id).all()

    def CheckPassword(self, password):
        return self.password == password
    
    def Foods(self):
        return Food.query.filter_by(posterID = self.id).all()
    
    def StringToIDList(self, IDString):
        IDs = IDString.replace(" ", "").split(",")
        for id in IDs: 
            if not id: IDs.remove(id)

        for i in range(len(IDs)): IDs[i] = int(IDs[i])
        return IDs

    def FollowingIDs(self):
        return self.StringToIDList(self.followingIDs)

    def SavedFoodIDs(self):
        return self.StringToIDList(self.savedFoodIds)
    
    def Followers(self):
        followers = []

        for user in User.query.all():
            if self.id in user.FollowingIDs():
                followers.append(user)
        return followers

    def Points(self):
        points = 0
        for food in Food.query.filter_by(posterID = self.id):
            points += food.Points()

        points += len(self.Followers()) * 10
        return points

    def CookLevel(self):
        cookRankings = {
            "Can't Boil Water": 0,
            "Kitchen Newbie": 10,
            "Rookie Cook": 50,
            "Home Cook": 100,
            "Intermediate Cook": 500,
            "Experienced Cook": 1000,
            "Expert Cook": 5000,
            "Chef": 10000,
            "Elite Chef": 50000,
            "Master Chef": 100000
        }

        points = self.Points()

        currentLevel = "Can't Boil Water"
        highestPointReq = 0

        for level, reqPoints in cookRankings.items():
            if points >= reqPoints:
                if reqPoints >= highestPointReq:
                    currentLevel = level
                    highestPointReq = reqPoints

        return currentLevel

    def SavedFoods(self):
        savedFoods = []
        
        for id in self.SavedFoodIDs():
            for food in Food.query.all():
                if food.id == id:
                    savedFoods.append(food)

        return savedFoods

    def HasSavedFood(self, foodID):
        return foodID in self.SavedFoodIDs()

class Food(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    posterID = db.Column(db.Integer, db.ForeignKey("user.id"), default = 0)
    name = db.Column(db.String(200), nullable = False)
    description = db.Column(db.String(1000), default = " ")
    postDate = db.Column(db.DateTime) 
    img = db.Column(db.String(100))
    ingredients = db.Column(db.String(100), nullable = False)
    duration = db.Column(db.Integer, default = 0)

    def Points(self):
        points = 0
        for review in self.Reviews():
            points += float(review.rating)
        return points

    def Date(self):
        return ConvertDate(self.postDate)

    def Ingredients(self):
        return self.ingredients.lower().replace(" ", "").split(",")
    
    def Poster(self):
        return User.query.filter_by(id = self.posterID).first()
    
    def Reviews(self):
        return Review.query.filter_by(foodID = self.id).all()
    
    def Rating(self):
        reviews = self.Reviews()
        if not reviews:
            return "Unrated"

        sum = 0
        for review in reviews:
            sum += float(review.rating)
        return str(sum / len(reviews))[:3]
    
    def HasUserReviewed(self, userID):
        for review in self.Reviews():
            if review.posterID == userID:
                return True
        return False
    
class Review(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    foodID = db.Column(db.Integer, db.ForeignKey("food.id"), default = 0)
    posterID = db.Column(db.Integer, db.ForeignKey("user.id"), default = 0)
    content = db.Column(db.String(1000), nullable = False)
    rating = db.Column(db.String(3))
    postDate = db.Column(db.DateTime) 

    def Date(self):
        return ConvertDate(self.postDate)

    def User(self):
        return User.query.filter_by(id = self.posterID).first()
    
    def Food(self):
        return Food.query.filter_by(id = self.foodID).first()
    
def ConvertDate(postDate):
        now = datetime.now()

        timeDifference = now - postDate

        days = timeDifference.days
        seconds = timeDifference.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60

        if days > 365:
            return f"{days // 365}y ago"
        elif days > 30:
            return f"{days // 30}m ago"
        elif days > 0:
            return f"{days}d ago"
        elif hours > 0:
            return f"{hours}h ago"
        elif minutes > 0:
            return f"{minutes}min ago"
        else:
            return "Just now"
        
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    userToID = db.Column(db.Integer, db.ForeignKey("user.id"), default = 0)
    userFromID = db.Column(db.Integer, db.ForeignKey("user.id"), default = 0)
    content = db.Column(db.String(1000), default = "Notification")
    link = db.Column(db.String(100), default = "#")