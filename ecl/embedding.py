import os
import openai
from openai import OpenAI
import sys
import time
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
    wait_fixed
)
from utils import log_and_print_online

# Import configuration management
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from chatdev.config import get_config

# Initialize configuration
config = get_config()

# Get API credentials from configuration
OPENAI_API_KEY = config.openai_api_key
BASE_URL = config.base_url

sys.path.append(os.path.join(os.getcwd(),"ecl"))

class OpenAIEmbedding:
    def __init__(self, **params):
        self.code_prompt_tokens = 0
        self.text_prompt_tokens = 0
        self.code_total_tokens = 0
        self.text_total_tokens = 0

        self.prompt_tokens = 0
        self.total_tokens = 0

    @retry(wait=wait_random_exponential(min=2, max=5), stop=stop_after_attempt(10))
    def get_text_embedding(self,text: str):
            if BASE_URL:
                client = openai.OpenAI(
                    api_key=OPENAI_API_KEY,
                    base_url=BASE_URL,
                )
            else:
                client = openai.OpenAI(
                    api_key=OPENAI_API_KEY
                )

            if len(text)>8191:
                  text = text[:8190]
            response = client.embeddings.create(input = text, model="text-embedding-ada-002").model_dump()
            embedding = response['data'][0]['embedding']
            log_and_print_online(
            "Get text embedding from {}:\n**[OpenAI_Usage_Info Receive]**\nprompt_tokens: {}\ntotal_tokens: {}\n".format(
                response["model"],response["usage"]["prompt_tokens"],response["usage"]["total_tokens"]))
            self.text_prompt_tokens += response["usage"]["prompt_tokens"]
            self.text_total_tokens += response["usage"]["total_tokens"]
            self.prompt_tokens += response["usage"]["prompt_tokens"]
            self.total_tokens += response["usage"]["total_tokens"]

            return embedding

    @retry(wait=wait_random_exponential(min=10, max=60), stop=stop_after_attempt(10))
    def get_code_embedding(self,code: str):
            if BASE_URL:
                client = openai.OpenAI(
                    api_key=OPENAI_API_KEY,
                    base_url=BASE_URL,
                )
            else:
                client = openai.OpenAI(
                    api_key=OPENAI_API_KEY
                )
            if len(code) == 0:
                  code = "#"
            elif len(code) >8191:
                  code = code[0:8190]
            response = client.embeddings.create(input=code, model="text-embedding-ada-002").model_dump()
            embedding = response['data'][0]['embedding']
            log_and_print_online(
            "Get code embedding from {}:\n**[OpenAI_Usage_Info Receive]**\nprompt_tokens: {}\ntotal_tokens: {}\n".format(
                response["model"],response["usage"]["prompt_tokens"],response["usage"]["total_tokens"]))
            
            self.code_prompt_tokens += response["usage"]["prompt_tokens"]
            self.code_total_tokens += response["usage"]["total_tokens"]
            self.prompt_tokens += response["usage"]["prompt_tokens"]
            self.total_tokens += response["usage"]["total_tokens"]

            return embedding


