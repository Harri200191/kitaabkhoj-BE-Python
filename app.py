from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import spacy
from collections import Counter
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
import time

app = Flask(__name__)

def is_person_name(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return True

    return False

def count_occurrences(soup, target_word):
    vicinity_words = ["book", "novel", "author"]
    content = soup.find('div', {'id': 'mw-content-text'})
    text = content.get_text().lower()

    target_word_count = text.count(target_word.lower())

    vicinity_counts = Counter()
    for vicinity_word in vicinity_words:
        vicinity_pattern = re.compile(fr'\b{vicinity_word.lower()}\b')
        vicinity_counts[vicinity_word] = len(re.findall(vicinity_pattern, text))

    return target_word_count, vicinity_counts

def process_text_lines(text_lines): 
    for line in text_lines:
        if is_person_name(line) == True:
            return line
        
    return None

def search_wikipedia(text_lines): 
    time.sleep(1)
    for line in text_lines:
        if is_person_name(line) == True: 
            continue
        else:
            search_url = f'https://en.wikipedia.org/wiki/{line}'
            response = requests.get(search_url)
            
            if response.status_code != 200:
                print(f"Failed to retrieve data. Status code: {response.status_code}")
                continue
            
            soup = BeautifulSoup(response.text, 'html.parser')


            if soup: 
                target_word_count, vicinity_counts = count_occurrences(soup, line)
 
                print(f"\nOccurrences of the word '{line}' in the article: {target_word_count}")
                print("\nOccurrences in the vicinity:")
                for word, count in vicinity_counts.items():
                    print(f"{word.capitalize()}: {count}")

                if vicinity_counts["book"] + vicinity_counts["novel"] > 30:
                    return line
                else:
                    time.sleep(1)
                    continue      
            else:
                return None
            
    return None

def get_wikipedia_previews(query): 
    driver = webdriver.Chrome()  
 
    driver.get('https://en.wikipedia.org/w/index.php?title=Special:Search&profile=default&search=')
 
    search_input = driver.find_element(By.NAME, 'search')
    search_input.send_keys(query)
    search_input.send_keys(Keys.RETURN)
 
    driver.implicitly_wait(5) 
 
    page_source = driver.page_source 
    soup = BeautifulSoup(page_source, 'html.parser')
    preview_divs = soup.find_all('span', id= 'Books_and_stories')

    if len(preview_divs) > 0:
        return True
    else:
        return False 
 

@app.route('/process_text', methods=['GET'])
def process_text():
    try:
        data = request.args.get('txt') 
        text_lines = data.split('\n')

        author = process_text_lines(text_lines)
        for line in text_lines:
            if (get_wikipedia_previews(line) == True):
                book = line
                break
            else:
                print("Nope") 

        return jsonify({'author': author, 'book': book})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=False)
