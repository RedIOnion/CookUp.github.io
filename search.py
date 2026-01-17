from models import Food
from datetime import datetime


def CleanedIngredientsList(ingredients): # გადაყავს ინგრედიენტების String-ი List-ში
    if ingredients == "": return None

    return ingredients.lower().replace(" ", "").split(",")

# ფუნქცია ამოწმებს რა ინგრედიენტები გვაქვს და ადარებს თითოეულ საჭმელს მისთვის საჭირო ინგრედიენტების სიას.
# თუ საჭმლისთვის საჭირო ყველა ინგრედიენტი ჩვენს სიაში შედის, მაშინ ეს საჭმელი შეიძლება მომზადდეს და ემატება შედეგს. 
# მაგალითად, თუ გვაქვს წყალი, ფქვილი, კვერცხი და მარილი, 
#
# ხოლო საჭმელებია 
# ბლინი    (სჭირდება ფქვილი, კვერცხი და წყალი),
# პური     (სჭირდება ფქვილი, წყალი და საფუარი),
# ომლეტი  (სჭირდება კვერცხი და ზეთი)
# 
# ფუნქცია დააბრუნებს მხოლოდ ბლინს, რადგან მისი ყველა ინგრედიენტი გვაქვს.
def FoodFromIngredients(cleanedIngredientsList):
    foods = Food.query.all() # ყველა საჭმელი

    # თუ ინგრედიენტები არ გვაქვს მითითებული ანუ მომხმარებელს არ აქვს სურვილი საჭმელი ინგრედეინეტის მიხედვით მოძებნოს და უბრალოდ ყველა საჭმელს ვაბრუნებთ
    if cleanedIngredientsList == None:
        return foods

    searchedFoods = []

    for food in foods:
        foodIngredients = food.Ingredients() # ინგრედიენტები რომელსაც უნდა ვაკმაყოფილებდეთ

        # ვქმნით ცვლადს რომელიც განსაზღვრავს გვაქვს თუ არა საჭმლის მომზადებისთვის საჭირო ინგრედიენტები, რომელსაც თუ საჭიროა მომავალში შევცვლით
        allIngredientsAllowed = True

        for ingredient in foodIngredients:
            if ingredient not in cleanedIngredientsList: # თუ რომელიმე ინგრედიენტი არ გვაქვს მაშინ არ გვატყობს ეს საჭმელი
                allIngredientsAllowed = False
                break

        if allIngredientsAllowed:
            searchedFoods.append(food)

    return searchedFoods

def SortedFoodFromIngredients(foodFromIngredients, sort): # sort ბრძანების საშუალებით ალაგებს საჭმელს მომხმარებლის მიერ არჩეული sort ტიპით
    if sort == "new":
        return foodFromIngredients
    elif sort == "top": 
        foodFromIngredients.sort(key=lambda item: item.Rating(), reverse=True)
        return foodFromIngredients
    elif sort == "review count":
        foodFromIngredients.sort(key=lambda item: item.Rating(), reverse=True)
        foodFromIngredients.sort(key=lambda food: len(food.Reviews()), reverse=True)
        return foodFromIngredients

def FilterTime(foods, seconds): # აბრუნებს იმ საჭმელს რომელიც მოცემულ დროზე ადრე დაიდო
    now = datetime.now()
    timedFoods = []

    for food in foods:
        if (now - food.postDate).total_seconds() <= seconds:
            timedFoods.append(food)
    return timedFoods

def Search(cleanedIngredientsList, sort, time):
    foodFromIngredients = FoodFromIngredients(cleanedIngredientsList)

    foods = SortedFoodFromIngredients(foodFromIngredients, sort)

    if time == "1h":
        foods = FilterTime(foods, 3600)
    elif time == "24h":
        foods = FilterTime(foods, 86400)
    elif time == "7d":
        foods = FilterTime(foods, 604800)
    elif time == "30d":
        foods = FilterTime(foods, 2592000)

    return foods