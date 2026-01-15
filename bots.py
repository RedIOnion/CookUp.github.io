from models import User, Food, db, Review
from app import app

from datetime import datetime, timedelta
import random

users = [
    User(email="nova4821@botmail.com", username="nova4821", password="A9$kP2!zQeR7"),
    User(email="atlas7392@botmail.com", username="atlas7392", password="fR8!mQ2$Zx91"),
    User(email="luna1048@botmail.com", username="luna1048", password="P@7Kx2L!9sE"),
    User(email="orion5520@botmail.com", username="orion5520", password="Z8!Sx$4A1mQ"),
    User(email="echo9931@botmail.com", username="echo9931", password="1R!kQx7P@Lz"),
    User(email="pixel2847@botmail.com", username="pixel2847", password="Q9$Z!m2KxP8"),
    User(email="zen6614@botmail.com", username="zen6614", password="!7PZKxR$Qm2"),
    User(email="apollo4509@botmail.com", username="apollo4509", password="mQ!8xP$Z2KR"),
    User(email="comet8732@botmail.com", username="comet8732", password="ZP!Q9K$xR2m"),
    User(email="ember1194@botmail.com", username="ember1194", password="8Q$!xZP2mKR"),
    User(email="neo7401@botmail.com", username="neo7401", password="RZ!$P8x2mQK"),
    User(email="astro6629@botmail.com", username="astro6629", password="x!K2QZ$P8Rm"),
    User(email="lyra3058@botmail.com", username="lyra3058", password="QZ8!x$2mKPR"),
    User(email="drift9142@botmail.com", username="drift9142", password="!QmP2Z8$KRx"),
    User(email="vortex2873@botmail.com", username="vortex2873", password="Kx8!Z$P2RQm"),
]

for user in users: user.profilePic = "pfp.jpg"

now = datetime.now()
one_year_ago = now - timedelta(days=365)

def random_post_date():
    return datetime.fromtimestamp(
        random.uniform(one_year_ago.timestamp(), now.timestamp())
    )


