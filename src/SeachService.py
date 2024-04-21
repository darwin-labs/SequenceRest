import os
import re
import pandas as p
import yaml
from search import GPTService
import search
import SourceService
import GoogleSearchService

class SearchService:

    def __init__(self):
        pass
    
    

    def handle_request(self, query, num_results, is_pro_user):
        google_search = GoogleSearchService()
        gpt_service = GPTService()
        
        results = google_search.search(query=query, num_results=num_results)
        
        for result in results:
            prompt = "Answer this question scientifically and fact-orientated using the text and information in this source: {result.url} with this content: {result.text}" 
            gpt_service.getResponse("")
        
        
search = SearchService()

search.handle_request("How to roast coffe", 5, False)
    