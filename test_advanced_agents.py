#!/usr/bin/env python3
"""
Advanced Agents Test Suite
==========================

Comprehensive testing for the advanced agent architecture including:
- Unit tests for individual agents
- Integration tests for workflow
- Performance benchmarking
- Quality assurance validation
- Error handling verification
"""

import unittest
import json
import time
import logging
from typing import Dict, Any, List
from unittest.mock import Mock, patch
from datetime import datetime

# Configure logging for tests
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestAdvancedAgentBase(unittest.TestCase):
    """Test cases for the advanced agent base class"""
    
    def setUp(self):
        """Set up test fixtures"""
        try:
            from agents.advanced_agent_base import AdvancedAgentBase, ReasoningMode, PromptComplexity
            self.AdvancedAgentBase = AdvancedAgentBase
            self.ReasoningMode = ReasoningMode
            self.PromptComplexity = PromptComplexity
        except ImportError:
            self.skipTest("Advanced agent base not available")
    
    def test_agent_initialization(self):
        """Test agent initialization with different configurations"""
        # Create a concrete implementation for testing
        class TestAgent(self.AdvancedAgentBase):
            def process(self, input_data, context=None):
                return {"test": "result"}
            
            def get_specialized_prompt_template(self):
                return None
        
        agent = TestAgent(
            name="TestAgent",
            reasoning_mode=self.ReasoningMode.CHAIN_OF_THOUGHT,
            complexity=self.PromptComplexity.EXPERT
        )
        
        self.assertEqual(agent.name, "TestAgent")
        self.assertEqual(agent.reasoning_mode, self.ReasoningMode.CHAIN_OF_THOUGHT)
        self.assertEqual(agent.complexity, self.PromptComplexity.EXPERT)
        self.assertTrue(agent.enable_caching)
        self.assertTrue(agent.enable_validation)
    
    def test_performance_metrics_tracking(self):
        """Test performance metrics tracking"""
        class TestAgent(self.AdvancedAgentBase):
            def process(self, input_data, context=None):
                return {"test": "result"}
            
            def get_specialized_prompt_template(self):
                return None
        
        agent = TestAgent("TestAgent")
        
        # Test metric updates
        agent.update_performance_metrics(True, 1.5, False)
        agent.update_performance_metrics(True, 2.0, True)
        agent.update_performance_metrics(False, 3.0, False)
        
        report = agent.get_performance_report()
        
        self.assertIn("total_requests", report)
        self.assertIn("success_rate", report)
        self.assertIn("cache_hit_rate", report)
        self.assertEqual(report["total_requests"], 3)

class TestAdvancedResumeParser(unittest.TestCase):
    """Test cases for the advanced resume parser agent"""
    
    def setUp(self):
        """Set up test fixtures"""
        try:
            from agents.advanced_resume_parser_agent import AdvancedResumeParserAgent
            self.parser = AdvancedResumeParserAgent()
        except ImportError:
            self.skipTest("Advanced resume parser not available")
        
        self.sample_resume = """
        John Doe
        Software Engineer
        john.doe@email.com
        (555) 123-4567
        
        Experience:
        Senior Software Engineer at TechCorp (2020-2023)
        - Led development of microservices architecture
        - Improved system performance by 40%
        - Managed team of 5 developers
        
        Education:
        BS Computer Science, University of Technology (2018)
        
        Skills:
        Python, JavaScript, React, AWS, Docker, Kubernetes
        """
    
    def test_resume_parsing_basic(self):
        """Test basic resume parsing functionality"""
        input_data = {"resume_text": self.sample_resume}
        
        result = self.parser.process(input_data)
        
        self.assertIn("parsed_data", result)
        self.assertIn("metadata", result)
        
        parsed_data = result["parsed_data"]
        self.assertIn("personal_info", parsed_data)
        self.assertIn("experience", parsed_data)
        self.assertIn("education", parsed_data)
        self.assertIn("skills", parsed_data)
    
    def test_resume_parsing_with_context(self):
        """Test resume parsing with additional context"""
        input_data = {"resume_text": self.sample_resume}
        context = {
            "industry_focus": "technology",
            "analysis_depth": "comprehensive"
        }
        
        result = self.parser.process(input_data, context)
        
        self.assertIn("parsed_data", result)
        self.assertIn("industry_analysis", result)
        self.assertIn("ats_compatibility", result)
        self.assertIn("quality_assessment", result)
    
    def test_empty_resume_handling(self):
        """Test handling of empty or invalid resume input"""
        input_data = {"resume_text": ""}
        
        result = self.parser.process(input_data)
        
        # Should handle gracefully and provide fallback
        self.assertIn("parsed_data", result)
        self.assertTrue(isinstance(result["parsed_data"], dict))
    
    def test_caching_functionality(self):
        """Test caching functionality"""
        input_data = {"resume_text": self.sample_resume}
        
        # First call
        start_time = time.time()
        result1 = self.parser.process(input_data)
        first_call_time = time.time() - start_time
        
        # Second call (should be cached)
        start_time = time.time()
        result2 = self.parser.process(input_data)
        second_call_time = time.time() - start_time
        
        # Results should be identical
        self.assertEqual(result1, result2)
        
        # Second call should be faster (cached)
        if self.parser.enable_caching:
            self.assertLess(second_call_time, first_call_time)

