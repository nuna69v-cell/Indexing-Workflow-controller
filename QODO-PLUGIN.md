# Qodo Plugin - Code Quality and Testing

## Overview

Qodo (formerly Codium AI) is an AI-powered code quality and testing plugin that helps generate meaningful tests, analyze code quality, and provide intelligent code suggestions.

## Features

- **Automated Test Generation**: Generate comprehensive unit tests for your code
- **Code Analysis**: Deep code quality analysis and suggestions
- **Test Coverage**: Analyze and improve test coverage
- **Bug Detection**: Identify potential bugs and edge cases
- **Code Review**: Automated code review with actionable feedback
- **Documentation**: Generate code documentation and docstrings

## Setup Instructions

### 1. Install Qodo Plugin

**For Visual Studio Code:**
```
1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X)
3. Search for "Qodo" or "Codium AI"
4. Click Install
```

**For JetBrains IDEs (PyCharm, IntelliJ, etc.):**
```
1. Open IDE Settings
2. Go to Plugins
3. Search for "Qodo" or "Codium AI"
4. Install and restart IDE
```

**For Cursor IDE:**
```
1. Qodo works with Cursor through VS Code extension compatibility
2. Install through Extensions panel
3. Configure in Cursor settings
```

### 2. Get API Key (Optional - Free tier available)

1. Visit [Qodo website](https://www.qodo.ai/)
2. Sign up or log in
3. Navigate to Settings → API Keys
4. Generate a new API key for enhanced features

### 3. Configure API Key

**Option A: Extension Settings**
```
1. Open extension settings
2. Find "Qodo: API Key"
3. Enter your API key
```

**Option B: Environment Variable**
```powershell
[System.Environment]::SetEnvironmentVariable('QODO_API_KEY', 'YOUR_API_KEY_HERE', 'User')
```

### 4. Configuration File

Create `qodo-config.json`:

```json
{
  "plugin_name": "Qodo",
  "provider": "qodo_ai",
  "features": {
    "test_generation": true,
    "code_analysis": true,
    "bug_detection": true,
    "documentation": true,
    "code_review": true
  },
  "test_generation": {
    "framework": "auto-detect",
    "coverage_threshold": 80,
    "generate_edge_cases": true,
    "include_mocks": true
  },
  "code_analysis": {
    "check_complexity": true,
    "check_security": true,
    "check_performance": true,
    "check_maintainability": true
  },
  "supported_languages": [
    "python",
    "javascript",
    "typescript",
    "java",
    "go",
    "c#",
    "ruby",
    "php"
  ],
  "ide_integration": {
    "vscode": true,
    "cursor": true,
    "jetbrains": true
  }
}
```

## Usage

### Generate Tests

**In IDE:**
1. Right-click on a function or class
2. Select "Qodo: Generate Tests"
3. Review and customize generated tests
4. Save tests to appropriate test file

**Command Line:**
```powershell
# Using Qodo CLI (if available)
qodo generate-tests --file path/to/file.py
```

### Code Analysis

**In IDE:**
1. Open any code file
2. Qodo will automatically analyze on save
3. View suggestions in the Problems/Issues panel
4. Click on suggestions for detailed explanations

### Bug Detection

Qodo automatically detects:
- Null pointer/undefined issues
- Type mismatches
- Logic errors
- Edge cases not handled
- Performance bottlenecks
- Security vulnerabilities

### Code Review

**Automated Review:**
```powershell
# Integrate with PR review process
.\review-with-qodo.ps1 -PrNumber 123
```

## PowerShell Integration Scripts

### Test Generation Script

Create `qodo-generate-tests.ps1`:

```powershell
# Generate tests for modified files
param([string[]]$Files)

foreach ($File in $Files) {
    Write-Host "[INFO] Generating tests for: $File" -ForegroundColor Cyan
    # Call Qodo API or CLI
    qodo generate-tests --file $File
}
```

### Code Quality Check Script

Create `qodo-quality-check.ps1`:

```powershell
# Run Qodo quality checks
param([switch]$FailOnIssues)

Write-Host "[INFO] Running Qodo quality checks..." -ForegroundColor Cyan

# Analyze all code files
$Issues = qodo analyze --format json

if ($Issues.Count -gt 0) {
    Write-Host "[WARNING] Found $($Issues.Count) issues" -ForegroundColor Yellow
    
    if ($FailOnIssues) {
        exit 1
    }
}
```

## Integration with CI/CD

### GitHub Actions

Add to `.github/workflows/code-quality.yml`:

```yaml
name: Code Quality with Qodo

on: [push, pull_request]

jobs:
  qodo-analysis:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Qodo Analysis
        uses: qodo-ai/qodo-action@v1
        with:
          api-key: ${{ secrets.QODO_API_KEY }}
          fail-on-issues: true
```

## Best Practices

1. **Review Generated Tests**: Always review and customize generated tests
2. **Incremental Adoption**: Start with critical code paths
3. **Combine with Manual Testing**: Use Qodo to augment, not replace manual testing
4. **Regular Analysis**: Run analysis on every commit
5. **Address Findings**: Don't ignore Qodo suggestions

## Supported Languages and Frameworks

### Languages
- Python (Django, Flask, FastAPI)
- JavaScript/TypeScript (Node.js, React, Vue, Angular)
- Java (Spring, JUnit)
- C# (.NET, NUnit, xUnit)
- Go
- Ruby (Rails, RSpec)
- PHP (Laravel, PHPUnit)

### Test Frameworks
- **Python**: pytest, unittest, nose
- **JavaScript**: Jest, Mocha, Jasmine, Vitest
- **Java**: JUnit, TestNG
- **C#**: NUnit, xUnit, MSTest
- **Go**: testing package
- **Ruby**: RSpec, Minitest

## Configuration for This Project

### PowerShell Scripts
```json
{
  "language": "powershell",
  "test_framework": "pester",
  "code_style": "PSScriptAnalyzer"
}
```

### Python Trading Bridge
```json
{
  "language": "python",
  "test_framework": "pytest",
  "coverage_target": 80
}
```

### Node.js Projects
```json
{
  "language": "javascript",
  "test_framework": "jest",
  "coverage_target": 85
}
```

## Troubleshooting

### Extension Not Working

**Issue**: Qodo not activating in IDE

**Solution**:
1. Check extension is enabled
2. Reload window/IDE
3. Check for conflicting extensions
4. Update to latest version

### API Rate Limits

**Issue**: Rate limit exceeded

**Solution**:
1. Upgrade to paid plan for higher limits
2. Cache analysis results
3. Run analysis less frequently

### Test Generation Fails

**Issue**: Cannot generate tests for file

**Solution**:
1. Ensure file has valid syntax
2. Check language is supported
3. Verify test framework is installed
4. Review Qodo logs for details

## Documentation Links

- [Qodo Website](https://www.qodo.ai/)
- [Qodo Documentation](https://docs.qodo.ai/)
- [VS Code Extension](https://marketplace.visualstudio.com/items?itemName=Codium.codium)
- [GitHub Repository](https://github.com/Codium-ai)

## Integration with Project Scripts

Qodo integrates with:
- `cleanup-code.ps1` - Code quality checks before cleanup
- `review-github-repository.ps1` - Enhanced repository analysis
- `security-check.ps1` - Security vulnerability detection
- CI/CD pipelines for automated quality gates

## Support

For issues or questions:
- Check Qodo documentation
- Review logs in IDE output panel
- Visit Qodo community forums
- Contact: support@qodo.ai
