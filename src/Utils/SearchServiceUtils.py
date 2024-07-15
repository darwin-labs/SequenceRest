import json
from tld import get_tld


def get_sources(results):
    index = 1
    
    output_string = ""
    
    for result in results:
        website_name = result['url']
        string_to_append = f"{index}. {website_name}, "
        
        output_string +=  string_to_append
    
    return output_string

def get_sources_string(results):
        sources_string = ""
        index = 1
        for result in results:
            tld = get_tld(result['url'])
            content = result['text']  # Assuming this retrieves text content from the result, adjust if necessary
            string_to_append = f"{index}. {tld}: {result['title']}, content: {content} \n"
            sources_string += string_to_append
            index += 1

        return sources_string