foods = [
    Food(
        posterID=random.randint(1, 15),
        name="Plain Spaghetti",
        description="Plain spaghetti is comfort at its simplest: long noodles, hot water, nothing else. Recipe: Boil water. Add noodles. Stir once. Cook until tender. Drain. Eat warm. No sauce, no salt, just pure, humble spaghetti doing its thing.",
        postDate=random_post_date(),
        img="plain_spaghetti.png",
        ingredients="Water, Noodles",
        duration=20
    ),
    Food(
        posterID=random.randint(1, 15),
        name="Grilled Cheese",
        description="Golden, crispy bread with melted cheese inside. Recipe: Butter bread. Add cheese. Grill until golden and gooey.",
        postDate=random_post_date(),
        img="grilled_cheese.png",
        ingredients="Bread, Cheese, Butter",
        duration=10
    ),
    Food(
        posterID=random.randint(1, 15),
        name="Scrambled Eggs",
        description="Soft and fluffy scrambled eggs. Recipe: Crack eggs. Whisk. Cook on low heat while stirring gently.",
        postDate=random_post_date(),
        img="scrambled_eggs.png",
        ingredients="Eggs, Butter, Salt",
        duration=8
    ),
    Food(
        posterID=random.randint(1, 15),
        name="Peanut Butter Toast",
        description="A quick and satisfying snack. Recipe: Toast bread. Spread peanut butter evenly. Serve warm.",
        postDate=random_post_date(),
        img="peanut_butter_toast.png",
        ingredients="Bread, Peanut Butter",
        duration=5
    ),
    Food(
        posterID=random.randint(1, 15),
        name="Chicken Stir Fry",
        description="Quick stir-fried chicken with veggies. Recipe: Cook chicken. Add vegetables. Stir-fry with sauce.",
        postDate=random_post_date(),
        img="chicken_stir_fry.png",
        ingredients="Chicken, Vegetables, Oil",
        duration=25
    ),
    Food(
        posterID=random.randint(1, 15),
        name="Fruit Salad",
        description="Fresh, colorful mix of seasonal fruits. Recipe: Chop fruits. Toss together. Chill before serving.",
        postDate=random_post_date(),
        img="fruit_salad.png",
        ingredients="Apple, Banana, Grapes, Orange",
        duration=10
    ),
    Food(
        posterID=random.randint(1, 15),
        name="Ramen Noodles",
        description="Classic instant ramen, fast and comforting. Recipe: Boil water. Add noodles and seasoning. Cook for 3 minutes. Slurp responsibly.",
        postDate=random_post_date(),
        img="ramen_noodles.png",
        ingredients="Ramen Noodles, Water",
        duration=5
    ),
    Food(
        posterID=random.randint(1, 15),
        name="Mashed Potatoes",
        description="Creamy mashed potatoes made simple. Recipe: Boil potatoes. Mash with butter and milk. Season to taste.",
        postDate=random_post_date(),
        img="mashed_potatoes.png",
        ingredients="Potatoes, Butter, Milk, Salt",
        duration=30
    ),
    Food(
        posterID=random.randint(1, 15),
        name="Pancakes",
        description="Fluffy pancakes perfect for breakfast. Recipe: Mix batter. Pour on pan. Flip when bubbly. Stack and enjoy.",
        postDate=random_post_date(),
        img="pancakes.png",
        ingredients="Flour, Eggs, Milk, Sugar",
        duration=15
    ),
    Food(
        posterID=random.randint(1, 15),
        name="Tuna Sandwich",
        description="A simple, protein-packed sandwich. Recipe: Mix tuna with mayo. Spread on bread. Close and eat.",
        postDate=random_post_date(),
        img="tuna_sandwich.png",
        ingredients="Tuna, Mayonnaise, Bread",
        duration=7
    ),
    Food(
        posterID=random.randint(1, 15),
        name="Cheese Quesadilla",
        description="Crispy tortilla with melted cheese. Recipe: Add cheese to tortilla. Cook until golden on both sides.",
        postDate=random_post_date(),
        img="cheese_quesadilla.png",
        ingredients="Tortilla, Cheese, Butter",
        duration=8
    ),
    Food(
        posterID=random.randint(1, 15),
        name="Baked Chicken",
        description="Juicy oven-baked chicken. Recipe: Season chicken. Bake until cooked through. Rest before serving.",
        postDate=random_post_date(),
        img="baked_chicken.png",
        ingredients="Chicken, Spices, Oil",
        duration=40
    ),
    Food(
        posterID=random.randint(1, 15),
        name="Oatmeal",
        description="Warm and filling oatmeal. Recipe: Boil oats with milk or water. Stir until thick. Add toppings.",
        postDate=random_post_date(),
        img="oatmeal.png",
        ingredients="Oats, Milk, Water",
        duration=6
    ),
    Food(
        posterID=random.randint(1, 15),
        name="Fried Rice",
        description="Leftover rice transformed into magic. Recipe: Fry rice with egg and veggies. Add soy sauce.",
        postDate=random_post_date(),
        img="fried_rice.png",
        ingredients="Rice, Egg",
        duration=15
    ),
    Food(
        posterID=random.randint(1, 15),
        name="Avocado Toast",
        description="Simple, trendy, and tasty. Recipe: Toast bread. Smash avocado. Spread and season.",
        postDate=random_post_date(),
        img="avocado_toast.png",
        ingredients="Bread, Avocado, Salt",
        duration=5
    ),
    Food(
        posterID=random.randint(1, 15),
        name="Chocolate Milk",
        description="Sweet and nostalgic. Recipe: Mix chocolate syrup into cold milk. Stir well and enjoy.",
        postDate=random_post_date(),
        img="chocolate_milk.png",
        ingredients="Milk, Chocolate",
        duration=2
    ),
    Food(
        posterID=random.randint(1, 15),
        name="Boiled Egg",
        description="An egg. Boiled. That’s it. Recipe: Boil water. Add egg. Wait. Peel. Eat.",
        postDate=random_post_date(),
        img="boiled_egg.png",
        ingredients="Egg, Water",
        duration=10
    ),
    Food(
        posterID=random.randint(1, 15),
        name="Fried Egg",
        description="A classic fried egg with a runny yolk. Recipe: Heat pan. Crack egg. Cook until whites set.",
        postDate=random_post_date(),
        img="fried_egg.png",
        ingredients="Egg, Oil",
        duration=4
    ),
    Food(
        posterID=random.randint(1, 15),
        name="Scrambled Eggs (Plain)",
        description="Just eggs, scrambled. Recipe: Crack eggs. Stir in pan. Cook until softly set.",
        postDate=random_post_date(),
        img="scrambled_eggs_plain.png",
        ingredients="Eggs",
        duration=5
    ),
    Food(
        posterID=random.randint(1, 15),
        name="Toast",
        description="Bread, but warm and crunchy. Recipe: Put bread in toaster. Wait. Done.",
        postDate=random_post_date(),
        img="toast.png",
        ingredients="Bread",
        duration=2
    ),
    Food(
        posterID=random.randint(1, 15),
        name="Butter Toast",
        description="Toast with butter melted on top. Recipe: Toast bread. Add butter.",
        postDate=random_post_date(),
        img="butter_toast.png",
        ingredients="Bread, Butter",
        duration=3
    ),
    Food(
        posterID=random.randint(1, 15),
        name="Plain Rice",
        description="Simple steamed rice. Recipe: Rinse rice. Boil with water. Let steam.",
        postDate=random_post_date(),
        img="plain_rice.png",
        ingredients="Rice, Water",
        duration=20
    ),
    Food(
        posterID=random.randint(1, 15),
        name="Cheese Slice",
        description="A single slice of cheese. No cooking required. Recipe: Unwrap. Eat.",
        postDate=random_post_date(),
        img="cheese_slice.png",
        ingredients="Cheese",
        duration=1
    ),
    Food(
        posterID=random.randint(1, 15),
        name="Banana",
        description="Nature’s snack. Recipe: Peel. Eat.",
        postDate=random_post_date(),
        img="banana.png",
        ingredients="Banana",
        duration=1
    ),
    Food(
        posterID=random.randint(1, 15),
        name="Hot Water",
        description="Water, but hot. Recipe: Heat water. Carefully drink.",
        postDate=random_post_date(),
        img="hot_water.png",
        ingredients="Water",
        duration=3
    ),
    Food(
        posterID=random.randint(1, 15),
        name="Egg Sandwich (Bare Minimum)",
        description="Egg between bread. Recipe: Cook egg. Put between bread slices.",
        postDate=random_post_date(),
        img="egg_sandwich.png",
        ingredients="Egg, Bread",
        duration=6
    )
]

