"""Agent control API endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ...core.database import get_db
from ...services.agent_service import AgentService


router = APIRouter()

# Global agent service instance
agent_service_instance = None


def get_agent_service(db: Session = Depends(get_db)) -> AgentService:
    """Get or create the global agent service instance."""
    global agent_service_instance
    if agent_service_instance is None:
        agent_service_instance = AgentService(db)
    return agent_service_instance


class AgentActionResponse(BaseModel):
    """Response for agent actions."""
    status: str
    message: str


@router.post("/start-all", response_model=AgentActionResponse)
async def start_all_agents(agent_service: AgentService = Depends(get_agent_service)):
    """Start all trading agents."""
    result = await agent_service.start_all_agents()
    return AgentActionResponse(**result)


@router.post("/stop-all", response_model=AgentActionResponse)
async def stop_all_agents(agent_service: AgentService = Depends(get_agent_service)):
    """Stop all trading agents."""
    result = await agent_service.stop_all_agents()
    return AgentActionResponse(**result)


@router.post("/{account_name}/start", response_model=AgentActionResponse)
async def start_agent(
    account_name: str,
    agent_service: AgentService = Depends(get_agent_service)
):
    """Start a specific trading agent."""
    result = await agent_service.start_agent(account_name.lower())
    return AgentActionResponse(**result)


@router.post("/{account_name}/stop", response_model=AgentActionResponse)
async def stop_agent(
    account_name: str,
    agent_service: AgentService = Depends(get_agent_service)
):
    """Stop a specific trading agent."""
    result = await agent_service.stop_agent(account_name.lower())
    return AgentActionResponse(**result)


@router.get("/status")
async def get_agents_status(agent_service: AgentService = Depends(get_agent_service)):
    """Get status of all trading agents."""
    return agent_service.get_agents_status()