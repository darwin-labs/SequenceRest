from transformers import GPT2TokenizerFast, AutoTokenizer, AutoModel
import torch

class EmbeddingService:
    def __init__(self, model_name='Xenova/text-embedding-ada-002', tokenizer_class=None):
        self.model_name = model_name
        self.tokenizer = self._load_tokenizer(model_name, tokenizer_class)
        self.model = self._load_model(model_name)
    
    def _load_tokenizer(self, model_name, tokenizer_class=None):
        try:
            if tokenizer_class:
                return tokenizer_class.from_pretrained(model_name)
            return AutoTokenizer.from_pretrained(model_name)
        except ValueError as e:
            print(f"Error loading tokenizer: {e}")
            print("Falling back to GPT2TokenizerFast")
            return GPT2TokenizerFast.from_pretrained('gpt2')
    
    def _load_model(self, model_name):
        return AutoModel.from_pretrained(model_name)
    
    def encode_text(self, text):
        tokens = self.tokenizer.encode(text, return_tensors='pt')
        return tokens
    
    def get_embedding(self, text):
        tokens = self.encode_text(text)
        with torch.no_grad():
            outputs = self.model(**tokens)
        # Use the embeddings from the last hidden state (you might need to adjust this based on the model)
        embeddings = outputs.last_hidden_state
        return embeddings.mean(dim=1).squeeze()

    def change_model(self, model_name, tokenizer_class=None):
        self.model_name = model_name
        self.tokenizer = self._load_tokenizer(model_name, tokenizer_class)
        self.model = self._load_model(model_name)

    def get_tokenizer(self):
        return self.tokenizer

    def get_model(self):
        return self.model

    def tokenize_text(self, text):
        return self.tokenizer.tokenize(text)

    def get_token_ids(self, text):
        return self.tokenizer.convert_tokens_to_ids(self.tokenize_text(text))

# Example Usage:
embedding_service = EmbeddingService('gpt2')  # Adjust model name if necessary
tokens = embedding_service.encode_text('hello world')
print(tokens)