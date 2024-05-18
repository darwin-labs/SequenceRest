from transformers import GPT2TokenizerFast
import torch
import transformers

tokenizer = GPT2TokenizerFast.from_pretrained('Xenova/text-embedding-ada-002')
tokens = tokenizer.encode('hello world') 
assert tokens == [15339, 1917]
print(tokens)

model_id = "meta-llama/Meta-Llama-3-8B"

pipeline = transformers.pipeline(
    "text-generation", model=model_id, model_kwargs={"torch_dtype": torch.bfloat16}, device_map="auto"
)

pipeline("How do i roast coffe?")
