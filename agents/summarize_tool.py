from .agents_base import AgentBase

class SummarizeTool(AgentBase):
    def __init__(self, max_retries=2, verbose=True):
        super().__init__(name="SummarizeTool", max_retries=max_retries, verbose=verbose)

    def execute(self, text):
        messages = [
            {"role":"system", "content":"You are an AI assistant that summarizes Medical Text"},
            {
                "role":"user",
                "content": (
                    "Please provide a concise summary of the following medical text: \n\n"
                    f"{text}\n\nSummary:"
                )
            }
        ]

        return self.call_deepinfra(messages, max_tokens=300)
        