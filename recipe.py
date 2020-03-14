from pprint import PrettyPrinter
from recipe_parser import parsed_recipe
from recipe_transformer import transform_recipe
from fractions import Fraction
import re


name = 'Recibot'
print('Hello! My name is ' + name)


def print_ingredients(input_recipe):
    pp = PrettyPrinter(indent=4)
    ingredients = input_recipe['ingredients']
    print('\nIngredients')
    for ingredient in ingredients:
        desc = ingredients[ingredient]['Descriptor']
        meas = ingredients[ingredient]['Measurement']
        prep = ingredients[ingredient]['Preparation']
        quantity = ingredients[ingredient]['Quantity']
        to_print = ''
        if quantity != 'to taste':
            if quantity % 1 and quantity > 1:
                to_print += str(int(quantity - (quantity % 1))) + ' '
                to_print += str(Fraction(quantity % 1)) + ' '
            else:
                to_print += str(Fraction(quantity)) + ' '
        if meas:
            to_print += meas + ' '
        if prep:
            to_print += prep + ' '
        if desc:
            to_print += desc + ' '
        to_print += ingredient
        if quantity == 'to taste':
            to_print += ' (to taste)'
        print(to_print)
    print('')


def print_tools(input_recipe):
    tools = input_recipe['tools']
    print('\nTools')
    to_print = ''
    first_tool = True
    for tool in tools:
        if first_tool:
            to_print += tool
            first_tool = False
        else:
            to_print += ', ' + tool
    print(to_print + '\n')


def print_changes(changed):
    print('\nChanges During Transformation')
    if not changed:
        print('None')
        return
    if isinstance(changed, str):
        print(changed)
    else:
        for change in changed:
            print('Substituted ' + change[1] + ' for ' + change[0])
    print('')


transformation_list = ['To vegetarian',
                       'From vegetarian to non-vegetarian',
                       'To healthy',
                       'From healthy to un-healthy',
                       'To chinese',
                       'Double the recipe',
                       'Halve the recipe',
                       'To vegan']

options = ''
for i in range(len(transformation_list)):
    options += str(i + 1) + '. ' + transformation_list[i] + '\n'


def transformation_loop(input_recipe):
    while True:
        option = input('Choose a transformation:\n' + options)
        choice = '[Error, this should never be printed]'
        try:
            i = int(option)
            choice = transformation_list[i - 1]
        except:
            print('Well, I crashed. Make sure you choose a valid number next time.')
            break

        print('You chose: ' + choice)

        input_recipe, changes = transform_recipe(input_recipe, choice)
        print_changes(changes)
        # print_recipe(recipe)

        choice = input('Would like to continue transforming the recipe or are you done with transformations?\n'
                       '1. Continue transforming\n'
                       '2. Done with transformations\n')
        if choice != '1':
            return input_recipe


def type_of_response(input_response):
    low = input_response.lower()
    if 'how do i' in low:
        return 'how to'
    for phrase in ['what is', 'ingredients', 'back', 'next']:
        if phrase in low:
            return phrase

    numbers = re.findall(r"[0-9]+", low)
    if numbers:
        number = numbers[0]
        return number

    for word in ['yes', 'no']:
        tokenized = re.findall(r"\w+", low)
        if word in tokenized:
            return word

    if 'tool' in low:
        return 'tools'

    return 'unknown'


def question(input_question):
    low = input_question.lower()
    if 'how do i ' in low:
        low = low.replace('how do i ', '')
        words = re.findall(r"\w+", low)
        params = ''
        for word in words:
            params += '+' + word
        youtube_link = 'https://www.youtube.com/results?search_query=how+to' + params
        return youtube_link
    elif 'what is ' in low:
        low = low.replace('what is ', '')
        words = re.findall(r"\w+", low)
        params = ''
        for word in words:
            if params:
                params += '+'
            params += word
        google_link = 'https://www.google.com/search?q=' + params
        return google_link
    return False


def get_next_step(current, res_type):
    if res_type == 'back':
        return current - 1
    elif res_type == 'next':
        return current + 1
    else:
        return int(res_type)


def print_step(input_recipe, step_num):
    steps = input_recipe['steps']
    if step_num > len(steps):
        print('Step ' + str(step_num) + ' is: Enjoy! (I made this one up myself)')
        return True
    else:
        step = steps[step_num - 1]
        print('Step ' + str(step_num) + ' is: ' + step)
        return False


recipe = False
while True:
    current_step = 0
    print('What would you like to do?')
    response = ''
    if not recipe:
        response = input('[1] Select a recipe or [2] Quit?\n')
    else:
        response = input('[1] Select a new recipe or [2] Quit?\n')
    if response == '2':
        break
    elif response == '1':
        url = input('Enter recipe URL: ')
        recipe = parsed_recipe(url)
    else:
        print('Sorry, I didn\'t understand that.')
        continue

    transform = input('Would you like to transform this recipe? "yes" or "no"\n')
    if 'yes' in transform.lower():
        recipe = transformation_loop(recipe)

    print('Ok, let\'s get started with "' + recipe['title'] + '." What would you like to do next?')

    recipe_done = False
    while not recipe_done:
        response = input()
        response_type = type_of_response(response)

        if response_type in ['how to', 'what is']:
            link = question(response)
            if not link:
                print('Sorry, I don\'t know how to answer that')
            else:
                print('No problem, I found this reference for you: ' + link)
            print('Should I continue to step ' + str(current_step + 1) + '?')

        elif response_type == 'ingredients':
            print_ingredients(recipe)
            print('Should I continue to step ' + str(current_step + 1) + '?')

        elif response_type == 'tools':
            print_tools(recipe)
            print('Should I continue to step ' + str(current_step + 1) + '?')

        elif response_type in ['back', 'next'] or response_type.isnumeric():
            next_step = get_next_step(current_step, response_type)
            current_step = next_step
            recipe_done = print_step(recipe, current_step)
            if recipe_done:
                break
            print('Should I continue to step ' + str(current_step + 1) + '?')

        elif response_type == 'yes':
            current_step += 1
            recipe_done = print_step(recipe, current_step)
            if recipe_done:
                break
            print('Should I continue to step ' + str(current_step + 1) + '?')

        elif response_type == 'no':
            print('What would you like to do next?')

        else:
            print('You can respond with a command, (listed in README.md) or with yes/no if asked if you would like to continue.')
            print('Should I continue to step ' + str(current_step + 1) + '?')