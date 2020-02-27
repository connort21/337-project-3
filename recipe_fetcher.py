from bs4 import BeautifulSoup
import requests


class RecipeFetcher:
    def scrape_recipe(self, recipe_url):
        results = {}
        page_html = requests.get(recipe_url)
        page_graph = BeautifulSoup(page_html.content, features="lxml")
        results['ingredients'] = [ingredient.text for ingredient in
                                  page_graph.find_all('span', {'itemprop': 'recipeIngredient'}) or
                                  page_graph.find_all('span', {'class': 'ingredients-item-name'})]
        results['directions'] = [direction.text.strip() for direction in
                                 page_graph.find_all('li', {'class': 'step'})
                                 or page_graph.find_all('li', {'class': 'subcontainer instructions-section-item'})]
        return results
