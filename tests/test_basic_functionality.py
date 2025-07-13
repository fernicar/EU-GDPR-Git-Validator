"""
Basic functionality tests for EU GDPR Git Validator

Tests core components to ensure they can be imported and instantiated correctly.
"""

import pytest
import sys
from pathlib import Path

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from gdpr_validator import GitScanner, GDPRAnalyser, ReportGenerator, ComplianceChecker


class TestBasicFunctionality:
    """Test basic functionality of core components."""
    
    def test_imports(self):
        """Test that all modules can be imported successfully."""
        from gdpr_validator.git_scanner import GitScanner
        from gdpr_validator.gdpr_analyser import GDPRAnalyser
        from gdpr_validator.report_generator import ReportGenerator
        from gdpr_validator.compliance_checker import ComplianceChecker
        
        assert GitScanner is not None
        assert GDPRAnalyser is not None
        assert ReportGenerator is not None
        assert ComplianceChecker is not None
    
    def test_gdpr_analyser_initialization(self):
        """Test GDPRAnalyser can be initialized."""
        analyser = GDPRAnalyser(verbose=False)
        assert analyser is not None
        assert analyser.verbose is False
        
        # Test supported articles
        supported_articles = analyser.get_supported_articles()
        assert isinstance(supported_articles, list)
        assert 6 in supported_articles
        assert 17 in supported_articles
    
    def test_compliance_checker_initialization(self):
        """Test ComplianceChecker can be initialized."""
        checker = ComplianceChecker(verbose=False)
        assert checker is not None
        assert checker.verbose is False
        
        # Test supported articles
        supported_articles = checker.get_supported_articles()
        assert isinstance(supported_articles, list)
        assert len(supported_articles) > 0
    
    def test_report_generator_initialization(self):
        """Test ReportGenerator can be initialized."""
        generator = ReportGenerator(verbose=False)
        assert generator is not None
        assert generator.verbose is False
    
    def test_gdpr_article_info(self):
        """Test GDPR article information retrieval."""
        analyser = GDPRAnalyser()
        
        # Test Article 6 info
        article_6_info = analyser.get_article_info(6)
        assert article_6_info is not None
        assert 'title' in article_6_info
        assert 'Lawful basis' in article_6_info['title']
        
        # Test Article 17 info
        article_17_info = analyser.get_article_info(17)
        assert article_17_info is not None
        assert 'title' in article_17_info
        assert 'erasure' in article_17_info['title'].lower()
    
    def test_mock_compliance_analysis(self):
        """Test compliance analysis with mock data."""
        analyser = GDPRAnalyser(verbose=False)
        
        # Mock scan results
        mock_scan_results = {
            'repository_path': '/test/repo',
            'scan_timestamp': '2025-07-13T19:00:00',
            'total_commits': 10,
            'total_branches': 2,
            'personal_data': {
                'emails': ['test@example.com'],
                'authors': ['Test Author <test@example.com>'],
                'committers': ['Test Author <test@example.com>'],
                'potential_pii': []
            },
            'cross_border_indicators': [],
            'hash_analysis': {},
            'data_retention': {}
        }
        
        # Test compliance analysis
        compliance_results = analyser.analyze_compliance(mock_scan_results, articles=[6, 17])
        
        assert compliance_results is not None
        assert 'overall_compliance' in compliance_results
        assert 'violations' in compliance_results
        assert 'article_results' in compliance_results
        assert 6 in compliance_results['article_results']
        assert 17 in compliance_results['article_results']
        
        # Article 17 should always be non-compliant due to Git's nature
        article_17_result = compliance_results['article_results'][17]
        assert article_17_result['compliant'] is False
    
    def test_mock_report_generation(self):
        """Test report generation with mock data."""
        generator = ReportGenerator(verbose=False)
        
        # Mock data
        mock_scan_results = {
            'repository_path': '/test/repo',
            'scan_timestamp': '2025-07-13T19:00:00',
            'total_commits': 5,
            'total_branches': 1,
            'personal_data': {
                'emails': ['test@example.com'],
                'authors': ['Test Author'],
                'committers': ['Test Author'],
                'potential_pii': []
            }
        }
        
        mock_compliance_results = {
            'overall_compliance': False,
            'violations': [
                {
                    'type': 'test_violation',
                    'description': 'Test violation description',
                    'article': '17',
                    'severity': 'critical'
                }
            ],
            'article_results': {
                17: {
                    'title': 'Right to erasure',
                    'compliant': False,
                    'violations': [],
                    'recommendations': ['Test recommendation'],
                    'severity': 'critical'
                }
            },
            'severity_level': 'critical'
        }
        
        # Test summary generation
        summary = generator.generate_summary_report(mock_scan_results, mock_compliance_results)
        assert isinstance(summary, str)
        assert 'GDPR Compliance Summary' in summary
        assert 'NON-COMPLIANT' in summary
    
    def test_fork_analysis_simulation(self):
        """Test fork analysis simulation."""
        analyser = GDPRAnalyser(verbose=False)
        
        # Test with local repository (should simulate)
        fork_results = analyser.analyze_fork_impact('/local/repo/path')
        
        assert fork_results is not None
        assert 'total_forks' in fork_results
        assert 'erasure_impossible' in fork_results
        assert fork_results['erasure_impossible'] is True  # Always true for Git
    
    def test_compliance_checker_quick_check(self):
        """Test compliance checker quick checks."""
        checker = ComplianceChecker(verbose=False)
        
        # Mock scan results
        mock_scan_results = {
            'personal_data': {
                'emails': ['test@example.com'],
                'authors': ['Test Author'],
                'committers': ['Test Author'],
                'potential_pii': []
            },
            'cross_border_indicators': []
        }
        
        # Test Article 17 quick check (should always fail)
        result = checker.check_article_compliance(mock_scan_results, 17)
        
        assert result is not None
        assert result['article'] == 17
        assert result['supported'] is True
        assert result['compliant'] is False  # Git cannot comply with erasure
        assert 'issues' in result
        assert len(result['issues']) > 0


if __name__ == "__main__":
    pytest.main([__file__])
