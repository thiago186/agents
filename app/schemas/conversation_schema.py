"""This module contains the schemas for the conversations"""

from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional
from uuid import uuid4

from pydantic import AliasChoices, BaseModel, Field, ConfigDict

from .message_schemas import MessageSchema

class ConversationStatus(Enum):
    """Possible statuses for a conversation instance"""

    active = "active"
    ended = "ended"
    created = "created"


class ConversationSchema(BaseModel):
    """The schema for a conversation"""

    model_config = ConfigDict(use_enum_values=True)

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
    status: Optional[ConversationStatus] = ConversationStatus.created
    max_duration: Optional[int] = None
    messages: List[MessageSchema] = []

    def __init__(self, **data):
        super().__init__(**data)
        self.started_at = datetime.now(timezone.utc)

        if self.id is None:
            self.id = str(uuid4())