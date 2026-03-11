import re
import uuid
import hashlib
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to remove unsafe characters
    
    Args:
        filename: Original filename
    
    Returns:
        Sanitized filename
    """
    # Remove unsafe characters
    safe_filename = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)
    # Limit length
    if len(safe_filename) > 200:
        name, ext = safe_filename.rsplit('.', 1) if '.' in safe_filename else (safe_filename, '')
        safe_filename = name[:195] + (f'.{ext}' if ext else '')
    return safe_filename


def generate_session_id() -> str:
    """
    Generate a unique session ID
    
    Returns:
        Session ID string
    """
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    random_part = uuid.uuid4().hex[:8]
    return f"session_{timestamp}_{random_part}"


def generate_task_id() -> str:
    """Generate a unique task ID"""
    return f"task_{uuid.uuid4().hex[:12]}"


def parse_code_blocks(text: str) -> List[Dict[str, str]]:
    """
    Parse code blocks from markdown text
    
    Args:
        text: Text containing code blocks
    
    Returns:
        List of dictionaries with 'language' and 'code' keys
    """
    pattern = r'```(\w+)?\n(.*?)```'
    matches = re.findall(pattern, text, re.DOTALL)
    
    code_blocks = []
    for lang, code in matches:
        code_blocks.append({
            'language': lang.lower() if lang else 'plaintext',
            'code': code.strip()
        })
    
    return code_blocks


def extract_file_structure(code: str) -> Dict[str, str]:
    """
    Extract file names and content from AI-generated code
    
    Args:
        code: Generated code with file markers
    
    Returns:
        Dictionary mapping filenames to content
    """
    files = {}
    
    # Pattern: // filename: path/to/file.js or # filename: path/to/file.py
    pattern = r'(?://|#)\s*filename:\s*([^\n]+)\n(.*?)(?=(?://|#)\s*filename:|$)'
    matches = re.findall(pattern, code, re.DOTALL)
    
    for filename, content in matches:
        filename = filename.strip()
        files[filename] = content.strip()
    
    # If no file markers, try to detect from code blocks
    if not files:
        code_blocks = parse_code_blocks(code)
        for i, block in enumerate(code_blocks):
            ext = {
                'javascript': 'js',
                'typescript': 'ts',
                'python': 'py',
                'java': 'java',
                'go': 'go'
            }.get(block['language'], 'txt')
            files[f'generated_{i+1}.{ext}'] = block['code']
    
    return files


def format_error_message(error: Exception, context: str = "") -> Dict[str, Any]:
    """
    Format error message for API response
    
    Args:
        error: Exception object
        context: Additional context
    
    Returns:
        Formatted error dictionary
    """
    return {
        'error': str(error),
        'type': type(error).__name__,
        'context': context,
        'timestamp': datetime.utcnow().isoformat()
    }


def calculate_code_hash(code: str) -> str:
    """
    Calculate hash of code content
    
    Args:
        code: Code string
    
    Returns:
        SHA256 hash
    """
    return hashlib.sha256(code.encode()).hexdigest()


def estimate_tokens(text: str) -> int:
    """
    Rough estimation of token count
    
    Args:
        text: Input text
    
    Returns:
        Estimated token count
    """
    # Rough estimation: 1 token ≈ 4 characters
    return len(text) // 4


def truncate_text(text: str, max_tokens: int = 2000) -> str:
    """
    Truncate text to maximum token count
    
    Args:
        text: Input text
        max_tokens: Maximum tokens
    
    Returns:
        Truncated text
    """
    max_chars = max_tokens * 4
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "... [truncated]"


def format_execution_time(seconds: float) -> str:
    """
    Format execution time in human-readable format
    
    Args:
        seconds: Execution time in seconds
    
    Returns:
        Formatted time string
    """
    if seconds < 1:
        return f"{seconds*1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.2f}s"
    else:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}m {secs:.1f}s"
