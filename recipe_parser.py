from recipe_fetcher import RecipeFetcher
import ingredient_parser as ingred_parse
import tool_parser as tool_parse
import method_parser as method_parse
import step_parser as step_parse


def parsed_recipe(url):
    rf = RecipeFetcher()
    scraped = rf.scrape_recipe(url)
    ingredients = ingred_parse.scrape_ingredients(scraped['ingredients'])
    tools = tool_parse.scrape_tools(scraped['directions'])
    methods = method_parse.scrape_methods(scraped['directions'])
    steps = step_parse.scrape_steps(scraped['directions'], tools, ingredients, methods)

    recipe = {'title': scraped['title'],
              'ingredients': ingredients,
              'tools': tools,
              'methods': methods,
              'steps': steps}
    return recipe
