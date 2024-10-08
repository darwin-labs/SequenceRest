import os
import requests
from search import GPTService
from abc import ABC, abstractmethod


import pandas as pd

class LLMService(ABC):
    
    prompt_limit = 3000
    
    
    def __init__(self):
        pass
    
    def clean_response_text(self, response_text: str):
        return response_text.replace("\n", "")
    
    def get_prompt(self, search_text: str, input_text: pd.DataFrame, websites: str, use_source: bool):
        
        if use_source: 
            prompt_engineering = f"\n\nAnswer this question in English: {search_text}; Respond scientifically and fact-orientated using the text and information provided to you from these websites: {websites}. Use the content provided for you to create your based answer. Use direct qoutes from the sources and link them with numbers in your response text. Quote from sources using these brackets []. Return you answer in markdown format."
            prompt = ""
            for index, row in input_text.iterrows():
                prompt += f"""{row['text']}\n"""
            prompt = prompt[:self.prompt_limit]
            return prompt_engineering + prompt
        else:
            return f"\n\nAnswer the question '{search_text}' with about 100 words:"
     
    def get_prompt_v2(self, search_text: str, input_text_df: pd.DataFrame):
        context_str = ""
        gpt_input_text_df = gpt_input_text_df.sort_values('url_id')
        url_id_list = gpt_input_text_df['url_id'].unique()
        for url_id in url_id_list:
            context_str += f"Source ({url_id})\n"
            for index, row in gpt_input_text_df[gpt_input_text_df['url_id'] == url_id].iterrows():
                context_str += f"{row['text']}\n"
            context_str += "\n"
        context_str = context_str[:prompt_limit]
        prompt = \
            f"""
Answer with 100 words for the question below based on the provided sources using a scientific tone. 
If the context is insufficient, reply "I cannot answer".
Use Markdown for formatting code or text.
Source:
{context_str}
Question: {search_text}
Answer:
"""
        return prompt       
    
    