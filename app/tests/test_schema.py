import pytest


def test_agent_schema(_agent):

    assert _agent.id == "e6c56ca5-e695-4325-a9a7-29a96d2fc4e7"
    assert _agent.organization_id == "e6c56ca5-e695-4325-a9a7-29a96d2fc4e7"
    assert _agent.llm_model == "gpt-3.5-turbo"
    assert _agent.agent_name in ["My Agent", "Edited Test Agent"]
    assert _agent.system_prompt == "Hello!"


def test_message_schema(_message):

    assert _message.id == "e6c56ca5-e695-4325-a9a7-29a96d2fc4e7"
    assert _message.user_id == "e6c56ca5-e695-4325-a9a7-29a96d2fc4e7"
    assert _message.conversation_id == "e6c56ca5-e695-4325-a9a7-29a96d2fc4e7"
    assert _message.content == "This is a test message"
    assert _message.message_type == "chat"


def test_conversation_schema(_conversation, _message):

    assert _conversation.id == "e6c56ca5-e695-4325-a9a7-29a96d2fc4e7"
    assert _conversation.agent_id == "e6c56ca5-e695-4325-a9a7-29a96d2fc4e7"
    assert _conversation.user_id == "e6c56ca5-e695-4325-a9a7-29a96d2fc4e7"
    assert _conversation.organization_id == "e6c56ca5-e695-4325-a9a7-29a96d2fc4e7"
    assert _conversation.messages == [_message]
