import re
from typing import Dict, Any, List
from pydantic import BaseModel, validator, Field

class TaskRequest(BaseModel):
    """Validation model for task requests"""
    prompt: str = Field(..., min_length=3, max_length=5000)
    language: str = Field(default="javascript", pattern="^(javascript|python|typescript|java|go|rust)$")
    framework: str = Field(default="", max_length=100)
    session_id: str = Field(default=None)
    
    @validator('prompt')
    def validate_prompt(cls, v):
        if not v.strip():
            raise ValueError('Prompt cannot be empty')
        return v.strip()


class CodeExecutionRequest(BaseModel):
    """Validation model for code execution"""
    code: str = Field(..., min_length=1)
    language: str = Field(..., pattern="^(javascript|python|typescript)$")
    timeout: int = Field(default=60, ge=1, le=300)


class GitHubRequest(BaseModel):
    """Validation model for GitHub operations"""
    action: str = Field(..., pattern="^(create_repo|push_code|create_pr)$")
    repo_name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(default="")
    is_private: bool = Field(default=False)
    code_files: Dict[str, str] = Field(default_factory=dict)


class ProjectAnalysisRequest(BaseModel):
    """Validation model for project analysis"""
    project_path: str = Field(..., min_length=1)
    include_tests: bool = Field(default=True)
    analyze_dependencies: bool = Field(default=True)


def validate_request(data: Dict[str, Any], model: BaseModel) -> tuple:
    """
    Validate request data against a Pydantic model
    
    Args:
        data: Request data dictionary
        model: Pydantic model class
    
    Returns:
        Tuple of (is_valid, validated_data_or_errors)
    """
    try:
        validated = model(**data)
        return True, validated.dict()
    except Exception as e:
        return False, str(e)


def validate_session_id(session_id: str) -> bool:
    """Validate session ID format"""
    pattern = r'^[a-zA-Z0-9_-]{8,64}$'
    return bool(re.match(pattern, session_id))


def validate_file_path(file_path: str, allowed_extensions: List[str] = None) -> bool:
    """
    Validate file path for security
    
    Args:
        file_path: File path to validate
        allowed_extensions: List of allowed file extensions
    
    Returns:
        True if valid, False otherwise
    """
    # Prevent path traversal
    if '..' in file_path or file_path.startswith('/'):
        return False
    
    # Check extension if provided
    if allowed_extensions:
        ext = file_path.split('.')[-1] if '.' in file_path else ''
        if ext not in allowed_extensions:
            return False
    
    return True
