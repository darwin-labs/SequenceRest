import requests 
import json
import jsonhelpers
import g4f
import requests
import re
import bs4
import pandas as pd
import csv

#GPTService for handling any type requests
class GPTService:

    MAX_CHARACTERS = 16385
    
    def getResponse(self, query):
        api_key = "lo-kud2TUZah6y5zdqTo6cSx3AE9QGn526hxktpn4A9zvT3mwwr"
        url = "https://api.llmos.dev/v1/chat/completions"

        headers = {
         "Authorization": f"Bearer {api_key}",
          "Content-Type": "application/json"
    }
        payload = self._getPayload(query, "user")

        response = requests.request("POST", url, json=payload, headers=headers)

        json_string = response.text
        
        return json_string
        

    def _getPayload(self, content, role="user", name="GPTService"):
        print(f"content is: {content} \nrole is: {role} \nname: {name}")
        model = "mistral-7b-instruct"
        payload = {
            "model": model,
        "messages": [
            {
            "content": content,
            "role": role,
            "name": "GPTService - Sequence"
            }
        ],
        "max_tokens": 10000,
        "stream": False,
        "temperture": 1,
        "top_p": 0,
        "presence_penalty": 0,
        "logit_bias": {}
    }
        print(f"payload: {payload}")
        return payload
    
    def request_with_query(self, query, model, role):
        query_len = len(query)
        print(f"Requst to gpt4free with query length: {query_len}")
        
        if query_len > MAX_CHARACTERS:
            print("Prompt to long")
            return
        
        comnpletion = g4f.completion(
            
            
        )
        
    

if __name__ == "__main__": 
    service = GPTService()
    json_content = service.getResponse("Test query")
    print(f"json content: {json_content}")
    extracted_json_data = jsonhelpers.get_model_response(json_content)
    print(f"response: {extracted_json_data}")
