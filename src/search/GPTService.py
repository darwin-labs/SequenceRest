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
#import requests 
import json
#import g4f
#from g4f.client import Client
import requests
import re
import bs4
import pandas as pd
import csv
import time
#import deprecated
from together import Together
import os
import time
import sys
import torch
from transformers import AutoTokenizer
from transformers import AutoModelForCausalLM


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
    
    '''
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
    '''
    
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
        
        print(f'Decoded response: {decoded_response}')
                
        response_text = decoded_response['choices'][0]['message']['content']
                
        return response_text
    
    def stream_response(self, query: str, system_prompt: str = None):
        query_len = len(query)

       # client = Together(api_key=os.environ.get('TOGETHER_API_KEY'))
        client = Together(api_key='8840dbe4d5a3e36272014dc405ecb6175847a08882b306999751764c2d0fe131')
        
        stream = client.chat.completions.create(
            model='meta-llama/Llama-2-13b-chat-hf',
            messages=[
                {"role": "user", "content": query},
                {"role": "system", "content": system_prompt}
            ], 
            stream=True
        )
        for chunk in stream:
            print(chunk.choices[0].delta.content or "", end="", flush=True)
            
        
        
            
    #@deperated('This function is not yet supported, since it first downloads the model.')
    def perform_search_v2(self, query: str, system_prompt=None):
        query_len = len(query)
        
        model_id = 'openchat/openchat-3.6-8b-20240522'
        
        #Load the tokeniizer and model from HuggingFace
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        
        model = AutoModelForCausalLM.from_pretrained(model_id, torch_type=torch.bfloat16, device_map='auto')
        
        messages = [
            {
               "role": "user", "content": query 
            },
            {
                "role": "system", "content": system_prompt
            }
        ]
        
        input_ids = tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensores='pt').to(model.device)
        
        outputs = model.generate(inputs_ids, do_sample=True, temperature=0.5, max_new_tokens=1024)
        
        response = outputs[0][input_ids.shape[-1]:]
        print(tokenizer.decode(response, skip_special_tokens=False))
        
            
start_time = time.time()

if __name__ == "__main__":
    
    service = GPTService()
    query = "Who were you developed by?"
    model = "gpt-3.5-turbo"
    request = service.stream_response(query=query)

end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time:.6f} seconds")
