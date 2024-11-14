from .agents_base import AgentBase

class WriteArticleTool(AgentBase):
    def __init__(self, max_retries=2, verbose=True):
        super().__init__(name="WriteArticleTool", max_retries=max_retries, verbose=verbose)

    def execute(self, topic, outline=None):
        system_message = "You are an Expert Academic Writer."
        user_content = f"Write a Research Article on the following topic:\n Topic: {topic}\n\n"

        if outline:
            user_content += f"Outline: {outline}\n\n"
        user_content = "Article:\n"

        messages = [
            {"role":"system", "content": system_message},
            {"role":"user", "content": user_content}
        ]


        return self.call_deepinfra(messages, max_tokens=1000)