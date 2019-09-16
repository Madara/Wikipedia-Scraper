import io
import os
import re
import csv  # unused at the moment

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
    topic_url = re.sub("en", lang.get(language), wikipedia.page(topic).url)
    response = requests.get(topic_url)

    try:
        assert response.ok
        return response
    except AssertionError:
        print("Assertion Error!")


def create_text_file(page):
    """
    Checks whether a folder and file exist for the scraped data.
    If not, create them. If yes, let the user know that the data's been scraped.
    Print a message indicating that the scrape was successful, if so
    :return: None
    """
    try:
        folder = f"{topic.capitalize()} - Wikipedia"
        os.mkdir(folder)

        with io.open((folder + "/" + f"{topic}_scrape.txt"), "w", encoding="utf-8") as file:
            file.write(f"{topic.upper()} - WIKIPEDIA: \n")
            file.write("------------------------------------------------------------\n")
            file.write(f"Wikipedia Link: {page.url}")
            file.write("\n------------------------------------------------------------\n")

            # Parses to HTML
            document = BeautifulSoup(page.text, 'html.parser')

            for paragraph in document.find_all('p'):
                text = (paragraph.get_text())
                # Removes all "[x]" items from the text. (e.g. [1], [2] etc.), replacing them with a newline.
                filtered_text = re.sub("\[(.*)\]", "\n", text)
                # Writes the final version of the text to the text file.
                file.write(filtered_text)

            print("Scrape Successful!")

    except FileExistsError:
        print("You have already scraped that page, please try something else.")


def main():
    page = get_page()
    create_text_file(page)


if __name__ == "__main__":
    main()
