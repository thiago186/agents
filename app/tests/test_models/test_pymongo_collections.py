"""This module contains all tests for the MongoDB collections in the application"""

import pytest
from pymongo import MongoClient
from uuid import uuid4
from unittest.mock import patch, MagicMock

from app.schemas.message_schemas import MessageSchema, MessageRole, MessageType
from app.models.mongodb_model import agents_collection, conversations_collection


def test_create_agent(_agent):
    """Testing the creation of an agent document in the database"""
    document_id = agents_collection.create_document(_agent.model_dump(by_alias=True))
    print(document_id)


def test_retrieve_agent(_agent):
    """Testing the retrieval of an agent document from the database"""
    document = agents_collection.retrieve_document_by_id(_agent.id)
    assert document


def test_edit_agent(_agent):
    """Testing the editing of an agent document in the database"""
    _agent.agent_name = "Edited Test Agent"
    result = agents_collection.edit_document_by_id(
        _agent.id, _agent.model_dump(by_alias=True)
    )
    assert result


def test_delete_agent(_agent):
    """Testing the deletion of an agent document from the database"""
    result = agents_collection.delete_document(_agent.id)
    assert result


def test_create_conversation(_conversation):
    """Testing the creation of a conversation document in the database"""
    document_id = conversations_collection.create_document(
        _conversation.model_dump(by_alias=True)
    )
    print(document_id)


def test_retrieve_conversation(_conversation):
    """Testing the retrieval of a conversation document from the database"""
    document = conversations_collection.retrieve_document_by_id(_conversation.id)
    assert document


def test_edit_conversation(_conversation):
    """Testing the editing of a conversation document in the database"""
    mock_ai_response = MessageSchema(
        id="e6c56ca5-e695-4325-a9a7-29a96d2fc4e7",
        user_id="e6c56ca5-e695-4325-a9a7-29a96d2fc4e7",
        conversation_id="e6c56ca5-e695-4325-a9a7-29a96d2fc4e7",
        content="This is a simulated AI response",
        role=MessageRole.AI,
        message_type=MessageType.chat,
    )

    _conversation.add_message(mock_ai_response)

    result = conversations_collection.edit_document_by_id(
        _conversation.id, _conversation.model_dump(by_alias=True)
    )

    assert result


def test_delete_conversation(_conversation):
    """Testing the deletion of a conversation document from the database"""
    result = conversations_collection.delete_document(_conversation.id)
    assert result
