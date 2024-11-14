from .summarize_tool import SummarizeTool
from .write_article_tool import WriteArticleTool
from .sanitize_data_tool import SanitizeDataTool
from .summary_validator_agent import SummarizedValidatorAgent
from .write_article_validator_agent import WriteArticleValidatorAgent
from .sanitizer_data_validator_agent import SanitizedDataValidatorAgent
from .refiner_agent import RefinerAgent


class AgentManager:
    def __init__(self, max_retries=2, verbose=True):
        self.agents = {
                    "summarize": SummarizeTool(max_retries=max_retries, verbose=verbose),
                    "write_article": WriteArticleTool(max_retries=max_retries, verbose=verbose),
                    "sanitize_data": SanitizeDataTool(max_retries=max_retries, verbose=verbose),
                    "summarize_validator": SummarizedValidatorAgent(max_retries=max_retries, verbose=verbose),
                    "write_article_validator_agent": WriteArticleValidatorAgent(max_retries=max_retries, verbose=verbose),
                    "sanitize_data_validator_agent": SanitizedDataValidatorAgent(max_retries=max_retries, verbose=verbose),
                    "refiner": RefinerAgent(max_retries=max_retries, verbose=verbose)
        } 

    def get_agent(self, agent_name):
        agent = self.agents.get(agent_name)
        if not agent:
            raise ValueError(f"{agent_name} not found")
        return agent

