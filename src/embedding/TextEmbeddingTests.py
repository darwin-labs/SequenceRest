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
from transformers import GPT2TokenizerFast
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import transformers

class HuggingFaceTokenizer: 
    def __init__(self, model: str):
        self.model = model
        
    def get_valid_models(self):
        valid_models_list = [
            "bert-base-uncased",
            "bert-base-cased",
            "bert-large-uncased",
            "bert-large-cased",
            "gpt2",
            "gpt2-medium",
            "gpt2-large",
            "gpt2-xl",
            "distilgpt2",
            "roberta-base",
            "roberta-large",
            "distilroberta-base",
            "albert-base-v1",
            "albert-large-v1",
            "albert-xlarge-v1",
            "albert-xxlarge-v1",
            "albert-base-v2",
            "albert-large-v2",
            "albert-xlarge-v2",
            "albert-xxlarge-v2",
            "xlm-roberta-base",
            "xlm-roberta-large",
            "distilbert-base-uncased",
            "distilbert-base-cased",
            "distilbert-base-multilingual-cased",
            "distilbert-base-german-cased",
            "camembert-base",
            "xlm-mlm-en-2048",
            "xlm-mlm-ende-1024",
            "xlm-mlm-enfr-1024",
            "xlm-mlm-enro-1024",
            "flaubert/flaubert_small_cased",
            "flaubert/flaubert_base_uncased",
            "flaubert/flaubert_large_cased",
            "facebook/bart-base",
            "facebook/bart-large",
            "facebook/bart-large-mnli",
            "facebook/bart-large-cnn",
            "t5-small",
            "t5-base",
            "t5-large",
            "t5-3b",
            "t5-11b",
            "google/mt5-small",
            "google/mt5-base",
            "google/mt5-large",
            "google/mt5-xl",
            "google/mt5-xxl",
            "google/pegasus-xsum",
            "google/pegasus-cnn_dailymail",
            "google/pegasus-large",
            "microsoft/DialoGPT-small",
            "microsoft/DialoGPT-medium",
            "microsoft/DialoGPT-large",
            "facebook/mbart-large-cc25",
            "facebook/mbart-large-50-many-to-many-mmt",
            "facebook/mbart-large-50-one-to-many-mmt",
            "facebook/mbart-large-50-many-to-one-mmt",
            "openai-gpt",
            "transfo-xl-wt103",
            "ctrl",
            "xlnet-base-cased",
            "xlnet-large-cased",
            "reformer-enwik8",
            "reformer-crime-and-punishment",
            "longformer-base-4096",
            "longformer-large-4096",
            "longformer-large-4096-finetuned-triviaqa",
            "allenai/longformer-base-4096",
            "allenai/longformer-large-4096",
            "allenai/longformer-large-4096-finetuned-triviaqa",
            "google/reformer-enwik8",
            "google/reformer-crime-and-punishment",
            "tapas-small",
            "tapas-base",
            "tapas-large",
            "tapas-base-finetuned-sqa",
            "tapas-large-finetuned-sqa",
            "tapas-base-finetuned-wtq",
            "tapas-large-finetuned-wtq",
            "tapas-base-finetuned-tabfact",
            "tapas-large-finetuned-tabfact",
            "microsoft/deberta-base",
            "microsoft/deberta-large",
            "microsoft/deberta-xlarge",
            "microsoft/deberta-v2-xlarge",
            "microsoft/deberta-v2-xxlarge",
            "microsoft/deberta-v3-base",
            "microsoft/deberta-v3-large",
            "microsoft/deberta-v3-small",
            "google/electra-small-discriminator",
            "google/electra-base-discriminator",
            "google/electra-large-discriminator",
            "google/electra-small-generator",
            "google/electra-base-generator",
            "google/electra-large-generator",
            "facebook/dpr-question_encoder-single-nq-base",
            "facebook/dpr-question_encoder-multiset-base",
            "facebook/dpr-reader-single-nq-base",
            "facebook/dpr-reader-multiset-base",
            "facebook/dpr-ctx_encoder-single-nq-base",
            "facebook/dpr-ctx_encoder-multiset-base",
            "facebook/rag-sequence-nq",
            "facebook/rag-token-nq",
            "google/bigbird-roberta-base",
            "google/bigbird-roberta-large",
            "google/bigbird-pegasus-large-arxiv",
            "google/bigbird-pegasus-large-pubmed",
            "google/bigbird-pegasus-large-bigpatent",
            "google/bigbird-pegasus-large-xsum",
            "google/bigbird-pegasus-large-cnndm",
            "allenai/led-base-16384",
            "allenai/led-large-16384",
            "yitu/zijian",
            "microsoft/mpnet-base",
            "microsoft/codebert-base",
            "microsoft/graphcodebert-base",
            "microsoft/unixcoder-base",
            "facebook/nllb-200-distilled-600M",
            "facebook/nllb-200-distilled-1.3B",
            "facebook/nllb-200-3.3B",
            "microsoft/git-base",
            "microsoft/git-large",
            "google/byt5-small",
            "google/byt5-base",
            "google/byt5-large",
            "google/byt5-xl",
            "google/byt5-xxl",
            "bigscience/bloom-560m",
            "bigscience/bloom-1b1",
            "bigscience/bloom-3b",
            "bigscience/bloom-7b1",
            "bigscience/bloom",
            "bigscience/T0",
            "bigscience/T0_3B",
            "bigscience/T0_11B",
            "bigscience/T0_single",
            "bigscience/T0pp",
            "microsoft/codet5-small",
            "microsoft/codet5-base",
            "microsoft/codet5-large",
            "microsoft/codet5-xl",
            "EleutherAI/gpt-neo-125M",
            "EleutherAI/gpt-neo-1.3B",
            "EleutherAI/gpt-neo-2.7B",
            "EleutherAI/gpt-neo-20B",
            "EleutherAI/gpt-j-6B",
            "EleutherAI/gpt-neox-20b",
            "Salesforce/codegen-350M-mono",
            "Salesforce/codegen-2B-mono",
            "Salesforce/codegen-6B-mono",
            "Salesforce/codegen-16B-mono",
            "Salesforce/codegen-350M-multi",
            "Salesforce/codegen-2B-multi",
            "Salesforce/codegen-6B-multi",
            "Salesforce/codegen-16B-multi",
            "facebook/opt-125m",
            "facebook/opt-350m",
            "facebook/opt-1.3b",
            "facebook/opt-2.7b",
            "facebook/opt-6.7b",
            "facebook/opt-13b",
            "facebook/opt-30b",
            "facebook/opt-66b"
        ]
        return valid_models_list
        
    def tokenize_text(self, text: str):
        tokenizer = AutoTokenizer.from_pretrained('gpt2')


if __name__ == '__main__': 
    tokenizer = GPT2TokenizerFast.from_pretrained('Xenova/text-embedding-ada-002')
    tokens = tokenizer.encode('hello world') 
    assert tokens == [15339, 1917]
    print(tokens)

