import io
import os
import re

import csv
import requests
import wikipedia
from bs4 import BeautifulSoup

print("Hello and Welcome to Wikipedia Scraper v0.1!")

topic = input("Topic Name: ")

language = input("Language: ").lower()

lang = {"english": "en", "dutch": "de", "french": "fr", "spanish": "es", "italian": "it", "polish": "pl",
        "swedish": "sv", "portuguese": "pt"}


def get_page():
    """
    Get Wikipedia page based on the topic and language that was inputted.
    :return: requests.models.Response
    """
    topic_page = wikipedia.page(topic)
    wikipedia.search(topic_page)
    topic_url = topic_page.url
    chosen_lang = lang.get(language)
    topic_url = re.sub("en", chosen_lang, topic_url)
    response = requests.get(topic_url)
    try:
        assert response.ok
    except AssertionError:
        print("Assertion Error!")
    return response


def create_text_file():
    """
    Checks whether a folder and file exist for the scraped data.
    If not, create them. If yes, let the user know that the data's been scraped.
    :return: None
    """
    try:
        folder = (f"{topic}".capitalize() + " Wikipedia")
        os.mkdir(folder)
    except FileExistsError:
        print("You have already scraped that page, please try something else.")

    page = get_page()

    with io.open((folder + "/" + f"{topic}_scrape.txt"), "w", encoding="utf-8") as file:
        file.write(f"{topic}".upper() + " WIKIPEDIA: \n")
        file.write("------------------------------------------------------------\n")
        file.write("Wikipedia Link: " + page.url)
        file.write("\n------------------------------------------------------------\n")

        # Parses to HTML
        document = BeautifulSoup(page.text, 'html.parser')

        for paragraph in document.find_all('p'):
            # Gets all text within all of the <p> tags.
            text = (paragraph.get_text())
            # Removes all "[x]" items from the text. (e.g. [1], [2] etc.)
            filtered_text = re.sub("\[(.*)\]", "", text)
            # Writes the final version of the text to the text file.
            file.write(filtered_text)


def main():
    create_text_file()

    print("Scrape Successful!")


if __name__ == "__main__":
    main()
