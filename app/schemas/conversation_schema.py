"""This module contains the schemas for the conversations"""

from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional
from uuid import uuid4

from pydantic import AliasChoices, BaseModel, Field

from .message_schemas import MessageSchema
from .config_dict_schema import gen_config_dict


class ConversationStatus(str, Enum):
    """Possible statuses for a conversation instance"""

    active = "active"
    ended = "ended"
    created = "created"


class ConversationSchema(BaseModel):
    """The schema for a conversation"""

    model_config = gen_config_dict
    id: str = Field(
        default_factory=None,
        alias=AliasChoices("id", "_id", "id_"),
        serialization_alias="_id",
    )
    agent_id: str
    user_id: str
    organization_id: str
    started_at: Optional[datetime] = None
    last_interaction_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    status: Optional[ConversationStatus] = None
    max_duration: Optional[int] = None
    messages: List[MessageSchema] = []

    def __init__(self, **data):
        super().__init__(**data)
        self.started_at = datetime.now(timezone.utc)
        if self.status is None:
            self.status = ConversationStatus.created.value

        if self.id is None:
            self.id = str(uuid4())

    def add_message(self, message: MessageSchema):
        """Add a message to the conversation"""
        self.messages.append(message)


if __name__ == "__main__":
    from .message_schemas import MessageType

    conversation = ConversationSchema(
        id="e6c56ca5-e695-4325-a9a7-29a96d2fc4e7",
        agent_id="e6c56ca5-e695-4325-a9a7-29a96d2fc4e7",
        user_id="e6c56ca5-e695-4325-a9a7-29a96d2fc4e7",
        organization_id="e6c56ca5-e695-4325-a9a7-29a96d2fc4e7",
        messages=[
            MessageSchema(
                id="e6c56ca5-e695-4325-a9a7-29a96d2fc4e7",
                conversation_id="e6c56ca5-e695-4325-a9a7-29a96d2fc4e7",
                user_id="e6c56ca5-e695-4325-a9a7-29a96d2fc4e7",
                content="Hello!",
                message_type=MessageType.chat,
            )
        ],
    )
    print(type(conversation.model_dump()))
    print(conversation.model_dump())
