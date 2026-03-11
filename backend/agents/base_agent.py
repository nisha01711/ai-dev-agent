from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from config import Config
from utils.logger import setup_logger

class BaseAgent(ABC):
    """
    Base class for all AI agents
    
    All agents inherit from this class and implement the execute method.
    Provides common functionality like LLM interaction, logging, and memory.
    """
    
    def __init__(self, name: str, system_prompt: str, temperature: float = 0.7):
        """
        Initialize base agent
        
        Args:
            name: Agent name
            system_prompt: System prompt for the agent
            temperature: LLM temperature (0-1)
        """
        self.name = name
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.logger = setup_logger(f"Agent.{name}")
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            model=Config.OPENAI_MODEL,
            temperature=temperature,
            openai_api_key=Config.OPENAI_API_KEY
        )
        
        # Conversation history
        self.conversation_history: List[Dict[str, str]] = []
        
        self.logger.info(f"{name} agent initialized")
    
    @abstractmethod
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute agent logic
        
        Args:
            input_data: Input data for the agent
        
        Returns:
            Dictionary with agent output
        """
        pass
    
    def _build_messages(self, prompt: str, context: Optional[str] = None) -> List:
        """
        Build message list for LLM
        
        Args:
            prompt: User prompt
            context: Optional context information
        
        Returns:
            List of messages
        """
        messages = [SystemMessage(content=self.system_prompt)]
        
        # Add context if provided
        if context:
            messages.append(SystemMessage(content=f"Context:\n{context}"))
        
        # Add conversation history
        for msg in self.conversation_history[-5:]:  # Last 5 messages
            if msg['role'] == 'user':
                messages.append(HumanMessage(content=msg['content']))
            elif msg['role'] == 'assistant':
                messages.append(AIMessage(content=msg['content']))
        
        # Add current prompt
        messages.append(HumanMessage(content=prompt))
        
        return messages
    
    async def _call_llm(self, prompt: str, context: Optional[str] = None) -> str:
        """
        Call LLM with prompt
        
        Args:
            prompt: User prompt
            context: Optional context
        
        Returns:
            LLM response
        """
        try:
            messages = self._build_messages(prompt, context)
            
            self.logger.info(f"Calling LLM for {self.name}")
            response = await self.llm.agenerate([messages])
            
            result = response.generations[0][0].text
            
            # Update conversation history
            self.conversation_history.append({
                'role': 'user',
                'content': prompt,
                'timestamp': datetime.utcnow().isoformat()
            })
            self.conversation_history.append({
                'role': 'assistant',
                'content': result,
                'timestamp': datetime.utcnow().isoformat()
            })
            
            return result
            
        except Exception as e:
            self.logger.error(f"LLM call failed: {str(e)}")
            raise
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        self.logger.info(f"Cleared conversation history for {self.name}")
    
    def get_history(self) -> List[Dict[str, str]]:
        """Get conversation history"""
        return self.conversation_history
    
    def _format_output(self, 
                      success: bool, 
                      data: Any = None, 
                      error: str = None,
                      execution_time: float = None) -> Dict[str, Any]:
        """
        Format agent output
        
        Args:
            success: Whether execution was successful
            data: Output data
            error: Error message if any
            execution_time: Execution time in seconds
        
        Returns:
            Formatted output dictionary
        """
        output = {
            'agent': self.name,
            'success': success,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        if data is not None:
            output['data'] = data
        
        if error:
            output['error'] = error
        
        if execution_time:
            output['execution_time'] = execution_time
        
        return output
