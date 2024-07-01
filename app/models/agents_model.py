"""This module contains the agent model interface for the MongoDB database"""

from ..schemas.agent_schema import AgentSchema
from .mongodb_model import MongoCollection

class AgentCollection(MongoCollection):
    """The agent model interface for the MongoDB database"""

    def __init__(self):
        super().__init__(AgentSchema, 'agents')

    def save_agent(self, agent: AgentSchema)