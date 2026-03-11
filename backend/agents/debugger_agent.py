import time
import re
from typing import Dict, Any, List, Optional
from agents.base_agent import BaseAgent
from prompts.debugger_prompts import DEBUGGER_SYSTEM_PROMPT, DEBUGGING_TEMPLATE
from utils.helpers import parse_code_blocks

class DebuggerAgent(BaseAgent):
    """
    Debugger Agent - Analyzes errors and fixes code
    
    Responsibilities:
    - Analyze error messages and stack traces
    - Identify root causes of bugs
    - Generate fixes for code issues
    - Suggest preventive measures
    """
    
    def __init__(self):
        super().__init__(
            name="Debugger",
            system_prompt=DEBUGGER_SYSTEM_PROMPT,
            temperature=0.2  # Very low temperature for precise fixes
        )
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Debug code and provide fixes
        
        Args:
            input_data: Dictionary containing:
                - code: Code with errors
                - error: Error message / stack trace
                - language: Programming language
                - context: Additional context (optional)
        
        Returns:
            Dictionary with:
                - diagnosis: Error analysis
                - fixed_code: Corrected code
                - explanation: Explanation of fixes
                - prevention: Tips to prevent similar errors
        """
        start_time = time.time()
        
        try:
            code = input_data.get('code', '')
            error = input_data.get('error', '')
            language = input_data.get('language', 'javascript')
            context = input_data.get('context', '')
            
            self.logger.info(f"Debugging {language} code")
            
            # Analyze error
            error_analysis = self._analyze_error(error, language)
            
            # Format code for prompt
            code_text = self._format_code_for_prompt(code)
            
            # Build debugging prompt
            debugging_prompt = DEBUGGING_TEMPLATE.format(
                code=code_text,
                error=error,
                language=language,
                error_type=error_analysis['type'],
                context=context if context else 'None'
            )
            
            # Call LLM
            response = await self._call_llm(debugging_prompt)
            
            # Parse debug response
            debug_data = self._parse_debug_response(response, language)
            debug_data['error_analysis'] = error_analysis
            
            execution_time = time.time() - start_time
            self.logger.info(f"Debugging completed in {execution_time:.2f}s")
            
            return self._format_output(
                success=True,
                data=debug_data,
                execution_time=execution_time
            )
            
        except Exception as e:
            self.logger.error(f"Debugging failed: {str(e)}")
            return self._format_output(
                success=False,
                error=str(e),
                execution_time=time.time() - start_time
            )
    
    def _analyze_error(self, error: str, language: str) -> Dict[str, Any]:
        """
        Analyze error message to identify error type
        
        Args:
            error: Error message
            language: Programming language
        
        Returns:
            Error analysis dictionary
        """
        error_lower = error.lower()
        
        # Common error patterns
        error_types = {
            'SyntaxError': ['syntaxerror', 'unexpected token', 'invalid syntax'],
            'TypeError': ['typeerror', 'cannot read property', 'undefined is not'],
            'ReferenceError': ['referenceerror', 'is not defined', 'undefined reference'],
            'RuntimeError': ['runtimeerror', 'runtime exception', 'execution error'],
            'ImportError': ['importerror', 'modulenotfounderror', 'cannot import'],
            'IndexError': ['indexerror', 'list index out of range', 'array index'],
            'KeyError': ['keyerror', 'key not found'],
            'ValueError': ['valueerror', 'invalid value'],
            'AttributeError': ['attributeerror', 'has no attribute']
        }
        
        error_type = 'UnknownError'
        for etype, patterns in error_types.items():
            if any(pattern in error_lower for pattern in patterns):
                error_type = etype
                break
        
        # Extract line number if present
        line_match = re.search(r'line (\d+)', error, re.IGNORECASE)
        line_number = int(line_match.group(1)) if line_match else None
        
        return {
            'type': error_type,
            'line_number': line_number,
            'severity': self._assess_severity(error_type),
            'message': error
        }
    
    def _assess_severity(self, error_type: str) -> str:
        """Assess error severity"""
        critical = ['SyntaxError', 'ImportError']
        high = ['TypeError', 'RuntimeError', 'AttributeError']
        
        if error_type in critical:
            return 'critical'
        elif error_type in high:
            return 'high'
        return 'medium'
    
    def _format_code_for_prompt(self, code: Any) -> str:
        """Format code for prompt"""
        if isinstance(code, dict):
            formatted = ""
            for filename, content in code.items():
                formatted += f"\n// File: {filename}\n{content}\n"
            return formatted
        return str(code)
    
    def _parse_debug_response(self, response: str, language: str) -> Dict[str, Any]:
        """
        Parse debugging response
        
        Args:
            response: LLM response
            language: Programming language
        
        Returns:
            Debug data dictionary
        """
        debug_data = {
            'diagnosis': '',
            'fixed_code': {},
            'explanation': '',
            'prevention': [],
            'raw_response': response
        }
        
        # Extract diagnosis (usually first section)
        sections = response.split('\n\n')
        if sections:
            debug_data['diagnosis'] = sections[0]
        
        # Extract fixed code
        code_blocks = parse_code_blocks(response)
        for i, block in enumerate(code_blocks):
            ext = self._get_extension(language)
            filename = f"fixed_{i+1}.{ext}"
            debug_data['fixed_code'][filename] = block['code']
        
        # If no code blocks, try to extract code directly
        if not debug_data['fixed_code'] and '```' in response:
            # Extract first code block
            start = response.find('```')
            end = response.find('```', start + 3)
            if end > start:
                code = response[start+3:end].strip()
                # Remove language identifier if present
                if '\n' in code:
                    lines = code.split('\n')
                    if lines[0].strip() in ['javascript', 'python', 'java', 'typescript']:
                        code = '\n'.join(lines[1:])
                debug_data['fixed_code'][f'fixed.{self._get_extension(language)}'] = code
        
        # Extract explanation
        if 'explanation' in response.lower():
            expl_start = response.lower().find('explanation')
            expl_section = response[expl_start:expl_start+500]
            debug_data['explanation'] = expl_section.split('\n\n')[0]
        
        # Extract prevention tips
        if 'prevent' in response.lower() or 'avoid' in response.lower():
            prevent_section = response.lower()
            if 'prevent' in prevent_section:
                prevent_section = response[response.lower().find('prevent'):]
            elif 'avoid' in prevent_section:
                prevent_section = response[response.lower().find('avoid'):]
            
            for line in prevent_section.split('\n')[:10]:
                if line.strip().startswith(('-', '*', '1', '2', '3')):
                    tip = line.strip().lstrip('-*123456789. ')
                    if tip and len(tip) > 10:
                        debug_data['prevention'].append(tip)
        
        return debug_data
    
    def _get_extension(self, language: str) -> str:
        """Get file extension for language"""
        extensions = {
            'javascript': 'js',
            'typescript': 'ts',
            'python': 'py',
            'java': 'java',
            'go': 'go',
            'rust': 'rs'
        }
        return extensions.get(language.lower(), 'txt')
    
    async def suggest_improvements(self, 
                                  code: str,
                                  language: str) -> Dict[str, Any]:
        """
        Suggest code quality improvements
        
        Args:
            code: Source code
            language: Programming language
        
        Returns:
            Improvement suggestions
        """
        start_time = time.time()
        
        try:
            improvement_prompt = f"""
Analyze the following {language} code and suggest improvements for:
1. Code quality and readability
2. Performance optimizations
3. Security vulnerabilities
4. Best practices adherence

Code:
```{language}
{code}
```

Provide specific, actionable suggestions.
"""
            
            response = await self._call_llm(improvement_prompt)
            
            improvements = {
                'suggestions': [],
                'priority': {},
                'summary': response
            }
            
            # Extract suggestions
            for line in response.split('\n'):
                if line.strip().startswith(('-', '*', '1', '2', '3')):
                    suggestion = line.strip().lstrip('-*123456789. ')
                    if suggestion and len(suggestion) > 10:
                        improvements['suggestions'].append(suggestion)
            
            return self._format_output(
                success=True,
                data=improvements,
                execution_time=time.time() - start_time
            )
            
        except Exception as e:
            self.logger.error(f"Improvement analysis failed: {str(e)}")
            return self._format_output(
                success=False,
                error=str(e),
                execution_time=time.time() - start_time
            )
