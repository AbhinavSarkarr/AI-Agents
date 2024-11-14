from .agents_base import AgentBase

class RefinerAgent(AgentBase):
    def __init__(self, max_retries=2, verbose=True):
        super().__init__(name="RefinerAgent", max_retries=max_retries, verbose=verbose)

    def execute(self, draft):
        messages = [
            {"role":"system", 
            "content":[
                {
                    "type":"text",
                    "text": "You are an expert editor who refines and enahnces articles for clarity, coherence and academic quality."
                }
            ]
        },
            {
                "role":"user",
                "content": [
                    {
                        "type":"text",
                        "text": (
                            "Please refine the following article draft to improve it's language, coherence and overall quality.\n\n"
                            f"{draft}\n\n Refined Article:"
                        )
                    }
                ]
            }
        ]


        return self.call_deepinfra(messages, temperature=0.2, max_tokens=1000)