import os
import requests
import re
import wikipedia
import io
import csv
from bs4 import BeautifulSoup


print("Hello and Welcome to Wikipedia Scraper v0.1!")

#Wikipedia Page Languages
lang = {"english":"en", "dutch":"de", "french":"fr", "spanish":"es", "italian":"it", "polish":"pl", "swedish":"sv", "portuguese":"pt"}

#User Enters the Topic of the Page they would like to Scrape.
topic = input("Topic Name: ")

#User Enters the Language they would like the page to be in from the "lang" dictionary.
language = input("Language: ").lower()

#Grabs the page that correlates to the entered topic.
topic_page = wikipedia.page(topic)

#Searches Wikipedia for the allocated page name.
wikipedia.search(topic_page)

#Gets the URL of the page found
topic_url = (topic_page.url)

#Grabs the language chosen from the dictionary.
chosen_lang = lang.get(language)

#adds shortened language (e.g. "en" (english), "fr" (french)).
topic_url = re.sub("en", chosen_lang, topic_url)

#Sends a GET request to the Wikipedia page URL (now with the added language prefix).
response = requests.get(topic_url)

#Checks if the GET request was successful.
try:
    assert response.ok
except:
    print("Assertion Error!")

#Creates a folder within the current directory titled based on the topic.
try:
    folder = (f"{topic}".capitalize() + " Wikipedia")
    os.mkdir(folder)
except FileExistsError:
    print("You have already scraped that page, please try something else.")

#Creates a text file titled based on the topic title within the created folder.
with io.open((folder + "/" + f"{topic}_scrape.txt"), "w", encoding="utf-8") as file:
    file.write((f"{topic}").upper() + " WIKIPEDIA: \n")
    file.write("------------------------------------------------------------\n")
    file.write("Wikipedia Link: " + topic_url)
    file.write("\n------------------------------------------------------------\n")

    #Parses to HTML
    document = BeautifulSoup(response.text, 'html.parser')

    #Grabs all <p> tags from the parsed data.
    for paragraph in document.find_all('p'):
        #Gets all text within all of the <p> tags.
        text = (paragraph.get_text())
        #Removes all "[x]" items from the text. (e.g. [1], [2] etc.)
        filtered_text = re.sub("\[(.*)\]", "", text)
        #Writes the final version of the text to the text file.
        file.write(filtered_text)

    print("Scrape Successful!")
