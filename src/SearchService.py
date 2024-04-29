import os
import re
import pandas as p
import yaml
from search import GPTService
import search
import SourceService
from GoogleSearchService import GoogleSearchService
from Utils import tld

class SearchService:
    def __init__(self):
        pass

    def handle_request(self, query, num_results, is_pro_user):
        google_search = GoogleSearchService()
        gpt_service = GPTService.GPTService()

        results = google_search.search(query=query, num_results=num_results)
        if results is None:
            print("No results found.")
            return

        print("Got results, now sending a request to GPTService")
        sources_string = self.get_sources_string(results)

        print(f"sources string: {sources_string}")

        # prompt = "Answer this question scientifically and fact-orientated using the text and information from these sources: {} with this content: {}"
        # answer = gpt_service.request_with_query()
        # print(f"Answer: {answer}")
        return

    def get_sources_string(self, results):
        sources_string = ""
        index = 1
        for result in results:
            tld = get_tld(result.url)
            content = result.text  # Assuming this retrieves text content from the result, adjust if necessary
            string_to_append = f"{index}. {tld}: {result.title}, content: {content} \n"
            sources_string += string_to_append
            index += 1

        return sources_string

        
        
search = SearchService()

search.handle_request("How to roast coffe", 1, False)
    