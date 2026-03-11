import subprocess
import asyncio
import os
from typing import Dict, Any, List
from pathlib import Path

from config import Config
from utils.logger import setup_logger

class TerminalExecutor:
    """
    Executes terminal commands safely
    
    Features:
    - Execute shell commands
    - Support multiple commands (git, npm, pip, etc.)
    - Working directory management
    - Timeout control
    - Output capture
    """
    
    # Allowed commands for security
    ALLOWED_COMMANDS = [
        'git', 'npm', 'pip', 'python', 'node', 'mkdir', 'cd',
        'ls', 'dir', 'cat', 'echo', 'which', 'where', 'npm',
        'yarn', 'pnpm', 'cargo', 'rustc', 'go', 'java', 'javac',
        'gcc', 'g++', 'make', 'cmake', 'dotnet'
    ]
    
    def __init__(self):
        """Initialize terminal executor"""
        self.logger = setup_logger("TerminalExecutor")
        self.default_timeout = 300  # 5 minutes
        
        self.logger.info("Terminal executor initialized")
    
    async def execute(self,
                     command: str,
                     cwd: str = None,
                     timeout: int = None,
                     env: Dict[str, str] = None) -> Dict[str, Any]:
        """
        Execute a terminal command
        
        Args:
            command: Command to execute
            cwd: Working directory
            timeout: Execution timeout
            env: Environment variables
        
        Returns:
            Execution result
        """
        try:
            # Security check
            if not self._is_command_safe(command):
                return {
                    'success': False,
                    'error': f'Command not allowed: {command.split()[0]}',
                    'stdout': '',
                    'stderr': 'Command blocked for security',
                    'exit_code': -1
                }
            
            self.logger.info(f"Executing command: {command[:100]}")
            
            # Set working directory
            work_dir = cwd or Config.PROJECTS_PATH
            if not os.path.exists(work_dir):
                os.makedirs(work_dir, exist_ok=True)
            
            # Prepare environment
            cmd_env = os.environ.copy()
            if env:
                cmd_env.update(env)
            
            # Execute command
            timeout_val = timeout or self.default_timeout
            
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=work_dir,
                env=cmd_env
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=timeout_val
                )
                
                success = process.returncode == 0
                
                return {
                    'success': success,
                    'stdout': stdout.decode('utf-8', errors='replace'),
                    'stderr': stderr.decode('utf-8', errors='replace'),
                    'exit_code': process.returncode,
                    'error': None if success else stderr.decode('utf-8', errors='replace')
                }
                
            except asyncio.TimeoutError:
                process.kill()
                return {
                    'success': False,
                    'stdout': '',
                    'stderr': f'Command timed out after {timeout_val} seconds',
                    'exit_code': -1,
                    'error': 'Timeout'
                }
                
        except Exception as e:
            self.logger.error(f"Command execution failed: {str(e)}")
            return {
                'success': False,
                'stdout': '',
                'stderr': str(e),
                'exit_code': -1,
                'error': str(e)
            }
    
    def _is_command_safe(self, command: str) -> bool:
        """Check if command is in allowed list"""
        base_command = command.strip().split()[0]
        
        # Check against whitelist
        return base_command in self.ALLOWED_COMMANDS
    
    async def git_clone(self,
                       repo_url: str,
                       target_dir: str,
                       branch: str = None) -> Dict[str, Any]:
        """Clone a git repository"""
        command = f"git clone {repo_url}"
        
        if branch:
            command += f" -b {branch}"
        
        command += f" {target_dir}"
        
        return await self.execute(command)
    
    async def npm_install(self, project_dir: str) -> Dict[str, Any]:
        """Run npm install in project"""
        return await self.execute("npm install", cwd=project_dir)
    
    async def pip_install(self,
                         packages: List[str],
                         project_dir: str = None) -> Dict[str, Any]:
        """Install Python packages"""
        command = f"pip install {' '.join(packages)}"
        return await self.execute(command, cwd=project_dir)
    
    async def git_init(self, project_dir: str) -> Dict[str, Any]:
        """Initialize git repository"""
        return await self.execute("git init", cwd=project_dir)
    
    async def git_add_commit(self,
                            project_dir: str,
                            message: str = "Initial commit") -> Dict[str, Any]:
        """Git add and commit"""
        # Add all files
        result1 = await self.execute("git add .", cwd=project_dir)
        
        if not result1['success']:
            return result1
        
        # Commit
        command = f'git commit -m "{message}"'
        return await self.execute(command, cwd=project_dir)
    
    async def npm_run_script(self,
                            script: str,
                            project_dir: str) -> Dict[str, Any]:
        """Run npm script"""
        command = f"npm run {script}"
        return await self.execute(command, cwd=project_dir)
    
    async def create_virtual_env(self, project_dir: str) -> Dict[str, Any]:
        """Create Python virtual environment"""
        command = "python -m venv venv"
        return await self.execute(command, cwd=project_dir)
    
    async def run_tests(self,
                       test_command: str,
                       project_dir: str) -> Dict[str, Any]:
        """Run test suite"""
        return await self.execute(test_command, cwd=project_dir)
    
    async def check_dependencies(self) -> Dict[str, bool]:
        """Check if required dependencies are installed"""
        dependencies = {
            'python': 'python --version',
            'node': 'node --version',
            'npm': 'npm --version',
            'git': 'git --version',
            'pip': 'pip --version'
        }
        
        results = {}
        
        for name, command in dependencies.items():
            try:
                result = await self.execute(command, timeout=5)
                results[name] = result['success']
            except:
                results[name] = False
        
        return results
