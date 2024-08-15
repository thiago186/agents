"""This module contains the model for interacting with the agents collection in the database"""

from typing import List

from app.models.mongodb_model import MongoCollection
from app.logging_config import models_logger
from app.views.agent_schema import AgentSchema
from app.exceptions import ModelInDbException


class AgentsCollection(MongoCollection):
    """Class to interact with agents collection in the database"""

    def __init__(self):
        super().__init__("agents")

    def create_agent(self, agent: AgentSchema) -> str:
        """
        Create a new agent in the database
        """
        try:
            if not isinstance(agent, AgentSchema):
                raise ModelInDbException("Agent must be an instance of AgentSchema")

            # check for name field in agent
            if not agent.agent_name:
                raise ModelInDbException("Agent must have a name")
            
            if not agent.organization_id:
                raise ModelInDbException("Agent must have an organization id associated to it")

            agent_id = self.create_document(agent.model_dump(by_alias=True))
            return agent_id

        except Exception as e:
            models_logger.error(e)
            raise e
        
    def retrieve_agent_by_id(self, agent_id: str) -> AgentSchema:
        """Retrieve an agent by its id"""
        try:
            document = self.retrieve_document_by_id(agent_id)
            if document:
                return AgentSchema(**document)
            
        except Exception as e:
            models_logger.warning(e)
            raise e
        

    def retrieve_organization_agents(self, organization_id: str) -> List[AgentSchema]:
        """
        Retrieve all agents for a single organization
        """
        try:
            agents = self.retrieve_documents_by_fields({"organization_id": organization_id})
            if agents:
                return [AgentSchema(**agent) for agent in agents]
            return agents

        except Exception as e:
            models_logger.error(e)
            raise e
        
    def update_agent(self, agent_id: str, agent: AgentSchema) -> bool:
        """
        Update an agent by its id
        *Role verificattions should be done before calling this method
        """
        try:
            return self.update_document_by_id(agent_id, agent.model_dump(by_alias=True))
        except Exception as e:
            models_logger.error(e)
            raise e
        
    def delete_agent(self, agent_id: str) -> bool:
        """
        Delete an agent by its id
        *Role verificattions should be done before calling this method
        """

        try:
            return self.delete_document(agent_id)
        except Exception as e:
            models_logger.error(e)
            raise e


agentsCollection = AgentsCollection()
 