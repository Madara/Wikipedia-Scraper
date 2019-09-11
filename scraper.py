import requests
import re
import wikipedia
import io
from bs4 import BeautifulSoup

print("Hello and Welcome to Wikipedia Scraper v0.1!")

lang = {"english":"en", "dutch":"de", "french":"fr", "spanish":"es", "italian":"it", "polish":"pl", "swedish":"sv"}

topic = input("Topic Name: ")
language = input("Language: ").lower()
topic_page = wikipedia.page(topic)
wikipedia.search(topic_page)
topic_url = (topic_page.url)
chosen_lang = lang.get(language)
topic_url = re.sub("en", chosen_lang, topic_url)
response = requests.get(topic_url)
assert response.ok

with io.open((f"{topic}_scrape.txt"), "w", encoding="utf-8") as file:
    file.write((f"{topic}").upper() + " WIKIPEDIA: \n")
    file.write("------------------------------------------------------------\n")
    file.write("Wikipedia Link: " + topic_url)
    file.write("\n------------------------------------------------------------\n")
    document = BeautifulSoup(response.text, 'html.parser')
    for paragraph in document.find_all('p'):
        text = (paragraph.get_text())
        filtered_text = re.sub("\[(.*)\]", "", text)
        file.write(filtered_text)
print("Scrape Successful!")
