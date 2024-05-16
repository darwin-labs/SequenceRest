import os
import re
import pandas as pd
import yaml
from search import GPTService
import search
import SourceService
from GoogleSearchService import GoogleSearchService
from Utils.tld import get_tld
from Utils.SearchServiceUtils import get_sources_string, get_sources

class SearchService:
    def __init__(self):
        pass

    def handle_request(self, query, num_results, is_pro_user):
        google_search = GoogleSearchService()
        gpt_service = GPTService.GPTService()

        results = google_search.perform_google_search(query=query, num_results=num_results)
        if results is None:
            print("No results found.")
            return

        print("Got results, now sending a request to GPTService")
        used_websites = get_sources(results)
        sources_string = get_sources_string(results)

        prompt = f"Answer this question in English: {query}; Respond scientifically and fact-orientated using the text and information provided to you from these websites: {used_websites} with this content: {sources_string}. Use the content provided for you to form you answer. Use direct qoutes from the sources."
        print(f"Promt: {prompt}")
        answer = gpt_service.request_with_query(query=prompt, model="gpt-3.5-turbo", role="user")
        print(f"Answer: {answer}")
        return answer


        
        
search = SearchService()

search.handle_request("What caused the SVB collapse?", 3, False)
    