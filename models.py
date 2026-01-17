from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

from datetime import datetime

db = SQLAlchemy()
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) # უნიკალური ID რომლითაც ვეძებთ მომხმარებელს
    email = db.Column(db.String(100), unique = True, nullable = False) # მომხმარებლის ემეილი
    username = db.Column(db.String(20), unique=True, nullable = False) # მომხმარებლის სახელი
    password = db.Column(db.String(200), nullable = False) # მომხმარებლის პაროლი
    profilePic = db.Column(db.String(200), default = "pfp.jpg") # მომხმარებლის პროფილის ფოტოს სახელი Static ფოლდერში
    followingIDs = db.Column(db.String(300), default = "") # იმათი ID ვისაც მომხმარებელი აფოლოვებს
    savedFoodIds = db.Column(db.String(300), default = "") # იმ საჭმლის ID რომელსაც მომხმარებელი ინახავს

    def Notifications(self): # ყველა ნოთიფიკაცია რაც მომხმარებელს არ უნახავს
        return Notification.query.filter_by(userToID = self.id).all()
    
    def Foods(self): # ყველა საჭმელი რაც მომხმარებელმა დადო
        return Food.query.filter_by(posterID = self.id).all()
    
    def StringToIDList(self, IDString): # ფუნქცია რომელიც გადაიყვანს მოცემულ ტექსტს ლისტად ( მაგალითან followingIDs ან savedFoodsIDs )
        IDs = IDString.replace(" ", "").split(",") # ამოშლის ყველა გამოტოვებულ ადგილს და "," character - ის მიხედვით შლის ლისტად
        for id in IDs: 
            if not id: IDs.remove(id) # თუ ეს ID არის NoneType ამოშლის

        # ამ ეტაპზე გვაქვს String ლისტი და ID ლისტისთვის გვჭირდება Int ლისტი

        for i in range(len(IDs)): IDs[i] = int(IDs[i]) # ყველა ელემეტნს გადაიყვანს Int-ად
        return IDs # დააბრუნებს Int ლისტს

    def FollowingIDs(self): # იმათი ID ლისტი ვისაც მომხმარებელი აფოლოვებს 
        return self.StringToIDList(self.followingIDs)

    def SavedFoodIDs(self): # იმ საჭმლის ID ლისტი რომელსაც მომხმარებელი ინახავს
        return self.StringToIDList(self.savedFoodIds)
    
    def Followers(self): # ამ მომხმარებლის ფოლოვერები
        followers = [] # ვქმნით ცარიელ ლისტს

        for user in User.query.all():
            if self.id in user.FollowingIDs(): # თუ მომხმარებლის ID არის ერთ-ერთი სხვა მომხმარებლის ფოლოვინგ ლისტში 
                followers.append(user) # დაამატებს ამ სხვა მომხმარებელს ფოლოვერების ლისტში
        return followers

    # ყველა უზერს აქვს თავისი ქულა, რომელიც განისაზღვრება:
    # ფოსტის ქულით;
    # ფოლოვერების რაოდენობით ( თითო ფოლოვერი = 10 ქულა );
    def Points(self): # ეს ფუნქცია აბრუნებს ამ ქულას
        points = 0 # ვქმნით points ცვლადს და ვანიჭებთ 0-ს

        for food in Food.query.filter_by(posterID = self.id): # ვიღებთ ყველა პოსტს
            points += food.Points() # ვუმატებთ ქულას ამ პოსტის ქულას

        points += len(self.Followers()) * 10 # ქულას ვუმატებთ ფოლოვერების რაოდენობას * 10 ზე
        return points

    def CookLevel(self):  
        # Dictionary: key არის Cooking Ranking-ის სახელი,
        # value არის მინიმალური ქულა, რაც ამ Ranking-ს სჭირდება
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

        # მომხმარებლის მიმდინარე ქულა
        points = self.Points()

        # საწყისად ვთვლით ყველაზე დაბალ Ranking-ს
        currentLevel = "Can't Boil Water"

        # ინახავს იმ Ranking-ის მინიმალურ ქულას,
        # რომელიც ამჟამად არჩეულია (თავიდან 0)
        highestPointReq = 0

        # ვამოწმებთ ყველა Ranking-ს
        for level, reqPoints in cookRankings.items():
            # თუ მომხმარებლის ქულა ჰყოფნის ამ Ranking-ს
            # და ეს Ranking უფრო მაღალია, ვიდრე აქამდე არჩეული
            if points >= reqPoints and reqPoints >= highestPointReq:
                # ვანახლებთ Ranking-ს
                currentLevel = level
                # ვიმახსოვრებთ მის ქულას როგორც ყველაზე მაღალს
                highestPointReq = reqPoints

        # ვაბრუნებთ მომხმარებლის საბოლოო Cooking Ranking-ს
        return currentLevel


    def SavedFoods(self): # საჭმელი რომელიც მომხმარებელს აქვს შენახული
        savedFoods = []
        
        # ამ კოდს გადაყავს SavedFoodIDs Int ლისტი, Food კლასის ლისტად.
        for id in self.SavedFoodIDs(): 
            for food in Food.query.all():
                if food.id == id: # თუ ერთ-ერთი საჭმლის ID ემთხვევა შენახულ საჭმლის IDs
                    savedFoods.append(food) # დაამატებს ლისტში

        return savedFoods

    def HasSavedFood(self, foodID): # აბრუნებს bool-ს ( აქვს თუ არა მომხმარებელს საჭმელი შენახული )
        return foodID in self.SavedFoodIDs()

