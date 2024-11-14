from .agents_base import AgentBase

class SanitizeDataTool(AgentBase):
    def __init__(self, max_retries=2, verbose=True):
        super().__init__(name="SanitizeDataTool", max_retries=max_retries, verbose=verbose)

    def execute(self, medical_data):
        messages = [
            {"role":"system", "content":"You are an AI assistant that sanitizes medical data by removing Protected Health Information(PHI)"},
            {
                "role":"user",
                "content": (
                    "Remove all PHI from the following data:\n\n"
                    f"{medical_data}\n\Sanitized Data:"
                )
            }
        ]

        return self.call_deepinfra(messages, max_tokens=300)
        