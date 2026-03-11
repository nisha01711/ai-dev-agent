import json
import time
from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from prompts.coder_prompts import CODER_SYSTEM_PROMPT, CODING_TEMPLATE
from utils.helpers import parse_code_blocks, extract_file_structure

class CoderAgent(BaseAgent):
    """
    Coder Agent - Generates code based on execution plan
    
    Responsibilities:
    - Generate production-ready code
    - Support multiple languages and frameworks
    - Follow best practices and design patterns
    - Create complete file structures
    """
    
    def __init__(self):
        super().__init__(
            name="Coder",
            system_prompt=CODER_SYSTEM_PROMPT,
            temperature=0.3  # Lower temperature for more consistent code
        )
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate code based on plan
        
        Args:
            input_data: Dictionary containing:
                - plan: Execution plan from Planner Agent
                - step: Current step being implemented (optional)
                - language: Programming language
                - framework: Framework to use (optional)
                - context: Additional context (optional)
        
        Returns:
            Dictionary with:
                - files: Dictionary mapping filenames to code content
                - summary: Implementation summary
                - next_steps: Suggested next steps
        """
        start_time = time.time()
        
        try:
            plan = input_data.get('plan', {})
            current_step = input_data.get('step')
            language = input_data.get('language', 'javascript')
            framework = input_data.get('framework', '')
            context = input_data.get('context', '')
            
            self.logger.info(f"Generating code for language: {language}")
            
            # Build coding prompt
            plan_text = self._format_plan_for_prompt(plan)
            
            coding_prompt = CODING_TEMPLATE.format(
                plan=plan_text,
                language=language,
                framework=framework if framework else 'Standard library',
                current_step=current_step if current_step else 'Complete implementation',
                context=context if context else 'None'
            )
            
            # Call LLM
            response = await self._call_llm(coding_prompt)
            
            # Parse generated code
            code_data = self._parse_code_response(response, language)
            
            execution_time = time.time() - start_time
            self.logger.info(f"Generated {len(code_data['files'])} file(s)")
            
            return self._format_output(
                success=True,
                data=code_data,
                execution_time=execution_time
            )
            
        except Exception as e:
            self.logger.error(f"Code generation failed: {str(e)}")
            return self._format_output(
                success=False,
                error=str(e),
                execution_time=time.time() - start_time
            )
    
    def _format_plan_for_prompt(self, plan: Dict[str, Any]) -> str:
        """Format plan into readable text for prompt"""
        if not plan or 'steps' not in plan:
            return "No plan provided"
        
        plan_text = "Execution Plan:\n\n"
        
        for i, step in enumerate(plan['steps'], 1):
            plan_text += f"Step {i}: {step.get('title', 'Unknown')}\n"
            if step.get('description'):
                plan_text += f"   Description: {step['description']}\n"
            plan_text += "\n"
        
        if plan.get('technologies'):
            plan_text += f"Technologies: {', '.join(plan['technologies'])}\n"
        
        return plan_text
    
    def _parse_code_response(self, response: str, language: str) -> Dict[str, Any]:
        """
        Parse LLM response to extract code files
        
        Args:
            response: LLM response
            language: Programming language
        
        Returns:
            Dictionary with files and metadata
        """
        code_data = {
            'files': {},
            'summary': '',
            'next_steps': [],
            'raw_response': response
        }
        
        # Extract code blocks
        code_blocks = parse_code_blocks(response)
        
        # Try to extract file structure
        files = extract_file_structure(response)
        
        if files:
            code_data['files'] = files
        elif code_blocks:
            # Use code blocks with generated filenames
            for i, block in enumerate(code_blocks):
                ext = self._get_extension(block['language'] or language)
                filename = f"generated_{i+1}.{ext}"
                code_data['files'][filename] = block['code']
        
        # Extract summary (first paragraph usually)
        lines = response.split('\n')
        summary_lines = []
        in_summary = False
        
        for line in lines:
            if line.strip() and not line.strip().startswith(('#', '//', '```')):
                summary_lines.append(line.strip())
                in_summary = True
            elif in_summary and line.strip().startswith(('#', '//', '```')):
                break
        
        if summary_lines:
            code_data['summary'] = ' '.join(summary_lines[:3])
        
        # Extract next steps
        if 'next steps' in response.lower():
            next_steps_section = response.lower().split('next steps')[-1]
            for line in next_steps_section.split('\n')[:5]:
                if line.strip().startswith(('-', '*', '1', '2', '3')):
                    step = line.strip().lstrip('-*123456789. ')
                    if step:
                        code_data['next_steps'].append(step)
        
        return code_data
    
    def _get_extension(self, language: str) -> str:
        """Get file extension for language"""
        extensions = {
            'javascript': 'js',
            'typescript': 'ts',
            'python': 'py',
            'java': 'java',
            'go': 'go',
            'rust': 'rs',
            'html': 'html',
            'css': 'css',
            'json': 'json'
        }
        return extensions.get(language.lower(), 'txt')
    
    async def refine_code(self, 
                         code: str, 
                         feedback: str,
                         language: str) -> Dict[str, Any]:
        """
        Refine generated code based on feedback
        
        Args:
            code: Original code
            feedback: Feedback/improvement suggestions
            language: Programming language
        
        Returns:
            Refined code
        """
        start_time = time.time()
        
        try:
            refine_prompt = f"""
Refine the following {language} code based on this feedback:

Feedback: {feedback}

Original Code:
```{language}
{code}
```

Provide the improved code with explanations of changes made.
"""
            
            response = await self._call_llm(refine_prompt)
            code_data = self._parse_code_response(response, language)
            
            return self._format_output(
                success=True,
                data=code_data,
                execution_time=time.time() - start_time
            )
            
        except Exception as e:
            self.logger.error(f"Code refinement failed: {str(e)}")
            return self._format_output(
                success=False,
                error=str(e),
                execution_time=time.time() - start_time
            )
