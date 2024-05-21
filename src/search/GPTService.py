import requests 
import json
import g4f
from g4f.client import Client
import requests
import re
import bs4
import pandas as pd
import csv
import time
import deprecated
from together import Together
import os

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
    
    def request_with_query(self, query: str, model: str, role: str):
        query_len = len(query)
        client = Client()
        print(f"Request to gpt4free with query length: {query_len}")
        
        if query_len > 16385:
            print("Prompt to long")
            return
        start_time = time.time()
        completion = client.chat.completions.create(
            model=model,
            messages=[{"role": role, "content": query}]
        )
        end_time = time.time()
        duration = end_time - start_time
        print(f"GPTService request took {duration} seconds")
        response = completion.choices[0].message.content
        print(f"GPTService responded with content: {response}")
        
        return response
    
    def perform_search(self, query: str, system_message=None):
        query_len = len(query)
        
        url = "https://api.together.xyz/v1/chat/completions"
        api_key = '8840dbe4d5a3e36272014dc405ecb6175847a08882b306999751764c2d0fe131'
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": query}
                ],
            "temperature": 1,
            "max_tokens": 500,
            "stream_tokens": False
        }
        
        response = requests.post(url, headers=headers, json=payload)
        
        decoded_response = json.loads(response.text)
                
        response_text = decoded_response['choices'][0]['message']['content']
                
        return response_text
            
        
    

if __name__ == "__main__": 
    service = GPTService()
    query = "Test query"
    model = "gpt-3.5-turbo"
    request = service.perform_search('How to roast coffe?', system_message='')
    
    
    
