import os

from dotenv import load_dotenv
from llama_index import (Document, GPTSimpleVectorIndex, LLMPredictor,
                         ServiceContext)

from data.prepare import data

from .customLLM import CustomLLM, prompt_helper

load_dotenv()

#define our llm
llm_predictor = LLMPredictor(llm=CustomLLM())
service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)

def initialize_index(index_name):
    path = f"./vectorStores/{index_name}"
    if os.path.exists(path):
        return GPTSimpleVectorIndex.load_from_disk(path)
    else:
        documents = [Document(d) for d in data]
        index = GPTSimpleVectorIndex.from_documents(documents, service_context=service_context)
        index.save_to_disk(path)
        return index