"""
Advanced Agent Base with Sophisticated Prompt Engineering
=========================================================

This module provides the foundation for all advanced AI agents with:
- Chain-of-thought reasoning
- Multi-step validation
- Context-aware prompt engineering
- Advanced error handling and recovery
- Performance optimization
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union, Callable
import json
import logging
import time
from datetime import datetime
import hashlib
from dataclasses import dataclass
from enum import Enum

class PromptComplexity(Enum):
    SIMPLE = "simple"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class ReasoningMode(Enum):
    DIRECT = "direct"
    CHAIN_OF_THOUGHT = "chain_of_thought"
    STEP_BY_STEP = "step_by_step"
    MULTI_PERSPECTIVE = "multi_perspective"

@dataclass
class PromptTemplate:
    """Advanced prompt template with context awareness"""
    system_prompt: str
    user_prompt: str
    reasoning_mode: ReasoningMode
    complexity: PromptComplexity
    context_variables: Dict[str, Any]
    validation_rules: List[str]
    examples: List[Dict[str, str]]
    constraints: List[str]

class AdvancedAgentBase(ABC):
    """
    Advanced base class for all AI agents with sophisticated prompt engineering
    """
    
    def __init__(
        self,
        name: str,
        version: str = "2.0",
        reasoning_mode: ReasoningMode = ReasoningMode.CHAIN_OF_THOUGHT,
        complexity: PromptComplexity = PromptComplexity.ADVANCED,
        enable_caching: bool = True,
        enable_validation: bool = True,
        max_retries: int = 3,
        timeout: int = 30
    ):
        self.name = name
        self.version = version
        self.reasoning_mode = reasoning_mode
        self.complexity = complexity
        self.enable_caching = enable_caching
        self.enable_validation = enable_validation
        self.max_retries = max_retries
        self.timeout = timeout
        
        # Performance tracking
        self.performance_metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "average_response_time": 0,
            "cache_hits": 0,
            "validation_failures": 0
        }
        
        # Caching system
        self._cache = {} if enable_caching else None
        
        # Setup logging
        self.logger = logging.getLogger(f"{self.name}Agent")
        
    def create_advanced_prompt(
        self,
        task_description: str,
        input_data: Any,
        context: Dict[str, Any] = None,
        examples: List[Dict[str, str]] = None,
        constraints: List[str] = None
    ) -> str:
        """
        Create sophisticated prompts with advanced engineering techniques
        """
        context = context or {}
        examples = examples or []
        constraints = constraints or []
        
        # Base system prompt with reasoning framework
        system_prompt = self._build_system_prompt()
        
        # Task-specific prompt with context
        task_prompt = self._build_task_prompt(task_description, input_data, context)
        
        # Reasoning instructions
        reasoning_prompt = self._build_reasoning_prompt()
        
        # Examples and constraints
        examples_prompt = self._build_examples_prompt(examples)
        constraints_prompt = self._build_constraints_prompt(constraints)
        
        # Output format specification
        format_prompt = self._build_format_prompt()
        
        # Combine all components
        full_prompt = f"""
{system_prompt}

{task_prompt}

{reasoning_prompt}

{examples_prompt}

{constraints_prompt}

{format_prompt}
"""
        
        return full_prompt.strip()
    
    def _build_system_prompt(self) -> str:
        """Build sophisticated system prompt"""
        return f"""
You are {self.name}, an advanced AI agent specialized in professional career intelligence and resume analysis.

CORE CAPABILITIES:
- Deep understanding of recruitment processes and industry standards
- Advanced natural language processing and pattern recognition
- Multi-dimensional analysis with contextual awareness
- Evidence-based recommendations with confidence scoring
- Adaptive learning from feedback and performance metrics

