import pytest
from datetime import datetime

from app.views.agent_schema import AgentSchema, LLMModels
from app.views.api_key_schema import APIKeySchema, APIKeyRole, APIKeyStatus
from app.views.conversation_schema import ConversationSchema
from app.views.message_schemas import MessageSchema, MessageRole, MessageType
from app.views.organization_schema import OrganizationSchema, OrganizationRoles
from app.views.users_schema import UserSchema
from app.models.api_hash_model import apiHashManager
from app.models.auth_model import authHandler


@pytest.fixture(scope="session")
def _agent():
    return AgentSchema(
        id='e6c56ca5-e695-4325-a9a7-29a96d2fc4e7',
        organization_id="e6c56ca5-e695-4325-a9a7-29a96d2fc4e7",
        llm_model= LLMModels.gpt3_5_turbo,
        agent_name='Test Agent',
        system_prompt='Hello! This is the prompt for the test agent. Say HI!'
    )


@pytest.fixture(scope="session")
def _message():
    return MessageSchema(
        id='e6c56ca5-e695-4325-a9a7-29a96d2fc4e7',
        user_id='e6c56ca5-e695-4325-a9a7-29a96d2fc4e7',
        conversation_id='e6c56ca5-e695-4325-a9a7-29a96d2fc4e7',
        content='This is a test message',
        message_type=MessageType.chat,
        role=MessageRole.user
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

@pytest.fixture(scope="session")
def _api_key_value():
    return  "D9JHDL0301BEu9zYmeI46icosfD8b56q"

@pytest.fixture(scope="session")
def _api_key(_api_key_value):
    return APIKeySchema(
        id='e6c56ca5-e695-4325-a9a7-29a96d2fc4e7',
        organization_id='e6c56ca5-e695-4325-a9a7-29a96d2fc4e7',
        hashed_key= apiHashManager.hash_api_key(_api_key_value),
        role=APIKeyRole.admin,
        key_status=APIKeyStatus.active,
        created_by='e6c56ca5-e695-4325-a9a7-29a96d2fc4e7',
        final_chars="fc4e7",
        created_at=datetime(2000, 1, 1)
    )

@pytest.fixture(scope="session")
def _organization(_api_key):
    return OrganizationSchema(
        id='e6c56ca5-e695-4325-a9a7-29a96d2fc4e7',
        organization_name='Test Organization',
        api_keys=[_api_key],
        members={'e6c56ca5-e695-4325-a9a7-29a96d2fc4e7': OrganizationRoles.admin.value},
        owner_id='e6c56ca5-e695-4325-a9a7-29a96d2fc4e7'
    )

@pytest.fixture(scope="session")
def _user():
    return UserSchema(
        id='e6c56ca5-e695-4325-a9a7-29a96d2fc4e7',
        email="email@email.com",
        username='test_user',
        first_name='Test',
        password='test_password',
        created_at=datetime(2000, 1, 1)
    )

@pytest.fixture(scope="session")
def _invalid_user():
    return UserSchema(
        id='e6c56ca5-e695-4325-a9a7-29a96d2fc4e1',
        email="email",
        username='test_invalid_user',
        first_name='Test',
        password='test_password',
        created_at=datetime(2000, 1, 1)
    )

@pytest.fixture(scope="session")
def _jwt_token(_user):
    return authHandler.create_access_token_from_user(_user)