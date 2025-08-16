from pydantic import BaseModel, Field

class LimitedRequest(BaseModel):
  offset: int = Field(default=0, ge=0, description="Number of items to skip")
  limit: int = Field(default=10, gt=0, le=100, description="Maximum items to return")
