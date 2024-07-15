# Copyright (c) 2024 Darwin and Timon Harz
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
from LLMService import LLMService


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
        llm_service = LLMService()

        results = google_search.perform_google_search_multithread(
            query=query, num_results=num_results)
        
        results_df = pd.DataFrame(results)
        
        
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

        prompt = llm_service.get_prompt(search_text=query, input_text=results_df, websites=used_websites, use_source=True)

        answer = ''
        
        for partial_response in response_generator:
            answer += partial_response
        
        print(f'Final answer: {answer}')

        # Measure the time
        end_time = time.time()
        execution_time = end_time - start_time

        print(f"Search Service took {execution_time} seconds to complete request.")

        return answer


if __name__ == '__main__':
    service = SearchService()
    
    query = "Who won the EM?"
    num = 30
    
    request = service.handle_request(query=query, num_results=num, is_pro_user=False)
    
    print(f"Search service returned this answer: {request}")