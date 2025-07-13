# Installation Guide

## Quick Start

For most users, the basic installation provides all core functionality:

```bash
pip install gdpr-git-validator
```

## Installation Options

### Core Installation (Recommended)
```bash
pip install gdpr-git-validator
```

**Includes:**
- Git repository scanning
- GDPR compliance analysis
- HTML and JSON report generation
- CLI interface
- Basic text summaries

### Full Installation
```bash
pip install gdpr-git-validator[full]
```

**Adds:**
- Advanced data visualization
- Enhanced statistical analysis
- PDF report generation (basic)
- Data export capabilities

### PDF Reports
```bash
pip install gdpr-git-validator[pdf]
```

**Adds:**
- Professional PDF report generation
- Requires system dependencies (see below)

### Data Analysis Features
```bash
pip install gdpr-git-validator[analysis]
```

**Adds:**
- Advanced data visualization with matplotlib/seaborn
- Statistical analysis capabilities
- Data export to CSV/Excel formats

### Development Installation
```bash
pip install gdpr-git-validator[dev]
```

**Adds:**
- Testing framework (pytest)
- Code quality tools (black, flake8, isort)
- Security scanning tools (bandit, safety)
- Type checking (mypy)

## System Dependencies

### For PDF Generation

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y \
    build-essential \
    python3-dev \
    python3-pip \
    python3-cffi \
    python3-brotli \
    libpango-1.0-0 \
    libharfbuzz0b \
    libpangoft2-1.0-0 \
    libfontconfig1 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info
```

**CentOS/RHEL/Fedora:**
```bash
sudo yum install -y \
    gcc \
    python3-devel \
    python3-pip \
    python3-cffi \
    pango \
    libffi-devel \
    cairo \
    gdk-pixbuf2
```

**macOS:**
```bash
brew install cairo pango gdk-pixbuf libffi
```

**Windows:**
PDF generation on Windows requires additional setup. Consider using the HTML reports instead, or use Docker.

## Docker Installation

For a consistent environment across all platforms:

```bash
docker pull gdprvalidator/eu-gdpr-git-validator:latest
docker run -v /path/to/your/repo:/repo gdprvalidator/eu-gdpr-git-validator scan /repo
```

## Troubleshooting

### Common Issues

**ImportError: No module named 'weasyprint'**
- Solution: Install PDF dependencies or use HTML reports instead

**Permission denied errors**
- Solution: Use `--user` flag: `pip install --user gdpr-git-validator`

**SSL certificate errors**
- Solution: Update certificates or use `--trusted-host pypi.org --trusted-host pypi.python.org`

### Minimal Installation

If you encounter dependency issues, try the minimal core installation:

```bash
pip install --no-deps gdpr-git-validator
pip install GitPython jinja2 click requests
```

This installs only the essential dependencies needed for basic functionality.

## Verification

Test your installation:

```bash
gdpr-validator --version
gdpr-validator --help
```

## Upgrading

```bash
pip install --upgrade gdpr-git-validator
```

To upgrade with all optional dependencies:

```bash
pip install --upgrade gdpr-git-validator[full]