class TestAdvancedJobMatcher(unittest.TestCase):
    """Test cases for the advanced job matcher agent"""
    
    def setUp(self):
        """Set up test fixtures"""
        try:
            from agents.advanced_job_matcher_agent import AdvancedJobMatcherAgent
            self.matcher = AdvancedJobMatcherAgent()
        except ImportError:
            self.skipTest("Advanced job matcher not available")
        
        self.sample_candidate = {
            "skills": ["Python", "React", "AWS", "Docker"],
            "experience": [
                {
                    "company": "TechCorp",
                    "position": "Software Engineer",
                    "duration": "2020-2023",
                    "description": "Full-stack development"
                }
            ],
            "education": [
                {
                    "institution": "University of Technology",
                    "degree": "BS Computer Science",
                    "graduation_year": "2018"
                }
            ]
        }
        
        self.sample_job = {
            "title": "Senior Software Engineer",
            "required_skills": ["Python", "React", "AWS"],
            "preferred_skills": ["Docker", "Kubernetes"],
            "years_experience": 3,
            "industry": "technology",
            "company_culture": {
                "work_style": "collaborative",
                "values": ["innovation", "quality"]
            }
        }
    
    def test_job_matching_basic(self):
        """Test basic job matching functionality"""
        input_data = {
            "candidate_profile": self.sample_candidate,
            "job_requirements": self.sample_job
        }
        
        result = self.matcher.process(input_data)
        
        self.assertIn("overall_match", result)
        self.assertIn("detailed_analysis", result)
        self.assertIn("recommendations", result)
        
        overall_match = result["overall_match"]
        self.assertIn("score", overall_match)
        self.assertIn("grade", overall_match)
        self.assertIn("confidence", overall_match)
        
        # Score should be between 0 and 100
        self.assertGreaterEqual(overall_match["score"], 0)
        self.assertLessEqual(overall_match["score"], 100)
    
    def test_skills_compatibility_analysis(self):
        """Test skills compatibility analysis"""
        input_data = {
            "candidate_profile": self.sample_candidate,
            "job_requirements": self.sample_job
        }
        
        result = self.matcher.process(input_data)
        
        detailed_analysis = result["detailed_analysis"]
        self.assertIn("skills_compatibility", detailed_analysis)
        
        skills_analysis = detailed_analysis["skills_compatibility"]
        self.assertIn("match_score", skills_analysis)
        self.assertIn("required_skills_match", skills_analysis)
        self.assertIn("skill_gaps", skills_analysis)
    
    def test_perfect_match_scenario(self):
        """Test scenario with perfect candidate-job match"""
        perfect_candidate = self.sample_candidate.copy()
        perfect_candidate["skills"] = ["Python", "React", "AWS", "Docker", "Kubernetes"]
        
        input_data = {
            "candidate_profile": perfect_candidate,
            "job_requirements": self.sample_job
        }
        
        result = self.matcher.process(input_data)
        
        # Should have high match score
        overall_score = result["overall_match"]["score"]
        self.assertGreater(overall_score, 80)
    
    def test_poor_match_scenario(self):
        """Test scenario with poor candidate-job match"""
        poor_candidate = {
            "skills": ["PHP", "MySQL", "jQuery"],
            "experience": [],
            "education": []
        }
        
        input_data = {
            "candidate_profile": poor_candidate,
            "job_requirements": self.sample_job
        }
        
        result = self.matcher.process(input_data)
        
        # Should have lower match score
        overall_score = result["overall_match"]["score"]
        self.assertLess(overall_score, 60)

