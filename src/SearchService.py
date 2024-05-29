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


class SearchService:
    def __init__(self):
        pass

    def handle_request(self, query, num_results, is_pro_user=False):
        start_time = time.time()  # Record the start time

        google_search = GoogleSearchService()
        gpt_service = GPTService.GPTService()
        semantic_search_service = HuggingfaceEmbeddingService()

        results = google_search.perform_google_search_multithread(
            query=query, num_results=num_results)
        if results is None:
            print("No results found.")
            return

        results_df = pd.DataFrame(results)

        # TODO: Call Semantic Search Service here to compute embeddings
        embeddings = semantic_search_service.compute_embeddings_for_text_df(
            results_df)

        print("Got results, now sending a request to GPTService")
        used_websites = get_sources(results)
        sources_string = get_sources_string(results)

        prompt = f"Answer this question in English: {query}; Respond scientifically and fact-orientated using the text and information provided to you from these websites: {used_websites} with this content: {sources_string}. Use the content provided for you to form you answer. Use direct qoutes from the sources and link them with numbers in your response text. Qoute from sources using these brackets []. Return you answer in markdown format."

        answer = gpt_service.perform_search(query=prompt)

        # Measure the time
        end_time = time.time()
        execution_time = end_time - start_time

        print(
            f"Search Service took {execution_time} seconds to complete request.")

        return answer