class Food(db.Model):
    id = db.Column(db.Integer, primary_key = True) # უნიკალური ID რომლითაც ვეძებთ საჭმელს
    posterID = db.Column(db.Integer, db.ForeignKey("user.id"), default = 0) # იმ მომხმარებლის ID რომელმაც ეს საჭმელი შექმნა 
    name = db.Column(db.String(200), nullable = False) # საჭმლის სახელი
    description = db.Column(db.String(1000), default = " ") # საჭმლის აღწერა
    postDate = db.Column(db.DateTime) # საჭმლის პოსტის დრო
    img = db.Column(db.String(100)) # საჭმლის ფოტოს სახელი, Static ფოლდერში 
    ingredients = db.Column(db.String(100), nullable = False) # საჭმლის ინგრედიენტები ( გამოიყოფა ','-თი )
    duration = db.Column(db.Integer, default = 0) # საჭმლის მომზადების დრო

    
    def Reviews(self): # ყველა რევიუ რაც ამ ფოსტს აქვს
        return Review.query.filter_by(foodID = self.id).all()
    
    # ყველა საჭმელს აქვს თავისი ქულა
    # რომელიც განისაზღვრება რევიუს მიხედვით
    def Points(self):
        points = 0
        for review in self.Reviews():
            points += float(review.rating) # ქულას ვუმატებთ ყველა რევიუს რეიტინგს
        return points

    def Date(self): # რამდენი ხნის წინ დაიდო პოსტი
        return ConvertDate(self.postDate)

    def Ingredients(self): # ინგრედიენტების ლისტი
        # იღებს ინგრედიენტების სტრინგს, lowercase-ში აყენებს, შლის გამოტოვებებს და შლის ელმენტებათ ","-თი
        # მაგალითად :
        # თუ self.ingredients = "Cheese, Milk, Bread", დააბრუნებს ["Cheese", "Milk", "Bread"] ლისტს
        return self.ingredients.lower().replace(" ", "").split(",")
    
    def Poster(self): # აბრუნებს იმ მომხმარებელს რომელმაც ეს საჭმელი გააკეთა
        return User.query.filter_by(id = self.posterID).first()
    
    def Rating(self): # აბრუნებს ამ ფოსტის რეიტინგს ( ყველა რევიუს რეიტინგის საშუალოს )
        reviews = self.Reviews()
        if not reviews:
            return "Unrated" # თუ ამ ფოსტს არ აქვს რევიუ დააბრუნებს "Unrated"

        sum = 0 # რეიტინგს ჯამი
        for review in reviews:
            sum += float(review.rating)

        return str(sum / len(reviews))[:3] # გადაყავს ჯამი გაყოფილი რევიუს რაოდენობაზე სტრინგში და იღებს პირველ 3 ნიშანს (.-ის ჩათვლით)
        # პირველ 3 ნიშანს, რადგან შეიძლება რიცხვი იყოს პერიოდული, მაგალითად 1.3333.., და კოდი დააბრუნებს 1.3-ს
    
    def HasUserReviewed(self, userID): # ამოწმებს მომხმარებელს აქვს თუ არა ეს პოსტი დარევიუებული
        for review in self.Reviews():
            if review.posterID == userID:
                return True
        return False
    
