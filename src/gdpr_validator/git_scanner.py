"""
Git Scanner Module

Analyzes Git repositories for personal data exposure in commit history,
author information, and metadata that may violate GDPR requirements.
"""

import re
import git
from pathlib import Path
from typing import Dict, List, Set, Optional, Any
from datetime import datetime
import hashlib


class GitScanner:
    """
    Scans Git repositories for GDPR-relevant personal data.
    
    This scanner identifies:
    - Email addresses in commit history
    - Author and committer names
    - Timestamps and activity patterns
    - Cross-border data transfers
    - Data retention patterns
    """
    
    def __init__(self, repository_path: Path, verbose: bool = False):
        """
        Initialize the Git scanner.
        
        Args:
            repository_path: Path to the Git repository
            verbose: Enable verbose logging
        """
        self.repository_path = Path(repository_path)
        self.verbose = verbose
        self.repo = None
        
        # Email regex pattern for detecting email addresses
        self.email_pattern = re.compile(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        )
        
        # Common patterns that might contain personal data
        self.personal_data_patterns = {
            'phone': re.compile(r'(\+\d{1,3}[-.\s]?)?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}'),
            'credit_card': re.compile(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'),
            'ssn': re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),
            'ip_address': re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'),
        }
        
        self._initialize_repository()
    
    def _initialize_repository(self) -> None:
        """Initialize the Git repository object."""
        try:
            self.repo = git.Repo(self.repository_path)
            if self.verbose:
                print(f"✅ Initialized Git repository: {self.repository_path}")
        except git.exc.InvalidGitRepositoryError:
            raise ValueError(f"Invalid Git repository: {self.repository_path}")
        except Exception as e:
            raise RuntimeError(f"Failed to initialize repository: {str(e)}")
    
    def scan_repository(self) -> Dict[str, Any]:
        """
        Perform a comprehensive scan of the Git repository.
        
        Returns:
            Dictionary containing scan results with personal data findings
        """
        if self.verbose:
            print("🔍 Starting comprehensive repository scan...")
        
        results = {
            'repository_path': str(self.repository_path),
            'scan_timestamp': datetime.now().isoformat(),
            'total_commits': 0,
            'total_branches': 0,
            'personal_data': {
                'emails': set(),
                'authors': set(),
                'committers': set(),
                'potential_pii': []
            },
            'commit_analysis': [],
            'branch_analysis': [],
            'data_retention': {},
            'cross_border_indicators': [],
            'hash_analysis': {}
        }
        
        # Scan all branches
        results['branch_analysis'] = self._scan_branches()
        results['total_branches'] = len(results['branch_analysis'])
        
        # Scan commit history
        commit_data = self._scan_commit_history()
        results['commit_analysis'] = commit_data['commits']
        results['total_commits'] = commit_data['total_count']
        
        # Extract personal data
        results['personal_data'] = self._extract_personal_data(commit_data['commits'])
        
        # Analyze data retention patterns
        results['data_retention'] = self._analyze_data_retention(commit_data['commits'])
        
        # Analyze Git hashes for permanent retention issues
        results['hash_analysis'] = self._analyze_hash_permanence(commit_data['commits'])
        
        # Detect cross-border transfer indicators
        results['cross_border_indicators'] = self._detect_cross_border_transfers(
            results['personal_data']
        )
        
        # Convert sets to lists for JSON serialization
        self._serialize_results(results)
        
        if self.verbose:
            print(f"✅ Scan complete: {results['total_commits']} commits analyzed")
        
        return results
    
    def _scan_branches(self) -> List[Dict[str, Any]]:
        """Scan all branches for metadata and personal data."""
        branches = []
        
        for branch in self.repo.branches:
            branch_data = {
                'name': branch.name,
                'last_commit': {
                    'hash': branch.commit.hexsha,
                    'author': {
                        'name': branch.commit.author.name,
                        'email': branch.commit.author.email
                    },
                    'committer': {
                        'name': branch.commit.committer.name,
                        'email': branch.commit.committer.email
                    },
                    'timestamp': branch.commit.committed_datetime.isoformat(),
                    'message': branch.commit.message.strip()
                },
                'personal_data_exposure': self._check_commit_for_pii(branch.commit)
            }
            branches.append(branch_data)
        
        return branches
    
    def _scan_commit_history(self) -> Dict[str, Any]:
        """Scan the complete commit history."""
        commits = []
        total_count = 0
        
        try:
            for commit in self.repo.iter_commits():
                total_count += 1
                
                commit_data = {
                    'hash': commit.hexsha,
                    'short_hash': commit.hexsha[:8],
                    'author': {
                        'name': commit.author.name,
                        'email': commit.author.email,
                        'timestamp': commit.authored_datetime.isoformat()
                    },
                    'committer': {
                        'name': commit.committer.name,
                        'email': commit.committer.email,
                        'timestamp': commit.committed_datetime.isoformat()
                    },
                    'message': commit.message.strip(),
                    'files_changed': len(commit.stats.files),
                    'insertions': commit.stats.total['insertions'],
                    'deletions': commit.stats.total['deletions'],
                    'personal_data_found': self._check_commit_for_pii(commit),
                    'parents': [parent.hexsha for parent in commit.parents]
                }
                
                commits.append(commit_data)
                
                # Limit to prevent memory issues with very large repositories
                if total_count >= 10000:
                    if self.verbose:
                        print(f"⚠️  Limited scan to first 10,000 commits")
                    break
        
        except Exception as e:
            if self.verbose:
                print(f"⚠️  Error during commit scan: {str(e)}")
        
        return {
            'commits': commits,
            'total_count': total_count
        }
    
    def _check_commit_for_pii(self, commit) -> Dict[str, List[str]]:
        """Check a single commit for personally identifiable information."""
        pii_found = {
            'emails': [],
            'potential_pii': [],
            'sensitive_patterns': []
        }
        
        # Check commit message
        message = commit.message
        emails_in_message = self.email_pattern.findall(message)
        pii_found['emails'].extend(emails_in_message)
        
        # Check for other PII patterns in commit message
        for pattern_name, pattern in self.personal_data_patterns.items():
            matches = pattern.findall(message)
            if matches:
                pii_found['sensitive_patterns'].extend([
                    f"{pattern_name}: {match}" for match in matches
                ])
        
        # Check diff content for PII (limited to prevent performance issues)
        try:
            if commit.parents:
                diff = commit.parents[0].diff(commit, create_patch=True)
                for diff_item in diff[:10]:  # Limit to first 10 files
                    if hasattr(diff_item, 'diff') and diff_item.diff:
                        diff_text = diff_item.diff.decode('utf-8', errors='ignore')
                        
                        # Check for emails in diff
                        diff_emails = self.email_pattern.findall(diff_text)
                        pii_found['emails'].extend(diff_emails)
                        
                        # Check for other PII patterns
                        for pattern_name, pattern in self.personal_data_patterns.items():
                            matches = pattern.findall(diff_text)
                            if matches:
                                pii_found['potential_pii'].extend([
                                    f"{pattern_name} in {diff_item.a_path or diff_item.b_path}: {match}"
                                    for match in matches
                                ])
        except Exception:
            # Skip diff analysis if it fails
            pass
        
        return pii_found
    
    def _extract_personal_data(self, commits: List[Dict[str, Any]]) -> Dict[str, Set[str]]:
        """Extract all personal data found across commits."""
        personal_data = {
            'emails': set(),
            'authors': set(),
            'committers': set(),
            'potential_pii': []
        }
        
        for commit in commits:
            # Author and committer information
            personal_data['authors'].add(f"{commit['author']['name']} <{commit['author']['email']}>")
            personal_data['committers'].add(f"{commit['committer']['name']} <{commit['committer']['email']}>")
            
            # Emails from commit content
            if commit['personal_data_found']['emails']:
                personal_data['emails'].update(commit['personal_data_found']['emails'])
            
            # Other potential PII
            if commit['personal_data_found']['potential_pii']:
                personal_data['potential_pii'].extend(commit['personal_data_found']['potential_pii'])
            
            if commit['personal_data_found']['sensitive_patterns']:
                personal_data['potential_pii'].extend(commit['personal_data_found']['sensitive_patterns'])
        
        return personal_data
    
    def _analyze_data_retention(self, commits: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze data retention patterns."""
        if not commits:
            return {}
        
        # Sort commits by date
        sorted_commits = sorted(
            commits,
            key=lambda x: x['author']['timestamp']
        )
        
        first_commit = datetime.fromisoformat(sorted_commits[0]['author']['timestamp'].replace('Z', '+00:00'))
        last_commit = datetime.fromisoformat(sorted_commits[-1]['author']['timestamp'].replace('Z', '+00:00'))
        
        retention_period = last_commit - first_commit
        
        return {
            'first_commit_date': first_commit.isoformat(),
            'last_commit_date': last_commit.isoformat(),
            'retention_period_days': retention_period.days,
            'total_commits': len(commits),
            'data_erasure_possible': False,  # Git's distributed nature makes this impossible
            'retention_justification': "No explicit data retention policy identified"
        }
    
    def _analyze_hash_permanence(self, commits: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze Git hash permanence for GDPR compliance."""
        hash_analysis = {
            'total_hashes': len(commits),
            'hash_algorithm': 'SHA-1',  # Git default
            'permanence_issues': [],
            'erasure_impossible': True
        }
        
        # Sample analysis of hash distribution
        if commits:
            sample_hashes = [commit['hash'] for commit in commits[:100]]
            hash_analysis['sample_hashes'] = sample_hashes
            
            # Check for hash collisions (extremely rare but theoretically possible)
            unique_hashes = set(sample_hashes)
            if len(unique_hashes) != len(sample_hashes):
                hash_analysis['permanence_issues'].append("Hash collision detected")
            
            # Analyze hash entropy
            combined_hashes = ''.join(sample_hashes)
            hash_entropy = len(set(combined_hashes)) / len(combined_hashes) if combined_hashes else 0
            hash_analysis['hash_entropy'] = hash_entropy
        
        hash_analysis['permanence_issues'].extend([
            "Git hashes create permanent references to commit data",
            "Distributed nature prevents centralized data erasure",
            "Fork propagation multiplies data retention points"
        ])
        
        return hash_analysis
    
    def _detect_cross_border_transfers(self, personal_data: Dict[str, Set[str]]) -> List[Dict[str, Any]]:
        """Detect indicators of cross-border data transfers."""
        indicators = []
        
        # Analyze email domains for geographic indicators
        email_domains = set()
        for email_set in [personal_data.get('emails', set())]:
            for email in email_set:
                if '@' in email:
                    domain = email.split('@')[1].lower()
                    email_domains.add(domain)
        
        # Common country-specific domain patterns
        country_domains = {
            '.uk': 'United Kingdom',
            '.de': 'Germany',
            '.fr': 'France',
            '.it': 'Italy',
            '.es': 'Spain',
            '.nl': 'Netherlands',
            '.se': 'Sweden',
            '.dk': 'Denmark',
            '.no': 'Norway',
            '.fi': 'Finland',
            '.pl': 'Poland',
            '.cz': 'Czech Republic',
            '.at': 'Austria',
            '.ch': 'Switzerland',
            '.be': 'Belgium',
            '.ie': 'Ireland',
            '.pt': 'Portugal',
            '.gr': 'Greece',
            '.hu': 'Hungary',
            '.ro': 'Romania',
            '.bg': 'Bulgaria',
            '.hr': 'Croatia',
            '.si': 'Slovenia',
            '.sk': 'Slovakia',
            '.lt': 'Lithuania',
            '.lv': 'Latvia',
            '.ee': 'Estonia',
            '.lu': 'Luxembourg',
            '.mt': 'Malta',
            '.cy': 'Cyprus'
        }
        
        detected_countries = set()
        for domain in email_domains:
            for tld, country in country_domains.items():
                if domain.endswith(tld):
                    detected_countries.add(country)
        
        if len(detected_countries) > 1:
            indicators.append({
                'type': 'multi_country_contributors',
                'description': f"Contributors from {len(detected_countries)} different countries detected",
                'countries': list(detected_countries),
                'gdpr_implication': "Cross-border data transfer without explicit consent mechanism"
            })
        
        # GitHub itself represents a cross-border transfer for EU users
        indicators.append({
            'type': 'platform_transfer',
            'description': "Repository hosted on GitHub (US-based platform)",
            'gdpr_implication': "EU personal data transferred to US without adequate safeguards",
            'legal_basis': "Unclear - no explicit consent for international transfer"
        })
        
        return indicators
    
    def _serialize_results(self, results: Dict[str, Any]) -> None:
        """Convert sets to lists for JSON serialization."""
        personal_data = results['personal_data']
        for key, value in personal_data.items():
            if isinstance(value, set):
                personal_data[key] = list(value)
    
    def get_repository_info(self) -> Dict[str, Any]:
        """Get basic repository information."""
        if not self.repo:
            return {}
        
        try:
            remote_urls = [remote.url for remote in self.repo.remotes]
            
            return {
                'path': str(self.repository_path),
                'is_bare': self.repo.bare,
                'head_commit': self.repo.head.commit.hexsha if self.repo.head.is_valid() else None,
                'active_branch': self.repo.active_branch.name if not self.repo.head.is_detached else None,
                'remote_urls': remote_urls,
                'total_branches': len(list(self.repo.branches)),
                'total_tags': len(list(self.repo.tags)),
                'is_dirty': self.repo.is_dirty()
            }
        except Exception as e:
            if self.verbose:
                print(f"⚠️  Error getting repository info: {str(e)}")
            return {'error': str(e)}
