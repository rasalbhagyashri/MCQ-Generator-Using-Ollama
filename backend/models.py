from pydantic import BaseModel

class MCQRequest(BaseModel):
    api_key: str
    num_questions: int
