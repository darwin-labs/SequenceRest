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

from langchain_together.embeddings import TogetherEmbeddings
from typing import List
import requests
import pandas as pd
import tiktoken
import os
import together 
import asyncio
from APIKeyLoader import APIKey_Loader

class TogetherAIEmbeddingService:

    def __init__(self, model_name= 'togethercomputer/m2-bert-80M-8k-retrieval'):
        self.api_key = _get_api_key()
        self.model_name = model_name
        
        
    def _get_api_key(self):
        api_key_service = APIKey_Loader()
        
        key = api_key_service.get_api_key('together_ai')

        return key        

    def get_text_embedding(self, text):

        model = TogetherEmbeddings(model=self.model_name)

        embedding = model.embed_query(text)        
        
        return embedding
    
    async def get_text_embedding_async(self, text: str):
        
        embedding_model = TogetherEmbeddings(model=model)
        
        embedding = embedding_model.aembed(text)
        
        return embedding
        
'''
    def get_embeddings(texts: lambdaist[str], model: str) -> list[list[float]]:
        texts = [text.replace("\n", " ") for text in texts]
        outputs = client.embeddings.create(model=model, input=texts)
        return [outputs.data[i].embedding for i in range(len(texts))]
        '''

