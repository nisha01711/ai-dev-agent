import asyncio
import time
from typing import Dict, Any, List, Optional
from enum import Enum

from agents import PlannerAgent, CoderAgent, TesterAgent, DebuggerAgent
from memory.vector_store import VectorStore
from memory.session_manager import SessionManager
from tools.code_executor import CodeExecutor
from utils.logger import setup_logger
from utils.helpers import generate_task_id

class AgentPhase(Enum):
    """Phases of agent execution pipeline"""
    PLANNING = "planning"
    CODING = "coding"
    TESTING = "testing"
    DEBUGGING = "debugging"
    COMPLETED = "completed"
    FAILED = "failed"

class AgentOrchestrator:
    """
    Orchestrates the multi-agent pipeline workflow
    
    Pipeline Flow:
    User Request → Planner → Coder → Tester → Debugger → Output
    
    The orchestrator:
    - Manages agent lifecycle
    - Coordinates data flow between agents
    - Handles errors and retries
    - Stores results in memory
    - Provides status updates
    """
    
    def __init__(self):
        """Initialize orchestrator and all agents"""
        self.logger = setup_logger("Orchestrator")
        
        # Initialize agents
        self.planner = PlannerAgent()
        self.coder = CoderAgent()
        self.tester = TesterAgent()
        self.debugger = DebuggerAgent()
        
        # Initialize supporting systems
        self.vector_store = VectorStore()
        self.session_manager = SessionManager()
        self.code_executor = CodeExecutor()
        
        # Execution state
        self.current_task_id: Optional[str] = None
        self.current_phase: AgentPhase = AgentPhase.PLANNING
        self.execution_history: List[Dict[str, Any]] = []
        
        self.logger.info("Agent Orchestrator initialized")
    
    async def execute_task(self, 
                          prompt: str,
                          language: str = 'javascript',
                          framework: str = '',
                          session_id: Optional[str] = None,
                          execute_code: bool = False,
                          auto_debug: bool = True) -> Dict[str, Any]:
        """
        Execute complete development pipeline
        
        Args:
            prompt: User's development request
            language: Target programming language
            framework: Target framework (optional)
            session_id: Session ID for memory (optional)
            execute_code: Whether to execute generated code
            auto_debug: Automatically debug if errors occur
        
        Returns:
            Complete task execution result
        """
        task_id = generate_task_id()
        self.current_task_id = task_id
        start_time = time.time()
        
        self.logger.info(f"Starting task execution: {task_id}")
        self.logger.info(f"Prompt: {prompt[:100]}...")
        
        # Create session if needed
        if not session_id:
            session_id = self.session_manager.create_session()
        
        # Check memory for similar tasks
        similar_tasks = await self.vector_store.search_similar(prompt, limit=3)
        context = self._format_memory_context(similar_tasks)
        
        result = {
            'task_id': task_id,
            'session_id': session_id,
            'prompt': prompt,
            'language': language,
            'framework': framework,
            'phases': {},
            'final_output': {},
            'execution_time': 0,
            'status': 'in_progress'
        }
        
        try:
            # Phase 1: Planning
            self.current_phase = AgentPhase.PLANNING
            self.logger.info("Phase 1: Planning")
            
            plan_result = await self.planner.execute({
                'prompt': prompt,
                'language': language,
                'framework': framework,
                'context': context
            })
            
            result['phases']['planning'] = plan_result
            
            if not plan_result['success']:
                raise Exception(f"Planning failed: {plan_result.get('error')}")
            
            plan = plan_result['data']
            
            # Phase 2: Coding
            self.current_phase = AgentPhase.CODING
            self.logger.info("Phase 2: Coding")
            
            code_result = await self.coder.execute({
                'plan': plan,
                'language': language,
                'framework': framework,
                'context': context
            })
            
            result['phases']['coding'] = code_result
            
            if not code_result['success']:
                raise Exception(f"Coding failed: {code_result.get('error')}")
            
            generated_code = code_result['data']
            
            # Phase 3: Testing (if requested)
            if execute_code or auto_debug:
                self.current_phase = AgentPhase.TESTING
                self.logger.info("Phase 3: Testing")
                
                test_result = await self.tester.execute({
                    'code': generated_code.get('files', {}),
                    'language': language,
                    'test_type': 'unit'
                })
                
                result['phases']['testing'] = test_result
            
            # Phase 4: Code Execution (if requested)
            execution_output = None
            if execute_code and generated_code.get('files'):
                self.logger.info("Executing generated code")
                
                # Execute main code file
                main_file = self._identify_main_file(generated_code['files'], language)
                if main_file:
                    execution_output = await self.code_executor.execute({
                        'code': generated_code['files'][main_file],
                        'language': language
                    })
                    
                    result['execution'] = execution_output
                    
                    # Phase 5: Debugging (if errors occur and auto_debug is True)
                    if execution_output.get('error') and auto_debug:
                        self.current_phase = AgentPhase.DEBUGGING
                        self.logger.info("Phase 5: Debugging")
                        
                        debug_result = await self.debugger.execute({
                            'code': generated_code['files'][main_file],
                            'error': execution_output['error'],
                            'language': language
                        })
                        
                        result['phases']['debugging'] = debug_result
                        
                        # If debugging successful, try execution again
                        if debug_result['success'] and debug_result['data'].get('fixed_code'):
                            fixed_code = list(debug_result['data']['fixed_code'].values())[0]
                            retry_execution = await self.code_executor.execute({
                                'code': fixed_code,
                                'language': language
                            })
                            result['execution_retry'] = retry_execution
            
            # Mark as completed
            self.current_phase = AgentPhase.COMPLETED
            result['status'] = 'completed'
            
            # Prepare final output
            result['final_output'] = {
                'plan': plan,
                'code': generated_code,
                'tests': result['phases'].get('testing', {}).get('data', {}),
                'execution': execution_output,
                'fixed_code': result['phases'].get('debugging', {}).get('data', {}).get('fixed_code', {})
            }
            
            # Store in memory
            await self.vector_store.store_task(
                task_id=task_id,
                prompt=prompt,
                result=result['final_output'],
                session_id=session_id
            )
            
            # Update session
            self.session_manager.add_task_to_session(session_id, task_id, result)
            
            execution_time = time.time() - start_time
            result['execution_time'] = execution_time
            
            self.logger.info(f"Task completed successfully in {execution_time:.2f}s")
            
        except Exception as e:
            self.logger.error(f"Task execution failed: {str(e)}")
            self.current_phase = AgentPhase.FAILED
            result['status'] = 'failed'
            result['error'] = str(e)
            result['execution_time'] = time.time() - start_time
        
        # Store execution record
        self.execution_history.append(result)
        
        return result
    
    def _format_memory_context(self, similar_tasks: List[Dict[str, Any]]) -> str:
        """Format similar tasks from memory as context"""
        if not similar_tasks:
            return ""
        
        context = "Similar previous tasks:\n\n"
        for i, task in enumerate(similar_tasks[:2], 1):
            context += f"{i}. {task.get('prompt', 'Unknown')[:100]}...\n"
            if task.get('metadata', {}).get('language'):
                context += f"   Language: {task['metadata']['language']}\n"
        
        return context
    
    def _identify_main_file(self, files: Dict[str, str], language: str) -> Optional[str]:
        """Identify the main executable file"""
        # Common main file names
        main_names = {
            'javascript': ['index.js', 'app.js', 'main.js', 'server.js'],
            'python': ['main.py', 'app.py', '__main__.py', 'run.py'],
            'typescript': ['index.ts', 'app.ts', 'main.ts'],
            'java': ['Main.java', 'App.java'],
            'go': ['main.go']
        }
        
        candidates = main_names.get(language, [])
        
        # Check for exact matches
        for filename in files.keys():
            if filename in candidates:
                return filename
        
        # Return first file if no match
        return list(files.keys())[0] if files else None
    
    async def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Get status of a task"""
        for task in self.execution_history:
            if task['task_id'] == task_id:
                return {
                    'task_id': task_id,
                    'status': task['status'],
                    'current_phase': task.get('current_phase'),
                    'execution_time': task.get('execution_time', 0)
                }
        
        return {'error': 'Task not found'}
    
    async def retry_task(self, task_id: str) -> Dict[str, Any]:
        """Retry a failed task"""
        # Find task in history
        original_task = None
        for task in self.execution_history:
            if task['task_id'] == task_id:
                original_task = task
                break
        
        if not original_task:
            return {'error': 'Task not found'}
        
        # Retry with same parameters
        return await self.execute_task(
            prompt=original_task['prompt'],
            language=original_task['language'],
            framework=original_task.get('framework', ''),
            session_id=original_task.get('session_id')
        )
    
    def get_session_history(self, session_id: str) -> List[Dict[str, Any]]:
        """Get all tasks for a session"""
        return self.session_manager.get_session_tasks(session_id)
    
    async def cleanup(self):
        """Cleanup resources"""
        self.logger.info("Cleaning up orchestrator resources")
        # Clear agent histories
        self.planner.clear_history()
        self.coder.clear_history()
        self.tester.clear_history()
        self.debugger.clear_history()