OPERATIONAL PRINCIPLES:
1. ACCURACY: Provide precise, factual information with confidence levels
2. RELEVANCE: Tailor responses to specific user context and industry requirements
3. ACTIONABILITY: Deliver concrete, implementable recommendations
4. TRANSPARENCY: Explain reasoning and methodology clearly
5. CONTINUOUS IMPROVEMENT: Learn from interactions and optimize performance

QUALITY STANDARDS:
- All outputs must be professional, accurate, and actionable
- Provide confidence scores for recommendations (0-100%)
- Include reasoning chains for complex decisions
- Validate outputs against industry best practices
- Maintain consistency across all interactions
"""

    def _build_task_prompt(self, task_description: str, input_data: Any, context: Dict[str, Any]) -> str:
        """Build task-specific prompt with context"""
        context_str = ""
        if context:
            context_str = f"""
CONTEXT INFORMATION:
{json.dumps(context, indent=2)}
"""
        
        return f"""
TASK: {task_description}

INPUT DATA:
{self._format_input_data(input_data)}

{context_str}
"""

    def _build_reasoning_prompt(self) -> str:
        """Build reasoning instructions based on mode"""
        if self.reasoning_mode == ReasoningMode.CHAIN_OF_THOUGHT:
            return """
REASONING APPROACH:
Use chain-of-thought reasoning for this task:
1. ANALYSIS: Break down the input into key components
2. EVALUATION: Assess each component against relevant criteria
3. SYNTHESIS: Combine insights to form comprehensive understanding
4. VALIDATION: Cross-check conclusions against best practices
5. RECOMMENDATION: Provide actionable next steps with confidence levels

Think step-by-step and show your reasoning process clearly.
"""
        elif self.reasoning_mode == ReasoningMode.STEP_BY_STEP:
            return """
REASONING APPROACH:
Follow a systematic step-by-step process:
1. Parse and understand the input thoroughly
2. Identify key patterns and relevant information
3. Apply domain expertise and industry knowledge
4. Generate preliminary conclusions
5. Validate and refine recommendations
6. Present final output with supporting evidence

Document each step clearly.
"""
        elif self.reasoning_mode == ReasoningMode.MULTI_PERSPECTIVE:
            return """
REASONING APPROACH:
Analyze from multiple perspectives:
1. CANDIDATE PERSPECTIVE: How does this benefit the job seeker?
2. RECRUITER PERSPECTIVE: What would hiring managers look for?
3. INDUSTRY PERSPECTIVE: How does this align with current trends?
4. TECHNICAL PERSPECTIVE: Are the skills and qualifications accurate?
5. STRATEGIC PERSPECTIVE: What are the long-term implications?

Synthesize insights from all perspectives.
"""
        else:
            return "Provide direct, concise analysis and recommendations."

    def _build_examples_prompt(self, examples: List[Dict[str, str]]) -> str:
        """Build examples section"""
        if not examples:
            return ""
        
        examples_str = ""
        for i, example in enumerate(examples, 1):
            examples_str += f"""
EXAMPLE {i}:
Input: {example.get('input', 'N/A')}
Output: {example.get('output', 'N/A')}
"""
        
        return f"""
REFERENCE EXAMPLES:
{examples_str}
"""

    def _build_constraints_prompt(self, constraints: List[str]) -> str:
        """Build constraints section"""
        if not constraints:
            return ""
        
        constraints_str = "\n".join(f"- {constraint}" for constraint in constraints)
        return f"""
CONSTRAINTS AND REQUIREMENTS:
{constraints_str}
"""

    def _build_format_prompt(self) -> str:
        """Build output format specification"""
        return """
OUTPUT REQUIREMENTS:
- Provide response in valid JSON format
- Include confidence scores (0-100%) for key recommendations
- Add reasoning explanations for important decisions
- Structure data logically with clear hierarchies
- Ensure all required fields are populated
- Use consistent naming conventions
- Include metadata about the analysis process

