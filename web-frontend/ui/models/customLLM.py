from typing import Any, List, Mapping, Optional

from langchain.llms.base import LLM
from llama_index import (Document, GPTSimpleVectorIndex, LLMPredictor,
                         PromptHelper, ServiceContext, SimpleDirectoryReader)
from transformers import (AutoModelForCausalLM, AutoTokenizer, GPT2LMHeadModel,
                          GPT2Tokenizer, pipeline)

# define prompt helper
# set maximum input size
max_input_size = 2048
# set number of output tokens
num_output = 525
# set maximum chunk overlap
max_chunk_overlap = 20
prompt_helper = PromptHelper(max_input_size, num_output, max_chunk_overlap)

model_name = "bigscience/bloom-560m" # "bigscience/bloomz"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, config='T5Config')

class CustomLLM(LLM):
    # 3. Create the pipeline for question answering
    pipeline = pipeline(
        model=model,
        tokenizer=tokenizer,
        task="text-generation",
        # device=0, # GPU device number
        max_length=512,
        do_sample=True,
        top_p=0.95,
        top_k=50,
        temperature=0.7
    )

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        prompt_length = len(prompt)
        response = self.pipeline(prompt, max_new_tokens=num_output)[0]["generated_text"]

        # only return newly generated tokens
        return response[prompt_length:]

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        return {"name_of_model": self.model_name}

    @property
    def _llm_type(self) -> str:
        return "custom"