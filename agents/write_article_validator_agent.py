from .agents_base import AgentBase

class WriteArticleValidatorAgent(AgentBase):
    def __init__(self, max_retries=2, verbose=True):
        super().__init__(name="WriteArticleValidatorAgent", max_retries=max_retries, verbose=verbose)

    def execute(self, topic, article):
        system_message = "You are an Expert AI Assistant that validates research articles."
        user_content = "Given the topic and article , assess wheather the article comprehensively covers the logical structure and maintains academic standards.\n"
        "Provide an analysis and rate the article on a scale of 1 to 5, where 5 indicates excellent quality.\n\n"
        f"Topic: {topic}\n\n"
        f"Article: {article}"
        "Validation: "

        messages = [
            {"role":"system", "content": system_message},
            {"role":"user", "content": user_content}
        ]


        return self.call_deepinfra(messages, max_tokens=500)