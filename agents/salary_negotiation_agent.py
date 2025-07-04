"""
Salary Negotiation Agent for JobSniper AI
Provides comprehensive salary negotiation strategies, market analysis, and negotiation coaching.
"""

from .multi_ai_base import MultiAIAgent
import json


class SalaryNegotiationAgent(MultiAIAgent):
    def __init__(self):
        super().__init__(name="SalaryNegotiationAgent")
        self.agent_name = "Salary Negotiation Agent"
        self.agent_role = "Compensation Strategy and Negotiation Specialist"

    def run(
        self,
        job_data,
        candidate_profile,
        negotiation_stage="preparation",
        current_offer=None,
    ):
        """
        Generate comprehensive salary negotiation strategy

        Args:
            job_data (dict): Job posting and company information
            candidate_profile (dict): Candidate's background and experience
            negotiation_stage (str): Stage of negotiation (preparation, negotiation, counter_offer)
            current_offer (dict): Current offer details if available
        """

        try:
            # Market salary analysis
            market_analysis = self._analyze_market_salary(job_data, candidate_profile)

            # Candidate value assessment
            value_assessment = self._assess_candidate_value(candidate_profile, job_data)

            # Negotiation strategy
            negotiation_strategy = self._develop_negotiation_strategy(
                job_data, candidate_profile, market_analysis, negotiation_stage
            )

            # Offer analysis (if current offer provided)
            offer_analysis = (
                self._analyze_current_offer(current_offer, market_analysis)
                if current_offer
                else {}
            )

            # Counter-offer recommendations
            counter_offer_recs = self._generate_counter_offer_recommendations(
                market_analysis, value_assessment, current_offer
            )

            # Negotiation scripts and phrases
            negotiation_scripts = self._generate_negotiation_scripts(negotiation_stage)

            # Total compensation analysis
            total_comp_analysis = self._analyze_total_compensation(
                job_data, current_offer
            )

            # Risk assessment
            risk_assessment = self._assess_negotiation_risks(
                job_data, candidate_profile
            )

            return {
                "market_analysis": market_analysis,
                "value_assessment": value_assessment,
                "negotiation_strategy": negotiation_strategy,
                "offer_analysis": offer_analysis,
                "counter_offer_recommendations": counter_offer_recs,
                "negotiation_scripts": negotiation_scripts,
                "total_compensation_analysis": total_comp_analysis,
                "risk_assessment": risk_assessment,
                "negotiation_timeline": self._create_negotiation_timeline(
                    negotiation_stage
                ),
                "success_probability": self._calculate_negotiation_success_probability(
                    candidate_profile, market_analysis
                ),
                "alternative_strategies": self._generate_alternative_strategies(
                    job_data, candidate_profile
                ),
            }

        except Exception as e:
            return self._create_fallback_response(str(e))

    def _analyze_market_salary(self, job_data, candidate_profile):
        """Analyze market salary data and benchmarks"""

        if not self.api_available:
            return self._get_fallback_market_analysis(job_data)

        try:
            prompt = f"""
            Analyze market salary data for this position:
            
            Job Title: {job_data.get("title", "N/A")}
            Company: {job_data.get("company", "N/A")}
            Location: {job_data.get("location", "N/A")}
            Industry: {job_data.get("industry", "N/A")}
            Company Size: {job_data.get("company_size", "Medium")}
            
            Candidate Profile:
            Experience: {candidate_profile.get("experience_years", 0)} years
            Skills: {", ".join(candidate_profile.get("technical_skills", []))}
            Current Role: {candidate_profile.get("current_role", "N/A")}
            Industry: {candidate_profile.get("industry", "N/A")}
            
            Please provide:
            1. Market salary ranges (25th, 50th, 75th, 90th percentiles)
            2. Location-based adjustments
            3. Company size and industry premiums
            4. Experience level impact
            5. Skill premium analysis
            6. Total compensation benchmarks
            
            Return as JSON format with detailed breakdowns.
            """

            response = self.generate_ai_response(prompt)

            try:
                market_data = json.loads(response)
                return market_data
            except (json.JSONDecodeError, ValueError):
                return self._parse_market_analysis_from_text(response)

        except Exception as e:
            print(f"Error analyzing market salary: {e}")
            return self._get_fallback_market_analysis(job_data)

    def _assess_candidate_value(self, candidate_profile, job_data):
        """Assess candidate's unique value proposition"""

        experience_years = candidate_profile.get("experience_years", 0)
        skills = candidate_profile.get("technical_skills", [])
        achievements = candidate_profile.get("achievements", [])

        # Calculate value multipliers
        experience_multiplier = min(1.5, 1.0 + (experience_years * 0.05))
        skills_multiplier = min(1.3, 1.0 + (len(skills) * 0.02))

        value_assessment = {
            "overall_value_score": min(
                95, 70 + (experience_years * 3) + (len(skills) * 2)
            ),
            "experience_premium": f"{(experience_multiplier - 1.0) * 100:.1f}%",
            "skills_premium": f"{(skills_multiplier - 1.0) * 100:.1f}%",
            "unique_value_propositions": [
                f"{experience_years}+ years of relevant experience",
                f"Expertise in {len(skills)} key technical areas",
                "Proven track record of results",
                "Strong industry knowledge",
            ],
            "negotiation_strengths": [
                "Rare skill combination",
                "High-demand expertise",
                "Strong performance history",
                "Market scarcity value",
            ],
            "value_quantification": {
                "revenue_impact_potential": "$500K+ annually",
                "cost_savings_potential": "$200K+ annually",
                "productivity_improvement": "20-30%",
                "team_impact_multiplier": "2-3x",
            },
            "competitive_advantages": [
                "Specialized technical skills",
                "Industry experience and network",
                "Leadership and mentoring ability",
                "Innovation and problem-solving track record",
            ],
        }

        # Add achievement-based value
        if achievements:
            value_assessment["achievement_highlights"] = achievements[:5]
            value_assessment["achievement_value"] = (
                "Demonstrated ROI through past accomplishments"
            )

        return value_assessment

    def _develop_negotiation_strategy(
        self, job_data, candidate_profile, market_analysis, stage
    ):
        """Develop comprehensive negotiation strategy"""

        strategy = {
            "negotiation_approach": {
                "style": "Collaborative and data-driven",
                "tone": "Professional and confident",
                "focus": "Mutual value creation",
                "timeline": "Patient but decisive",
            },
            "key_principles": [
                "Lead with value, not need",
                "Use market data as foundation",
                "Focus on total compensation",
                "Maintain professional relationships",
                "Have alternatives ready (BATNA)",
            ],
            "negotiation_sequence": [
                {
                    "step": 1,
                    "action": "Express enthusiasm and gratitude",
                    "message": "Thank you for the offer. I'm excited about the opportunity.",
                },
                {
                    "step": 2,
                    "action": "Request time to review",
                    "message": "I'd like to review the complete package and get back to you.",
                },
                {
                    "step": 3,
                    "action": "Present market research",
                    "message": "Based on my research, here's what I found about market rates.",
                },
                {
                    "step": 4,
                    "action": "Highlight unique value",
                    "message": "Here's the specific value I bring to this role.",
                },
                {
                    "step": 5,
                    "action": "Make counter-proposal",
                    "message": "Based on this analysis, I'd like to discuss adjustments.",
                },
            ],
            "leverage_points": [
                "Market demand for skills",
                "Unique experience combination",
                "Multiple opportunities available",
                "Strong performance track record",
                "Network and industry relationships",
            ],
            "fallback_options": [
                "Additional vacation time",
                "Flexible work arrangements",
                "Professional development budget",
                "Stock options or equity",
                "Performance-based bonuses",
            ],
        }

        # Adjust strategy based on stage
        if stage == "preparation":
            strategy["immediate_actions"] = [
                "Research market salary data",
                "Document unique value proposition",
                "Identify multiple leverage points",
                "Prepare negotiation scripts",
                "Define minimum acceptable terms",
            ]
        elif stage == "negotiation":
            strategy["immediate_actions"] = [
                "Present counter-offer professionally",
                "Use data to support requests",
                "Remain collaborative and positive",
                "Listen actively to concerns",
                "Be prepared to compromise",
            ]
        elif stage == "counter_offer":
            strategy["immediate_actions"] = [
                "Evaluate offer against criteria",
                "Calculate total compensation value",
                "Consider non-salary benefits",
                "Assess career growth potential",
                "Make final decision confidently",
            ]

        return strategy

    def _analyze_current_offer(self, current_offer, market_analysis):
        """Analyze current offer against market benchmarks"""

        if not current_offer:
            return {}

        base_salary = current_offer.get("base_salary", 0)
        market_median = market_analysis.get("salary_ranges", {}).get(
            "median", base_salary
        )

        analysis = {
            "offer_assessment": {
                "base_salary": base_salary,
                "market_position": self._calculate_market_position(
                    base_salary, market_median
                ),
                "competitiveness": self._assess_offer_competitiveness(
                    base_salary, market_analysis
                ),
                "total_package_value": self._calculate_total_package_value(
                    current_offer
                ),
            },
            "gap_analysis": {
                "salary_gap": max(0, market_median - base_salary),
                "percentile_position": self._calculate_percentile_position(
                    base_salary, market_analysis
                ),
                "improvement_potential": self._calculate_improvement_potential(
                    current_offer, market_analysis
                ),
            },
            "offer_strengths": [
                strength for strength in self._identify_offer_strengths(current_offer)
            ],
            "improvement_areas": [
                area
                for area in self._identify_improvement_areas(
                    current_offer, market_analysis
                )
            ],
            "negotiation_priority": self._determine_negotiation_priority(
                current_offer, market_analysis
            ),
        }

        return analysis

    def _generate_counter_offer_recommendations(
        self, market_analysis, value_assessment, current_offer
    ):
        """Generate specific counter-offer recommendations"""

        recommendations = {
            "salary_recommendations": {
                "target_salary": self._calculate_target_salary(
                    market_analysis, value_assessment
                ),
                "minimum_acceptable": self._calculate_minimum_salary(market_analysis),
                "stretch_goal": self._calculate_stretch_salary(
                    market_analysis, value_assessment
                ),
                "negotiation_range": self._calculate_negotiation_range(market_analysis),
            },
            "total_compensation_recommendations": {
                "bonus_target": "15-25% of base salary",
                "equity_request": "Stock options or RSUs",
                "benefits_optimization": [
                    "Additional vacation days",
                    "Flexible work arrangements",
                    "Professional development budget",
                    "Health and wellness benefits",
                ],
            },
            "negotiation_packages": [
                {
                    "package_name": "Aggressive",
                    "salary_increase": "20-25%",
                    "success_probability": "30-40%",
                    "justification": "Top-tier market positioning",
                },
                {
                    "package_name": "Balanced",
                    "salary_increase": "10-15%",
                    "success_probability": "60-70%",
                    "justification": "Market-aligned with value premium",
                },
                {
                    "package_name": "Conservative",
                    "salary_increase": "5-10%",
                    "success_probability": "80-90%",
                    "justification": "Modest adjustment to market rate",
                },
            ],
            "alternative_value_adds": [
                "Signing bonus to offset salary gap",
                "Earlier performance review cycle",
                "Additional stock options",
                "Flexible work-from-home policy",
                "Conference and training budget",
            ],
        }

        return recommendations

    def _generate_negotiation_scripts(self, stage):
        """Generate negotiation scripts and key phrases"""

        scripts = {
            "opening_scripts": {
                "enthusiasm_first": "I'm really excited about this opportunity and the chance to contribute to [Company]. Thank you for the offer.",
                "gratitude_expression": "I appreciate the time you've taken to put together this offer package.",
                "professional_approach": "I'd like to discuss the compensation package to ensure it aligns with the value I'll bring.",
            },
            "research_presentation": {
                "market_data": "Based on my research using [sources], the market range for this role appears to be $X-Y.",
                "value_proposition": "Given my X years of experience and expertise in [skills], I believe I bring exceptional value.",
                "specific_contributions": "I'm confident I can contribute [specific value] in the first year.",
            },
            "counter_offer_scripts": {
                "collaborative_approach": "I'm hoping we can work together to bridge this gap.",
                "specific_request": "Based on my research and experience, I was hoping for a salary in the range of $X-Y.",
                "flexible_negotiation": "I'm open to discussing various ways to structure the compensation.",
            },
            "handling_objections": {
                "budget_constraints": "I understand budget considerations. Are there other forms of compensation we could explore?",
                "company_policy": "I appreciate the policy. What flexibility exists within those guidelines?",
                "equity_instead": "I'd be interested in understanding the equity component and how it complements base salary.",
            },
            "closing_scripts": {
                "positive_close": "I'm confident we can find a solution that works for both of us.",
                "timeline_setting": "When would be a good time to continue this conversation?",
                "relationship_maintenance": "I want to ensure we maintain the positive momentum in our discussions.",
            },
        }

        return scripts

    def _analyze_total_compensation(self, job_data, current_offer):
        """Analyze total compensation package"""

        if not current_offer:
            return self._get_default_compensation_analysis()

        base_salary = current_offer.get("base_salary", 0)
        bonus = current_offer.get("bonus", 0)
        equity_value = current_offer.get("equity_value", 0)
        benefits_value = current_offer.get(
            "benefits_value", base_salary * 0.3
        )  # Estimate 30%

        total_comp = base_salary + bonus + equity_value + benefits_value

        analysis = {
            "total_compensation_breakdown": {
                "base_salary": base_salary,
                "annual_bonus": bonus,
                "equity_value": equity_value,
                "benefits_value": benefits_value,
                "total_package": total_comp,
            },
            "compensation_ratios": {
                "base_to_total": f"{(base_salary / total_comp * 100):.1f}%",
                "variable_to_total": f"{((bonus + equity_value) / total_comp * 100):.1f}%",
                "benefits_to_total": f"{(benefits_value / total_comp * 100):.1f}%",
            },
            "package_assessment": {
                "cash_heavy": base_salary > (total_comp * 0.7),
                "equity_heavy": equity_value > (total_comp * 0.3),
                "benefits_rich": benefits_value > (base_salary * 0.35),
                "balanced_package": abs(base_salary - (total_comp * 0.6))
                < (total_comp * 0.1),
            },
            "optimization_opportunities": [
                "Increase base salary for guaranteed income",
                "Negotiate higher bonus targets",
                "Request additional equity for upside potential",
                "Enhance benefits package value",
            ],
        }

        return analysis

    def _assess_negotiation_risks(self, job_data, candidate_profile):
        """Assess risks associated with salary negotiation"""

        risk_factors = []
        risk_level = "Low"

        # Company-based risks
        company_size = job_data.get("company_size", "Medium")
        if company_size == "Startup":
            risk_factors.append("Startup may have limited cash but more equity")
            risk_level = "Medium"

        # Market-based risks
        if candidate_profile.get("employment_status") == "unemployed":
            risk_factors.append("Unemployment may reduce negotiation leverage")
            risk_level = "Medium"

        # Experience-based risks
        if candidate_profile.get("experience_years", 0) < 2:
            risk_factors.append("Limited experience may reduce negotiation power")

        risk_assessment = {
            "overall_risk_level": risk_level,
            "risk_factors": risk_factors,
            "risk_mitigation_strategies": [
                "Present data-driven justification",
                "Maintain professional and collaborative tone",
                "Have backup options (BATNA) ready",
                "Focus on value creation, not just extraction",
                "Be prepared to compromise on non-critical items",
            ],
            "negotiation_confidence": {
                "recommended_approach": "Confident but respectful",
                "leverage_assessment": "Moderate to Strong",
                "success_probability": "70-80%",
                "fallback_strategies": [
                    "Accept offer and negotiate raise after 6 months",
                    "Request non-salary improvements",
                    "Negotiate start date or other terms",
                ],
            },
        }

        return risk_assessment

    def _create_negotiation_timeline(self, stage):
        """Create negotiation timeline and milestones"""

        timelines = {
            "preparation": {
                "duration": "3-5 days",
                "milestones": [
                    {
                        "day": 1,
                        "task": "Market research and data collection",
                        "deliverable": "Salary range analysis",
                    },
                    {
                        "day": 2,
                        "task": "Value proposition development",
                        "deliverable": "Unique value summary",
                    },
                    {
                        "day": 3,
                        "task": "Strategy development and script preparation",
                        "deliverable": "Negotiation plan",
                    },
                ],
            },
            "negotiation": {
                "duration": "1-2 weeks",
                "milestones": [
                    {
                        "day": 1,
                        "task": "Initial counter-offer presentation",
                        "deliverable": "Professional counter-proposal",
                    },
                    {
                        "day": 3 - 5,
                        "task": "Follow-up and clarification",
                        "deliverable": "Refined negotiation position",
                    },
                    {
                        "day": 7 - 10,
                        "task": "Final negotiation and agreement",
                        "deliverable": "Agreed compensation package",
                    },
                ],
            },
            "post_negotiation": {
                "duration": "1-2 days",
                "milestones": [
                    {
                        "task": "Offer acceptance and documentation",
                        "deliverable": "Signed offer letter",
                    },
                    {
                        "task": "Transition planning",
                        "deliverable": "Start date confirmation",
                    },
                ],
            },
        }

        return timelines.get(stage, timelines["preparation"])

    def _calculate_negotiation_success_probability(
        self, candidate_profile, market_analysis
    ):
        """Calculate probability of successful negotiation"""

        base_probability = 0.6  # 60% base success rate

        # Experience factor
        experience_years = candidate_profile.get("experience_years", 0)
        experience_factor = min(0.2, experience_years * 0.03)  # Up to 20% bonus

        # Market demand factor
        market_demand = market_analysis.get("market_demand", "Medium")
        demand_factor = {"High": 0.15, "Medium": 0.05, "Low": -0.05}.get(
            market_demand, 0.05
        )

        # Skills rarity factor
        skills_count = len(candidate_profile.get("technical_skills", []))
        skills_factor = min(0.1, skills_count * 0.01)

        total_probability = (
            base_probability + experience_factor + demand_factor + skills_factor
        )

        return {
            "success_probability": min(0.95, total_probability),
            "confidence_level": "High"
            if total_probability > 0.75
            else "Medium"
            if total_probability > 0.6
            else "Moderate",
            "key_success_factors": [
                f"Experience level: {experience_years} years",
                f"Market demand: {market_demand}",
                f"Skills portfolio: {skills_count} technical skills",
                "Professional approach and preparation",
            ],
            "probability_breakdown": {
                "base_rate": f"{base_probability:.1%}",
                "experience_bonus": f"{experience_factor:.1%}",
                "market_demand_factor": f"{demand_factor:.1%}",
                "skills_factor": f"{skills_factor:.1%}",
            },
        }

    def _generate_alternative_strategies(self, job_data, candidate_profile):
        """Generate alternative negotiation strategies"""

        strategies = [
            {
                "strategy_name": "Value-First Approach",
                "description": "Lead with unique value proposition before discussing compensation",
                "best_for": "Candidates with strong track record",
                "success_rate": "75%",
                "approach": [
                    "Demonstrate specific value you'll bring",
                    "Quantify impact in dollars or percentages",
                    "Connect value to compensation request",
                    "Use past achievements as evidence",
                ],
            },
            {
                "strategy_name": "Market-Data Driven",
                "description": "Use comprehensive market research as primary justification",
                "best_for": "Well-researched candidates with market data",
                "success_rate": "70%",
                "approach": [
                    "Present multiple salary data sources",
                    "Show location and industry adjustments",
                    "Highlight experience and skill premiums",
                    "Request alignment with market rates",
                ],
            },
            {
                "strategy_name": "Total Package Optimization",
                "description": "Focus on optimizing entire compensation package",
                "best_for": "When base salary has limited flexibility",
                "success_rate": "65%",
                "approach": [
                    "Negotiate bonus structure",
                    "Request additional equity or stock options",
                    "Improve benefits package",
                    "Add non-monetary perks",
                ],
            },
            {
                "strategy_name": "Performance-Based Approach",
                "description": "Tie compensation increases to performance milestones",
                "best_for": "Entry to mid-level candidates",
                "success_rate": "60%",
                "approach": [
                    "Propose 6-month performance review",
                    "Set specific achievement targets",
                    "Agree on compensation adjustments",
                    "Document performance criteria",
                ],
            },
        ]

        return strategies

    # Helper methods for calculations
    def _calculate_market_position(self, salary, market_median):
        if market_median == 0:
            return "Unable to determine"

        ratio = salary / market_median
        if ratio >= 1.1:
            return "Above Market"
        elif ratio >= 0.9:
            return "Market Rate"
        else:
            return "Below Market"

    def _assess_offer_competitiveness(self, salary, market_analysis):
        market_ranges = market_analysis.get("salary_ranges", {})
        percentile_75 = market_ranges.get("75th_percentile", salary)

        if salary >= percentile_75:
            return "Highly Competitive"
        elif salary >= market_ranges.get("median", salary):
            return "Competitive"
        else:
            return "Below Market"

    def _calculate_total_package_value(self, offer):
        return (
            offer.get("base_salary", 0)
            + offer.get("bonus", 0)
            + offer.get("equity_value", 0)
            + offer.get("benefits_value", 0)
        )

    def _calculate_percentile_position(self, salary, market_analysis):
        ranges = market_analysis.get("salary_ranges", {})
        if salary >= ranges.get("90th_percentile", salary):
            return "90th+ percentile"
        elif salary >= ranges.get("75th_percentile", salary):
            return "75th-90th percentile"
        elif salary >= ranges.get("median", salary):
            return "50th-75th percentile"
        else:
            return "Below 50th percentile"

    def _calculate_improvement_potential(self, offer, market_analysis):
        current_salary = offer.get("base_salary", 0)
        market_75th = market_analysis.get("salary_ranges", {}).get(
            "75th_percentile", current_salary
        )

        if current_salary == 0:
            return "Unable to calculate"

        improvement = ((market_75th - current_salary) / current_salary) * 100
        return f"{improvement:.1f}% to 75th percentile"

    def _identify_offer_strengths(self, offer):
        strengths = []
        if offer.get("bonus", 0) > 0:
            strengths.append("Performance bonus included")
        if offer.get("equity_value", 0) > 0:
            strengths.append("Equity compensation offered")
        if offer.get("benefits_comprehensive", False):
            strengths.append("Comprehensive benefits package")
        return strengths

    def _identify_improvement_areas(self, offer, market_analysis):
        areas = []
        base_salary = offer.get("base_salary", 0)
        market_median = market_analysis.get("salary_ranges", {}).get(
            "median", base_salary
        )

        if base_salary < market_median:
            areas.append("Base salary below market median")
        if offer.get("bonus", 0) == 0:
            areas.append("No performance bonus component")
        if offer.get("equity_value", 0) == 0:
            areas.append("Limited equity upside")

        return areas

    def _determine_negotiation_priority(self, offer, market_analysis):
        base_salary = offer.get("base_salary", 0)
        market_median = market_analysis.get("salary_ranges", {}).get(
            "median", base_salary
        )

        if base_salary < market_median * 0.9:
            return "High Priority"
        elif base_salary < market_median:
            return "Medium Priority"
        else:
            return "Low Priority"

    def _calculate_target_salary(self, market_analysis, value_assessment):
        market_75th = market_analysis.get("salary_ranges", {}).get(
            "75th_percentile", 100000
        )
        value_score = value_assessment.get("overall_value_score", 70)

        # Adjust target based on value score
        adjustment = (value_score - 70) / 100  # Scale adjustment
        return int(market_75th * (1 + adjustment))

    def _calculate_minimum_salary(self, market_analysis):
        return market_analysis.get("salary_ranges", {}).get("median", 80000)

    def _calculate_stretch_salary(self, market_analysis, value_assessment):
        market_90th = market_analysis.get("salary_ranges", {}).get(
            "90th_percentile", 120000
        )
        return int(market_90th * 1.05)  # 5% above 90th percentile

    def _calculate_negotiation_range(self, market_analysis):
        ranges = market_analysis.get("salary_ranges", {})
        return {
            "minimum": ranges.get("median", 80000),
            "target": ranges.get("75th_percentile", 100000),
            "stretch": ranges.get("90th_percentile", 120000),
        }

    def _get_fallback_market_analysis(self, job_data):
        """Provide fallback market analysis when API is unavailable"""

        # Simplified market analysis based on job title
        job_title = job_data.get("title", "").lower()

        # Basic salary estimates (would be more sophisticated in production)
        base_estimates = {
            "software engineer": 95000,
            "data scientist": 110000,
            "product manager": 120000,
            "marketing manager": 85000,
            "sales manager": 90000,
        }

        base_salary = 80000  # Default
        for title, salary in base_estimates.items():
            if title in job_title:
                base_salary = salary
                break

        return {
            "salary_ranges": {
                "25th_percentile": int(base_salary * 0.8),
                "median": base_salary,
                "75th_percentile": int(base_salary * 1.25),
                "90th_percentile": int(base_salary * 1.5),
            },
            "market_factors": {
                "location_adjustment": "Varies by location",
                "company_size_premium": "10-20% for large companies",
                "industry_premium": "Varies by industry",
                "experience_premium": "3-8% per year of experience",
            },
            "data_sources": [
                "Glassdoor salary data",
                "PayScale market reports",
                "LinkedIn salary insights",
                "Bureau of Labor Statistics",
                "Industry salary surveys",
            ],
            "note": "Limited analysis - recommend using salary research tools",
        }

    def _parse_market_analysis_from_text(self, response_text):
        """Parse market analysis from text response"""

        return {
            "market_analysis": response_text,
            "note": "Detailed parsing requires structured data - use manual analysis",
        }

    def _get_default_compensation_analysis(self):
        """Get default compensation analysis template"""

        return {
            "analysis_note": "No current offer provided - general compensation guidelines",
            "compensation_components": [
                "Base salary (typically 60-80% of total)",
                "Annual bonus (10-25% of base)",
                "Equity/stock options (varies widely)",
                "Benefits package (20-30% of base value)",
            ],
            "negotiation_focus": [
                "Research market rates thoroughly",
                "Document unique value proposition",
                "Consider total compensation package",
                "Prepare multiple negotiation scenarios",
            ],
        }

    def _create_fallback_response(self, error_message):
        """Create fallback response when main processing fails"""

        return {
            "status": "Limited analysis available",
            "error_note": f"Analysis limited due to: {error_message}",
            "basic_negotiation_tips": [
                "Research market salary data thoroughly",
                "Document your unique value proposition",
                "Practice your negotiation conversation",
                "Be professional and collaborative",
                "Have backup options ready",
            ],
            "key_negotiation_principles": [
                "Lead with value, not need",
                "Use data to support requests",
                "Focus on total compensation",
                "Maintain positive relationships",
                "Be prepared to compromise",
            ],
            "research_recommendations": [
                "Use Glassdoor, PayScale, LinkedIn for salary data",
                "Research company-specific compensation trends",
                "Network with professionals in similar roles",
                "Consult industry salary reports",
                "Consider cost of living adjustments",
            ],
        }
