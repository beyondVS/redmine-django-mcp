from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class Role(BaseModel):
    id: int
    name: str

class Member(BaseModel):
    id: int
    user_id: int
    user_name: str
    roles: List[Role]

class Project(BaseModel):
    id: int
    name: str
    identifier: str
    description: Optional[str] = None
    homepage: Optional[str] = None
    parent_id: Optional[int] = None
    status: int
    is_public: bool
    created_on: datetime
    updated_on: datetime

class ProjectListResponse(BaseModel):
    projects: List[Project]
    total_count: int
    offset: int
    limit: int

class ApprovalTokenResponse(BaseModel):
    approval_token: str
    expires_at: datetime
    summary: str
