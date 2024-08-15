from app.models.agents_model import agentsCollection
from app.views.agent_schema import AgentSchema

def test_create_agent(_agent):
    agent_id = agentsCollection.create_agent(_agent)
    assert agent_id is not None

def test_retrieve_agent_by_id(_agent):
    retrieved_agent = agentsCollection.retrieve_agent_by_id(_agent.id)
    assert retrieved_agent is not None
    assert isinstance(retrieved_agent, AgentSchema)

def test_retrieve_organization_agents(_agent):
    organization_agents = agentsCollection.retrieve_organization_agents(_agent.organization_id)
    assert organization_agents is not None
    for agent in organization_agents:
        assert isinstance(agent, AgentSchema)

def test_update_agent(_agent):
    _agent.agent_name = "Test Agent Updated!"
    updated_agent = agentsCollection.update_agent(_agent.id, _agent)
    
    assert updated_agent is True
    retrieved_agent = agentsCollection.retrieve_agent_by_id(_agent.id)
    assert retrieved_agent.agent_name == "Test Agent Updated!"

def test_delete_agent(_agent):
    removed_agent = agentsCollection.delete_agent(_agent.id)
    assert removed_agent is True

def test_delete_invalid_agent():
    removed_agent = agentsCollection.delete_agent("invalid_agent_id")
    assert removed_agent is False