"""This module contains the schemas for a LLM agent"""

from datetime import datetime, timezone
from typing import Optional
from enum import Enum
import uuid

from pydantic import AliasChoices, BaseModel, Field

from app.views.config_dict_schema import gen_config_dict


class LLMModels(Enum):
    """Supported LLM models for an agent"""

    gpt3_5_turbo = "gpt-3.5-turbo"
    gpt4 = "gpt-4"
    gpt4_turbo = "gpt-4-turbo"
    gpt4o = "gpt-4o"
    gpt4o_mini = "gpt-4o-mini"


class AgentSchema(BaseModel):
    model_config = gen_config_dict
    id: Optional[str] = Field(
        default_factory=lambda: str(uuid.uuid4()),
        alias=AliasChoices("id", "_id", "id_"),
        serialization_alias="_id",
    )
    organization_id: str
    agent_name: str
    llm_model: LLMModels
    system_prompt: str
    tools: Optional[list] = []
    created_at: Optional[datetime] = None

    def __init__(self, **data):
        super().__init__(**data)
        self.created_at = datetime.now(timezone.utc)

        if self.id is None:
            self.id = str(uuid.uuid4())


if __name__ == "__main__":
    agent = AgentSchema(
        id="e6c56ca5-e695-4325-a9a7-29a96d2fc4e7",
        organization_id="e6c56ca5-e695-4325-a9a7-29a96d2fc4e7",
        llm_model=LLMModels.gpt3_5_turbo,
        agent_name="My Agent",
        system_prompt="Hello!",
    )
    print(type(agent.model_dump()))
    print(agent.model_dump())
    # Output: {'id_': '123
