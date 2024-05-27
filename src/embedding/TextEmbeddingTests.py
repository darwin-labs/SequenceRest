from transformers import GPT2TokenizerFast
import torch
import transformers

tokenizer = GPT2TokenizerFast.from_pretrained('Xenova/text-embedding-ada-002')
tokens = tokenizer.encode('hello world') 
assert tokens == [15339, 1917]
print(tokens)

