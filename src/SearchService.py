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
import time
from embedding.SemanticEmbeddingService import HuggingfaceEmbeddingService
from embedding.TogetherAIEmbedding import TogetherAIEmbeddingService
from LoggingService import LoggingService
from credentials.APIKeyLoader import APIKey_Loader


class SearchService:
    def __init__(self):
        api_key_loader = APIKey_Loader(file_path='credentials/api_keys.json')
        pass

    def handle_request(self, query, num_results, is_pro_user=False):
        start_time = time.time()  # Record the start time

        google_search = GoogleSearchService()
        gpt_service = GPTService.GPTService()
        semantic_search_service = TogetherAIEmbeddingService()
        logging_service = LoggingService.LoggingService()

        results = google_search.perform_google_search_multithread(
            query=query, num_results=num_results)
        if results is None:
            print("No results found.")
            return

        # TODO: Call Semantic Search Service here to compute embeddings
        # embeddings = semantic_search_service.get_embedding()
            #results_df)

        print("Got results, now sending a request to GPTService")
        print(f'Results: {results}')
        used_websites = get_sources(results)
        
        print(f'Used sources: {used_websites}')
        
        sources_string = get_sources_string(results)

        prompt = f"Answer this question in English: {query}; Respond scientifically and fact-orientated using the text and information provided to you from these websites: {used_websites} with this content: {sources_string}. Use the content provided for you to form you answer. Use direct qoutes from the sources and link them with numbers in your response text. Qoute from sources using these brackets []. Return you answer in markdown format."

        answer = gpt_service.stream_response(query=prompt)
        
        print(f'Final answer: {answer}')

        # Measure the time
        end_time = time.time()
        execution_time = end_time - start_time

        print(
            f"Search Service took {execution_time} seconds to complete request.")

        return answer


if __name__ == '__main__':
    service = SearchService()
    
    query = "Recent attack on donald trump"
    num = 30
    
    request = service.handle_request(query=query, num_results=num, is_pro_user=False)
    
    print(f"Search service returned this answer: {request}")