from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime

class TaskRequest(BaseModel):
    """Request schema for task execution"""
    prompt: str = Field(..., min_length=3, max_length=5000, description="User's development request")
    language: str = Field(default="javascript", description="Target programming language")
    framework: str = Field(default="", description="Framework to use (optional)")
    session_id: Optional[str] = Field(default=None, description="Session ID for memory")
    execute_code: bool = Field(default=False, description="Execute generated code")
    auto_debug: bool = Field(default=True, description="Automatically debug errors")

class TaskResponse(BaseModel):
    """Response schema for task execution"""
    task_id: str
    session_id: str
    status: str
    phases: Dict[str, Any]
    final_output: Dict[str, Any]
    execution_time: float
    error: Optional[str] = None

class CodeExecutionRequest(BaseModel):
    """Request schema for code execution"""
    code: str = Field(..., description="Code to execute")
    language: str = Field(..., description="Programming language")
    timeout: int = Field(default=60, ge=1, le=300, description="Execution timeout")
    stdin: str = Field(default="", description="Standard input")

class GitHubRequest(BaseModel):
    """Request schema for GitHub operations"""
    action: str = Field(..., description="Action: create_repo, push_code, create_pr")
    repo_name: str = Field(..., description="Repository name")
    description: str = Field(default="", description="Repository description")
    private: bool = Field(default=False, description="Make repository private")
    files: Dict[str, str] = Field(default_factory=dict, description="Files to push")
    branch: str = Field(default="main", description="Target branch")
    commit_message: str = Field(default="Add generated code", description="Commit message")

class ProjectRequest(BaseModel):
    """Request schema for project operations"""
    project_name: str = Field(..., description="Project name")
    files: Dict[str, str] = Field(default_factory=dict, description="Files to create")

class MemorySearchRequest(BaseModel):
    """Request schema for memory search"""
    query: str = Field(..., description="Search query")
    limit: int = Field(default=5, ge=1, le=20, description="Maximum results")
    filter_language: Optional[str] = Field(default=None, description="Filter by language")

class ErrorResponse(BaseModel):
    """Error response schema"""
    error: str
    detail: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class SuccessResponse(BaseModel):
    """Generic success response"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None

class SessionResponse(BaseModel):
    """Session information response"""
    session_id: str
    created_at: str
    last_activity: str
    total_tasks: int
    successful_tasks: int
    languages_used: List[str]

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    dependencies: Dict[str, bool]
    memory_stats: Dict[str, int]
