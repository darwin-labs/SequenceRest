import requests
import faiss
import pandas as pd
import numpy as np
from transformers import GPT2TokenizerFast
import tiktoken

class SemanticSearchService:
    
    def __init__(self, sender=None):
        self.index = None
        self.sender = sender
    
    def _build_index(self, embeddings):
        dim = embeddings.shape[1]
        index = faiss.IndexFlatIP(dim)
        index.add(embeddings)
        self.index = index
        
    @staticmethod
    def batch_compute_embeddings(texts, chunk_size=1000):
        texts = [text.replace("\n", " ") for text in texts]
        embeddings = []
        for i in range(0, len(texts), chunk_size):
            # Placeholder for actual embedding computation logic
            # Example: Use a pre-trained model like BERT to compute embeddings
            chunk_embeddings = np.random.rand(len(texts[i:i+chunk_size]), 768)
            embeddings.append(chunk_embeddings)
        return np.concatenate(embeddings, axis=0)
        
    def search_sources_with_relation(self, data_frame: pd.DataFrame, search_text, n=30):
        if self.sender is not None:
            self.sender.send_message(msg_type=MSG_TYPE_SEARCH_STEP, msg="Searching from extracted text")
        print(f'search_similar() text: {target_text}')

        if self.index is None:
            embeddings = np.array(text_df['embedding'].tolist(), dtype=np.float32)
            self._build_index(embeddings)

        # Placeholder for actual target text embedding computation logic
        # Example: Use a pre-trained model like BERT to compute embedding for target text
        target_embedding = np.random.rand(1, 768)  # Placeholder for target text embedding

        D, I = self.index.search(target_embedding, n)
        result_df = text_df.iloc[I[0]]
        result_df['similarities'] = 1 - D[0]  # Similarity = 1 - Distance
        result_df['rank'] = range(1, len(result_df) + 1)
        result_df['docno'] = range(1, len(result_df) + 1)
        return result_df
    
    