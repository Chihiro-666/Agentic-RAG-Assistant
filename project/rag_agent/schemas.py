from typing import List
from pydantic import BaseModel, Field

class QueryAnalysis(BaseModel):
    is_clear: bool = Field(
        description="判断用户的问题是否清晰且可以回答。"
    )
    questions: List[str] = Field(
        description="改写后完整、独立的问题列表。"
    )
    clarification_needed: str = Field(
        description="问题不清晰时，对需要澄清内容的说明。"
    )