with app.app_context():
    for user in users:
        db.session.add(user)
    db.session.commit()

    for food in foods:
        db.session.add(food)

    db.session.commit()

good_reviews = [
    "Way better than I expected.",
    "Simple, but honestly really good.",
    "Perfect when you don’t want anything complicated.",
    "Comfort food at its finest.",
    "I make this all the time now.",
    "Easy, fast, and tastes great.",
    "Surprisingly enjoyable.",
    "Would definitely make again.",
]

bad_reviews = [
    "This was way too plain for me.",
    "Honestly pretty boring.",
    "Didn’t really enjoy this.",
    "Felt like something was missing.",
    "Probably wouldn’t make this again.",
    "Not terrible, but not good either.",
    "Way too bland.",
    "Disappointing overall.",
]

mixed_reviews = [
    "It’s okay, nothing special.",
    "Fine if you’re in a rush.",
    "Not bad, not great.",
    "Does the job, I guess.",
]

ratings_good = ["4", "5"]
ratings_mixed = ["3"]
ratings_bad = ["1", "2"]

def random_review_date(food_date):
    return datetime.fromtimestamp(
        random.uniform(food_date.timestamp(), now.timestamp())
    )

with app.app_context():
    users = User.query.all()
    foods = Food.query.all()

    reviews = []

    for food in foods:
        review_count = random.randint(1, 6)
        used_users = set()

        for _ in range(review_count):
            user = random.choice(users)

            # prevent same user reviewing same food twice
            if user.id in used_users:
                continue
            used_users.add(user.id)

            rating_type = random.choices(
                population=["good", "mixed", "bad"],
                weights=[50, 20, 30],  # realistic balance
                k=1
            )[0]

            if rating_type == "good":
                content = random.choice(good_reviews)
                rating = random.choice(ratings_good)
            elif rating_type == "mixed":
                content = random.choice(mixed_reviews)
                rating = random.choice(ratings_mixed)
            else:
                content = random.choice(bad_reviews)
                rating = random.choice(ratings_bad)

            review = Review(
                foodID=food.id,
                posterID=user.id,
                content=content,
                rating=rating,
                postDate=random_review_date(food.postDate)
            )

            reviews.append(review)

    db.session.add_all(reviews)
    db.session.commit()