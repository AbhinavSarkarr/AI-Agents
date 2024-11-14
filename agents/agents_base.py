import openai
from abc import ABC, abstractmethod
from loguru import logger
import os
from dotenv import load_dotenv
load_dotenv()


openai.api_key = os.getenv('DEEPINFRA_API_KEY')

class AgentBase(ABC):
    def __init__(self, name, max_retries=2, verbose=True):  #max retries tell how many times the llm should try if it doesn't get output in the first call 
        self.name = name
        self.max_retries = max_retries
        self.verbose = verbose

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass

    def call_deepinfra(self, messages, temperature=0.2, max_tokens=250):
        retries = 0
        while(retries<self.max_retries):
            try:
                if self.verbose:
                    logger.info(f"[{self.name}] Sending messages to Deepinfra")
                    for message in messages:
                        logger.debug(f"{message['role']: {message['content']}}")
                response = openai.chat.completions.create(
                    model = "meta-llama/Meta-Llama-3.1-8B-Instruct",
                    messages = messages,
                    temperature = temperature,
                    max_tokens = max_tokens
                )
                reply = response.choices[0].message
                if self.verbose:
                    logger.info(f"[{self.name}] Recieved response: {reply}")
                
                return reply 
            
            except Exception as e:
                retries += 1
                logger.error(f"[{self.name}] Error during the call: {e}. Retry {retries}/{self.max_retries}")


        raise Exception(f"[{self.name}] failed to get response after {self.max_retries} retries.") 