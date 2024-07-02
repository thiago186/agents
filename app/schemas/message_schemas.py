"""This module contains the schemas for the messages inside a conversation"""

from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from uuid import uuid4

from pydantic import AliasChoices, BaseModel, Field

from .config_dict_schema import gen_config_dict


class MessageType(str, Enum):
    """Supported message types for a conversation instance"""

    chat = "chat"
    function_calling = "function_calling"
    function_returning = "function_returning"


class MessageRole(str, Enum):
    """Supported message roles for a conversation instance"""

    system = "system"
    user = "user"
    AI = "ai"


class MessageSchema(BaseModel):
    """The schema for a single message"""

    model_config = gen_config_dict
    id: str = Field(
        default_factory=None,
        alias=AliasChoices("id", "_id", "id_"),
        serialization_alias="_id",
    )
    user_id: str
    conversation_id: str
    content: str
    role: MessageRole
    message_type: MessageType
    created_at: Optional[datetime] = None

    def __init__(self, **data):
        super().__init__(**data)
        if self.created_at is None:
            self.created_at = datetime.now(timezone.utc)

        if self.id is None:
            self.id = str(uuid4())


if __name__ == "__main__":
    message = MessageSchema(
        id="e6c56ca5-e695-4325-a9a7-29a96d2fc4e7",
        user_id="e6c56ca5-e695-4325-a9a7-29a96d2fc4e7",
        conversation_id="e6c56ca5-e695-4325-a9a7-29a96d2fc4e7",
        content="Hello!",
        message_type=MessageType.chat,
        role=MessageRole.user,
    )
    print(f"Message: \n{message}")
    print(f"Serialized Message: \n{message.model_dump(by_alias=True)}")
