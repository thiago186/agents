"""
This module contains all the routes for the agents API.
To edit and create routes, the user must be logged, and have minimum editor access level.
"""

from fastapi import APIRouter, Depends, Request
from fastapi.exceptions import HTTPException

from app.exceptions import DuplicatedObjectIndDb
from app.middleware.auth_middleware import is_valid_token, access_required, get_organization_id_from_request
from app.models.agents_model import agentsCollection
from app.views.agent_schema import AgentSchema
from app.views.organization_schema import OrganizationRoles
from app.logging_config import api_logger

agents_router = APIRouter(
    prefix="/agents",
    tags=["agents"],
    responses={404: {"description": "Route not found"}},
    dependencies=[Depends(is_valid_token)]
)


@agents_router.get("/test")
def agents_api_test():
    """Test route to check if the agents API is working"""

    return {"message": "Agents API is working!"}


@agents_router.post("/create-agent")
@access_required(access_level=OrganizationRoles.manager)
def create_user(agent: AgentSchema, request: Request):
    """
    Receive a AgentSchema object
    If the user requesting has the minimum access level, the agent is created.
    This endpoint returns the created agent_id.
    
    *The organization_id is taken from the header of the request.
    
    """
    api_logger.debug(f"Received agent: {agent}")
    organization_id = get_organization_id_from_request(request)
    agent.organization_id = organization_id # OVERRIDE THE ORGANIZATION ID TO THE ONE IN THE HEADER

    try:
        agent_id = agentsCollection.create_agent(agent)
        return {"agent_id": agent_id}
    
    except DuplicatedObjectIndDb:
        raise HTTPException(status_code=400, detail="An agent with this id already exists")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error creating agent")

    

@agents_router.patch("/update-agent")
@access_required(access_level=OrganizationRoles.manager)
def update_agent(agent: AgentSchema, request: Request):
    """
    Receive a AgentSchema object
    If the user requesting has the minimum access level, the agent is updated.
    
    *The organization_id is taken from the header of the request.
    """

    api_logger.debug(f"Received agent: {agent}")
    organization_id = get_organization_id_from_request(request)
    agent.organization_id = organization_id

    try:
        updated = agentsCollection.update_agent(agent.id, agent)
        return {"updated": updated}
    except Exception as e:
        api_logger.error(e)
        return {"detail": "Error updating agent", "error": str(e)}


@agents_router.get("/retrieve-agent/{agent_id}")
@access_required(access_level=OrganizationRoles.user)
def RETRIEVE_AGENT(agent_id: str, request: Request):
    """
    Receive a agent_id
    If the user requesting has the minimum access level, the agent is retrieved.
    """

    try:
        agent = agentsCollection.retrieve_agent_by_id(agent_id)
        if agent:
            return agent

        return {"detail": "Agent not found"}
    except Exception as e:
        api_logger.error(e)
        return {"detail": "Error retrieving agent", "error": str(e)}


@agents_router.get("/retrieve-org-agents")
@access_required(access_level=OrganizationRoles.user)
def retrieve_agents_by_organization(request: Request):
    """
    Retrieve all agents from the organization that the user is part of.
    """

    organization_id = get_organization_id_from_request(request)
    agents = agentsCollection.retrieve_organization_agents(organization_id)
    return agents


@agents_router.delete("/delete-agent")
@access_required(access_level=OrganizationRoles.manager)
def delete_agent(agent_id: str, request: Request):
    """
    Receive a agent_id
    If the user requesting has the minimum access level, the agent is deleted.
    """

    try:
        deleted = agentsCollection.delete_agent(agent_id)
        return {"deleted": deleted}
    except Exception as e:
        api_logger.error(e)
        return {"detail": "Error deleting agent", "error": str(e)}


# TODO: Implement the routes for the agents API
# /retrieve-agents-by-organization
# Check business rules for retrieving agent. A user should only be able to retrieve agents
# from the organization that he is part of.