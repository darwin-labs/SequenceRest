import requests
# import faiss
import pandas as pd
import numpy as np
from transformers import GPT2TokenizerFast
import tiktoken
from embedding import EmbeddingService
import os
from together import Together


class HuggingfaceEmbeddingService:
    def __init__(self, config):
        self.config = config
        openai.api_key = config.get('llm_service').get(
            'openai_api').get('api_key')

    @staticmethod
    def batch_call_embeddings(texts, chunk_size=1000):
        texts = [text.replace("\n", " ") for text in texts]
        embeddings = []
        for i in range(0, len(texts), chunk_size):
            response = openai.Embedding.create(
                input=texts[i: i + chunk_size], engine=BASE_MODEL
            )
            embeddings += [r["embedding"] for r in response["data"]]
        return embeddings

    @staticmethod
    def compute_embeddings_for_text_df(text_df: pd.DataFrame):
        """Compute embeddings for a text_df and return the text_df with the embeddings column added."""
        print(f'compute_embeddings_for_text_df() len(texts): {len(text_df)}')
        text_df['combined_text'] = text_df.apply(
            lambda x: f"{x['title']} {x['description']} {x['text']}".replace("\n", " "), axis=1)
        text_df['embedding'] = BatchOpenAISemanticSearchService.batch_call_embeddings(
            text_df['combined_text'].tolist())
        return text_df

    def search_related_source(self, text_df: pd.DataFrame, target_text, n=30):
        if not self.config.get('source_service').get('is_use_source'):
            col = ['title', 'url', 'description',
                   'text', 'similarities', 'rank', 'docno']
            return pd.DataFrame(columns=col)

        if self.sender is not None:
            self.sender.send_message(
                msg_type=MSG_TYPE_SEARCH_STEP, msg="Searching from extracted text")
        print(f'search_similar() text: {target_text}')
        embedding = BatchOpenAISemanticSearchService.batch_call_embeddings([target_text])[
            0]
        text_df = BatchOpenAISemanticSearchService.compute_embeddings_for_text_df(
            text_df)
        text_df['similarities'] = text_df['embedding'].apply(
            lambda x: cosine_similarity(x, embedding))
        result_df = text_df.sort_values(
            'similarities', ascending=False).head(n)
        result_df['rank'] = range(1, len(result_df) + 1)
        result_df['docno'] = range(1, len(result_df) + 1)
        return result_df[['title', 'url', 'description', 'text', 'similarities', 'rank', 'docno']]

    def together_get_embeddings(self, text):
        model = ''

    @staticmethod
    def post_process_gpt_input_text_df(gpt_input_text_df, prompt_token_limit):
        gpt_input_text_df['text'] = gpt_input_text_df['text'].apply(
            lambda x: re.sub(r'\[[0-9]+\]', '', x))
        gpt_input_text_df['len_text'] = gpt_input_text_df['text'].apply(
            lambda x: len(x))
        gpt_input_text_df['len_token'] = gpt_input_text_df['text'].apply(
            lambda x: num_tokens_from_string(x))

        gpt_input_text_df['cumsum_len_text'] = gpt_input_text_df['len_text'].cumsum(
        )
        gpt_input_text_df['cumsum_len_token'] = gpt_input_text_df['len_token'].cumsum(
        )

        max_rank = gpt_input_text_df[gpt_input_text_df['cumsum_len_token']
                                     <= prompt_token_limit]['rank'].max() + 1
        gpt_input_text_df['in_scope'] = gpt_input_text_df['rank'] <= max_rank
        url_id_list = gpt_input_text_df['url_id'].unique()
        url_id_map = dict(zip(url_id_list, range(1, len(url_id_list) + 1)))
        gpt_input_text_df['url_id'] = gpt_input_text_df['url_id'].map(
            url_id_map)
        return gpt_input_text_df


class TogetherAIEmbeddingService:

    def __init__(self, api_key):
        self.api_key = api_key

    def get_text_embedding(self, text):
        model_name = 'togethercomputer/m2-bert-80M-8k-retrieval'

        model = TogetherEmbedding(model_name=model_name, api_key=api_key)

        embedding = model.get_text_embedding(text)

        return embedding
'''
    def get_embeddings(texts: lambdaist[str], model: str) -> list[list[float]]:
        texts = [text.replace("\n", " ") for text in texts]
        outputs = client.embeddings.create(model=model, input=texts)
        return [outputs.data[i].embedding for i in range(len(texts))]
        '''
