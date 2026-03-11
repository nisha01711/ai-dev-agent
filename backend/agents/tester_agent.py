import time
from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from prompts.tester_prompts import TESTER_SYSTEM_PROMPT, TESTING_TEMPLATE
from utils.helpers import parse_code_blocks

class TesterAgent(BaseAgent):
    """
    Tester Agent - Generates and executes tests for generated code
    
    Responsibilities:
    - Generate comprehensive test cases
    - Create unit tests and integration tests
    - Generate test data
    - Validate code quality
    """
    
    def __init__(self):
        super().__init__(
            name="Tester",
            system_prompt=TESTER_SYSTEM_PROMPT,
            temperature=0.4
        )
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate tests for code
        
        Args:
            input_data: Dictionary containing:
                - code: Code to test
                - language: Programming language
                - test_type: Type of tests (unit, integration, e2e)
                - coverage_target: Target coverage percentage (optional)
        
        Returns:
            Dictionary with:
                - test_files: Generated test code
                - test_cases: List of test cases
                - coverage: Expected coverage info
        """
        start_time = time.time()
        
        try:
            code = input_data.get('code', {})
            language = input_data.get('language', 'javascript')
            test_type = input_data.get('test_type', 'unit')
            coverage_target = input_data.get('coverage_target', 80)
            
            self.logger.info(f"Generating {test_type} tests for {language}")
            
            # Format code for prompt
            code_text = self._format_code_for_prompt(code)
            
            # Build testing prompt
            testing_prompt = TESTING_TEMPLATE.format(
                code=code_text,
                language=language,
                test_type=test_type,
                coverage_target=coverage_target
            )
            
            # Call LLM
            response = await self._call_llm(testing_prompt)
            
            # Parse test response
            test_data = self._parse_test_response(response, language)
            
            execution_time = time.time() - start_time
            self.logger.info(f"Generated {len(test_data['test_cases'])} test case(s)")
            
            return self._format_output(
                success=True,
                data=test_data,
                execution_time=execution_time
            )
            
        except Exception as e:
            self.logger.error(f"Test generation failed: {str(e)}")
            return self._format_output(
                success=False,
                error=str(e),
                execution_time=time.time() - start_time
            )
    
    def _format_code_for_prompt(self, code: Any) -> str:
        """Format code dictionary into readable text"""
        if isinstance(code, dict):
            formatted = ""
            for filename, content in code.items():
                formatted += f"\n// File: {filename}\n{content}\n"
            return formatted
        return str(code)
    
    def _parse_test_response(self, response: str, language: str) -> Dict[str, Any]:
        """
        Parse LLM response to extract test code and cases
        
        Args:
            response: LLM response
            language: Programming language
        
        Returns:
            Dictionary with test data
        """
        test_data = {
            'test_files': {},
            'test_cases': [],
            'coverage': {},
            'framework': self._detect_test_framework(response, language),
            'raw_response': response
        }
        
        # Extract code blocks
        code_blocks = parse_code_blocks(response)
        
        for i, block in enumerate(code_blocks):
            ext = self._get_test_extension(language)
            filename = f"test_{i+1}.{ext}"
            test_data['test_files'][filename] = block['code']
            
            # Extract test cases from code
            test_cases = self._extract_test_cases(block['code'], language)
            test_data['test_cases'].extend(test_cases)
        
        # Extract coverage info
        if 'coverage' in response.lower():
            test_data['coverage'] = {
                'target': 80,
                'estimated': 'High',
                'details': 'Comprehensive test coverage'
            }
        
        return test_data
    
    def _detect_test_framework(self, response: str, language: str) -> str:
        """Detect which test framework is being used"""
        frameworks = {
            'javascript': ['jest', 'mocha', 'jasmine', 'vitest'],
            'typescript': ['jest', 'vitest', 'mocha'],
            'python': ['pytest', 'unittest', 'nose'],
            'java': ['junit', 'testng'],
            'go': ['testing']
        }
        
        response_lower = response.lower()
        
        for framework in frameworks.get(language, []):
            if framework in response_lower:
                return framework
        
        # Return default
        defaults = {
            'javascript': 'jest',
            'typescript': 'jest',
            'python': 'pytest',
            'java': 'junit',
            'go': 'testing'
        }
        return defaults.get(language, 'generic')
    
    def _extract_test_cases(self, code: str, language: str) -> List[Dict[str, str]]:
        """Extract individual test cases from test code"""
        test_cases = []
        
        # Patterns for different languages
        patterns = {
            'javascript': [r"test\('(.+?)'", r'it\("(.+?)"', r"describe\('(.+?)'"],
            'python': [r'def test_(\w+)', r'class Test(\w+)'],
            'java': [r'@Test.*?void\s+(\w+)']
        }
        
        import re
        for pattern in patterns.get(language, []):
            matches = re.findall(pattern, code)
            for match in matches:
                test_cases.append({
                    'name': match,
                    'type': 'unit',
                    'status': 'pending'
                })
        
        return test_cases
    
    def _get_test_extension(self, language: str) -> str:
        """Get test file extension"""
        extensions = {
            'javascript': 'test.js',
            'typescript': 'test.ts',
            'python': 'test.py',
            'java': 'Test.java',
            'go': 'test.go'
        }
        return extensions.get(language, 'test.txt')
    
    async def analyze_test_results(self, 
                                   test_output: str,
                                   language: str) -> Dict[str, Any]:
        """
        Analyze test execution results
        
        Args:
            test_output: Test execution output
            language: Programming language
        
        Returns:
            Analysis of test results
        """
        start_time = time.time()
        
        try:
            analysis_prompt = f"""
Analyze the following test execution output for {language} code:

{test_output}

Provide:
1. Summary of test results (passed/failed/skipped)
2. Specific failures and their causes
3. Recommendations for fixing failures
4. Coverage analysis if available
"""
            
            response = await self._call_llm(analysis_prompt)
            
            analysis = {
                'summary': response,
                'passed': 0,
                'failed': 0,
                'skipped': 0,
                'recommendations': []
            }
            
            # Try to extract numbers
            import re
            passed = re.search(r'(\d+)\s+passed', test_output, re.IGNORECASE)
            failed = re.search(r'(\d+)\s+failed', test_output, re.IGNORECASE)
            
            if passed:
                analysis['passed'] = int(passed.group(1))
            if failed:
                analysis['failed'] = int(failed.group(1))
            
            return self._format_output(
                success=True,
                data=analysis,
                execution_time=time.time() - start_time
            )
            
        except Exception as e:
            self.logger.error(f"Test analysis failed: {str(e)}")
            return self._format_output(
                success=False,
                error=str(e),
                execution_time=time.time() - start_time
            )
