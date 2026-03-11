import json
import time
from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from prompts.planner_prompts import PLANNER_SYSTEM_PROMPT, PLANNING_TEMPLATE

class PlannerAgent(BaseAgent):
    """
    Planner Agent - Understands user requests and creates step-by-step execution plans
    
    Responsibilities:
    - Analyze user requirements
    - Break down complex tasks into actionable steps
    - Identify required technologies and dependencies
    - Create structured execution plan
    """
    
    def __init__(self):
        super().__init__(
            name="Planner",
            system_prompt=PLANNER_SYSTEM_PROMPT,
            temperature=0.7
        )
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create execution plan from user request
        
        Args:
            input_data: Dictionary containing:
                - prompt: User's request/requirement
                - language: Target programming language (optional)
                - framework: Target framework (optional)
                - context: Additional context (optional)
        
        Returns:
            Dictionary with:
                - plan: List of execution steps
                - technologies: Required technologies/dependencies
                - estimated_time: Estimated completion time
        """
        start_time = time.time()
        
        try:
            prompt = input_data.get('prompt')
            language = input_data.get('language', 'javascript')
            framework = input_data.get('framework', '')
            context = input_data.get('context', '')
            
            self.logger.info(f"Creating execution plan for: {prompt[:100]}...")
            
            # Build planning prompt
            planning_prompt = PLANNING_TEMPLATE.format(
                user_request=prompt,
                language=language,
                framework=framework if framework else 'None',
                context=context if context else 'None'
            )
            
            # Call LLM
            response = await self._call_llm(planning_prompt)
            
            # Parse response
            plan_data = self._parse_plan(response)
            
            execution_time = time.time() - start_time
            self.logger.info(f"Plan created with {len(plan_data['steps'])} steps")
            
            return self._format_output(
                success=True,
                data=plan_data,
                execution_time=execution_time
            )
            
        except Exception as e:
            self.logger.error(f"Planning failed: {str(e)}")
            return self._format_output(
                success=False,
                error=str(e),
                execution_time=time.time() - start_time
            )
    
    def _parse_plan(self, response: str) -> Dict[str, Any]:
        """
        Parse LLM response into structured plan
        
        Args:
            response: LLM response text
        
        Returns:
            Structured plan dictionary
        """
        try:
            # Try to extract JSON if present
            if '```json' in response:
                json_start = response.find('```json') + 7
                json_end = response.find('```', json_start)
                json_str = response[json_start:json_end].strip()
                return json.loads(json_str)
            
            # Otherwise parse manually
            plan = {
                'steps': [],
                'technologies': [],
                'estimated_time': 'Unknown',
                'complexity': 'Medium'
            }
            
            lines = response.split('\n')
            current_step = None
            
            for line in lines:
                line = line.strip()
                
                # Parse steps (Step 1:, Step 2:, etc.)
                if line.lower().startswith('step '):
                    if current_step:
                        plan['steps'].append(current_step)
                    
                    # Extract step number and title
                    parts = line.split(':', 1)
                    if len(parts) == 2:
                        title = parts[1].strip()
                        current_step = {
                            'title': title,
                            'description': '',
                            'dependencies': [],
                            'estimated_time': '5-10 minutes'
                        }
                
                # Parse description
                elif current_step and line and not line.startswith('-'):
                    if current_step['description']:
                        current_step['description'] += ' ' + line
                    else:
                        current_step['description'] = line
                
                # Parse technologies
                elif 'technologies:' in line.lower() or 'dependencies:' in line.lower():
                    idx = lines.index(line)
                    # Get next lines that start with - or *
                    for next_line in lines[idx+1:]:
                        if next_line.strip().startswith(('-', '*')):
                            tech = next_line.strip().lstrip('-*').strip()
                            if tech:
                                plan['technologies'].append(tech)
                        elif next_line.strip():
                            break
            
            # Add last step
            if current_step:
                plan['steps'].append(current_step)
            
            # Ensure at least some steps
            if not plan['steps']:
                plan['steps'] = [
                    {
                        'title': 'Setup Development Environment',
                        'description': 'Initialize project structure and install dependencies',
                        'dependencies': [],
                        'estimated_time': '5 minutes'
                    },
                    {
                        'title': 'Implement Core Logic',
                        'description': 'Build main functionality based on requirements',
                        'dependencies': ['Setup Development Environment'],
                        'estimated_time': '15-30 minutes'
                    },
                    {
                        'title': 'Test and Debug',
                        'description': 'Test the implementation and fix any issues',
                        'dependencies': ['Implement Core Logic'],
                        'estimated_time': '10 minutes'
                    }
                ]
            
            return plan
            
        except Exception as e:
            self.logger.warning(f"Failed to parse plan, using fallback: {str(e)}")
            # Return a basic fallback plan
            return {
                'steps': [
                    {
                        'title': 'Analyze Requirements',
                        'description': 'Understand the user requirements',
                        'dependencies': [],
                        'estimated_time': '5 minutes'
                    },
                    {
                        'title': 'Implement Solution',
                        'description': 'Build the requested functionality',
                        'dependencies': ['Analyze Requirements'],
                        'estimated_time': '20 minutes'
                    }
                ],
                'technologies': ['General Programming'],
                'estimated_time': '25 minutes',
                'complexity': 'Medium',
                'raw_response': response
            }
    
    def validate_plan(self, plan: Dict[str, Any]) -> bool:
        """
        Validate that a plan is well-formed
        
        Args:
            plan: Plan dictionary
        
        Returns:
            True if valid
        """
        required_keys = ['steps', 'technologies']
        
        if not all(key in plan for key in required_keys):
            return False
        
        if not plan['steps']:
            return False
        
        # Validate each step
        for step in plan['steps']:
            if not isinstance(step, dict):
                return False
            if 'title' not in step:
                return False
        
        return True
