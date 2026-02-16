from pydantic import BaseModel, EmailStr, Field

class LeadSchema(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    message: str = Field(..., min_length=5)