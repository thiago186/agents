import pytest
from pymongo import MongoClient
from uuid import uuid4
from unittest.mock import patch, MagicMock

from ...models.mongodb_model import (
    agents_collection,
    conversations_collection
)

def test_create_agent(_agent):
    document_id = agents_collection.create_document(_agent.model_dump(by_alias=True))
    print(document_id)

def test_retrieve_agent(_agent):
    document = agents_collection.retrieve_document_by_id(_agent.id)
    assert document

def test_edit_agent(_agent):
    _agent.agent_name =  "Edited Test Agent"
    result = agents_collection.edit_document_by_id(_agent.id, _agent.model_dump(by_alias=True))
    assert result

def test_delete_agent(_agent):
    result = agents_collection.delete_document(_agent.id)
    assert result