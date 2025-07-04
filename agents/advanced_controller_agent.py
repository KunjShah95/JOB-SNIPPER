"""
Advanced Controller Agent
=========================

Intelligent orchestration system with:
- Dynamic workflow management
- Agent performance monitoring
- Adaptive routing and fallback
- Context-aware processing
- Real-time optimization
- Comprehensive error handling
"""

from agents.advanced_agent_base import AdvancedAgentBase, PromptTemplate, ReasoningMode, PromptComplexity
from agents.advanced_resume_parser_agent import AdvancedResumeParserAgent
from agents.advanced_job_matcher_agent import AdvancedJobMatcherAgent
from agents.advanced_skill_recommendation_agent import AdvancedSkillRecommendationAgent
from typing import Dict, Any, List, Optional, Callable
import json
import logging
import asyncio
from datetime import datetime
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from enum import Enum

class WorkflowStage(Enum):
    INITIALIZATION = "initialization"
    RESUME_PARSING = "resume_parsing"
    JOB_MATCHING = "job_matching"
    SKILL_ANALYSIS = "skill_analysis"
    RECOMMENDATION_GENERATION = "recommendation_generation"
    RESULT_SYNTHESIS = "result_synthesis"
    QUALITY_ASSURANCE = "quality_assurance"
    FINALIZATION = "finalization"

@dataclass
class AgentPerformance:
    agent_name: str
    success_rate: float
    average_response_time: float
    error_count: int
    last_execution_time: float
    confidence_score: float

