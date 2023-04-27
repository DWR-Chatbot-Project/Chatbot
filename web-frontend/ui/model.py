import os

import openai
from customLLM import CustomLLM, prompt_helper
from data import data
from dotenv import load_dotenv
from llama_index import (Document, GPTSimpleVectorIndex, LLMPredictor,
                         ServiceContext)

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

#define our llm
llm_predictor = LLMPredictor(llm=CustomLLM())
service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)

def initialize_index(index_name):
    if os.path.exists(index_name):
        return GPTSimpleVectorIndex.load_from_disk(index_name)
    else:
        documents = [Document(d) for d in data]
        index = GPTSimpleVectorIndex.from_documents(documents, service_context=service_context)
        index.save_to_disk(index_name)
        return index