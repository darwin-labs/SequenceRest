import requests
import faiss
import pandas as pd
import numpy as np
from transformers import GPT2TokenizerFast
import tiktoken
import EmbeddingService

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
        embedding_service = EmbeddingService('gpt2')
        
        texts = [text.replace("\n", " ") for text in texts]
        embeddings = []
        for i in range(0, len(texts), chunk_size):
            chunk_texts = texts[i:i+chunk_size]
            chunk_embeddings = np.array([self.embedding_service.get_embedding(text) for text in chunk_texts])
            embeddings.append(chunk_embeddings)
        return np.concatenate(embeddings, axis=0)
    
    def compute_embeddings_for_text_df(self, text_df: pd.DataFrame):
        """Compute embeddings for a text_df and return the text_df with the embeddings column added."""
        print(f'compute_embeddings_for_text_df() len(texts): {len(text_df)}')
        text_df['text'] = text_df['text'].apply(lambda x: x.replace("\n", " "))
        embeddings = self.batch_compute_embeddings(text_df['text'].tolist())
        text_df['embedding'] = embeddings.tolist()
        return text_df
        
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
    
    @staticmethod
    def post_process_gpt_input_text_df(gpt_input_text_df, prompt_token_limit):
        # clean out of prompt texts for existing [1], [2], [3]... in the source_text for response output stability
        gpt_input_text_df['text'] = gpt_input_text_df['text'].apply(lambda x: re.sub(r'\[[0-9]+\]', '', x))
        # length of char and token
        gpt_input_text_df['len_text'] = gpt_input_text_df['text'].apply(lambda x: len(x))
        gpt_input_text_df['len_token'] = gpt_input_text_df['text'].apply(lambda x: num_tokens_from_string(x))

        gpt_input_text_df['cumsum_len_text'] = gpt_input_text_df['len_text'].cumsum()
        gpt_input_text_df['cumsum_len_token'] = gpt_input_text_df['len_token'].cumsum()

        max_rank = gpt_input_text_df[gpt_input_text_df['cumsum_len_token'] <= prompt_token_limit]['rank'].max() + 1
        gpt_input_text_df['in_scope'] = gpt_input_text_df['rank'] <= max_rank  # In order to get also the row slightly larger than prompt_length_limit
        # reorder url_id with url that in scope.
        url_id_list = gpt_input_text_df['url_id'].unique()
        url_id_map = dict(zip(url_id_list, range(1, len(url_id_list) + 1)))
        gpt_input_text_df['url_id'] = gpt_input_text_df['url_id'].map(url_id_map)
        return gpt_input_text_df