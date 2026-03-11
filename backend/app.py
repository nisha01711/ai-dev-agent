"""
AI Software Engineer Agent - Main Application
A multi-agent AI system that can plan, code, test, and debug autonomously.
"""

from flask import Flask, jsonify
from flask_cors import CORS
import os

from config import Config
from api import api
from utils.logger import app_logger

def create_app(config_name='default'):
    """
    Application factory pattern
    
    Args:
        config_name: Configuration environment (development/production/testing)
    
    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Initialize CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": Config.CORS_ORIGINS,
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Initialize app directories
    Config.init_app()
    
    # Register blueprints
    app.register_blueprint(api)
    
    # Root endpoint
    @app.route('/')
    def index():
        return jsonify({
            'name': 'AI Software Engineer Agent API',
            'version': '1.0.0',
            'description': 'Multi-agent AI system for autonomous software development',
            'endpoints': {
                'health': '/api/health',
                'task_execution': '/api/task/execute',
                'code_execution': '/api/code/execute',
                'projects': '/api/project/*',
                'github': '/api/github/*',
                'memory': '/api/memory/*',
                'sessions': '/api/session/*',
                'terminal': '/api/terminal/*'
            },
            'docs': '/docs'
        })
    
    @app.route('/docs')
    def docs():
        """API documentation endpoint"""
        return jsonify({
            'api_documentation': {
                'base_url': f"http://{Config.API_HOST}:{Config.API_PORT}/api",
                'endpoints': [
                    {
                        'path': '/task/execute',
                        'method': 'POST',
                        'description': 'Execute a complete development task',
                        'body': {
                            'prompt': 'string (required)',
                            'language': 'string (default: javascript)',
                            'framework': 'string (optional)',
                            'session_id': 'string (optional)',
                            'execute_code': 'boolean (default: false)',
                            'auto_debug': 'boolean (default: true)'
                        }
                    },
                    {
                        'path': '/code/execute',
                        'method': 'POST',
                        'description': 'Execute code directly',
                        'body': {
                            'code': 'string (required)',
                            'language': 'string (required)',
                            'timeout': 'integer (default: 60)'
                        }
                    },
                    {
                        'path': '/project/create',
                        'method': 'POST',
                        'description': 'Create a new project',
                        'body': {
                            'project_name': 'string (required)',
                            'files': 'object (optional)'
                        }
                    },
                    {
                        'path': '/github/action',
                        'method': 'POST',
                        'description': 'Perform GitHub actions',
                        'body': {
                            'action': 'string (create_repo|push_code|create_pr)',
                            'repo_name': 'string (required)',
                            'files': 'object (for push_code)',
                            'description': 'string (optional)'
                        }
                    },
                    {
                        'path': '/memory/search',
                        'method': 'POST',
                        'description': 'Search memory for similar tasks',
                        'body': {
                            'query': 'string (required)',
                            'limit': 'integer (default: 5)'
                        }
                    },
                    {
                        'path': '/session/create',
                        'method': 'POST',
                        'description': 'Create a new session',
                        'body': {
                            'user_id': 'string (optional)'
                        }
                    }
                ]
            }
        })
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        app_logger.error(f"Internal error: {str(error)}")
        return jsonify({'error': 'Internal server error'}), 500
    
    @app.before_request
    def log_request():
        app_logger.info(f"Request: {Flask.request.method} {Flask.request.path}")
    
    app_logger.info("Flask application initialized")
    
    return app


def main():
    """Main entry point"""
    # Create application
    app = create_app()
    
    # Log startup info
    app_logger.info("=" * 80)
    app_logger.info("AI Software Engineer Agent - Backend API")
    app_logger.info("=" * 80)
    app_logger.info(f"Environment: {Config.FLASK_ENV}")
    app_logger.info(f"Debug Mode: {Config.DEBUG}")
    app_logger.info(f"Host: {Config.API_HOST}")
    app_logger.info(f"Port: {Config.API_PORT}")
    app_logger.info(f"OpenAI Model: {Config.OPENAI_MODEL}")
    app_logger.info(f"Code Execution: {'Enabled' if Config.ENABLE_CODE_EXECUTION else 'Disabled'}")
    app_logger.info(f"GitHub Integration: {'Configured' if Config.GITHUB_TOKEN else 'Not Configured'}")
    app_logger.info("=" * 80)
    
    # Run application
    try:
        app.run(
            host=Config.API_HOST,
            port=Config.API_PORT,
            debug=Config.DEBUG,
            threaded=True
        )
    except KeyboardInterrupt:
        app_logger.info("\nShutting down gracefully...")
    except Exception as e:
        app_logger.error(f"Application error: {str(e)}")
        raise


if __name__ == '__main__':
    main()
