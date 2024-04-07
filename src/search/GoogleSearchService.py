from bs4 import BeautifulSoup
import json
import requests
import GPTService
from serpapi import GoogleSearch
from googlesearch import search as google_search
import time

GOOGLE_SEARCH_API_KEY = "AIzaSyD3aAJ8LXW-4BaDCgjPPx1zXWrbBwOcyBY"

class GoogleSearchService:
    def __init__(self):
        pass

    def search(self, query, num_results=10, lang='en', advanced=True, sleep_interval=0):
        try:
            results = google_search(query, num_results=num_results, lang=lang, advanced=True, sleep_interval=sleep_interval)
            search_results = []
            for result in results:
                
                search_results.append({
                    "title": result.title,
                    "url": result.url
                })
            return search_results
        except Exception as e:
            print("Error making request:", e)
            return None

search_service = GoogleSearchService()
    
query = "Coffee"
num_results = 15
    
start_time = time.time()
search_results = search_service.search(query, num_results=num_results)
end_time = time.time()
elapsed_time = end_time - start_time
print(f'request took {elapsed_time} to finish')
if search_results:
    print(f'search results: {search_results}')
else:
    print("No results found.")
