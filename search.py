from models import Food
from datetime import datetime


def CleanedIngredientsList(ingredients):
    rawIngredients = ingredients.split(",")

    ingredientList = []

    for ingredient in rawIngredients:
        cleanedIngredient = ingredient.lower().replace(" ", "")

        if cleanedIngredient != "":
            ingredientList.append(cleanedIngredient)

    return ingredientList

def FoodFromIngredients(cleanedIngredientsList):
    foods = Food.query.all()

    if not cleanedIngredientsList:
        return foods

    searchedFoods = []

    for food in foods:
        foodIngredients = food.Ingredients()
        allIngredientsAllowed = True

        for ingredient in foodIngredients:
            if ingredient not in cleanedIngredientsList:
                allIngredientsAllowed = False
                break

        if allIngredientsAllowed:
            searchedFoods.append(food)

    return searchedFoods

def SortedFoodFromIngredients(foodFromIngredients, sort):
    if sort == "new":
        return foodFromIngredients
    elif sort == "top": 
        foodFromIngredients.sort(key=lambda item: item.Rating(), reverse=True)
        return foodFromIngredients
    elif sort == "review count":
        foodFromIngredients.sort(key=lambda item: item.Rating(), reverse=True)
        foodFromIngredients.sort(key=lambda food: len(food.Reviews()), reverse=True)
        return foodFromIngredients

def FilterTime(foods, seconds):
    now = datetime.now()
    return [
        food for food in foods
        if (now - food.postDate).total_seconds() <= seconds
    ]

def Search(cleanedIngredientsList, sort, time):
    foodFromIngredients = FoodFromIngredients(cleanedIngredientsList)

    foods = SortedFoodFromIngredients(foodFromIngredients, sort)

    now = datetime.now()

    if time == "1h":
        foods = FilterTime(foods, 3600)
    elif time == "24h":
        foods = FilterTime(foods, 86400)
    elif time == "7d":
        foods = FilterTime(foods, 604800)
    elif time == "30d":
        foods = FilterTime(foods, 2592000)

    return foods