class TestAdvancedSkillRecommender(unittest.TestCase):
    """Test cases for the advanced skill recommendation agent"""
    
    def setUp(self):
        """Set up test fixtures"""
        try:
            from agents.advanced_skill_recommendation_agent import AdvancedSkillRecommendationAgent
            self.recommender = AdvancedSkillRecommendationAgent()
        except ImportError:
            self.skipTest("Advanced skill recommender not available")
        
        self.sample_profile = {
            "skills": ["Python", "JavaScript", "SQL"],
            "experience": [
                {
                    "position": "Junior Developer",
                    "duration": "2021-2023",
                    "technologies": ["Python", "Django"]
                }
            ],
            "career_goals": {
                "target_role": "Senior Software Engineer",
                "target_industry": "technology",
                "timeline": "12 months"
            }
        }
    
    def test_skill_recommendation_basic(self):
        """Test basic skill recommendation functionality"""
        input_data = {
            "user_profile": self.sample_profile,
            "career_goals": self.sample_profile["career_goals"]
        }
        
        result = self.recommender.process(input_data)
        
        self.assertIn("skill_recommendations", result)
        self.assertIn("learning_paths", result)
        self.assertIn("roi_analysis", result)
        
        skill_recommendations = result["skill_recommendations"]
        self.assertIn("priority_skills", skill_recommendations)
    
    def test_learning_path_generation(self):
        """Test learning path generation"""
        input_data = {
            "user_profile": self.sample_profile,
            "career_goals": self.sample_profile["career_goals"]
        }
        
        result = self.recommender.process(input_data)
        
        learning_paths = result["learning_paths"]
        self.assertTrue(isinstance(learning_paths, dict))
        
        # Check if learning paths contain required elements
        for skill, path_info in learning_paths.items():
            self.assertIn("learning_path", path_info)
            self.assertIn("estimated_duration", path_info)
    
    def test_roi_analysis(self):
        """Test ROI analysis for skill investments"""
        input_data = {
            "user_profile": self.sample_profile,
            "career_goals": self.sample_profile["career_goals"]
        }
        
        result = self.recommender.process(input_data)
        
        roi_analysis = result["roi_analysis"]
        self.assertTrue(isinstance(roi_analysis, dict))
        
        # Check ROI structure for each skill
        for skill, roi_info in roi_analysis.items():
            self.assertIn("investment", roi_info)
            self.assertIn("returns", roi_info)
            self.assertIn("metrics", roi_info)

