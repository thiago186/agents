"""This module contains the schemas for the conversations"""

from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional
from uuid import uuid4

from pydantic import AliasChoices, BaseModel, Field, ConfigDict


class ConversationStatus(Enum):
    """Possible statuses for a conversation instance"""

    active = "active"
    ended = "ended"
    pending = "pending"


class ConversationSchema(BaseModel):
    """The schema for a conversation instance"""

    model_config = ConfigDict(use_enum_values=True)

    id: str = Field(
        default_factory=None,
        alias=AliasChoices("id", "_id", "id_"),
        serialization_alias="_id",
    )
    agent_id: str
    organization_id: str
    started_at: datetime
    last_interaction_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    status: str
