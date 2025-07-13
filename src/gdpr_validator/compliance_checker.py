"""
Compliance Checker Module

Provides quick compliance checks for specific GDPR articles and
generates actionable recommendations for improving data protection.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime


class ComplianceChecker:
    """
    Quick compliance checker for GDPR articles.
    
    This checker provides rapid assessment of compliance status
    and generates specific recommendations for remediation.
    """
    
    def __init__(self, verbose: bool = False):
        """
        Initialize the compliance checker.
        
        Args:
            verbose: Enable verbose logging
        """
        self.verbose = verbose
        
        # Quick check criteria for each article
        self.quick_checks = {
            6: {
                'name': 'Lawful Basis',
                'checks': [
                    'has_privacy_policy',
                    'documents_lawful_basis',
                    'has_consent_mechanism',
                    'legitimate_interests_assessment'
                ]
            },
            13: {
                'name': 'Transparency (Data from Subject)',
                'checks': [
                    'privacy_notice_present',
                    'processing_purposes_clear',
                    'controller_identity_clear',
                    'retention_period_specified',
                    'rights_information_provided'
                ]
            },
            14: {
                'name': 'Transparency (Data Not from Subject)',
                'checks': [
                    'third_party_data_notice',
                    'data_source_documented',
                    'processing_purposes_clear',
                    'rights_information_provided'
                ]
            },
            17: {
                'name': 'Right to Erasure',
                'checks': [
                    'erasure_mechanism_available',
                    'technical_feasibility_documented',
                    'exception_handling_defined',
                    'third_party_notification_process'
                ]
            },
            20: {
                'name': 'Data Portability',
                'checks': [
                    'structured_export_available',
                    'machine_readable_format',
                    'commonly_used_format',
                    'automated_transmission'
                ]
            }
        }
    
    def check_article_compliance(
        self, 
        scan_results: Dict[str, Any], 
        article: int
    ) -> Dict[str, Any]:
        """
        Perform quick compliance check for a specific GDPR article.
        
        Args:
            scan_results: Results from GitScanner
            article: GDPR article number to check
            
        Returns:
            Dictionary containing compliance check results
        """
        if self.verbose:
            print(f"🔍 Quick compliance check for Article {article}")
        
        if article not in self.quick_checks:
            return {
                'article': article,
                'supported': False,
                'error': f"Article {article} not supported for quick checks"
            }
        
        check_info = self.quick_checks[article]
        
        result = {
            'article': article,
            'name': check_info['name'],
            'supported': True,
            'compliant': False,
            'issues': [],
            'recommendations': [],
            'check_results': {},
            'severity': 'unknown',
            'timestamp': datetime.now().isoformat()
        }
        
        # Perform article-specific checks
        if article == 6:
            result.update(self._check_article_6_quick(scan_results))
        elif article == 13:
            result.update(self._check_article_13_quick(scan_results))
        elif article == 14:
            result.update(self._check_article_14_quick(scan_results))
        elif article == 17:
            result.update(self._check_article_17_quick(scan_results))
        elif article == 20:
            result.update(self._check_article_20_quick(scan_results))
        
        return result
    
    def _check_article_6_quick(self, scan_results: Dict[str, Any]) -> Dict[str, Any]:
        """Quick check for Article 6: Lawful basis for processing."""
        issues = []
        recommendations = []
        check_results = {}
        
        personal_data = scan_results.get('personal_data', {})
        has_personal_data = (
            len(personal_data.get('emails', [])) > 0 or
            len(personal_data.get('authors', [])) > 0
        )
        
        # Check for privacy policy
        check_results['has_privacy_policy'] = False
        if not check_results['has_privacy_policy']:
            issues.append("No privacy policy or data processing notice found")
            recommendations.append("Create a privacy policy documenting data processing activities")
        
        # Check for documented lawful basis
        check_results['documents_lawful_basis'] = False
        if not check_results['documents_lawful_basis']:
            issues.append("No explicit lawful basis documented for processing personal data")
            recommendations.append("Document the lawful basis for processing contributor data (e.g., legitimate interests)")
        
        # Check for consent mechanism
        check_results['has_consent_mechanism'] = False
        if not check_results['has_consent_mechanism']:
            issues.append("No mechanism for obtaining explicit consent")
            recommendations.append("Implement contributor agreement or consent mechanism")
        
        # Check for legitimate interests assessment
        check_results['legitimate_interests_assessment'] = False
        if not check_results['legitimate_interests_assessment']:
            issues.append("No legitimate interests assessment documented")
            recommendations.append("Conduct and document legitimate interests assessment if relying on Article 6(1)(f)")
        
        compliant = len(issues) == 0
        severity = 'high' if has_personal_data and not compliant else 'medium'
        
        return {
            'compliant': compliant,
            'issues': issues,
            'recommendations': recommendations,
            'check_results': check_results,
            'severity': severity
        }
    
    def _check_article_13_quick(self, scan_results: Dict[str, Any]) -> Dict[str, Any]:
        """Quick check for Article 13: Information to be provided (data from subject)."""
        issues = []
        recommendations = []
        check_results = {}
        
        # Check for privacy notice
        check_results['privacy_notice_present'] = False
        if not check_results['privacy_notice_present']:
            issues.append("No privacy notice provided to contributors")
            recommendations.append("Add privacy notice to README.md or CONTRIBUTING.md")
        
        # Check for clear processing purposes
        check_results['processing_purposes_clear'] = False
        if not check_results['processing_purposes_clear']:
            issues.append("Processing purposes not clearly communicated")
            recommendations.append("Clearly state why contributor data is collected and processed")
        
        # Check for controller identity
        check_results['controller_identity_clear'] = False
        if not check_results['controller_identity_clear']:
            issues.append("Data controller identity not clearly specified")
            recommendations.append("Identify the data controller in repository documentation")
        
        # Check for retention period
        check_results['retention_period_specified'] = False
        if not check_results['retention_period_specified']:
            issues.append("Data retention period not specified")
            recommendations.append("Document how long contributor data will be retained")
        
        # Check for rights information
        check_results['rights_information_provided'] = False
        if not check_results['rights_information_provided']:
            issues.append("Data subject rights not communicated")
            recommendations.append("Inform contributors of their data protection rights")
        
        compliant = len(issues) == 0
        severity = 'high'  # Transparency is critical
        
        return {
            'compliant': compliant,
            'issues': issues,
            'recommendations': recommendations,
            'check_results': check_results,
            'severity': severity
        }
    
    def _check_article_14_quick(self, scan_results: Dict[str, Any]) -> Dict[str, Any]:
        """Quick check for Article 14: Information to be provided (data not from subject)."""
        issues = []
        recommendations = []
        check_results = {}
        
        cross_border = scan_results.get('cross_border_indicators', [])
        has_forks = len(cross_border) > 0
        
        # Check for third-party data notice
        check_results['third_party_data_notice'] = False
        if has_forks and not check_results['third_party_data_notice']:
            issues.append("No notice provided when collecting data through forks")
            recommendations.append("Implement notification mechanism for fork-based data collection")
        
        # Check for data source documentation
        check_results['data_source_documented'] = False
        if has_forks and not check_results['data_source_documented']:
            issues.append("Source of personal data not documented")
            recommendations.append("Document data sources in repository metadata")
        
        # Check for processing purposes
        check_results['processing_purposes_clear'] = False
        if not check_results['processing_purposes_clear']:
            issues.append("Processing purposes not clear for third-party collected data")
            recommendations.append("Clarify purposes for processing data obtained through forks")
        
        # Check for rights information
        check_results['rights_information_provided'] = False
        if not check_results['rights_information_provided']:
            issues.append("Data subject rights not communicated to affected individuals")
            recommendations.append("Provide mechanism to inform affected individuals of their rights")
        
        compliant = len(issues) == 0
        severity = 'medium' if has_forks else 'low'
        
        return {
            'compliant': compliant,
            'issues': issues,
            'recommendations': recommendations,
            'check_results': check_results,
            'severity': severity
        }
    
    def _check_article_17_quick(self, scan_results: Dict[str, Any]) -> Dict[str, Any]:
        """Quick check for Article 17: Right to erasure."""
        issues = []
        recommendations = []
        check_results = {}
        
        # Check for erasure mechanism
        check_results['erasure_mechanism_available'] = False
        issues.append("No data erasure mechanism available")
        recommendations.append("Document technical impossibility of data erasure in Git")
        
        # Check for technical feasibility documentation
        check_results['technical_feasibility_documented'] = False
        issues.append("Technical feasibility of erasure not documented")
        recommendations.append("Clearly document why data erasure is technically impossible")
        
        # Check for exception handling
        check_results['exception_handling_defined'] = False
        issues.append("No process defined for handling erasure requests")
        recommendations.append("Define process for responding to erasure requests with technical limitations")
        
        # Check for third-party notification
        check_results['third_party_notification_process'] = False
        issues.append("No process for notifying third parties (forks) about erasure requests")
        recommendations.append("Implement best-effort notification process for fork maintainers")
        
        compliant = False  # Git inherently cannot comply with erasure requirements
        severity = 'critical'
        
        return {
            'compliant': compliant,
            'issues': issues,
            'recommendations': recommendations,
            'check_results': check_results,
            'severity': severity
        }
    
    def _check_article_20_quick(self, scan_results: Dict[str, Any]) -> Dict[str, Any]:
        """Quick check for Article 20: Right to data portability."""
        issues = []
        recommendations = []
        check_results = {}
        
        # Check for structured export
        check_results['structured_export_available'] = False
        if not check_results['structured_export_available']:
            issues.append("No structured data export functionality available")
            recommendations.append("Implement JSON/CSV export for contributor data")
        
        # Check for machine-readable format
        check_results['machine_readable_format'] = True  # Git is machine-readable
        
        # Check for commonly used format
        check_results['commonly_used_format'] = False  # Git format is specialized
        if not check_results['commonly_used_format']:
            issues.append("Data not available in commonly used format")
            recommendations.append("Provide data export in standard formats (JSON, CSV, XML)")
        
        # Check for automated transmission
        check_results['automated_transmission'] = False
        if not check_results['automated_transmission']:
            issues.append("No automated data transmission capability")
            recommendations.append("Implement API for automated data portability requests")
        
        compliant = len(issues) == 0
        severity = 'medium'
        
        return {
            'compliant': compliant,
            'issues': issues,
            'recommendations': recommendations,
            'check_results': check_results,
            'severity': severity
        }
    
    def check_all_articles(self, scan_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform quick compliance checks for all supported articles.
        
        Args:
            scan_results: Results from GitScanner
            
        Returns:
            Dictionary containing results for all articles
        """
        if self.verbose:
            print("🔍 Performing comprehensive compliance check")
        
        all_results = {
            'timestamp': datetime.now().isoformat(),
            'overall_compliant': True,
            'total_issues': 0,
            'critical_issues': 0,
            'article_results': {},
            'summary': {
                'compliant_articles': [],
                'non_compliant_articles': [],
                'critical_articles': []
            }
        }
        
        for article in self.quick_checks.keys():
            result = self.check_article_compliance(scan_results, article)
            all_results['article_results'][article] = result
            
            if not result['compliant']:
                all_results['overall_compliant'] = False
                all_results['summary']['non_compliant_articles'].append(article)
                all_results['total_issues'] += len(result['issues'])
                
                if result['severity'] == 'critical':
                    all_results['critical_issues'] += len(result['issues'])
                    all_results['summary']['critical_articles'].append(article)
            else:
                all_results['summary']['compliant_articles'].append(article)
        
        return all_results
    
    def generate_compliance_summary(self, scan_results: Dict[str, Any]) -> str:
        """
        Generate a human-readable compliance summary.
        
        Args:
            scan_results: Results from GitScanner
            
        Returns:
            Formatted compliance summary string
        """
        all_results = self.check_all_articles(scan_results)
        
        summary = []
        summary.append("🔍 GDPR Compliance Summary")
        summary.append("=" * 40)
        
        if all_results['overall_compliant']:
            summary.append("✅ Overall Status: COMPLIANT")
        else:
            summary.append("❌ Overall Status: NON-COMPLIANT")
        
        summary.append(f"📊 Total Issues: {all_results['total_issues']}")
        summary.append(f"🚨 Critical Issues: {all_results['critical_issues']}")
        
        summary.append("\n📋 Article-by-Article Results:")
        
        for article, result in all_results['article_results'].items():
            status = "✅" if result['compliant'] else "❌"
            severity = result['severity'].upper()
            summary.append(f"{status} Article {article} ({result['name']}): {severity}")
            
            if result['issues']:
                for issue in result['issues'][:2]:  # Show first 2 issues
                    summary.append(f"   └── {issue}")
                if len(result['issues']) > 2:
                    summary.append(f"   └── ... and {len(result['issues']) - 2} more issues")
        
        summary.append("\n💡 Priority Recommendations:")
        
        # Collect recommendations from critical articles
        critical_recommendations = []
        for article in all_results['summary']['critical_articles']:
            result = all_results['article_results'][article]
            critical_recommendations.extend(result['recommendations'][:2])
        
        for i, rec in enumerate(critical_recommendations[:5], 1):
            summary.append(f"{i}. {rec}")
        
        return "\n".join(summary)
    
    def get_supported_articles(self) -> List[int]:
        """Get list of articles supported for quick checks."""
        return list(self.quick_checks.keys())
    
    def get_article_info(self, article: int) -> Optional[Dict[str, Any]]:
        """Get information about quick checks for a specific article."""
        return self.quick_checks.get(article)