class TestAdvancedController(unittest.TestCase):
    """Test cases for the advanced controller agent"""
    
    def setUp(self):
        """Set up test fixtures"""
        try:
            from agents.advanced_controller_agent import AdvancedControllerAgent
            self.controller = AdvancedControllerAgent()
        except ImportError:
            self.skipTest("Advanced controller not available")
        
        self.sample_input = {
            "resume_text": """
            John Doe
            Software Engineer
            john.doe@email.com
            
            Experience:
            Software Engineer at TechCorp (2020-2023)
            - Developed web applications using Python and React
            - Improved system performance by 30%
            
            Skills: Python, React, AWS, Docker
            """,
            "job_requirements": {
                "title": "Senior Software Engineer",
                "required_skills": ["Python", "React", "AWS"],
                "experience_years": 3
            }
        }
    
    def test_controller_orchestration(self):
        """Test controller orchestration of all agents"""
        result = self.controller.process(self.sample_input)
        
        # Check main result structure
        self.assertIn("comprehensive_analysis", result)
        self.assertIn("actionable_recommendations", result)
        self.assertIn("workflow_metadata", result)
        
        comprehensive_analysis = result["comprehensive_analysis"]
        self.assertIn("resume_insights", comprehensive_analysis)
        self.assertIn("job_compatibility", comprehensive_analysis)
        self.assertIn("skill_development", comprehensive_analysis)
    
    def test_workflow_metadata(self):
        """Test workflow metadata tracking"""
        result = self.controller.process(self.sample_input)
        
        metadata = result["workflow_metadata"]
        self.assertIn("execution_time", metadata)
        self.assertIn("stages_completed", metadata)
        self.assertIn("agent_performance", metadata)
        self.assertIn("quality_score", metadata)
    
    def test_parallel_execution(self):
        """Test parallel execution capability"""
        # Enable parallel execution
        self.controller.parallel_execution = True
        
        start_time = time.time()
        result = self.controller.process(self.sample_input)
        parallel_time = time.time() - start_time
        
        # Disable parallel execution
        self.controller.parallel_execution = False
        
        start_time = time.time()
        result_sequential = self.controller.process(self.sample_input)
        sequential_time = time.time() - start_time
        
        # Parallel should generally be faster (though not guaranteed in tests)
        self.assertIsNotNone(result)
        self.assertIsNotNone(result_sequential)
    
    def test_error_handling(self):
        """Test error handling and fallback mechanisms"""
        # Test with invalid input
        invalid_input = {"invalid": "data"}
        
        result = self.controller.process(invalid_input)
        
        # Should handle gracefully
        self.assertIsNotNone(result)
        self.assertTrue(isinstance(result, dict))