RESPONSE STRUCTURE:
{
    "analysis": {
        "summary": "Brief overview of findings",
        "confidence_score": 85,
        "reasoning": "Explanation of analysis approach"
    },
    "results": {
        // Main results based on specific task
    },
    "recommendations": [
        {
            "action": "Specific recommendation",
            "priority": "high|medium|low",
            "confidence": 90,
            "reasoning": "Why this recommendation is important"
        }
    ],
    "metadata": {
        "processing_time": "Time taken for analysis",
        "data_quality": "Assessment of input data quality",
        "limitations": "Any limitations or caveats"
    }
}
"""

    def _format_input_data(self, input_data: Any) -> str:
        """Format input data for prompt inclusion"""
        if isinstance(input_data, dict):
            return json.dumps(input_data, indent=2)
        elif isinstance(input_data, list):
            return json.dumps(input_data, indent=2)
        else:
            return str(input_data)

    def _generate_cache_key(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Generate cache key for prompt and context"""
        content = prompt + json.dumps(context or {}, sort_keys=True)
        return hashlib.md5(content.encode()).hexdigest()

    def _validate_response(self, response: Any, validation_rules: List[str] = None) -> bool:
        """Validate AI response against rules"""
        if not self.enable_validation:
            return True
        
        try:
            # Basic JSON validation
            if isinstance(response, str):
                json.loads(response)
            
            # Custom validation rules
            if validation_rules:
                for rule in validation_rules:
                    if not self._apply_validation_rule(response, rule):
                        return False
            
            return True
        except Exception as e:
            self.logger.error(f"Validation failed: {e}")
            return False

    def _apply_validation_rule(self, response: Any, rule: str) -> bool:
        """Apply specific validation rule"""
        # Implement custom validation logic based on rule
        return True

    def update_performance_metrics(self, success: bool, response_time: float, cached: bool = False):
        """Update performance tracking metrics"""
        self.performance_metrics["total_requests"] += 1
        
        if success:
            self.performance_metrics["successful_requests"] += 1
        else:
            self.performance_metrics["failed_requests"] += 1
        
        if cached:
            self.performance_metrics["cache_hits"] += 1
        
        # Update average response time
        total = self.performance_metrics["total_requests"]
        current_avg = self.performance_metrics["average_response_time"]
        self.performance_metrics["average_response_time"] = (
            (current_avg * (total - 1) + response_time) / total
        )

    def get_performance_report(self) -> Dict[str, Any]:
        """Get detailed performance report"""
        total = self.performance_metrics["total_requests"]
        if total == 0:
            return {"message": "No requests processed yet"}
        
        success_rate = (self.performance_metrics["successful_requests"] / total) * 100
        cache_hit_rate = (self.performance_metrics["cache_hits"] / total) * 100
        
        return {
            "agent_name": self.name,
            "version": self.version,
            "total_requests": total,
            "success_rate": f"{success_rate:.2f}%",
            "cache_hit_rate": f"{cache_hit_rate:.2f}%",
            "average_response_time": f"{self.performance_metrics['average_response_time']:.2f}s",
            "failed_requests": self.performance_metrics["failed_requests"],
            "validation_failures": self.performance_metrics["validation_failures"]
        }

    @abstractmethod
    def process(self, input_data: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Abstract method for processing input data
        Must be implemented by all agent subclasses
        """
        pass

    @abstractmethod
    def get_specialized_prompt_template(self) -> PromptTemplate:
        """
        Get agent-specific prompt template
        Must be implemented by all agent subclasses
        """
        pass

    def execute_with_retry(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with retry logic"""
        last_exception = None
        
        for attempt in range(self.max_retries):
            try:
                start_time = time.time()
                result = func(*args, **kwargs)
                response_time = time.time() - start_time
                
                self.update_performance_metrics(True, response_time)
                return result
                
            except Exception as e:
                last_exception = e
                self.logger.warning(f"Attempt {attempt + 1} failed: {e}")
                
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
        
        # All retries failed
        self.update_performance_metrics(False, 0)
        raise last_exception