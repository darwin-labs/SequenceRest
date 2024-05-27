import src.SearchService
import time
import pandas as pd

search_service = SearchService()

if __name__ == '__main__':
    test_query = 'What IDE is the best for python programming?'
    num_result = 10
    is_pro = True
    
    start_time = time.time()
    
    result = search_service.handle_request(query, num_result, isPro)
    
    