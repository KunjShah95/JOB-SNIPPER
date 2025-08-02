"""
AI-Powered Interview Preparation Module for Job Snipper AI
Generates personalized interview questions and provides practice sessions
"""
import random
import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime
import re

logger = logging.getLogger(__name__)

@dataclass
class InterviewQuestion:
    """Interview question data structure"""
    question: str
    category: str  # technical, behavioral, situational
    difficulty: str  # easy, medium, hard
    expected_answer_points: List[str]
    follow_up_questions: List[str]
    skills_tested: List[str]

@dataclass
class InterviewSession:
    """Interview practice session"""
    session_id: str
    questions: List[InterviewQuestion]
    user_answers: Dict[str, str]
    feedback: Dict[str, Any]
    score: float
    timestamp: datetime

class InterviewPreparation:
    """AI-powered interview preparation system"""
    
    def __init__(self):
        self.question_database = self._load_question_database()
        self.feedback_templates = self._load_feedback_templates()
    
    def _load_question_database(self) -> Dict[str, List[Dict]]:
        """Load comprehensive interview question database"""
        return {
            'technical': {
                'python': [
                    {
                        'question': 'Explain the difference between list and tuple in Python.',
                        'difficulty': 'easy',
                        'expected_points': [
                            'Lists are mutable, tuples are immutable',
                            'Lists use square brackets, tuples use parentheses',
                            'Tuples are faster for iteration',
                            'Lists have more methods available'
                        ],
                        'follow_ups': [
                            'When would you choose a tuple over a list?',
                            'How does memory usage differ between them?'
                        ],
                        'skills': ['python', 'data structures']
                    },
                    {
                        'question': 'What is a decorator in Python and how would you implement one?',
                        'difficulty': 'medium',
                        'expected_points': [
                            'Function that modifies behavior of another function',
                            'Uses @ syntax',
                            'Can be used for logging, timing, authentication',
                            'Returns a wrapper function'
                        ],
                        'follow_ups': [
                            'Can you write a simple timing decorator?',
                            'What are class decorators?'
                        ],
                        'skills': ['python', 'advanced concepts']
                    },
                    {
                        'question': 'Explain the Global Interpreter Lock (GIL) in Python.',
                        'difficulty': 'hard',
                        'expected_points': [
                            'Prevents multiple threads from executing Python code simultaneously',
                            'Affects CPU-bound multithreaded programs',
                            'Not an issue for I/O-bound operations',
                            'Can use multiprocessing as alternative'
                        ],
                        'follow_ups': [
                            'How does this affect performance?',
                            'What are alternatives to overcome GIL limitations?'
                        ],
                        'skills': ['python', 'concurrency', 'performance']
                    }
                ],
                'javascript': [
                    {
                        'question': 'What is the difference between var, let, and const in JavaScript?',
                        'difficulty': 'easy',
                        'expected_points': [
                            'var has function scope, let/const have block scope',
                            'var can be redeclared, let/const cannot',
                            'const cannot be reassigned',
                            'let/const have temporal dead zone'
                        ],
                        'follow_ups': [
                            'What is hoisting?',
                            'When would you use each one?'
                        ],
                        'skills': ['javascript', 'variables', 'scope']
                    },
                    {
                        'question': 'Explain closures in JavaScript with an example.',
                        'difficulty': 'medium',
                        'expected_points': [
                            'Function that has access to outer scope variables',
                            'Variables remain accessible after outer function returns',
                            'Creates private variables',
                            'Common in module patterns'
                        ],
                        'follow_ups': [
                            'What are practical uses of closures?',
                            'How do closures relate to memory leaks?'
                        ],
                        'skills': ['javascript', 'closures', 'scope']
                    }
                ],
                'react': [
                    {
                        'question': 'What is the Virtual DOM and how does it work?',
                        'difficulty': 'medium',
                        'expected_points': [
                            'JavaScript representation of real DOM',
                            'Enables efficient updates through diffing',
                            'Batch updates for better performance',
                            'Reconciliation process'
                        ],
                        'follow_ups': [
                            'What are the benefits over direct DOM manipulation?',
                            'How does React decide what to update?'
                        ],
                        'skills': ['react', 'virtual dom', 'performance']
                    }
                ],
                'databases': [
                    {
                        'question': 'Explain ACID properties in database transactions.',
                        'difficulty': 'medium',
                        'expected_points': [
                            'Atomicity: All or nothing',
                            'Consistency: Valid state transitions',
                            'Isolation: Concurrent transactions don\'t interfere',
                            'Durability: Committed changes persist'
                        ],
                        'follow_ups': [
                            'How do these properties ensure data integrity?',
                            'What happens when ACID properties are violated?'
                        ],
                        'skills': ['databases', 'transactions', 'data integrity']
                    }
                ],
                'algorithms': [
                    {
                        'question': 'Explain the time complexity of common sorting algorithms.',
                        'difficulty': 'medium',
                        'expected_points': [
                            'Bubble Sort: O(n²)',
                            'Quick Sort: O(n log n) average, O(n²) worst',
                            'Merge Sort: O(n log n) always',
                            'Heap Sort: O(n log n)'
                        ],
                        'follow_ups': [
                            'Which sorting algorithm would you choose and why?',
                            'What factors affect algorithm choice?'
                        ],
                        'skills': ['algorithms', 'time complexity', 'sorting']
                    }
                ]
            },
            'behavioral': [
                {
                    'question': 'Tell me about a time when you had to learn a new technology quickly.',
                    'difficulty': 'easy',
                    'expected_points': [
                        'Specific situation and context',
                        'Learning approach and resources used',
                        'Challenges faced and how overcome',
                        'Results and what was learned'
                    ],
                    'follow_ups': [
                        'How do you typically approach learning new technologies?',
                        'What resources do you find most helpful?'
                    ],
                    'skills': ['learning agility', 'adaptability']
                },
                {
                    'question': 'Describe a challenging project you worked on and how you overcame obstacles.',
                    'difficulty': 'medium',
                    'expected_points': [
                        'Project context and your role',
                        'Specific challenges encountered',
                        'Problem-solving approach',
                        'Outcome and lessons learned'
                    ],
                    'follow_ups': [
                        'What would you do differently?',
                        'How did this experience change your approach?'
                    ],
                    'skills': ['problem solving', 'resilience', 'project management']
                },
                {
                    'question': 'How do you handle disagreements with team members?',
                    'difficulty': 'medium',
                    'expected_points': [
                        'Listen to understand different perspectives',
                        'Focus on facts and project goals',
                        'Seek compromise or alternative solutions',
                        'Escalate if necessary'
                    ],
                    'follow_ups': [
                        'Can you give a specific example?',
                        'How do you prevent conflicts from escalating?'
                    ],
                    'skills': ['communication', 'conflict resolution', 'teamwork']
                }
            ],
            'situational': [
                {
                    'question': 'How would you approach debugging a production issue that you can\'t reproduce locally?',
                    'difficulty': 'medium',
                    'expected_points': [
                        'Check logs and monitoring systems',
                        'Gather information about when issue occurs',
                        'Compare production and local environments',
                        'Use debugging tools and techniques',
                        'Implement additional logging if needed'
                    ],
                    'follow_ups': [
                        'What tools would you use for monitoring?',
                        'How would you prevent similar issues?'
                    ],
                    'skills': ['debugging', 'problem solving', 'production support']
                },
                {
                    'question': 'You\'re given a legacy codebase with no documentation. How do you approach understanding it?',
                    'difficulty': 'medium',
                    'expected_points': [
                        'Start with high-level architecture',
                        'Identify entry points and main flows',
                        'Read tests if available',
                        'Use debugging tools to trace execution',
                        'Document findings as you go'
                    ],
                    'follow_ups': [
                        'How would you prioritize what to understand first?',
                        'What would you do to improve the codebase?'
                    ],
                    'skills': ['code analysis', 'documentation', 'reverse engineering']
                }
            ]
        }
    
    def _load_feedback_templates(self) -> Dict[str, List[str]]:
        """Load feedback templates for different answer qualities"""
        return {
            'excellent': [
                "Excellent answer! You covered all key points comprehensively.",
                "Outstanding response with great technical depth.",
                "Perfect! You demonstrated strong understanding and provided concrete examples."
            ],
            'good': [
                "Good answer! You covered most important points.",
                "Solid response, but could be enhanced with more specific examples.",
                "Well done! Consider adding more technical details."
            ],
            'average': [
                "Decent answer, but missing some key points.",
                "You're on the right track, but could elaborate more.",
                "Good start, but needs more depth and examples."
            ],
            'poor': [
                "Your answer needs significant improvement.",
                "Consider reviewing the fundamental concepts.",
                "This answer doesn't demonstrate sufficient understanding."
            ]
        }
    
    def generate_interview_questions(self, skills: List[str], experience_level: str = 'mid', 
                                   num_questions: int = 10) -> List[InterviewQuestion]:
        """
        Generate personalized interview questions based on skills and experience
        
        Args:
            skills: List of technical skills
            experience_level: 'entry', 'mid', 'senior'
            num_questions: Number of questions to generate
            
        Returns:
            List of interview questions
        """
        questions = []
        
        try:
            # Determine difficulty distribution based on experience level
            if experience_level == 'entry':
                difficulty_dist = {'easy': 0.6, 'medium': 0.3, 'hard': 0.1}
            elif experience_level == 'mid':
                difficulty_dist = {'easy': 0.3, 'medium': 0.5, 'hard': 0.2}
            else:  # senior
                difficulty_dist = {'easy': 0.2, 'medium': 0.4, 'hard': 0.4}
            
            # Calculate number of questions per category
            technical_count = max(int(num_questions * 0.6), 1)
            behavioral_count = max(int(num_questions * 0.25), 1)
            situational_count = num_questions - technical_count - behavioral_count
            
            # Generate technical questions based on skills
            tech_questions = self._generate_technical_questions(
                skills, technical_count, difficulty_dist
            )
            questions.extend(tech_questions)
            
            # Generate behavioral questions
            behavioral_questions = self._generate_behavioral_questions(
                behavioral_count, difficulty_dist
            )
            questions.extend(behavioral_questions)
            
            # Generate situational questions
            situational_questions = self._generate_situational_questions(
                situational_count, difficulty_dist
            )
            questions.extend(situational_questions)
            
            # Shuffle questions for variety
            random.shuffle(questions)
            
            return questions[:num_questions]
            
        except Exception as e:
            logger.error(f"❌ Error generating interview questions: {e}")
            return self._get_fallback_questions()
    
    def _generate_technical_questions(self, skills: List[str], count: int, 
                                    difficulty_dist: Dict[str, float]) -> List[InterviewQuestion]:
        """Generate technical questions based on user skills"""
        questions = []
        
        # Map skills to question categories
        skill_mapping = {
            'python': 'python',
            'javascript': 'javascript',
            'react': 'react',
            'sql': 'databases',
            'mysql': 'databases',
            'postgresql': 'databases',
            'algorithms': 'algorithms',
            'data structures': 'algorithms'
        }
        
        available_categories = []
        for skill in skills:
            skill_lower = skill.lower()
            if skill_lower in skill_mapping:
                category = skill_mapping[skill_lower]
                if category in self.question_database['technical']:
                    available_categories.append(category)
        
        # If no matching categories, use general algorithms/databases
        if not available_categories:
            available_categories = ['algorithms', 'databases']
        
        # Generate questions
        for _ in range(count):
            category = random.choice(available_categories)
            category_questions = self.question_database['technical'][category]
            
            # Select difficulty based on distribution
            difficulty = self._select_difficulty(difficulty_dist)
            
            # Filter questions by difficulty
            filtered_questions = [q for q in category_questions if q['difficulty'] == difficulty]
            if not filtered_questions:
                filtered_questions = category_questions  # Fallback to all questions
            
            question_data = random.choice(filtered_questions)
            
            question = InterviewQuestion(
                question=question_data['question'],
                category='technical',
                difficulty=question_data['difficulty'],
                expected_answer_points=question_data['expected_points'],
                follow_up_questions=question_data['follow_ups'],
                skills_tested=question_data['skills']
            )
            
            questions.append(question)
        
        return questions
    
    def _generate_behavioral_questions(self, count: int, 
                                     difficulty_dist: Dict[str, float]) -> List[InterviewQuestion]:
        """Generate behavioral questions"""
        questions = []
        
        behavioral_questions = self.question_database['behavioral']
        
        for _ in range(count):
            question_data = random.choice(behavioral_questions)
            
            question = InterviewQuestion(
                question=question_data['question'],
                category='behavioral',
                difficulty=question_data['difficulty'],
                expected_answer_points=question_data['expected_points'],
                follow_up_questions=question_data['follow_ups'],
                skills_tested=question_data['skills']
            )
            
            questions.append(question)
        
        return questions
    
    def _generate_situational_questions(self, count: int, 
                                      difficulty_dist: Dict[str, float]) -> List[InterviewQuestion]:
        """Generate situational questions"""
        questions = []
        
        situational_questions = self.question_database['situational']
        
        for _ in range(count):
            question_data = random.choice(situational_questions)
            
            question = InterviewQuestion(
                question=question_data['question'],
                category='situational',
                difficulty=question_data['difficulty'],
                expected_answer_points=question_data['expected_points'],
                follow_up_questions=question_data['follow_ups'],
                skills_tested=question_data['skills']
            )
            
            questions.append(question)
        
        return questions
    
    def _select_difficulty(self, difficulty_dist: Dict[str, float]) -> str:
        """Select difficulty level based on distribution"""
        rand = random.random()
        cumulative = 0
        
        for difficulty, prob in difficulty_dist.items():
            cumulative += prob
            if rand <= cumulative:
                return difficulty
        
        return 'medium'  # Fallback
    
    def evaluate_answer(self, question: InterviewQuestion, answer: str) -> Dict[str, Any]:
        """
        Evaluate user's answer to interview question
        
        Args:
            question: The interview question
            answer: User's answer
            
        Returns:
            Evaluation results with score and feedback
        """
        try:
            if not answer or len(answer.strip()) < 10:
                return {
                    'score': 0.0,
                    'feedback': "Answer is too short. Please provide a more detailed response.",
                    'missing_points': question.expected_answer_points,
                    'suggestions': ["Provide specific examples", "Elaborate on your approach"]
                }
            
            answer_lower = answer.lower()
            
            # Check coverage of expected points
            covered_points = []
            missing_points = []
            
            for point in question.expected_answer_points:
                point_keywords = point.lower().split()
                if any(keyword in answer_lower for keyword in point_keywords):
                    covered_points.append(point)
                else:
                    missing_points.append(point)
            
            # Calculate score based on coverage
            coverage_score = len(covered_points) / len(question.expected_answer_points)
            
            # Bonus points for length and structure
            length_bonus = min(len(answer.split()) / 100, 0.2)  # Up to 20% bonus
            
            # Check for examples (STAR method for behavioral questions)
            example_bonus = 0.0
            if question.category == 'behavioral':
                star_keywords = ['situation', 'task', 'action', 'result', 'example', 'when', 'how']
                if any(keyword in answer_lower for keyword in star_keywords):
                    example_bonus = 0.1
            
            final_score = min(coverage_score + length_bonus + example_bonus, 1.0)
            
            # Generate feedback
            feedback = self._generate_feedback(final_score, covered_points, missing_points)
            
            # Generate suggestions
            suggestions = self._generate_suggestions(question, missing_points, final_score)
            
            return {
                'score': final_score,
                'feedback': feedback,
                'covered_points': covered_points,
                'missing_points': missing_points,
                'suggestions': suggestions
            }
            
        except Exception as e:
            logger.error(f"❌ Error evaluating answer: {e}")
            return {
                'score': 0.5,
                'feedback': "Unable to evaluate answer properly.",
                'missing_points': [],
                'suggestions': ["Please try again with a more detailed answer."]
            }
    
    def _generate_feedback(self, score: float, covered_points: List[str], 
                          missing_points: List[str]) -> str:
        """Generate personalized feedback based on answer quality"""
        if score >= 0.8:
            template = random.choice(self.feedback_templates['excellent'])
        elif score >= 0.6:
            template = random.choice(self.feedback_templates['good'])
        elif score >= 0.4:
            template = random.choice(self.feedback_templates['average'])
        else:
            template = random.choice(self.feedback_templates['poor'])
        
        feedback = template
        
        if covered_points:
            feedback += f" You successfully covered: {', '.join(covered_points[:2])}."
        
        if missing_points:
            feedback += f" Consider mentioning: {', '.join(missing_points[:2])}."
        
        return feedback
    
    def _generate_suggestions(self, question: InterviewQuestion, missing_points: List[str], 
                            score: float) -> List[str]:
        """Generate improvement suggestions"""
        suggestions = []
        
        if score < 0.6:
            suggestions.append("Provide more specific details and examples")
        
        if question.category == 'behavioral' and score < 0.7:
            suggestions.append("Use the STAR method (Situation, Task, Action, Result)")
        
        if question.category == 'technical' and score < 0.7:
            suggestions.append("Include code examples or technical details")
        
        if missing_points:
            suggestions.append(f"Address these key points: {', '.join(missing_points[:2])}")
        
        suggestions.append("Practice explaining concepts clearly and concisely")
        
        return suggestions[:3]  # Limit to 3 suggestions
    
    def create_practice_session(self, skills: List[str], experience_level: str = 'mid') -> InterviewSession:
        """Create a complete interview practice session"""
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        questions = self.generate_interview_questions(skills, experience_level, 8)
        
        return InterviewSession(
            session_id=session_id,
            questions=questions,
            user_answers={},
            feedback={},
            score=0.0,
            timestamp=datetime.now()
        )
    
    def _get_fallback_questions(self) -> List[InterviewQuestion]:
        """Get fallback questions when generation fails"""
        fallback_data = [
            {
                'question': 'Tell me about yourself and your technical background.',
                'category': 'general',
                'difficulty': 'easy',
                'expected_points': ['Background summary', 'Technical skills', 'Career goals'],
                'follow_ups': ['What interests you most about this role?'],
                'skills': ['communication']
            },
            {
                'question': 'What is your experience with version control systems?',
                'category': 'technical',
                'difficulty': 'easy',
                'expected_points': ['Git usage', 'Branching strategies', 'Collaboration'],
                'follow_ups': ['How do you handle merge conflicts?'],
                'skills': ['git', 'collaboration']
            }
        ]
        
        return [
            InterviewQuestion(
                question=q['question'],
                category=q['category'],
                difficulty=q['difficulty'],
                expected_answer_points=q['expected_points'],
                follow_up_questions=q['follow_ups'],
                skills_tested=q['skills']
            )
            for q in fallback_data
        ]

# Create global instance
interview_prep = InterviewPreparation()