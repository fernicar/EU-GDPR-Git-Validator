# EU GDPR Git Validator - Setup Guide

This document provides setup instructions for the EU GDPR Git Validator project.

## Quick Start

### Prerequisites

- Python 3.8 or higher
- Git
- pip

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/EU-GDPR-Git-Validator.git
   cd EU-GDPR-Git-Validator
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the package:**
   ```bash
   pip install -e .
   ```

4. **Install development dependencies (optional):**
   ```bash
   pip install pytest pytest-cov black isort flake8
   ```

### Basic Usage

```bash
# Show help
gdpr-validator --help

# Scan a repository
gdpr-validator scan /path/to/repository

# Generate HTML report
gdpr-validator scan /path/to/repository --output report.html --format html

# Analyze specific GDPR articles
gdpr-validator scan /path/to/repository --articles 6,17 --verbose
```

## Development Setup

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/gdpr_validator

# Run specific test file
pytest tests/test_basic_functionality.py -v
```

### Code Quality

```bash
# Format code
black src tests

# Sort imports
isort src tests

# Lint code
flake8 src tests
```

## Docker Usage

### Build Docker Image

```bash
docker build -t eu-gdpr-git-validator .
```

### Run with Docker

```bash
# Scan a repository
docker run --rm -v /path/to/repo:/app/data -v /path/to/output:/app/reports \
  eu-gdpr-git-validator scan /app/data --output /app/reports/report.html

# Interactive mode
docker run --rm -it -v /path/to/repo:/app/data \
  eu-gdpr-git-validator scan /app/data --verbose
```

## Project Structure

```
EU-GDPR-Git-Validator/
├── src/
│   └── gdpr_validator/
│       ├── __init__.py
│       ├── cli.py
│       ├── git_scanner.py
│       ├── gdpr_analyser.py
│       ├── compliance_checker.py
│       └── report_generator.py
├── tests/
│   ├── __init__.py
│   └── test_basic_functionality.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── README.md
├── LICENSE
├── requirements.txt
├── pyproject.toml
├── Dockerfile
├── .dockerignore
├── .gitignore
├── CONTRIBUTING.md
└── SETUP.md
```

## Features

- **Git Repository Scanning**: Analyzes commit history, branches, and metadata
- **GDPR Compliance Analysis**: Checks against Articles 6, 17, and others
- **Multiple Output Formats**: JSON, HTML, and text reports
- **CLI Interface**: Easy-to-use command-line tool
- **Docker Support**: Containerized deployment
- **CI/CD Pipeline**: Automated testing and deployment

## Supported GDPR Articles

- **Article 6**: Lawful basis for processing
- **Article 17**: Right to erasure ("right to be forgotten")
- **Article 20**: Right to data portability
- **Article 25**: Data protection by design and by default

## Configuration

The tool can be configured through:

1. **Command-line arguments**
2. **Environment variables**
3. **Configuration files** (future enhancement)

## Troubleshooting

### Common Issues

1. **Import errors**: Ensure the package is installed with `pip install -e .`
2. **Permission errors**: Check file permissions for the target repository
3. **Git errors**: Ensure the target directory is a valid Git repository

### Getting Help

- Check the [README.md](README.md) for detailed usage instructions
- Review [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines
- Open an issue on GitHub for bugs or feature requests

## Next Steps

1. **Initialize Git repository**: `git init`
2. **Add remote origin**: `git remote add origin <your-github-repo-url>`
3. **Make initial commit**: `git add . && git commit -m "Initial commit"`
4. **Push to GitHub**: `git push -u origin main`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
