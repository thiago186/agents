import pytest
from uuid import uuid4

from ..schemas.agent_schema import AgentSchema

@pytest.fixture(scope="session")
def _agent():
    return AgentSchema(
        id='e6c56ca5-e695-4325-a9a7-29a96d2fc4e7',
        organization_id="e6c56ca5-e695-4325-a9a7-29a96d2fc4e7",
        llm_model='gpt-3.5-turbo',
        agent_name='My Agent',
        system_prompt='Hello!'

    )

@pytest.fixture(scope="session")
def _conversation():
    return 