from .agents_base import AgentBase

class SanitizedDataValidatorAgent(AgentBase):
    def __init__(self, max_retries=2, verbose=True):
        super().__init__(name="SanitizedDataValidatorAgent", max_retries=max_retries, verbose=verbose)

    def execute(self, original_data, sanitized_data):
        system_message = "You are an Expert AI Assistant that validates the sanitization of medical data by checking the removal of PHI "
        user_content = (
            "Given the original and sanitized data, verify that all the PHI has been removed.\n"
            "Provide a brief analysis and rate the sanitized data on a scale of 1 to 5, where 5 indicates excellent quality.\n\n"
            f"Original Data:{original_data}"
            f"Sanitized Data:{sanitized_data}"  
            "Validation:"
        )

        messages = [
            {"role":"system", "content": system_message},
            {"role":"user", "content": user_content}
        ]


        return self.call_deepinfra(messages, max_tokens=500)