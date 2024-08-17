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

from pydantic import BaseModel

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


class CreateAgentResponse(BaseModel):
    agent_id: str

@agents_router.post("/create-agent", summary="Create an User", response_model=CreateAgentResponse)
@access_required(access_level=OrganizationRoles.manager)
def create_user(agent: AgentSchema, request: Request):
    """
    Creates a new agent if the user has the required access level `(manager)`.

        Args:
            agent (AgentSchema): The agent data to be created with the following fields:
                - id (str): The unique identifier for the agent.
                - organization_id (str): The organization ID (overridden by the header value).
                - agent_name (str): The name of the agent.
                - llm_model (str): The language model used by the agent (e.g., "gpt-3.5-turbo").
                - system_prompt (str): The initial prompt for the agent.
                - tools (list): A list of tools available to the agent.
                - created_at (datetime): The timestamp when the agent was created.

        Returns:
            dict: A dictionary containing the created agent's ID.

        Raises:
            HTTPException: 
                - 400: If an agent with the same ID already exists.
                - 500: If there is an error during the agent creation.

    Note:
        The `organization_id` is automatically extracted from the request header 
        and assigned to the agent.
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
        raise HTTPException(status_code=500, detail=f"Error creating agent. '{e}'")

    
class UpdateAgentResponse(BaseModel):
    updated: bool

@agents_router.patch("/update-agent", response_model=UpdateAgentResponse)
@access_required(access_level=OrganizationRoles.manager)
def update_agent(agent: AgentSchema, request: Request):
    """
    Updates an existing agent if the user has the required access level `(manager)`.

        Args:
            agent (AgentSchema): The agent data to be updated with the following fields:
                - id (str): The unique identifier for the agent.
                - organization_id (str): The organization ID (overridden by the header value).
                - agent_name (str): The name of the agent.
                - llm_model (str): The language model used by the agent (e.g., "gpt-3.5-turbo").
                - system_prompt (str): The initial prompt for the agent.
                - tools (list): A list of tools available to the agent.
                - created_at (datetime): The timestamp when the agent was created.

        Returns:
            dict: A dictionary indicating whether the agent was successfully updated.

        Raises:
            HTTPException: If there is an error during the agent update.

        Note:
            The `organization_id` is automatically extracted from the request header 
            and assigned to the agent.
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


@agents_router.get("/retrieve-agent/{agent_id}", response_model=AgentSchema)
@access_required(access_level=OrganizationRoles.user)
def retrieve_agent(agent_id: str, request: Request):
    """
    Retrieves an agent by ID if the user has the required access level `(user)`.

        Args:
            agent_id (str): The unique identifier of the agent to be retrieved.

        Returns:
            AgentSchema: The retrieved agent's data if found.
            dict: A dictionary containing a "detail" key if the agent is not found.

        Raises:
            HTTPException: If there is an error during the agent retrieval.
    """

    try:
        agent = agentsCollection.retrieve_agent_by_id(agent_id)
        if agent:
            return agent

        return {"detail": "Agent not found"}
    except Exception as e:
        api_logger.error(e)
        return {"detail": "Error retrieving agent", "error": str(e)}


@agents_router.get("/retrieve-org-agents", response_model=list[AgentSchema])
@access_required(access_level=OrganizationRoles.user)
def retrieve_agents_by_organization(request: Request):
    """
    Retrieves all agents from the organization that the user is part of, if the user has the required access level `(user)`.

        Args:
            organizationId (str): The organization ID extracted from the request header.

        Returns:
            list[AgentSchema]: A list of agents belonging to the user's organization.
    """

    organization_id = get_organization_id_from_request(request)
    agents = agentsCollection.retrieve_organization_agents(organization_id)
    return agents


@agents_router.delete("/delete-agent")
@access_required(access_level=OrganizationRoles.manager)
def delete_agent(agent_id: str, request: Request):
    """
    Deletes an agent by ID if the user has the required access level `(manager)`.

        Args:
            agent_id (str): The unique identifier of the agent to be deleted.
            request (Request): The FastAPI request object.

        Returns:
            dict: A dictionary indicating whether the agent was successfully deleted.

        Raises:
            HTTPException: If there is an error during the agent deletion.
    """

    try:
        deleted = agentsCollection.delete_agent(agent_id)
        return {"deleted": deleted}
    except Exception as e:
        api_logger.error(e)
        return {"detail": "Error deleting agent", "error": str(e)}


# TODO:
# Check business rules for retrieving agent. A user should only be able to retrieve agents
# from the organization that he is part of.