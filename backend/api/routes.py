from flask import Blueprint, request, jsonify
from typing import Dict, Any
import asyncio

from orchestrator import AgentOrchestrator
from tools import CodeExecutor, FileManager, GitHubIntegration, TerminalExecutor
from memory import VectorStore, SessionManager
from utils.logger import app_logger
from utils.validators import validate_request
from api.schemas import (
    TaskRequest, CodeExecutionRequest, GitHubRequest,
    ProjectRequest, MemorySearchRequest, ErrorResponse
)

# Create Blueprint
api = Blueprint('api', __name__, url_prefix='/api')

# Initialize components
orchestrator = AgentOrchestrator()
code_executor = CodeExecutor()
file_manager = FileManager()
github = GitHubIntegration()
terminal = TerminalExecutor()
vector_store = VectorStore()
session_manager = SessionManager()

def async_route(f):
    """Decorator to handle async routes"""
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    wrapper.__name__ = f.__name__
    return wrapper

@api.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Check dependencies
        stats = vector_store.get_collection_stats()
        
        return jsonify({
            'status': 'healthy',
            'version': '1.0.0',
            'memory_stats': stats,
            'github_configured': github.is_configured()
        }), 200
    except Exception as e:
        app_logger.error(f"Health check failed: {str(e)}")
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

