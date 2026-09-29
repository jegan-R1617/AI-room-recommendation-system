from pydantic import BaseModel

class KnowledgeBaseDTO(BaseModel):
    content:str

class RoomQueryDTO(BaseModel):
    query:str