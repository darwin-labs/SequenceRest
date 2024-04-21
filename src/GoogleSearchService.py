from bs4 import BeautifulSoup
import json
import pandas as pd
import requests
from search import GPTService   
from serpapi import GoogleSearch
from googlesearch import search as google_search
import time
from text_extract.html.trafilactura import TrafilaturaSvc
from text_extract.html.beautifulsoup_extract import BeautifulSoupSvc

from search import SearchErrors

from time import sleep


GOOGLE_SEARCH_API_KEY = "AIzaSyD3aAJ8LXW-4BaDCgjPPx1zXWrbBwOcyBY"

class GoogleSearchService:
    def __init__(self):
        pass

    def search(self, query, num_results=10, lang='en', advanced=True, sleep_interval=0):
        try:
            results = google_search(query, num_results=num_results, lang=lang, advanced=True, sleep_interval=1)
            search_results = []
            for result in results:
                text_content = extracted_sentences_from_url(result.url)
                print("result: ", result)
                search_results.append({
                    "title": result.title,
                    "url": result.url,
                    "description": result.description,
                    "text": result.text_content
                })
            return search_results
        except Exception as e:
            print("Error making request:", e)
            return None

    def call_urls_and_extract_sentences(self, results):
        name_list, url_list, description_list, text_list = [], [], [], []

        for result in search_results:
            result_url = result['url']
            text_content = self.extract_sentences_from_url(result_url)
            description = result['description']

            print(f"text content: {text_content}")


            url_list.append(result_url)
            name_list.append(result_url)
            description_list.append(description)
            text_list.append(text_content)
            
            extracted_sentences = self.extract_sentences_from_url(result_url)
            
        return name_list, url_list, description_list, text_list

    def call_one_url(self, website_tuple):
        name, url, snippet, url_id = website_tuple
        logger.info(f"Processing url: {url}")
        sentences = self.extract_sentences_from_url(url)
        logger.info(f"  receive sentences: {len(sentences)}")
        return sentences, name, url, url_id, snippet

    
    def extract_sentences_from_url(self, url):
        print("exract sentences from url being called")
        # Fetch the HTML content of the page
        try:
            response = requests.get(url, timeout=5)
        except:
            raise SearchErrors.TextExtractionFromURLFailed("Text extraction failed")
            return []
        html_content = response.text

        # Use BeautifulSoup to parse the HTML and extract the text
        extract_text = BeautifulSoupSvc.extract_from_html(self,html_content)
        print(f"Google Search Service extracted this text: {extract_text} from this url: {url}")
        return extract_text
    
    def count_tokens(input_string):
        # Split the string into tokens
        tokens = input_string.split()
    
        # Get the number of tokens
        num_tokens = len(tokens)
    
        return num_tokens

        


search_service = GoogleSearchService()
    
query = "Coffee"
num_results = 3
    
start_time = time.time()
search_results = search_service.search(query, num_results=num_results)
if search_results:
    print(f'search results: {search_results}')
    extracted_sentences = search_service.call_urls_and_extract_sentences(results=search_results)
    
    print("extracted sentences: ", extracted_sentences)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'request took {elapsed_time} to finish')
else:
    print("No results found.")