class Review(db.Model):
    id = db.Column(db.Integer, primary_key = True) # უნიკალური ID რომლითაც ვეძებთ რევიუს
    foodID = db.Column(db.Integer, db.ForeignKey("food.id"), default = 0) # საჭმლის ID
    posterID = db.Column(db.Integer, db.ForeignKey("user.id"), default = 0) # მომხმარებლის ID ( ვინც დაწერა რევიუ )
    content = db.Column(db.String(1000), nullable = False) # რევიუს Content-ი / Comment-ი
    rating = db.Column(db.String(3)) # რევიუს რეიტინგი
    postDate = db.Column(db.DateTime) # რევიუს დაპოსტვის დრო

    def Date(self): # რამდენი ხნის წინ დაიდო რევიუ
        return ConvertDate(self.postDate)

    def User(self): # მომხმარებელი რომელმაც ეს რევიუ დადო
        return User.query.filter_by(id = self.posterID).first()
    
    def Food(self): # საჭმელი რომელზეც ეს რევიუ დაიწერა
        return Food.query.filter_by(id = self.foodID).first()
    
def ConvertDate(postDate): # ეს ფუნქცია აბრუნებს რამდენი დრო გავიდა postDate-ი დან.
        now = datetime.now() # იღებს ეხლანდელ დროს

        timeDifference = now - postDate # გამოიანგარიშებს გასულ დროს

        days = timeDifference.days       # გასული დრო დღეებში
        seconds = timeDifference.seconds # გასული დრო წამებში
        hours = seconds // 3600          # გასული დრო საათებში
        minutes = (seconds % 3600) // 60 # გასული დრო წუთებში

        if days > 365:      return f"{days // 365}y ago" # თუ დღეები აჭარბებს 365-ს დააბრუნებს "{დღეები გაყოფილი 365-ზე} წლის წინ"
        elif days > 30:     return f"{days // 30}m ago"  # თუ დღეები აჭარბებს 30-ს და არ აჭარბებს 365-ს დააბრუნებს "{დღეები გაყოფილი 30-ზე} თვის წინ"
        elif days > 0:      return f"{days}d ago"        # თუ დღეები აჭარბებს 0-ს და არ აჭარბებს 30-ს დააბრუნებს "{დღეები} დღის წინ"
        elif hours > 0:     return f"{hours}h ago"       # თუ საათები აჭარბებს 0-ს და არ აჭარბებს 24-ს დააბრუნებს "{საათები} საათის წინ"
        elif minutes > 0:   return f"{minutes}min ago"   # თუ წუთები აჭარბებს 0-ს და არ აჭარბებს 60-ს დააბრუნებს "{წუთები} წუთის წინ"
        else:               return "Just now"            # თუ წამები აჭარბებს 0-ს და არ აჭარბებს 60-ს დააბრუნებს "Just Now"
        
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    userToID = db.Column(db.Integer, db.ForeignKey("user.id"), default = 0)
    userFromID = db.Column(db.Integer, db.ForeignKey("user.id"), default = 0)
    content = db.Column(db.String(1000), default = "Notification")
    link = db.Column(db.String(100), default = "#")