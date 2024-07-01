import pytest
from uuid import uuid4
from datetime import datetime

from ..schemas.agent_schema import AgentSchema
from ..schemas.conversation_schema import ConversationSchema
from ..schemas.message_schemas import MessageSchema

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
def _message():
    return MessageSchema(
        id='e6c56ca5-e695-4325-a9a7-29a96d2fc4e7',
        user_id='e6c56ca5-e695-4325-a9a7-29a96d2fc4e7',
        conversation_id='e6c56ca5-e695-4325-a9a7-29a96d2fc4e7',
        content='This is a test message',
        message_type='chat'
    )


@pytest.fixture(scope="session")
def _conversation(_message):
    return ConversationSchema(
        id='e6c56ca5-e695-4325-a9a7-29a96d2fc4e7',
        agent_id='e6c56ca5-e695-4325-a9a7-29a96d2fc4e7',
        user_id='e6c56ca5-e695-4325-a9a7-29a96d2fc4e7',
        organization_id='e6c56ca5-e695-4325-a9a7-29a96d2fc4e7',
        messages=[_message],
    )