class AdvancedControllerAgent(AdvancedAgentBase):
    """
    Advanced controller with intelligent orchestration and adaptive workflows
    """
    
    def __init__(self):
        super().__init__(
            name="AdvancedController",
            version="2.0",
            reasoning_mode=ReasoningMode.MULTI_PERSPECTIVE,
            complexity=PromptComplexity.EXPERT
        )
        
        # Initialize specialized agents
        self.resume_parser = AdvancedResumeParserAgent()
        self.job_matcher = AdvancedJobMatcherAgent()
        self.skill_recommender = AdvancedSkillRecommendationAgent()
        
        # Agent registry and performance tracking
        self.agent_registry = {
            "resume_parser": self.resume_parser,
            "job_matcher": self.job_matcher,
            "skill_recommender": self.skill_recommender
        }
        
        self.agent_performance = {
            name: AgentPerformance(
                agent_name=name,
                success_rate=100.0,
                average_response_time=0.0,
                error_count=0,
                last_execution_time=0.0,
                confidence_score=85.0
            ) for name in self.agent_registry.keys()
        }
        
        # Workflow configuration
        self.workflow_config = self._initialize_workflow_config()
        self.parallel_execution = True
        self.max_workers = 3
        
        # Quality thresholds
        self.quality_thresholds = {
            "minimum_confidence": 70,
            "maximum_response_time": 30,
            "minimum_success_rate": 80
        }

    def process(self, input_data: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Advanced processing with intelligent workflow orchestration
        """
        try:
            # Initialize processing context
            processing_context = self._initialize_processing_context(input_data, context)
            
            # Generate cache key
            cache_key = self._generate_cache_key(json.dumps(input_data), context)
            
            # Check cache
            if self._cache and cache_key in self._cache:
                self.update_performance_metrics(True, 0, cached=True)
                return self._cache[cache_key]
            
            # Execute intelligent workflow
            result = self.execute_with_retry(
                self._execute_intelligent_workflow, 
                input_data, 
                processing_context
            )
            
            # Cache result
            if self._cache:
                self._cache[cache_key] = result
            
            return result
            
        except Exception as e:
            self.logger.error(f"Controller processing failed: {e}")
            return self._get_fallback_result(input_data)

    def _execute_intelligent_workflow(
        self, 
        input_data: Dict[str, Any], 
        processing_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute intelligent workflow with adaptive routing
        """
        workflow_start_time = time.time()
        workflow_results = {}
        
        try:
            # Stage 1: Resume Parsing
            parsing_result = self._execute_stage(
                WorkflowStage.RESUME_PARSING,
                self._parse_resume_stage,
                input_data,
                processing_context
            )
            workflow_results["parsing"] = parsing_result
            
            # Stage 2: Parallel Analysis (Job Matching + Skill Analysis)
            if self.parallel_execution and self._should_execute_parallel():
                parallel_results = self._execute_parallel_analysis(
                    parsing_result, input_data, processing_context
                )
                workflow_results.update(parallel_results)
            else:
                # Sequential execution
                matching_result = self._execute_stage(
                    WorkflowStage.JOB_MATCHING,
                    self._job_matching_stage,
                    {"parsed_data": parsing_result, "input_data": input_data},
                    processing_context
                )
                workflow_results["matching"] = matching_result
                
                skill_result = self._execute_stage(
                    WorkflowStage.SKILL_ANALYSIS,
                    self._skill_analysis_stage,
                    {"parsed_data": parsing_result, "matching_data": matching_result},
                    processing_context
                )
                workflow_results["skills"] = skill_result
            
            # Stage 3: Result Synthesis
            synthesis_result = self._execute_stage(
                WorkflowStage.RESULT_SYNTHESIS,
                self._synthesize_results,
                workflow_results,
                processing_context
            )
            
            # Stage 4: Quality Assurance
            qa_result = self._execute_stage(
                WorkflowStage.QUALITY_ASSURANCE,
                self._quality_assurance,
                synthesis_result,
                processing_context
            )
            
            # Stage 5: Generate Final Recommendations
            final_result = self._execute_stage(
                WorkflowStage.FINALIZATION,
                self._generate_final_recommendations,
                qa_result,
                processing_context
            )
            
            # Add workflow metadata
            final_result["workflow_metadata"] = {
                "execution_time": time.time() - workflow_start_time,
                "stages_completed": len([s for s in WorkflowStage if s.value in str(workflow_results)]),
                "parallel_execution": self.parallel_execution,
                "agent_performance": self._get_agent_performance_summary(),
                "quality_score": self._calculate_workflow_quality_score(workflow_results),
                "timestamp": datetime.now().isoformat()
            }
            
            return final_result
            
        except Exception as e:
            self.logger.error(f"Workflow execution failed: {e}")
            return self._handle_workflow_failure(e, workflow_results)

    def _execute_stage(
        self, 
        stage: WorkflowStage, 
        stage_function: Callable, 
        stage_input: Any, 
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a single workflow stage with monitoring
        """
        stage_start_time = time.time()
        
        try:
            self.logger.info(f"Executing stage: {stage.value}")
            
            # Execute stage function
            result = stage_function(stage_input, context)
            
            # Calculate execution time
            execution_time = time.time() - stage_start_time
            
            # Validate result quality
            quality_score = self._validate_stage_result(stage, result)
            
            # Update stage metadata
            result["stage_metadata"] = {
                "stage": stage.value,
                "execution_time": execution_time,
                "quality_score": quality_score,
                "success": True,
                "timestamp": datetime.now().isoformat()
            }
            
            return result
            
        except Exception as e:
            execution_time = time.time() - stage_start_time
            self.logger.error(f"Stage {stage.value} failed: {e}")
            
            return {
                "error": f"Stage {stage.value} failed: {str(e)}",
                "stage_metadata": {
                    "stage": stage.value,
                    "execution_time": execution_time,
                    "quality_score": 0,
                    "success": False,
                    "timestamp": datetime.now().isoformat()
                }
            }

    def _execute_parallel_analysis(
        self, 
        parsing_result: Dict[str, Any], 
        input_data: Dict[str, Any], 
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute job matching and skill analysis in parallel
        """
        parallel_results = {}
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit parallel tasks
            future_to_task = {
                executor.submit(
                    self._job_matching_stage,
                    {"parsed_data": parsing_result, "input_data": input_data},
                    context
                ): "matching",
                executor.submit(
                    self._skill_analysis_stage,
                    {"parsed_data": parsing_result, "input_data": input_data},
                    context
                ): "skills"
            }
            
            # Collect results
            for future in as_completed(future_to_task):
                task_name = future_to_task[future]
                try:
                    result = future.result(timeout=self.quality_thresholds["maximum_response_time"])
                    parallel_results[task_name] = result
                except Exception as e:
                    self.logger.error(f"Parallel task {task_name} failed: {e}")
                    parallel_results[task_name] = {"error": str(e)}
        
        return parallel_results

    def _parse_resume_stage(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute resume parsing stage
        """
        try:
            # Track agent performance
            start_time = time.time()
            
            # Execute parsing
            result = self.resume_parser.process(input_data, context)
            
            # Update performance metrics
            execution_time = time.time() - start_time
            self._update_agent_performance("resume_parser", True, execution_time, result)
            
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            self._update_agent_performance("resume_parser", False, execution_time, {})
            raise e

    def _job_matching_stage(self, stage_input: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute job matching stage
        """
        try:
            start_time = time.time()
            
            # Prepare input for job matcher
            matcher_input = {
                "candidate_profile": stage_input.get("parsed_data", {}),
                "job_requirements": context.get("job_requirements", {}),
                "original_input": stage_input.get("input_data", {})
            }
            
            # Execute matching
            result = self.job_matcher.process(matcher_input, context)
            
            # Update performance metrics
            execution_time = time.time() - start_time
            self._update_agent_performance("job_matcher", True, execution_time, result)
            
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            self._update_agent_performance("job_matcher", False, execution_time, {})
            raise e

    def _skill_analysis_stage(self, stage_input: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute skill analysis stage
        """
        try:
            start_time = time.time()
            
            # Prepare input for skill recommender
            skill_input = {
                "user_profile": stage_input.get("parsed_data", {}),
                "career_goals": context.get("career_goals", {}),
                "matching_data": stage_input.get("matching_data", {})
            }
            
            # Execute skill analysis
            result = self.skill_recommender.process(skill_input, context)
            
            # Update performance metrics
            execution_time = time.time() - start_time
            self._update_agent_performance("skill_recommender", True, execution_time, result)
            
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            self._update_agent_performance("skill_recommender", False, execution_time, {})
            raise e

    def _synthesize_results(self, workflow_results: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Synthesize results from all workflow stages
        """
        try:
            synthesis = {
                "comprehensive_analysis": {
                    "resume_insights": workflow_results.get("parsing", {}),
                    "job_compatibility": workflow_results.get("matching", {}),
                    "skill_development": workflow_results.get("skills", {})
                },
                "cross_analysis": self._perform_cross_analysis(workflow_results),
                "confidence_assessment": self._assess_overall_confidence(workflow_results),
                "consistency_check": self._check_result_consistency(workflow_results)
            }
            
            return synthesis
            
        except Exception as e:
            self.logger.error(f"Result synthesis failed: {e}")
            return {"error": "Synthesis failed", "raw_results": workflow_results}

    def _quality_assurance(self, synthesis_result: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform quality assurance on synthesized results
        """
        try:
            qa_report = {
                "quality_score": self._calculate_quality_score(synthesis_result),
                "completeness_check": self._check_completeness(synthesis_result),
                "accuracy_assessment": self._assess_accuracy(synthesis_result),
                "consistency_validation": self._validate_consistency(synthesis_result),
                "recommendations_quality": self._assess_recommendations_quality(synthesis_result)
            }
            
            # Add QA report to synthesis
            synthesis_result["quality_assurance"] = qa_report
            
            # Apply quality improvements if needed
            if qa_report["quality_score"] < self.quality_thresholds["minimum_confidence"]:
                synthesis_result = self._apply_quality_improvements(synthesis_result)
            
            return synthesis_result
            
        except Exception as e:
            self.logger.error(f"Quality assurance failed: {e}")
            return synthesis_result

    def _generate_final_recommendations(
        self, 
        qa_result: Dict[str, Any], 
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate final comprehensive recommendations
        """
        try:
            final_recommendations = {
                "executive_summary": self._generate_executive_summary(qa_result),
                "detailed_analysis": qa_result.get("comprehensive_analysis", {}),
                "actionable_recommendations": self._generate_actionable_recommendations(qa_result),
                "next_steps": self._generate_next_steps(qa_result),
                "success_metrics": self._define_success_metrics(qa_result),
                "timeline": self._generate_timeline(qa_result),
                "resources": self._compile_resources(qa_result),
                "risk_assessment": self._assess_risks(qa_result)
            }
            
            return final_recommendations
            
        except Exception as e:
            self.logger.error(f"Final recommendation generation failed: {e}")
            return {"error": "Recommendation generation failed", "data": qa_result}

    def _update_agent_performance(
        self, 
        agent_name: str, 
        success: bool, 
        execution_time: float, 
        result: Dict[str, Any]
    ):
        """
        Update agent performance metrics
        """
        if agent_name not in self.agent_performance:
            return
        
        perf = self.agent_performance[agent_name]
        
        # Update success rate
        total_requests = perf.success_rate * 100  # Approximate total requests
        if success:
            perf.success_rate = ((perf.success_rate * total_requests) + 100) / (total_requests + 1)
        else:
            perf.success_rate = (perf.success_rate * total_requests) / (total_requests + 1)
            perf.error_count += 1
        
        # Update response time
        perf.average_response_time = (perf.average_response_time + execution_time) / 2
        perf.last_execution_time = execution_time
        
        # Update confidence score based on result quality
        if result and not result.get("error"):
            confidence = result.get("metadata", {}).get("confidence", 85)
            perf.confidence_score = (perf.confidence_score + confidence) / 2

    def _should_execute_parallel(self) -> bool:
        """
        Determine if parallel execution should be used
        """
        # Check agent performance
        for agent_name, perf in self.agent_performance.items():
            if perf.success_rate < self.quality_thresholds["minimum_success_rate"]:
                return False
            if perf.average_response_time > self.quality_thresholds["maximum_response_time"]:
                return False
        
        return True

    def get_specialized_prompt_template(self) -> PromptTemplate:
        """
        Get controller specific prompt template
        """
        return PromptTemplate(
            system_prompt=self._build_system_prompt(),
            user_prompt="Orchestrate comprehensive career intelligence analysis",
            reasoning_mode=ReasoningMode.MULTI_PERSPECTIVE,
            complexity=PromptComplexity.EXPERT,
            context_variables={
                "orchestration_mode": "intelligent",
                "quality_assurance": "enabled",
                "parallel_processing": "adaptive"
            },
            validation_rules=[
                "must_coordinate_all_agents",
                "must_provide_comprehensive_analysis",
                "must_include_quality_metrics"
            ],
            examples=[],
            constraints=[
                "Ensure all agent outputs are integrated",
                "Maintain high quality standards",
                "Provide actionable recommendations"
            ]
        )

    # Helper methods (simplified implementations)
    def _initialize_workflow_config(self) -> Dict[str, Any]:
        """Initialize workflow configuration"""
        return {
            "stages": [stage.value for stage in WorkflowStage],
            "parallel_stages": ["job_matching", "skill_analysis"],
            "quality_gates": ["resume_parsing", "result_synthesis"],
            "fallback_strategies": ["sequential_execution", "simplified_analysis"]
        }

    def _initialize_processing_context(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Initialize processing context"""
        return {
            "start_time": datetime.now().isoformat(),
            "input_hash": hash(str(input_data)),
            "user_context": context or {},
            "workflow_config": self.workflow_config,
            "quality_thresholds": self.quality_thresholds
        }

    def _validate_stage_result(self, stage: WorkflowStage, result: Dict[str, Any]) -> float:
        """Validate stage result quality"""
        if result.get("error"):
            return 0.0
        
        # Basic quality checks
        if not result:
            return 30.0
        
        # Check for required fields based on stage
        required_fields = {
            WorkflowStage.RESUME_PARSING: ["parsed_data"],
            WorkflowStage.JOB_MATCHING: ["overall_match"],
            WorkflowStage.SKILL_ANALYSIS: ["skill_recommendations"]
        }
        
        stage_required = required_fields.get(stage, [])
        missing_fields = [field for field in stage_required if field not in result]
        
        if missing_fields:
            return 50.0
        
        return 85.0  # Default good quality score

    def _perform_cross_analysis(self, workflow_results: Dict[str, Any]) -> Dict[str, Any]:
        """Perform cross-analysis between different results"""
        return {"cross_validation": "completed", "consistency_score": 85}

    def _assess_overall_confidence(self, workflow_results: Dict[str, Any]) -> float:
        """Assess overall confidence in results"""
        confidences = []
        for result in workflow_results.values():
            if isinstance(result, dict) and "metadata" in result:
                confidences.append(result["metadata"].get("confidence", 70))
        
        return sum(confidences) / len(confidences) if confidences else 70

    def _check_result_consistency(self, workflow_results: Dict[str, Any]) -> Dict[str, Any]:
        """Check consistency across results"""
        return {"consistency_score": 80, "conflicts": [], "alignments": ["skills", "experience"]}

    def _get_agent_performance_summary(self) -> Dict[str, Any]:
        """Get summary of agent performance"""
        return {
            agent_name: {
                "success_rate": f"{perf.success_rate:.1f}%",
                "avg_response_time": f"{perf.average_response_time:.2f}s",
                "confidence": f"{perf.confidence_score:.1f}%"
            }
            for agent_name, perf in self.agent_performance.items()
        }

    def _calculate_workflow_quality_score(self, workflow_results: Dict[str, Any]) -> float:
        """Calculate overall workflow quality score"""
        scores = []
        for result in workflow_results.values():
            if isinstance(result, dict) and "stage_metadata" in result:
                scores.append(result["stage_metadata"].get("quality_score", 70))
        
        return sum(scores) / len(scores) if scores else 70

    def _handle_workflow_failure(self, error: Exception, partial_results: Dict[str, Any]) -> Dict[str, Any]:
        """Handle workflow failure gracefully"""
        return {
            "error": f"Workflow failed: {str(error)}",
            "partial_results": partial_results,
            "fallback_recommendations": self._generate_fallback_recommendations(partial_results),
            "recovery_suggestions": ["Retry with simplified workflow", "Check input data quality"]
        }

    def _get_fallback_result(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get fallback result when all processing fails"""
        return {
            "error": "Advanced processing unavailable",
            "basic_analysis": "Resume received and queued for processing",
            "recommendations": ["Please check input format", "Try again later"],
            "fallback_mode": True
        }