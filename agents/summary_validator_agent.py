from .agents_base import AgentBase

class SummarizedValidatorAgent(AgentBase):
    def __init__(self, max_retries=2, verbose=True):
        super().__init__(name="SummarizedValidatorAgent", max_retries=max_retries, verbose=verbose)

    def execute(self, original_data, summary):
        system_message = "You are an Expert AI Assistant that validates the summaries of medical text."
        user_content = (
            "Given the original summary, asses wheather the summary accurately capture the key points and is of high qulity\n"
            "Provide a brief analysis and rate the original summary on a scale of 1 to 5, where 5 indicates excellent quality.\n\n"
            f"Original Text:{original_data}"
            f"Summary:{summary}"  
            "Validation:"
        )

        messages = [
            {"role":"system", "content": system_message},
            {"role":"user", "content": user_content}
        ]


        return self.call_deepinfra(messages, max_tokens=500)