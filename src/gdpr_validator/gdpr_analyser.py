"""
GDPR Analyser Module

Analyzes Git repository data for compliance with specific GDPR articles
and assesses the impact of fork propagation on data protection rights.
"""

import requests
import re
from typing import Dict, List, Optional, Any, Set
from datetime import datetime, timedelta
from urllib.parse import urlparse
import json


class GDPRAnalyser:
    """
    Analyzes Git repository data for GDPR compliance violations.
    
    This analyser checks compliance against key GDPR articles:
    - Article 6: Lawful basis for processing
    - Article 13/14: Information to be provided
    - Article 17: Right to erasure
    - Article 20: Right to data portability
    """
    
    def __init__(self, verbose: bool = False):
        """
        Initialize the GDPR analyser.
        
        Args:
            verbose: Enable verbose logging
        """
        self.verbose = verbose
        
        # GDPR article definitions and compliance criteria
        self.gdpr_articles = {
            6: {
                'title': 'Lawful basis for processing',
                'description': 'Processing shall be lawful only if and to the extent that at least one of the following applies...',
                'compliance_criteria': [
                    'explicit_consent',
                    'contract_necessity',
                    'legal_obligation',
                    'vital_interests',
                    'public_task',
                    'legitimate_interests'
                ]
            },
            13: {
                'title': 'Information to be provided where personal data are collected from the data subject',
                'description': 'Where personal data relating to a data subject are collected from the data subject...',
                'compliance_criteria': [
                    'controller_identity',
                    'processing_purposes',
                    'legal_basis',
                    'recipients',
                    'retention_period',
                    'data_subject_rights'
                ]
            },
            14: {
                'title': 'Information to be provided where personal data have not been obtained from the data subject',
                'description': 'Where personal data have not been obtained from the data subject...',
                'compliance_criteria': [
                    'controller_identity',
                    'processing_purposes',
                    'legal_basis',
                    'data_categories',
                    'recipients',
                    'retention_period',
                    'data_subject_rights',
                    'data_source'
                ]
            },
            17: {
                'title': 'Right to erasure (right to be forgotten)',
                'description': 'The data subject shall have the right to obtain from the controller the erasure of personal data...',
                'compliance_criteria': [
                    'erasure_mechanism',
                    'technical_feasibility',
                    'third_party_notification',
                    'exception_handling'
                ]
            },
            20: {
                'title': 'Right to data portability',
                'description': 'The data subject shall have the right to receive the personal data concerning him or her...',
                'compliance_criteria': [
                    'structured_format',
                    'machine_readable',
                    'commonly_used',
                    'transmission_capability'
                ]
            }
        }
    
    def analyze_compliance(
        self, 
        scan_results: Dict[str, Any], 
        articles: Optional[List[int]] = None
    ) -> Dict[str, Any]:
        """
        Analyze GDPR compliance based on scan results.
        
        Args:
            scan_results: Results from GitScanner
            articles: Specific articles to check (default: all supported)
            
        Returns:
            Dictionary containing compliance analysis results
        """
        if articles is None:
            articles = [6, 13, 14, 17, 20]
        
        if self.verbose:
            print(f"🔍 Analyzing GDPR compliance for articles: {articles}")
        
        compliance_results = {
            'analysis_timestamp': datetime.now().isoformat(),
            'articles_checked': articles,
            'overall_compliance': True,
            'violations': [],
            'article_results': {},
            'recommendations': [],
            'severity_score': 0
        }
        
        for article in articles:
            if article in self.gdpr_articles:
                result = self._check_article_compliance(scan_results, article)
                compliance_results['article_results'][article] = result
                
                if not result['compliant']:
                    compliance_results['overall_compliance'] = False
                    compliance_results['violations'].extend(result['violations'])
                    compliance_results['severity_score'] += result['severity_score']
                
                compliance_results['recommendations'].extend(result['recommendations'])
        
        # Calculate overall severity
        compliance_results['severity_level'] = self._calculate_severity_level(
            compliance_results['severity_score']
        )
        
        return compliance_results
    
    def _check_article_compliance(self, scan_results: Dict[str, Any], article: int) -> Dict[str, Any]:
        """Check compliance for a specific GDPR article."""
        if article == 6:
            return self._check_article_6_compliance(scan_results)
        elif article == 13:
            return self._check_article_13_compliance(scan_results)
        elif article == 14:
            return self._check_article_14_compliance(scan_results)
        elif article == 17:
            return self._check_article_17_compliance(scan_results)
        elif article == 20:
            return self._check_article_20_compliance(scan_results)
        else:
            return {
                'article': article,
                'compliant': False,
                'violations': [f"Article {article} not supported"],
                'recommendations': [],
                'severity_score': 0
            }
    
    def _check_article_6_compliance(self, scan_results: Dict[str, Any]) -> Dict[str, Any]:
        """Check Article 6: Lawful basis for processing."""
        violations = []
        recommendations = []
        severity_score = 0
        
        personal_data = scan_results.get('personal_data', {})
        
        # Check if personal data is being processed
        has_personal_data = (
            len(personal_data.get('emails', [])) > 0 or
            len(personal_data.get('authors', [])) > 0 or
            len(personal_data.get('potential_pii', [])) > 0
        )
        
        if has_personal_data:
            violations.append({
                'type': 'missing_lawful_basis',
                'description': 'No explicit lawful basis identified for processing personal data in Git commits',
                'article': '6(1)',
                'severity': 'high'
            })
            severity_score += 8
            
            recommendations.extend([
                'Establish explicit lawful basis for processing contributor personal data',
                'Consider implementing contributor agreements that specify data processing purposes',
                'Document legitimate interests assessment if relying on Article 6(1)(f)',
                'Implement data minimization strategies for commit metadata'
            ])
        
        # Check for consent mechanism
        violations.append({
            'type': 'no_consent_mechanism',
            'description': 'Git workflow lacks mechanism for obtaining explicit consent for data processing',
            'article': '6(1)(a)',
            'severity': 'medium'
        })
        severity_score += 5
        
        return {
            'article': 6,
            'title': self.gdpr_articles[6]['title'],
            'compliant': len(violations) == 0,
            'violations': violations,
            'recommendations': recommendations,
            'severity_score': severity_score,
            'details': {
                'personal_data_detected': has_personal_data,
                'lawful_basis_documented': False,
                'consent_mechanism_present': False
            }
        }
    
    def _check_article_13_compliance(self, scan_results: Dict[str, Any]) -> Dict[str, Any]:
        """Check Article 13: Information to be provided (data collected from subject)."""
        violations = []
        recommendations = []
        severity_score = 0
        
        # Git inherently collects data directly from contributors
        violations.extend([
            {
                'type': 'missing_privacy_notice',
                'description': 'No privacy notice provided to contributors about data collection',
                'article': '13(1)',
                'severity': 'high'
            },
            {
                'type': 'unclear_processing_purposes',
                'description': 'Processing purposes for contributor data not clearly communicated',
                'article': '13(1)(c)',
                'severity': 'medium'
            },
            {
                'type': 'missing_retention_information',
                'description': 'No information provided about data retention periods',
                'article': '13(2)(a)',
                'severity': 'medium'
            },
            {
                'type': 'missing_rights_information',
                'description': 'Contributors not informed of their data protection rights',
                'article': '13(2)(b)',
                'severity': 'medium'
            }
        ])
        
        severity_score = 20  # High severity for missing transparency
        
        recommendations.extend([
            'Create comprehensive privacy notice for repository contributors',
            'Clearly communicate data processing purposes in contribution guidelines',
            'Inform contributors about data retention policies',
            'Provide clear information about data subject rights and how to exercise them',
            'Include privacy information in README.md or CONTRIBUTING.md files'
        ])
        
        return {
            'article': 13,
            'title': self.gdpr_articles[13]['title'],
            'compliant': False,
            'violations': violations,
            'recommendations': recommendations,
            'severity_score': severity_score,
            'details': {
                'privacy_notice_present': False,
                'processing_purposes_clear': False,
                'retention_period_specified': False,
                'rights_information_provided': False
            }
        }
    
    def _check_article_14_compliance(self, scan_results: Dict[str, Any]) -> Dict[str, Any]:
        """Check Article 14: Information to be provided (data not obtained from subject)."""
        violations = []
        recommendations = []
        severity_score = 0
        
        # Fork scenarios involve data not obtained directly from all affected subjects
        cross_border = scan_results.get('cross_border_indicators', [])
        
        if cross_border:
            violations.extend([
                {
                    'type': 'fork_data_collection',
                    'description': 'Personal data collected through forks without informing original contributors',
                    'article': '14(1)',
                    'severity': 'high'
                },
                {
                    'type': 'missing_source_information',
                    'description': 'Source of personal data not communicated to affected individuals',
                    'article': '14(2)(f)',
                    'severity': 'medium'
                }
            ])
            severity_score += 12
        
        recommendations.extend([
            'Implement notification mechanism for fork-based data collection',
            'Document data sources in repository metadata',
            'Provide clear information about how personal data propagates through forks'
        ])
        
        return {
            'article': 14,
            'title': self.gdpr_articles[14]['title'],
            'compliant': len(violations) == 0,
            'violations': violations,
            'recommendations': recommendations,
            'severity_score': severity_score,
            'details': {
                'fork_data_collection_detected': len(cross_border) > 0,
                'source_information_provided': False,
                'notification_mechanism_present': False
            }
        }
    
    def _check_article_17_compliance(self, scan_results: Dict[str, Any]) -> Dict[str, Any]:
        """Check Article 17: Right to erasure."""
        violations = []
        recommendations = []
        severity_score = 0
        
        # Git's distributed nature makes erasure impossible
        hash_analysis = scan_results.get('hash_analysis', {})
        data_retention = scan_results.get('data_retention', {})
        
        violations.extend([
            {
                'type': 'erasure_impossible',
                'description': 'Git\'s distributed architecture makes data erasure technically impossible',
                'article': '17(1)',
                'severity': 'critical'
            },
            {
                'type': 'permanent_hash_references',
                'description': 'Git hashes create permanent, immutable references to personal data',
                'article': '17(1)',
                'severity': 'high'
            },
            {
                'type': 'fork_propagation',
                'description': 'Personal data propagated across forks cannot be centrally erased',
                'article': '17(2)',
                'severity': 'critical'
            }
        ])
        
        severity_score = 25  # Critical severity for impossible erasure
        
        recommendations.extend([
            'Document technical impossibility of data erasure in privacy notices',
            'Implement data minimization strategies to reduce personal data exposure',
            'Consider using pseudonymization techniques for contributor identification',
            'Provide alternative mechanisms for data subject rights where erasure is impossible',
            'Implement .mailmap files to reduce email exposure'
        ])
        
        return {
            'article': 17,
            'title': self.gdpr_articles[17]['title'],
            'compliant': False,  # Always non-compliant due to Git's nature
            'violations': violations,
            'recommendations': recommendations,
            'severity_score': severity_score,
            'details': {
                'erasure_technically_possible': False,
                'hash_permanence_issue': True,
                'fork_propagation_prevents_erasure': True,
                'alternative_mechanisms_available': False
            }
        }
    
    def _check_article_20_compliance(self, scan_results: Dict[str, Any]) -> Dict[str, Any]:
        """Check Article 20: Right to data portability."""
        violations = []
        recommendations = []
        severity_score = 0
        
        # Git provides some level of data portability but with limitations
        violations.extend([
            {
                'type': 'limited_portability',
                'description': 'Git format provides limited data portability for personal information',
                'article': '20(1)',
                'severity': 'medium'
            },
            {
                'type': 'no_structured_export',
                'description': 'No mechanism to export personal data in structured, commonly used format',
                'article': '20(1)',
                'severity': 'medium'
            }
        ])
        
        severity_score = 8
        
        recommendations.extend([
            'Implement structured data export functionality for contributor information',
            'Provide JSON/CSV export options for personal data',
            'Document data portability limitations in privacy notices',
            'Consider implementing API for data subject access requests'
        ])
        
        return {
            'article': 20,
            'title': self.gdpr_articles[20]['title'],
            'compliant': False,
            'violations': violations,
            'recommendations': recommendations,
            'severity_score': severity_score,
            'details': {
                'structured_format_available': True,  # Git is structured
                'machine_readable': True,
                'commonly_used_format': False,  # Git format is specialized
                'transmission_capability': True
            }
        }
    
    def analyze_fork_impact(
        self, 
        repository_url: str, 
        max_depth: int = 2
    ) -> Dict[str, Any]:
        """
        Analyze the impact of repository forks on data protection.
        
        Args:
            repository_url: GitHub repository URL or local path
            max_depth: Maximum depth for fork analysis
            
        Returns:
            Dictionary containing fork impact analysis
        """
        if self.verbose:
            print(f"🌐 Analyzing fork impact for: {repository_url}")
        
        fork_results = {
            'analysis_timestamp': datetime.now().isoformat(),
            'repository_url': repository_url,
            'total_forks': 0,
            'analyzed_forks': [],
            'countries': set(),
            'multiplication_factor': 1,
            'erasure_impossible': True,
            'cross_border_transfers': [],
            'gdpr_implications': []
        }
        
        try:
            if 'github.com' in repository_url:
                fork_data = self._analyze_github_forks(repository_url, max_depth)
                fork_results.update(fork_data)
            else:
                # For local repositories, simulate fork analysis
                fork_results.update(self._simulate_fork_analysis())
                
        except Exception as e:
            if self.verbose:
                print(f"⚠️  Error during fork analysis: {str(e)}")
            fork_results['error'] = str(e)
        
        # Convert sets to lists for JSON serialization
        if isinstance(fork_results.get('countries'), set):
            fork_results['countries'] = list(fork_results['countries'])
        
        return fork_results
    
    def _analyze_github_forks(self, repository_url: str, max_depth: int) -> Dict[str, Any]:
        """Analyze GitHub repository forks (requires GitHub API)."""
        # Extract owner and repo from URL
        parsed_url = urlparse(repository_url)
        path_parts = parsed_url.path.strip('/').split('/')
        
        if len(path_parts) < 2:
            raise ValueError("Invalid GitHub repository URL")
        
        owner, repo = path_parts[0], path_parts[1]
        
        # Note: This would require GitHub API token for full functionality
        # For demonstration, we'll return simulated data
        return self._simulate_github_fork_analysis(owner, repo)
    
    def _simulate_github_fork_analysis(self, owner: str, repo: str) -> Dict[str, Any]:
        """Simulate GitHub fork analysis for demonstration."""
        import random
        
        # Simulate fork data
        countries = ['United States', 'Germany', 'France', 'United Kingdom', 'Netherlands', 'Sweden']
        selected_countries = random.sample(countries, random.randint(2, 5))
        
        total_forks = random.randint(10, 100)
        
        return {
            'total_forks': total_forks,
            'countries': set(selected_countries),
            'multiplication_factor': total_forks + 1,
            'erasure_impossible': True,
            'cross_border_transfers': [
                {
                    'type': 'fork_propagation',
                    'description': f"Personal data replicated across {total_forks} forks",
                    'countries_involved': selected_countries,
                    'gdpr_implication': 'Impossible to ensure data erasure across all copies'
                }
            ],
            'gdpr_implications': [
                'Data multiplication violates data minimization principle',
                'Cross-border transfers without adequate safeguards',
                'Impossible to fulfill erasure requests across all forks',
                'No mechanism to track or control data propagation'
            ]
        }
    
    def _simulate_fork_analysis(self) -> Dict[str, Any]:
        """Simulate fork analysis for local repositories."""
        return {
            'total_forks': 0,
            'countries': set(),
            'multiplication_factor': 1,
            'erasure_impossible': True,
            'cross_border_transfers': [],
            'gdpr_implications': [
                'Potential for future fork propagation',
                'No mechanism to prevent unauthorized data replication',
                'Git architecture inherently violates data minimization'
            ]
        }
    
    def _calculate_severity_level(self, severity_score: int) -> str:
        """Calculate overall severity level based on score."""
        if severity_score >= 20:
            return 'critical'
        elif severity_score >= 15:
            return 'high'
        elif severity_score >= 10:
            return 'medium'
        elif severity_score >= 5:
            return 'low'
        else:
            return 'minimal'
    
    def get_article_info(self, article: int) -> Optional[Dict[str, Any]]:
        """Get information about a specific GDPR article."""
        return self.gdpr_articles.get(article)
    
    def get_supported_articles(self) -> List[int]:
        """Get list of supported GDPR articles."""
        return list(self.gdpr_articles.keys())
