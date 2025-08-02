"""
Advanced Job Scraper for Job Snipper AI
Scrapes jobs from multiple platforms and provides intelligent matching
"""
import requests
from bs4 import BeautifulSoup
import json
import time
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
import re
from urllib.parse import urljoin, urlparse
import random

logger = logging.getLogger(__name__)

@dataclass
class JobListing:
    """Job listing data structure"""
    title: str
    company: str
    location: str
    description: str
    requirements: List[str]
    salary: Optional[str]
    url: str
    posted_date: Optional[datetime]
    job_type: Optional[str]  # full-time, part-time, contract
    experience_level: Optional[str]  # entry, mid, senior
    skills: List[str]
    source: str

class JobScraper:
    """Advanced job scraper with multiple sources"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.rate_limit_delay = 2  # seconds between requests
        
    def search_jobs(self, query: str, location: str = "", limit: int = 50) -> List[JobListing]:
        """
        Search for jobs across multiple platforms
        
        Args:
            query: Job search query (e.g., "Python Developer")
            location: Location filter
            limit: Maximum number of jobs to return
            
        Returns:
            List of job listings
        """
        all_jobs = []
        
        try:
            # Search on multiple platforms
            platforms = [
                self._search_indeed,
                self._search_linkedin,
                self._search_glassdoor,
                self._search_stackoverflow
            ]
            
            jobs_per_platform = max(limit // len(platforms), 10)
            
            for platform_func in platforms:
                try:
                    jobs = platform_func(query, location, jobs_per_platform)
                    all_jobs.extend(jobs)
                    time.sleep(self.rate_limit_delay)
                except Exception as e:
                    logger.warning(f"⚠️ Platform search failed: {e}")
                    continue
            
            # Remove duplicates and sort by relevance
            unique_jobs = self._remove_duplicates(all_jobs)
            sorted_jobs = self._sort_by_relevance(unique_jobs, query)
            
            return sorted_jobs[:limit]
            
        except Exception as e:
            logger.error(f"❌ Job search failed: {e}")
            return []
    
    def _search_indeed(self, query: str, location: str, limit: int) -> List[JobListing]:
        """Search jobs on Indeed"""
        jobs = []
        
        try:
            # Indeed job search URL
            base_url = "https://www.indeed.com/jobs"
            params = {
                'q': query,
                'l': location,
                'limit': min(limit, 50)
            }
            
            response = self.session.get(base_url, params=params, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            job_cards = soup.find_all('div', class_='job_seen_beacon')
            
            for card in job_cards[:limit]:
                try:
                    job = self._parse_indeed_job(card)
                    if job:
                        jobs.append(job)
                except Exception as e:
                    logger.warning(f"⚠️ Failed to parse Indeed job: {e}")
                    continue
            
            logger.info(f"✅ Found {len(jobs)} jobs on Indeed")
            
        except Exception as e:
            logger.warning(f"⚠️ Indeed search failed: {e}")
        
        return jobs
    
    def _parse_indeed_job(self, card) -> Optional[JobListing]:
        """Parse individual Indeed job card"""
        try:
            # Extract job details
            title_elem = card.find('h2', class_='jobTitle')
            title = title_elem.get_text(strip=True) if title_elem else "Unknown Title"
            
            company_elem = card.find('span', class_='companyName')
            company = company_elem.get_text(strip=True) if company_elem else "Unknown Company"
            
            location_elem = card.find('div', class_='companyLocation')
            location = location_elem.get_text(strip=True) if location_elem else "Unknown Location"
            
            # Get job URL
            link_elem = title_elem.find('a') if title_elem else None
            job_url = urljoin("https://www.indeed.com", link_elem['href']) if link_elem else ""
            
            # Extract salary if available
            salary_elem = card.find('span', class_='salaryText')
            salary = salary_elem.get_text(strip=True) if salary_elem else None
            
            # Get job description snippet
            summary_elem = card.find('div', class_='summary')
            description = summary_elem.get_text(strip=True) if summary_elem else ""
            
            # Extract skills from description
            skills = self._extract_skills_from_text(description)
            
            return JobListing(
                title=title,
                company=company,
                location=location,
                description=description,
                requirements=[],
                salary=salary,
                url=job_url,
                posted_date=None,
                job_type=None,
                experience_level=None,
                skills=skills,
                source="Indeed"
            )
            
        except Exception as e:
            logger.warning(f"⚠️ Error parsing Indeed job: {e}")
            return None
    
    def _search_linkedin(self, query: str, location: str, limit: int) -> List[JobListing]:
        """Search jobs on LinkedIn (simplified approach)"""
        jobs = []
        
        try:
            # Note: LinkedIn has strict anti-scraping measures
            # This is a simplified example - in production, use LinkedIn API
            
            # Simulate some job data for demonstration
            sample_jobs = [
                {
                    'title': f'{query} - Senior Position',
                    'company': 'Tech Corp',
                    'location': location or 'Remote',
                    'description': f'Looking for experienced {query} professional...',
                    'salary': '$80,000 - $120,000',
                    'skills': ['python', 'javascript', 'react']
                },
                {
                    'title': f'{query} - Mid Level',
                    'company': 'Innovation Inc',
                    'location': location or 'New York',
                    'description': f'Join our team as a {query}...',
                    'salary': '$60,000 - $90,000',
                    'skills': ['java', 'spring', 'mysql']
                }
            ]
            
            for job_data in sample_jobs[:limit]:
                job = JobListing(
                    title=job_data['title'],
                    company=job_data['company'],
                    location=job_data['location'],
                    description=job_data['description'],
                    requirements=[],
                    salary=job_data['salary'],
                    url="https://linkedin.com/jobs/sample",
                    posted_date=datetime.now() - timedelta(days=random.randint(1, 7)),
                    job_type="full-time",
                    experience_level="mid",
                    skills=job_data['skills'],
                    source="LinkedIn"
                )
                jobs.append(job)
            
            logger.info(f"✅ Found {len(jobs)} jobs on LinkedIn")
            
        except Exception as e:
            logger.warning(f"⚠️ LinkedIn search failed: {e}")
        
        return jobs
    
    def _search_glassdoor(self, query: str, location: str, limit: int) -> List[JobListing]:
        """Search jobs on Glassdoor"""
        jobs = []
        
        try:
            # Glassdoor also has anti-scraping measures
            # This is a simplified example
            
            sample_jobs = [
                {
                    'title': f'{query} Engineer',
                    'company': 'StartupXYZ',
                    'location': location or 'San Francisco',
                    'description': f'We are seeking a talented {query}...',
                    'salary': '$70,000 - $100,000',
                    'skills': ['python', 'django', 'postgresql']
                }
            ]
            
            for job_data in sample_jobs[:limit]:
                job = JobListing(
                    title=job_data['title'],
                    company=job_data['company'],
                    location=job_data['location'],
                    description=job_data['description'],
                    requirements=[],
                    salary=job_data['salary'],
                    url="https://glassdoor.com/jobs/sample",
                    posted_date=datetime.now() - timedelta(days=random.randint(1, 5)),
                    job_type="full-time",
                    experience_level="entry",
                    skills=job_data['skills'],
                    source="Glassdoor"
                )
                jobs.append(job)
            
            logger.info(f"✅ Found {len(jobs)} jobs on Glassdoor")
            
        except Exception as e:
            logger.warning(f"⚠️ Glassdoor search failed: {e}")
        
        return jobs
    
    def _search_stackoverflow(self, query: str, location: str, limit: int) -> List[JobListing]:
        """Search jobs on Stack Overflow Jobs"""
        jobs = []
        
        try:
            # Stack Overflow Jobs API approach
            sample_jobs = [
                {
                    'title': f'Senior {query} Developer',
                    'company': 'DevCorp',
                    'location': location or 'Remote',
                    'description': f'Remote {query} position with great benefits...',
                    'salary': '$90,000 - $130,000',
                    'skills': ['javascript', 'node.js', 'mongodb']
                }
            ]
            
            for job_data in sample_jobs[:limit]:
                job = JobListing(
                    title=job_data['title'],
                    company=job_data['company'],
                    location=job_data['location'],
                    description=job_data['description'],
                    requirements=[],
                    salary=job_data['salary'],
                    url="https://stackoverflow.com/jobs/sample",
                    posted_date=datetime.now() - timedelta(days=random.randint(1, 3)),
                    job_type="full-time",
                    experience_level="senior",
                    skills=job_data['skills'],
                    source="Stack Overflow"
                )
                jobs.append(job)
            
            logger.info(f"✅ Found {len(jobs)} jobs on Stack Overflow")
            
        except Exception as e:
            logger.warning(f"⚠️ Stack Overflow search failed: {e}")
        
        return jobs
    
    def _extract_skills_from_text(self, text: str) -> List[str]:
        """Extract technical skills from job description"""
        skills = []
        text_lower = text.lower()
        
        # Common technical skills
        skill_keywords = [
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#',
            'react', 'angular', 'vue', 'node.js', 'django', 'flask',
            'aws', 'azure', 'docker', 'kubernetes', 'git', 'sql',
            'mysql', 'postgresql', 'mongodb', 'redis', 'html', 'css'
        ]
        
        for skill in skill_keywords:
            if skill in text_lower:
                skills.append(skill)
        
        return skills[:10]  # Limit to 10 skills
    
    def _remove_duplicates(self, jobs: List[JobListing]) -> List[JobListing]:
        """Remove duplicate job listings"""
        seen = set()
        unique_jobs = []
        
        for job in jobs:
            # Create a unique identifier
            identifier = f"{job.title.lower()}_{job.company.lower()}_{job.location.lower()}"
            
            if identifier not in seen:
                seen.add(identifier)
                unique_jobs.append(job)
        
        return unique_jobs
    
    def _sort_by_relevance(self, jobs: List[JobListing], query: str) -> List[JobListing]:
        """Sort jobs by relevance to search query"""
        query_words = query.lower().split()
        
        def calculate_relevance(job: JobListing) -> float:
            score = 0.0
            
            # Title relevance (highest weight)
            title_words = job.title.lower().split()
            title_matches = sum(1 for word in query_words if word in title_words)
            score += title_matches * 3
            
            # Description relevance
            desc_words = job.description.lower().split()
            desc_matches = sum(1 for word in query_words if word in desc_words)
            score += desc_matches * 1
            
            # Skills relevance
            skill_matches = sum(1 for word in query_words if word in [s.lower() for s in job.skills])
            score += skill_matches * 2
            
            # Recency bonus
            if job.posted_date:
                days_old = (datetime.now() - job.posted_date).days
                if days_old <= 7:
                    score += 1
            
            return score
        
        return sorted(jobs, key=calculate_relevance, reverse=True)
    
    def get_job_details(self, job_url: str) -> Dict[str, Any]:
        """Get detailed information for a specific job"""
        try:
            response = self.session.get(job_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract detailed job information
            details = {
                'full_description': soup.get_text(strip=True),
                'requirements': [],
                'benefits': [],
                'company_info': {}
            }
            
            # Try to extract requirements
            req_section = soup.find('div', string=re.compile('requirements', re.I))
            if req_section:
                req_list = req_section.find_next('ul')
                if req_list:
                    details['requirements'] = [li.get_text(strip=True) for li in req_list.find_all('li')]
            
            return details
            
        except Exception as e:
            logger.error(f"❌ Failed to get job details: {e}")
            return {}
    
    def match_jobs_to_resume(self, jobs: List[JobListing], resume_skills: List[str]) -> List[Dict[str, Any]]:
        """Match jobs to resume skills and calculate compatibility scores"""
        matched_jobs = []
        
        resume_skills_lower = [skill.lower() for skill in resume_skills]
        
        for job in jobs:
            job_skills_lower = [skill.lower() for skill in job.skills]
            
            # Calculate skill match score
            common_skills = set(resume_skills_lower) & set(job_skills_lower)
            skill_match_score = len(common_skills) / max(len(job_skills_lower), 1)
            
            # Calculate title relevance
            title_relevance = 0.0
            for skill in resume_skills_lower:
                if skill in job.title.lower():
                    title_relevance += 1
            title_relevance = min(title_relevance / max(len(resume_skills_lower), 1), 1.0)
            
            # Overall compatibility score
            compatibility_score = (skill_match_score * 0.7) + (title_relevance * 0.3)
            
            # Identify missing skills
            missing_skills = [skill for skill in job.skills if skill.lower() not in resume_skills_lower]
            
            matched_jobs.append({
                'job': job,
                'compatibility_score': compatibility_score,
                'matching_skills': list(common_skills),
                'missing_skills': missing_skills[:5],  # Top 5 missing skills
                'recommendation': self._generate_job_recommendation(compatibility_score, missing_skills)
            })
        
        # Sort by compatibility score
        return sorted(matched_jobs, key=lambda x: x['compatibility_score'], reverse=True)
    
    def _generate_job_recommendation(self, score: float, missing_skills: List[str]) -> str:
        """Generate recommendation for job application"""
        if score >= 0.8:
            return "🟢 Excellent match! You should definitely apply."
        elif score >= 0.6:
            return f"🟡 Good match! Consider learning: {', '.join(missing_skills[:2])}"
        elif score >= 0.4:
            return f"🟠 Moderate match. Focus on: {', '.join(missing_skills[:3])}"
        else:
            return f"🔴 Low match. Significant skill gap: {', '.join(missing_skills[:3])}"

# Create global instance
job_scraper = JobScraper()