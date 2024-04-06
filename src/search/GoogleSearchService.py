from bs4 import BeautifulSoup
import json
import requests
import GPTService
from serpapi import GoogleSearch
from googlesearch import search as google_search

GOOGLE_SEARCH_API_KEY = "AIzaSyD3aAJ8LXW-4BaDCgjPPx1zXWrbBwOcyBY"

class GoogleSearchService:
    def __init__(self):
        pass

    def search(self, query, num_results=10, lang='en', advanced=True, sleep_interval=0.5):
        try:
            results = google_search(query, num_results=num_results, lang=lang)
            search_results = []
            for result in results:
                search_results.append({
                    "title": result,
                    "url": result
                })
            return search_results
        except Exception as e:
            print("Error making request:", e)
            return None

search_service = GoogleSearchService()
    
query = "Coffee"
num_results = 20
    
search_results = search_service.search(query, num_results=num_results)
if search_results:
    for result in search_results:
        print(result.get("title"), ":", result.get("url"))
else:
    print("No results found.")
