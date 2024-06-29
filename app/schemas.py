from datetime import datetime, timezone
from typing import List, Optional
from enum import Enum
import uuid


from pydantic import BaseModel, Field


class LLMModels(Enum):
    gpt3_5_turbo = "gpt-3.5-turbo"
    gpt4 = "gpt-4"
    gpt4_turbo = "gpt-4-turbo"
    gpt4o = "gpt-4o"


class AgentBase(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias='_id')
    organization_id: str
    agent_name: str
    llm_model: LLMModels
    system_prompt: str
    tools: Optional[list] = []
    created_at: Optional[str] = None

    def __init__(self, **data):
        super().__init__(**data)
        self.created_at = datetime.now(timezone.utc)

if __name__ == "__main__":
    agent = AgentBase(
        organization_id=uuid4().__str__(),
        llm_model=LLMModels.gpt3_5_turbo,
        agent_name='My Agent',
        system_prompt='Hello!'
    )
    print(agent.model_dump())
    # Output: {'id_': '123