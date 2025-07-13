# Contributing to EU GDPR Git Validator

Thank you for your interest in contributing to the EU GDPR Git Validator! This project aims to help developers understand and address GDPR compliance issues in Git repositories.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Guidelines](#contributing-guidelines)
- [Testing](#testing)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)
- [GDPR Compliance Notice](#gdpr-compliance-notice)

## Code of Conduct

This project adheres to a code of conduct that promotes an inclusive and respectful environment. By participating, you agree to uphold these standards.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/EU-GDPR-Git-Validator.git
   cd EU-GDPR-Git-Validator
   ```

3. **Set up the development environment** (see below)

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- pip

### Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install the package in development mode:
   ```bash
   pip install -e .
   pip install -r requirements-dev.txt  # If available
   ```

3. Install development dependencies:
   ```bash
   pip install pytest pytest-cov black isort flake8 mypy
   ```

### Verify Installation

Run the tool to ensure it's working:
```bash
gdpr-validator --help
```

## Contributing Guidelines

### Types of Contributions

We welcome various types of contributions:

- **Bug reports** - Help us identify and fix issues
- **Feature requests** - Suggest new functionality
- **Code contributions** - Implement features or fix bugs
- **Documentation** - Improve or add documentation
- **GDPR expertise** - Help improve compliance analysis
- **Testing** - Add or improve test coverage

### Before You Start

1. **Check existing issues** to avoid duplicating work
2. **Create an issue** for significant changes to discuss the approach
3. **Follow the coding standards** outlined below

### Coding Standards

#### Python Code Style

- Follow **PEP 8** style guidelines
- Use **Black** for code formatting:
  ```bash
  black src tests
  ```
- Use **isort** for import sorting:
  ```bash
  isort src tests
  ```
- Use **flake8** for linting:
  ```bash
  flake8 src tests
  ```

#### Code Quality

- Write **clear, self-documenting code**
- Add **docstrings** for all public functions and classes
- Use **type hints** where appropriate
- Follow **SOLID principles**
- Keep functions **small and focused**

#### GDPR Analysis Guidelines

When contributing to GDPR analysis features:

- **Cite relevant GDPR articles** in comments and documentation
- **Provide clear explanations** of compliance requirements
- **Include practical recommendations** for remediation
- **Consider edge cases** and different repository structures
- **Test with various Git configurations**

### Git Workflow

1. **Create a feature branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** with clear, atomic commits
3. **Write descriptive commit messages**:
   ```
   feat: add Article 20 data portability analysis
   
   - Implement structured data export functionality
   - Add JSON/CSV export options for personal data
   - Include compliance recommendations
   
   Closes #123
   ```

4. **Push to your fork** and create a pull request

### Commit Message Format

Use conventional commits format:
- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `test:` - Test additions or modifications
- `refactor:` - Code refactoring
- `style:` - Code style changes
- `chore:` - Maintenance tasks

## Testing

### Running Tests

Run the full test suite:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=src/gdpr_validator --cov-report=html
```

Run specific tests:
```bash
pytest tests/test_specific_module.py
```

### Writing Tests

- **Write tests** for all new functionality
- **Maintain high test coverage** (aim for >90%)
- **Use descriptive test names** that explain what is being tested
- **Include edge cases** and error conditions
- **Mock external dependencies** appropriately

### Test Categories

1. **Unit tests** - Test individual components
2. **Integration tests** - Test component interactions
3. **End-to-end tests** - Test complete workflows
4. **GDPR compliance tests** - Verify analysis accuracy

## Documentation

### Types of Documentation

- **Code documentation** - Docstrings and inline comments
- **User documentation** - README, usage guides
- **API documentation** - Function and class documentation
- **GDPR guidance** - Compliance explanations and recommendations

### Documentation Standards

- Use **clear, concise language**
- **Provide examples** where helpful
- **Keep documentation up-to-date** with code changes
- **Include GDPR article references** where relevant

## Submitting Changes

### Pull Request Process

1. **Ensure all tests pass**:
   ```bash
   pytest
   black --check src tests
   isort --check-only src tests
   flake8 src tests
   ```

2. **Update documentation** as needed
3. **Add tests** for new functionality
4. **Create a pull request** with:
   - Clear title and description
   - Reference to related issues
   - Summary of changes
   - Testing performed

### Pull Request Template

```markdown
## Description
Brief description of changes

## Related Issues
Closes #123

## Changes Made
- List of specific changes
- New features added
- Bugs fixed

## Testing
- [ ] All existing tests pass
- [ ] New tests added for new functionality
- [ ] Manual testing performed

## GDPR Impact
- Description of any GDPR analysis changes
- New compliance checks added
- Updated recommendations

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
```

### Review Process

1. **Automated checks** must pass (CI/CD pipeline)
2. **Code review** by maintainers
3. **GDPR expertise review** for compliance-related changes
4. **Testing verification**
5. **Documentation review**

## GDPR Compliance Notice

### Data Processing in Contributions

By contributing to this project, you acknowledge that:

- Your **Git commit metadata** (name, email, timestamps) will be processed
- This data becomes part of the **public Git history**
- The data may be **replicated across forks** and mirrors
- **Complete erasure** of this data is technically impossible due to Git's distributed nature

### Contributor Rights

As a contributor, you have the right to:

- **Access** your personal data in the repository
- **Rectification** of inaccurate information where technically possible
- **Information** about how your data is processed
- **Portability** of your contribution data

### Data Minimization

To minimize personal data exposure:

- Consider using a **pseudonymous Git identity**
- Use a **dedicated email** for open source contributions
- Be mindful of **personal information** in commit messages
- Avoid including **sensitive data** in code or comments

### Contact for Data Protection

For data protection inquiries related to your contributions, please contact the project maintainers through GitHub issues or the designated contact method.

## Getting Help

- **GitHub Issues** - For bugs and feature requests
- **Discussions** - For questions and general discussion
- **Documentation** - Check existing documentation first
- **Code Review** - Learn from feedback on pull requests

## Recognition

Contributors are recognized in:
- **CONTRIBUTORS.md** file
- **Release notes** for significant contributions
- **GitHub contributors** page

Thank you for contributing to making Git repositories more GDPR compliant!
