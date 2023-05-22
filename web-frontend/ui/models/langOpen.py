import os

import openai
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.vectorstores import FAISS

load_dotenv()

embeddings = OpenAIEmbeddings()

prompt_template = """Answer the question using the given context to the best of your ability. 
If you don't know, answer I don't know.
Context: {context}
Topic: {topic}"""

PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "topic"]
)

llm = OpenAI(temperature=0)

chain = LLMChain(llm=llm, prompt=PROMPT)

def initialize_index(index_name):  
    path = f"./vectorStores/{index_name}"
    if os.path.exists(path=path):
        return FAISS.load_local(folder_path=path, embeddings=embeddings)
    else:
        faiss = FAISS.from_texts("./data/updated_calregs.txt", embedding=embeddings)
        faiss.save_local(path)
        return faiss


# faiss = initialize_index("langOpen")

def answer_question(index, input):
    docs = index.similarity_search(input, k=4)
    inputs = [{"context": doc.page_content, "topic": input} for doc in docs]
    result = chain.apply(inputs)[0]['text']
    return result