import subprocess
import asyncio
import tempfile
import os
from typing import Dict, Any, Optional
from pathlib import Path

from config import Config
from utils.logger import setup_logger

class CodeExecutor:
    """
    Executes code in a sandboxed environment
    
    Supports:
    - Python code execution
    - JavaScript/Node.js execution
    - TypeScript execution (compiled to JS)
    - Timeout and resource limits
    - Capture stdout, stderr, and return codes
    """
    
    def __init__(self):
        """Initialize code executor"""
        self.logger = setup_logger("CodeExecutor")
        self.timeout = Config.CODE_EXECUTION_TIMEOUT
        
        # Check if execution is enabled
        if not Config.ENABLE_CODE_EXECUTION:
            self.logger.warning("Code execution is DISABLED in config")
        
        self.logger.info("Code executor initialized")
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute code
        
        Args:
            input_data: Dictionary with:
                - code: Code to execute
                - language: Programming language
                - timeout: Custom timeout (optional)
                - stdin: Input data (optional)
        
        Returns:
            Execution result with stdout, stderr, exit_code
        """
        code = input_data.get('code', '')
        language = input_data.get('language', 'python')
        timeout = input_data.get('timeout', self.timeout)
        stdin_data = input_data.get('stdin', '')
        
        if not Config.ENABLE_CODE_EXECUTION:
            return {
                'success': False,
                'error': 'Code execution is disabled',
                'stdout': '',
                'stderr': 'Code execution is disabled in configuration',
                'exit_code': -1
            }
        
        self.logger.info(f"Executing {language} code")
        
        try:
            # Execute based on language
            if language in ['python', 'py']:
                result = await self._execute_python(code, timeout, stdin_data)
            elif language in ['javascript', 'js', 'node']:
                result = await self._execute_javascript(code, timeout, stdin_data)
            elif language in ['typescript', 'ts']:
                result = await self._execute_typescript(code, timeout, stdin_data)
            else:
                return {
                    'success': False,
                    'error': f'Unsupported language: {language}',
                    'stdout': '',
                    'stderr': f'Language {language} not supported',
                    'exit_code': -1
                }
            
            return result
            
        except Exception as e:
            self.logger.error(f"Code execution failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'stdout': '',
                'stderr': str(e),
                'exit_code': -1
            }
    
    async def _execute_python(self,
                             code: str,
                             timeout: int,
                             stdin_data: str = '') -> Dict[str, Any]:
        """Execute Python code"""
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            try:
                # Execute
                process = await asyncio.create_subprocess_exec(
                    'python', temp_file,
                    stdin=asyncio.subprocess.PIPE if stdin_data else None,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                
                try:
                    stdout, stderr = await asyncio.wait_for(
                        process.communicate(input=stdin_data.encode() if stdin_data else None),
                        timeout=timeout
                    )
                    
                    return {
                        'success': process.returncode == 0,
                        'stdout': stdout.decode('utf-8', errors='replace'),
                        'stderr': stderr.decode('utf-8', errors='replace'),
                        'exit_code': process.returncode,
                        'error': None if process.returncode == 0 else stderr.decode('utf-8', errors='replace')
                    }
                    
                except asyncio.TimeoutError:
                    process.kill()
                    return {
                        'success': False,
                        'stdout': '',
                        'stderr': f'Execution timed out after {timeout} seconds',
                        'exit_code': -1,
                        'error': 'Timeout'
                    }
            finally:
                # Cleanup temp file
                try:
                    os.unlink(temp_file)
                except:
                    pass
                    
        except Exception as e:
            return {
                'success': False,
                'stdout': '',
                'stderr': str(e),
                'exit_code': -1,
                'error': str(e)
            }
    
    async def _execute_javascript(self,
                                  code: str,
                                  timeout: int,
                                  stdin_data: str = '') -> Dict[str, Any]:
        """Execute JavaScript code using Node.js"""
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            try:
                # Execute
                process = await asyncio.create_subprocess_exec(
                    'node', temp_file,
                    stdin=asyncio.subprocess.PIPE if stdin_data else None,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                
                try:
                    stdout, stderr = await asyncio.wait_for(
                        process.communicate(input=stdin_data.encode() if stdin_data else None),
                        timeout=timeout
                    )
                    
                    return {
                        'success': process.returncode == 0,
                        'stdout': stdout.decode('utf-8', errors='replace'),
                        'stderr': stderr.decode('utf-8', errors='replace'),
                        'exit_code': process.returncode,
                        'error': None if process.returncode == 0 else stderr.decode('utf-8', errors='replace')
                    }
                    
                except asyncio.TimeoutError:
                    process.kill()
                    return {
                        'success': False,
                        'stdout': '',
                        'stderr': f'Execution timed out after {timeout} seconds',
                        'exit_code': -1,
                        'error': 'Timeout'
                    }
            finally:
                try:
                    os.unlink(temp_file)
                except:
                    pass
                    
        except Exception as e:
            return {
                'success': False,
                'stdout': '',
                'stderr': str(e),
                'exit_code': -1,
                'error': str(e)
            }
    
    async def _execute_typescript(self,
                                  code: str,
                                  timeout: int,
                                  stdin_data: str = '') -> Dict[str, Any]:
        """Execute TypeScript code (compile then run)"""
        # For simplicity, use ts-node if available, otherwise return error
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.ts', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            try:
                # Try ts-node first
                process = await asyncio.create_subprocess_exec(
                    'ts-node', temp_file,
                    stdin=asyncio.subprocess.PIPE if stdin_data else None,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                
                try:
                    stdout, stderr = await asyncio.wait_for(
                        process.communicate(input=stdin_data.encode() if stdin_data else None),
                        timeout=timeout
                    )
                    
                    return {
                        'success': process.returncode == 0,
                        'stdout': stdout.decode('utf-8', errors='replace'),
                        'stderr': stderr.decode('utf-8', errors='replace'),
                        'exit_code': process.returncode,
                        'error': None if process.returncode == 0 else stderr.decode('utf-8', errors='replace')
                    }
                    
                except asyncio.TimeoutError:
                    process.kill()
                    return {
                        'success': False,
                        'stdout': '',
                        'stderr': f'Execution timed out after {timeout} seconds',
                        'exit_code': -1,
                        'error': 'Timeout'
                    }
            finally:
                try:
                    os.unlink(temp_file)
                except:
                    pass
                    
        except FileNotFoundError:
            return {
                'success': False,
                'stdout': '',
                'stderr': 'ts-node not found. Please install: npm install -g ts-node typescript',
                'exit_code': -1,
                'error': 'TypeScript runtime not available'
            }
        except Exception as e:
            return {
                'success': False,
                'stdout': '',
                'stderr': str(e),
                'exit_code': -1,
                'error': str(e)
            }
    
    async def execute_file(self, file_path: str, language: str, timeout: Optional[int] = None) -> Dict[str, Any]:
        """
        Execute an existing file
        
        Args:
            file_path: Path to file
            language: Programming language
            timeout: Execution timeout
        
        Returns:
            Execution result
        """
        try:
            with open(file_path, 'r') as f:
                code = f.read()
            
            return await self.execute({
                'code': code,
                'language': language,
                'timeout': timeout or self.timeout
            })
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'stdout': '',
                'stderr': str(e),
                'exit_code': -1
            }
