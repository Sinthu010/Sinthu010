
import requests
from pprint import pprint




def get_first_request():
    ingredient = input("What ingredient would you like to search for? ")
    meal_type = input("What meal type are you looking for? Breakfast, Lunch, Dinner, Snack or Teatime: ")
    url = "https://api.edamam.com/api/recipes/v2?type=public&q={}&app_id=5dd21489&app_key=f376ebeef0cd80b4a7e7bc5324835a67&mealType={}".format(ingredient, meal_type)
    response = requests.get(url)
    recipe = response.json()
    print("{} recipe's found.".format(recipe['count']) + '\n')
    number = 1
    with open('recipe.txt', 'w+') as text_file:
        for item in recipe['hits']:
            print("{}. ".format(number) + item['recipe']['label'])
            name = "{}. ".format(number) + item['recipe']['label'] + '\n'
            text_file.write(name)
            number += 1
    more_rec = input("Would you like to see more recipes? y/n: " + '\n')
    if more_rec == 'y':
        get_next_request(recipe['_links']['next']['href'], number)
    else:
        print("Done")
    
    wanted_recipe = input("Which recipe would you like to see? ")
    for item in recipe['hits']:
        
        # SOMETIMES THE RECIPE NAME IS IN THE LIST TWICE!
        
        if wanted_recipe == item['recipe']['label']:
            print("Recipe found!")
            print("Ingredients for this recipe: ")
            x = 0
            while x < len(item['recipe']['ingredientLines']):
                print(item['recipe']['ingredientLines'][x])
                x += 1
                
                
            print(item['recipe']['mealType'])
            recipe_url = item['recipe']['url']
            print(recipe_url)
            get_recipe(recipe_url)

def get_next_request(next_url, number):
    response = requests.get(next_url)
    recipe = response.json()
    with open('recipe.txt', 'a') as text_file:
        for item in recipe['hits']:
            print("{}. ".format(number) + item['recipe']['label'])
            name = "{}. ".format(number) + item['recipe']['label'] + '\n'
            text_file.write(name)
            number += 1
    more_rec = input("Would you like to see more recipes? y/n: " + '\n')
    if more_rec == 'y':
        get_next_request(recipe['_links']['next']['href'], number)
    else:
        print("Done")
    wanted_recipe = input("Which recipe would you like to see? ")
    for item in recipe['hits']:
        if wanted_recipe == item['recipe']['label']:
            print("Recipe found!")
            print(item['recipe']['ingredientLines'])
            print(item['recipe']['mealType'])
            recipe_uri = item['recipe']['uri']
            print(recipe_uri)
            response = requests.get(recipe_uri)
            print(response)
            recipe_page = response.json()
            #print(recipe_page)
            #with open("file.json", "r") as read_file:
            #    data = json.load(read_file)
            #    print(response)
            return recipe_uri
            break
        
def get_recipe(recipe_url):
    import json 
    #https://researchdatapod.com/how-to-solve-python-jsondecodeerror-expecting-value-line-1-column-1-char-0/
    # to solve: Python JSONDecodeError: Expecting value: line 1 column 1 (char 0)
    from requests.exceptions import HTTPError
    try:
        response = requests.get(recipe_url)
        status = response.status_code
        print(status)
        if (status != 204 and response.headers["content-type"].strip().startswith("application/json")):
            try:
                print("JSON RESPONSE")
                json_response = response.json()
                print(json_response)
            except ValueError:
                print('Bad Data from Server. Response content is not valid JSON')
        elif (status != 204):
            try:
                print("RESPONSE.TEXT")
                #print(response.text)
                #response = requests.get(...)
                json_data = json.loads(response.text)
                print(json_data)
            except ValueError:
                print('Bad Data From Server. Reponse content is not valid text')
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

get_first_request()



# Python Tutorial: Working with JSON Data using the json Module
# Working With APIs in Python - Pagination and Data Extraction

#search returns 20 results
#returns next 20 results
# variable scope: local, enclosing, global, built-in
