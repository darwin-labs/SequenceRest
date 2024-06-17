from googlesearch import search
import requests


if __name__ == '_main__':
    query = "WWWDC24"

    result = search(query, num_results=5)
    
     Print the results
    print(f"Top {len(list(results))} results for '{query}':")
    for i, result in enumerate(results, start=1):
        print(f"{i}. {result}")