import io
import os
import re

import requests
import wikipedia
from bs4 import BeautifulSoup

print("Hello and Welcome to Wikipedia Scraper v0.1!")

# Wikipedia Page Languages
lang = {"english": "en", "dutch": "de", "french": "fr", "spanish": "es", "italian": "it", "polish": "pl",
        "swedish": "sv", "portuguese": "pt"}

# User Enters the Topic of the Page they would like to Scrape.
topic = input("Topic Name: ")

# User Enters the Language they would like the page to be in from the "lang" dictionary.
language = input("Language: ").lower()


def get_page():
    topic_page = wikipedia.page(topic)
    wikipedia.search(topic_page)
    topic_url = topic_page.url
    chosen_lang = lang.get(language)
    topic_url = re.sub("en", chosen_lang, topic_url)
    response = requests.get(topic_url)
    return response


page = get_page()

try:
    assert page.ok
except AssertionError:
    print("Assertion Error!")

try:
    folder = (f"{topic}".capitalize() + " Wikipedia")
    os.mkdir(folder)
except FileExistsError:
    print("You have already scraped that page, please try something else.")

# Creates a text file titled based on the topic title within the created folder.
with io.open((folder + "/" + f"{topic}_scrape.txt"), "w", encoding="utf-8") as file:
    file.write((f"{topic}").upper() + " WIKIPEDIA: \n")
    file.write("------------------------------------------------------------\n")
    file.write("Wikipedia Link: " + page.url)
    file.write("\n------------------------------------------------------------\n")

    # Parses to HTML
    document = BeautifulSoup(page.text, 'html.parser')

    # Grabs all <p> tags from the parsed data.
    for paragraph in document.find_all('p'):
        # Gets all text within all of the <p> tags.
        text = (paragraph.get_text())
        # Removes all "[x]" items from the text. (e.g. [1], [2] etc.)
        filtered_text = re.sub("\[(.*)\]", "", text)
        # Writes the final version of the text to the text file.
        file.write(filtered_text)

    print("Scrape Successful!")