@api.route('/task/execute', methods=['POST'])
@async_route
async def execute_task():
    """Execute a development task"""
    try:
        data = request.get_json()
        
        # Validate request
        is_valid, validated = validate_request(data, TaskRequest)
        if not is_valid:
            return jsonify({'error': validated}), 400
        
        app_logger.info(f"Executing task: {validated['prompt'][:100]}...")
        
        # Execute task through orchestrator
        result = await orchestrator.execute_task(
            prompt=validated['prompt'],
            language=validated.get('language', 'javascript'),
            framework=validated.get('framework', ''),
            session_id=validated.get('session_id'),
            execute_code=validated.get('execute_code', False),
            auto_debug=validated.get('auto_debug', True)
        )
        
        return jsonify(result), 200 if result['status'] == 'completed' else 500
        
    except Exception as e:
        app_logger.error(f"Task execution failed: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api.route('/task/status/<task_id>', methods=['GET'])
@async_route
async def get_task_status(task_id: str):
    """Get status of a task"""
    try:
        status = await orchestrator.get_task_status(task_id)
        
        if 'error' in status:
            return jsonify(status), 404
        
        return jsonify(status), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/code/execute', methods=['POST'])
@async_route
async def execute_code():
    """Execute code directly"""
    try:
        data = request.get_json()
        
        is_valid, validated = validate_request(data, CodeExecutionRequest)
        if not is_valid:
            return jsonify({'error': validated}), 400
        
        result = await code_executor.execute(validated)
        
        return jsonify(result), 200
        
    except Exception as e:
        app_logger.error(f"Code execution failed: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api.route('/project/create', methods=['POST'])
def create_project():
    """Create a new project"""
    try:
        data = request.get_json()
        
        is_valid, validated = validate_request(data, ProjectRequest)
        if not is_valid:
            return jsonify({'error': validated}), 400
        
        # Create project
        result = file_manager.create_project(validated['project_name'])
        
        if not result['success']:
            return jsonify(result), 400
        
        # Create files if provided
        if validated.get('files'):
            files_result = file_manager.create_multiple_files(
                validated['project_name'],
                validated['files']
            )
            result['files'] = files_result
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/project/list', methods=['GET'])
def list_projects():
    """List all projects"""
    try:
        projects = file_manager.list_projects()
        return jsonify({'success': True, 'projects': projects}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/project/<project_name>', methods=['GET'])
def get_project_structure(project_name: str):
    """Get project structure"""
    try:
        result = file_manager.get_project_structure(project_name)
        
        if not result['success']:
            return jsonify(result), 404
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/project/<project_name>', methods=['DELETE'])
def delete_project(project_name: str):
    """Delete a project"""
    try:
        result = file_manager.delete_project(project_name)
        return jsonify(result), 200 if result['success'] else 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/github/action', methods=['POST'])
def github_action():
    """Perform GitHub action"""
    try:
        data = request.get_json()
        
        is_valid, validated = validate_request(data, GitHubRequest)
        if not is_valid:
            return jsonify({'error': validated}), 400
        
        action = validated['action']
        
        if action == 'create_repo':
            result = github.create_repository(
                name=validated['repo_name'],
                description=validated.get('description', ''),
                private=validated.get('private', False)
            )
        elif action == 'push_code':
            result = github.push_code(
                repo_name=validated['repo_name'],
                files=validated.get('files', {}),
                branch=validated.get('branch', 'main'),
                commit_message=validated.get('commit_message', 'Add code')
            )
        elif action == 'create_pr':
            result = github.create_pull_request(
                repo_name=validated['repo_name'],
                title=validated.get('title', 'New PR'),
                body=validated.get('body', ''),
                head=validated.get('head', 'feature'),
                base=validated.get('base', 'main')
            )
        else:
            return jsonify({'error': f'Unknown action: {action}'}), 400
        
        return jsonify(result), 200 if result['success'] else 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/github/repos', methods=['GET'])
def list_github_repos():
    """List GitHub repositories"""
    try:
        limit = request.args.get('limit', 10, type=int)
        repos = github.list_repositories(limit=limit)
        return jsonify({'success': True, 'repositories': repos}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/memory/search', methods=['POST'])
@async_route
async def search_memory():
    """Search memory for similar tasks"""
    try:
        data = request.get_json()
        
        is_valid, validated = validate_request(data, MemorySearchRequest)
        if not is_valid:
            return jsonify({'error': validated}), 400
        
        results = await vector_store.search_similar(
            query=validated['query'],
            limit=validated.get('limit', 5)
        )
        
        return jsonify({
            'success': True,
            'results': results,
            'count': len(results)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/memory/stats', methods=['GET'])
def memory_stats():
    """Get memory statistics"""
    try:
        stats = vector_store.get_collection_stats()
        return jsonify({'success': True, 'stats': stats}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/session/create', methods=['POST'])
def create_session():
    """Create a new session"""
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id')
        
        session_id = session_manager.create_session(user_id=user_id)
        session = session_manager.get_session(session_id)
        
        return jsonify({
            'success': True,
            'session': session
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/session/<session_id>', methods=['GET'])
def get_session(session_id: str):
    """Get session information"""
    try:
        session = session_manager.get_session(session_id)
        
        if not session:
            return jsonify({'error': 'Session not found'}), 404
        
        stats = session_manager.get_session_statistics(session_id)
        
        return jsonify({
            'success': True,
            'session': session,
            'statistics': stats
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/session/<session_id>/tasks', methods=['GET'])
def get_session_tasks(session_id: str):
    """Get all tasks for a session"""
    try:
        tasks = session_manager.get_session_tasks(session_id)
        
        return jsonify({
            'success': True,
            'tasks': tasks,
            'count': len(tasks)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/terminal/execute', methods=['POST'])
@async_route
async def execute_terminal_command():
    """Execute a terminal command"""
    try:
        data = request.get_json()
        
        command = data.get('command')
        cwd = data.get('cwd')
        timeout = data.get('timeout')
        
        if not command:
            return jsonify({'error': 'Command required'}), 400
        
        result = await terminal.execute(command, cwd=cwd, timeout=timeout)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/terminal/dependencies', methods=['GET'])
@async_route
async def check_dependencies():
    """Check system dependencies"""
    try:
        deps = await terminal.check_dependencies()
        return jsonify({'success': True, 'dependencies': deps}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Error handlers
@api.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@api.errorhandler(500)
def internal_error(error):
    app_logger.error(f"Internal error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500
