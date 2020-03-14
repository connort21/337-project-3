# 337-project-3
CS 337: Natural Language Processing, Project 3: Conversational Interface- pulls information from online recipes, now with a conversational interface

This project is built on Python 3.8
Project can be found on Github at <https://github.com/connort21/337-project-3>

## To run submission:
* Install dependencies using `pip install -r requirements.txt`
* In console, type `python recipe.py` to begin.  Follow instructions.
* Commands
    * Recipe retrieval and display
        * "Show me the ingredients list"
        * "Show me the tools list"
    * Navigation utterances
        * "Go back one step"
        * "Go to the next step"
        * "Take me to the 1st step"
        * "Take me to the <i>n</i>-th step"
    * Simple "how to" questions
        * "How do I ...?"
    * Simple "what is" questions
        * "What is ...?"

Recipes provided to the project must be from <https://www.allrecipes.com/>

## Dependencies:
This project requires the following Python modules:
* PrettyPrinter
* fractions
* copy
* bs4 (BeautifulSoup)
* spacy
* unicodedata
* re
* nltk
