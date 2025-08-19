import requests
import logging
from typing import Dict, List, Optional
from agents.multi_ai_base import MultiAIAgent


class WebScraperAgent(MultiAIAgent):
    """Advanced web scraping agent using Firecrawl for job and company research"""  # noqa: SPELL001
    
    def __init__(self, firecrawl_api_key: str = None):  # noqa: SPELL001
        super().__init__(
            name="WebScraperAgent",
            use_gemini=True,
            use_mistral=True,
            return_mode="compare"
        )
        self.firecrawl_api_key = firecrawl_api_key or "your-firecrawl-api-key"  # noqa: SPELL001
        self.base_url = "https://api.firecrawl.dev/v0"
        
    def scrape_job_posting(self, job_url: str) -> Dict:
        """Scrape detailed job posting information"""
        try:
            # Use Firecrawl to scrape the job posting  # noqa: SPELL001
            scraped_data = self._firecrawl_scrape(job_url)  # noqa: SPELL001
            
            if scraped_data:
                # Extract job details using AI
                job_details = self._extract_job_details(scraped_data)
                return {
                    "success": True,
                    "job_details": job_details,
                    "raw_content": scraped_data.get("content", ""),
                    "metadata": scraped_data.get("metadata", {})
                }
            else:
                return self._fallback_job_scraping(job_url)
                
        except Exception as e:
            logging.error(f"Error scraping job posting: {e}")
            return self._fallback_job_scraping(job_url)
    
    def scrape_company_info(self, company_name: str, company_url: str = None) -> Dict:
        """Scrape comprehensive company information"""
        try:
            company_data = {}
            
            # Scrape company website if URL provided
            if company_url:
                website_data = self._firecrawl_scrape(company_url)  # noqa: SPELL001
                company_data["website"] = website_data
            
            # Search for company information across multiple sources
            search_results = self._search_company_info(company_name)
            company_data["search_results"] = search_results
            
            # Extract and analyze company insights
            company_insights = self._analyze_company_data(company_data, company_name)
            
            return {
                "success": True,
                "company_name": company_name,
                "insights": company_insights,
                "raw_data": company_data
            }
            
        except Exception as e:
            logging.error(f"Error scraping company info: {e}")
            return self._fallback_company_info(company_name)
    
    def scrape_salary_data(self, job_title: str, location: str = "United States") -> Dict:
        """Scrape salary information from multiple sources"""
        try:
            salary_sources = [
                f"https://www.glassdoor.com/Salaries/{job_title.replace(' ', '-').lower()}-salary-SRCH_KO0,{len(job_title)}.htm",  # noqa: SPELL001
                f"https://www.indeed.com/career/salaries?q={job_title.replace(' ', '+')}&l={location.replace(' ', '+')}",
                f"https://www.payscale.com/research/US/Job={job_title.replace(' ', '_')}/Salary"
            ]
            
            salary_data = []
            for url in salary_sources:
                try:
                    scraped = self._firecrawl_scrape(url)  # noqa: SPELL001
                    if scraped:
                        salary_info = self._extract_salary_info(scraped, job_title)
                        salary_data.append(salary_info)
                except Exception:
                    continue
            
            # Analyze and consolidate salary data
            consolidated_salary = self._consolidate_salary_data(salary_data, job_title, location)
            
            return {
                "success": True,
                "job_title": job_title,
                "location": location,
                "salary_analysis": consolidated_salary,
                "sources": len(salary_data)
            }
            
        except Exception as e:
            logging.error(f"Error scraping salary data: {e}")
            return self._fallback_salary_data(job_title, location)
    
    def scrape_interview_questions(self, company_name: str, job_title: str) -> Dict:
        """Scrape interview questions from Glassdoor and other sources"""  # noqa: SPELL001
        try:
            # Search for interview experiences
            search_queries = [
                f"{company_name} {job_title} interview questions",
                f"{company_name} interview experience",
                f"{job_title} interview questions"
            ]
            
            interview_data = []
            for query in search_queries:
                search_results = self._search_interview_content(query)
                interview_data.extend(search_results)
            
            # Extract and categorize questions
            categorized_questions = self._categorize_interview_questions(interview_data)
            
            return {
                "success": True,
                "company": company_name,
                "role": job_title,
                "questions": categorized_questions,
                "sources_found": len(interview_data)
            }
            
        except Exception as e:
            logging.error(f"Error scraping interview questions: {e}")
            return self._fallback_interview_questions(company_name, job_title)
    
    def _firecrawl_scrape(self, url: str) -> Optional[Dict]:  # noqa: SPELL001
        """Core Firecrawl scraping function"""  # noqa: SPELL001
        try:
            headers = {
                "Authorization": f"Bearer {self.firecrawl_api_key}",  # noqa: SPELL001
                "Content-Type": "application/json"
            }
            
            payload = {
                "url": url,
                "formats": ["markdown", "html"],
                "includeTags": ["title", "meta", "h1", "h2", "h3", "p", "div", "span"],
                "excludeTags": ["script", "style", "nav", "footer"],
                "waitFor": 3000,
                "timeout": 30000
            }
            
            response = requests.post(
                f"{self.base_url}/scrape",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logging.warning(f"Firecrawl API error: {response.status_code}")  # noqa: SPELL001
                return None
                
        except Exception as e:
            logging.error(f"Firecrawl scraping error: {e}")  # noqa: SPELL001
            return None
    
    def _extract_job_details(self, scraped_data: Dict) -> Dict:
        """Extract structured job details using AI"""
        content = scraped_data.get("content", "")
        
        prompt = f"""
        Extract structured job information from this scraped content:
        
        {content[:3000]}
        
        Extract and return in JSON format:
        {{
            "job_title": "",
            "company": "",
            "location": "",
            "salary_range": "",
            "employment_type": "",
            "experience_level": "",
            "required_skills": [],
            "preferred_skills": [],
            "responsibilities": [],
            "qualifications": [],
            "benefits": [],
            "application_deadline": "",
            "remote_options": "",
            "company_size": "",
            "industry": ""
        }}
        """
        
        try:
            ai_response = self.generate_ai_response(prompt)
            # Parse JSON response
            import json
            return json.loads(ai_response)
        except Exception:
            return self._fallback_job_details()
    
    def _search_company_info(self, company_name: str) -> List[Dict]:
        """Search for company information across multiple sources"""
        search_urls = [
            f"https://www.crunchbase.com/organization/{company_name.lower().replace(' ', '-')}",
            f"https://www.linkedin.com/company/{company_name.lower().replace(' ', '-')}",
            f"https://en.wikipedia.org/wiki/{company_name.replace(' ', '_')}"
        ]
        
        results = []
        for url in search_urls:
            try:
                scraped = self._firecrawl_scrape(url)  # noqa: SPELL001
                if scraped:
                    results.append({
                        "source": url,
                        "content": scraped.get("content", "")[:2000],
                        "metadata": scraped.get("metadata", {})
                    })
            except Exception:
                continue
        
        return results
    
    def _analyze_company_data(self, company_data: Dict, company_name: str) -> Dict:
        """Analyze scraped company data using AI"""
        
        # Combine all scraped content
        combined_content = ""
        if "website" in company_data:
            combined_content += company_data["website"].get("content", "")[:1500]
        
        for result in company_data.get("search_results", []):
            combined_content += result.get("content", "")[:1000]
        
        prompt = f"""
        Analyze this company information for {company_name}:
        
        {combined_content[:4000]}
        
        Provide analysis in JSON format:
        {{
            "company_overview": "",
            "industry": "",
            "company_size": "",
            "founded_year": "",
            "headquarters": "",
            "key_products": [],
            "recent_news": [],
            "company_culture": "",
            "values": [],
            "growth_stage": "",
            "funding_status": "",
            "competitors": [],
            "interview_tips": [],
            "why_work_here": []
        }}
        """
        
        try:
            ai_response = self.generate_ai_response(prompt)
            import json
            return json.loads(ai_response)
        except Exception:
            return self._fallback_company_analysis(company_name)
    
    def _fallback_job_scraping(self, job_url: str) -> Dict:
        """Fallback when Firecrawl fails"""  # noqa: SPELL001
        return {
            "success": False,
            "job_details": {
                "job_title": "Unable to extract",
                "company": "Unable to extract",
                "location": "Remote/On-site",
                "required_skills": ["Check job posting directly"],
                "note": f"Please visit {job_url} for full details"
            },
            "error": "Scraping failed, manual review required"
        }
    
    def _fallback_company_info(self, company_name: str) -> Dict:
        """Fallback company information"""
        return {
            "success": False,
            "company_name": company_name,
            "insights": {
                "company_overview": f"Research {company_name} manually for detailed information",
                "interview_tips": [
                    "Research the company's recent news and achievements",
                    "Understand their products and services",
                    "Learn about their company culture and values",
                    "Prepare questions about growth opportunities"
                ]
            },
            "error": "Company research failed, manual research recommended"
        }
    
    def _fallback_salary_data(self, job_title: str, location: str) -> Dict:
        """Fallback salary information"""
        # Basic salary estimates based on common ranges
        salary_ranges = {
            "software engineer": {"min": 70000, "max": 150000, "median": 110000},
            "data scientist": {"min": 80000, "max": 160000, "median": 120000},
            "product manager": {"min": 90000, "max": 180000, "median": 135000},
            "marketing manager": {"min": 60000, "max": 120000, "median": 90000},
            "sales manager": {"min": 65000, "max": 140000, "median": 100000}
        }
        
        # Find closest match
        job_lower = job_title.lower()
        salary_estimate = {"min": 50000, "max": 100000, "median": 75000}
        
        for key, value in salary_ranges.items():
            if key in job_lower:
                salary_estimate = value
                break
        
        return {
            "success": False,
            "job_title": job_title,
            "location": location,
            "salary_analysis": {
                "estimated_range": salary_estimate,
                "note": "Estimates based on general market data. Research specific companies for accurate information."
            },
            "error": "Live salary data unavailable"
        }