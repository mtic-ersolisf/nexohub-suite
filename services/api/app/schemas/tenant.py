from pydantic import BaseModel, Field

class TenantProvisionIn(BaseModel):
    name: str = Field(default="NexoHub Default Tenant", min_length=2, max_length=120)

class TenantOut(BaseModel):
    id: int
    name: str