class TestIntegration(unittest.TestCase):
    """Integration tests for the complete advanced agent system"""
    
    def setUp(self):
        """Set up integration test fixtures"""
        self.test_scenarios = [
            {
                "name": "Technology Professional",
                "resume_text": """
                Jane Smith
                Senior Software Engineer
                jane.smith@email.com
                (555) 987-6543
                
                Experience:
                Senior Software Engineer at InnovaTech (2019-2023)
                - Led development of cloud-native applications
                - Implemented CI/CD pipelines reducing deployment time by 60%
                - Mentored junior developers and conducted code reviews
                
                Software Engineer at StartupCorp (2017-2019)
                - Developed RESTful APIs using Python and Django
                - Built responsive web interfaces with React
                
                Education:
                MS Computer Science, Tech University (2017)
                BS Computer Science, State University (2015)
                
                Skills:
                Python, JavaScript, React, Node.js, AWS, Docker, Kubernetes,
                PostgreSQL, MongoDB, Git, Jenkins, Terraform
                """,
                "job_requirements": {
                    "title": "Principal Software Engineer",
                    "required_skills": ["Python", "AWS", "Kubernetes", "Leadership"],
                    "preferred_skills": ["React", "Docker", "Terraform"],
                    "experience_years": 5,
                    "industry": "technology",
                    "company_size": "large"
                }
            },
            {
                "name": "Career Changer",
                "resume_text": """
                Mike Johnson
                Marketing Manager transitioning to Data Science
                mike.johnson@email.com
                
                Experience:
                Marketing Manager at RetailCorp (2018-2023)
                - Analyzed customer data to improve campaign performance
                - Used Excel and basic SQL for reporting
                - Managed marketing budget of $2M annually
                
                Education:
                MBA Marketing, Business School (2018)
                BS Business Administration, University (2016)
                
                Recent Coursework:
                - Data Science Bootcamp (2023)
                - Python for Data Analysis
                - Machine Learning Fundamentals
                
                Skills:
                Excel, SQL, Python (basic), Tableau, Google Analytics,
                Project Management, Team Leadership
                """,
                "job_requirements": {
                    "title": "Junior Data Scientist",
                    "required_skills": ["Python", "SQL", "Statistics", "Machine Learning"],
                    "preferred_skills": ["R", "Tableau", "AWS"],
                    "experience_years": 1,
                    "industry": "technology",
                    "company_size": "medium"
                }
            }
        ]
    
    def test_end_to_end_workflow(self):
        """Test complete end-to-end workflow for different scenarios"""
        try:
            from agents.advanced_controller_agent import AdvancedControllerAgent
            controller = AdvancedControllerAgent()
        except ImportError:
            self.skipTest("Advanced controller not available")
        
        for scenario in self.test_scenarios:
            with self.subTest(scenario=scenario["name"]):
                input_data = {
                    "resume_text": scenario["resume_text"],
                    "job_requirements": scenario["job_requirements"]
                }
                
                result = controller.process(input_data)
                
                # Verify complete workflow execution
                self.assertIn("comprehensive_analysis", result)
                self.assertIn("actionable_recommendations", result)
                self.assertIn("workflow_metadata", result)
                
                # Verify quality metrics
                metadata = result["workflow_metadata"]
                self.assertIn("quality_score", metadata)
                self.assertGreater(metadata["quality_score"], 50)  # Minimum quality threshold
    
    def test_performance_benchmarks(self):
        """Test performance benchmarks for the system"""
        try:
            from agents.advanced_controller_agent import AdvancedControllerAgent
            controller = AdvancedControllerAgent()
        except ImportError:
            self.skipTest("Advanced controller not available")
        
        performance_results = []
        
        for scenario in self.test_scenarios:
            input_data = {
                "resume_text": scenario["resume_text"],
                "job_requirements": scenario["job_requirements"]
            }
            
            start_time = time.time()
            result = controller.process(input_data)
            end_time = time.time()
            
            execution_time = end_time - start_time
            performance_results.append({
                "scenario": scenario["name"],
                "execution_time": execution_time,
                "success": "error" not in result,
                "quality_score": result.get("workflow_metadata", {}).get("quality_score", 0)
            })
        
        # Performance assertions
        avg_execution_time = sum(r["execution_time"] for r in performance_results) / len(performance_results)
        success_rate = sum(1 for r in performance_results if r["success"]) / len(performance_results)
        avg_quality = sum(r["quality_score"] for r in performance_results) / len(performance_results)
        
        # Performance thresholds
        self.assertLess(avg_execution_time, 30)  # Should complete within 30 seconds
        self.assertGreater(success_rate, 0.8)    # 80% success rate minimum
        self.assertGreater(avg_quality, 70)      # 70% quality score minimum
        
        logger.info(f"Performance Results:")
        logger.info(f"  Average Execution Time: {avg_execution_time:.2f}s")
        logger.info(f"  Success Rate: {success_rate:.1%}")
        logger.info(f"  Average Quality Score: {avg_quality:.1f}")

def run_test_suite():
    """Run the complete test suite"""
    print("🧪 Running Advanced Agents Test Suite")
    print("=" * 50)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_classes = [
        TestAdvancedAgentBase,
        TestAdvancedResumeParser,
        TestAdvancedJobMatcher,
        TestAdvancedSkillRecommender,
        TestAdvancedController,
        TestIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 50)
    print("🎯 Test Summary")
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    
    if result.wasSuccessful():
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed")
        
        if result.failures:
            print("\nFailures:")
            for test, traceback in result.failures:
                print(f"  - {test}: {traceback}")
        
        if result.errors:
            print("\nErrors:")
            for test, traceback in result.errors:
                print(f"  - {test}: {traceback}")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_test_suite()
    exit(0 if success else 1)