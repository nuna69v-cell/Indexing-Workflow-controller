# Jules Agent - Google AI Integration

## Overview

Jules is an AI agent powered by Google AI Studio (Gemini) that provides automated trading schedule management, code review, merge automation, and commit management for this project.

## Features

- **Trading Schedule Management**: Automate trading operations based on predefined schedules
- **Automated Code Review**: Review pull requests and commits automatically
- **Auto-Merge**: Automatically merge approved pull requests
- **Auto-Commit**: Generate intelligent commit messages and commit changes
- **API Integration**: Full integration with Google AI Studio API

## Setup Instructions

### 1. Get Google AI Studio API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account (Lengkundee01@gmail.com)
3. Create a new API key
4. Copy the API key (it will only be shown once)

### 2. Configure API Key

**Option A: Environment Variable (Recommended)**

```powershell
# Set environment variable (PowerShell)
[System.Environment]::SetEnvironmentVariable('GOOGLE_AI_API_KEY', 'YOUR_API_KEY_HERE', 'User')
```

**Option B: Windows Credential Manager**

```powershell
# Store in Credential Manager
.\setup-jules-agent.ps1 -ApiKey "YOUR_API_KEY_HERE"
```

### 3. Configuration File

Create or edit `jules-agent-config.json`:

```json
{
  "agent_name": "Jules",
  "provider": "google_ai_studio",
  "model": "gemini-pro",
  "features": {
    "auto_review": true,
    "auto_merge": true,
    "auto_commit": true,
    "trading_schedule": true
  },
  "trading_schedule": {
    "enabled": true,
    "timezone": "Asia/Bangkok",
    "sessions": {
      "london": {
        "start": "15:00",
        "end": "24:00",
        "days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
      },
      "new_york": {
        "start": "20:00",
        "end": "05:00",
        "days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
      },
      "tokyo": {
        "start": "07:00",
        "end": "16:00",
        "days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
      }
    }
  },
  "auto_review": {
    "enabled": true,
    "min_approval_score": 0.8,
    "check_security": true,
    "check_tests": true,
    "check_style": true
  },
  "auto_merge": {
    "enabled": true,
    "require_reviews": 1,
    "require_ci_pass": true,
    "merge_method": "squash"
  },
  "auto_commit": {
    "enabled": true,
    "use_conventional_commits": true,
    "sign_commits": false
  }
}
```

### 4. Install Required Dependencies

```powershell
# If using Python for API integration
pip install google-generativeai

# Or using npm
npm install @google/generative-ai
```

### 5. Test Configuration

```powershell
# Test Jules agent
.\test-jules-agent.ps1
```

## Usage

### Automated Code Review

Jules will automatically review all pull requests and provide:
- Code quality analysis
- Security vulnerability detection
- Style compliance checking
- Test coverage analysis

### Trading Schedule Automation

Configure trading sessions in the config file:
- **London Session**: 15:00-24:00 ICT
- **New York Session**: 20:00-05:00 ICT
- **Tokyo Session**: 07:00-16:00 ICT

Jules will automatically:
- Enable/disable trading based on schedule
- Monitor market conditions
- Execute trading strategies
- Generate reports

### Auto-Merge Pull Requests

Jules will automatically merge PRs when:
- All CI/CD checks pass
- Required reviews are approved
- No security vulnerabilities detected
- Code quality meets standards

### Auto-Commit

Jules can generate intelligent commit messages:
- Follows Conventional Commits standard
- Analyzes code changes
- Suggests appropriate commit types (feat, fix, docs, etc.)

## API Reference

### Google AI Studio API

```python
import google.generativeai as genai

# Configure API
genai.configure(api_key=os.environ['GOOGLE_AI_API_KEY'])

# Create model
model = genai.GenerativeModel('gemini-pro')

# Generate response
response = model.generate_content("Review this code...")
```

### PowerShell Integration

```powershell
# Review PR
.\jules-agent-review-pr.ps1 -PrNumber 123

# Merge approved PRs
.\jules-agent-merge.ps1 -AutoMerge

# Generate commit message
.\jules-agent-commit.ps1 -Files @("file1.ps1", "file2.ps1")
```

## Security Best Practices

1. **Never commit API keys** - Use environment variables or credential manager
2. **Rotate keys regularly** - Generate new API keys every 90 days
3. **Use least privilege** - Only grant necessary permissions
4. **Monitor usage** - Check API usage in Google Cloud Console
5. **Enable audit logging** - Track all API calls and automations

## Troubleshooting

### API Key Not Found

```
Error: GOOGLE_AI_API_KEY environment variable not set
```

**Solution**: Set the environment variable or configure credential manager

### Rate Limiting

```
Error: API rate limit exceeded
```

**Solution**: Implement exponential backoff or upgrade API quota

### Invalid API Key

```
Error: Invalid API key
```

**Solution**: Verify API key is correct and not expired

## Integration with Other Scripts

Jules agent integrates with:
- `review-and-merge-prs.ps1` - Auto-review and merge
- `auto-review-merge-inject-repos.ps1` - Multi-repo automation
- `master-trading-orchestrator.ps1` - Trading schedule management
- `github-review-and-decide.ps1` - Intelligent PR decisions

## Documentation Links

- [Google AI Studio](https://makersuite.google.com/)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Google AI Python SDK](https://github.com/google/generative-ai-python)
- [Conventional Commits](https://www.conventionalcommits.org/)

## Support

For issues or questions:
- Check Google AI Studio documentation
- Review error logs in `logs/jules-agent.log`
- Contact: Lengkundee01@gmail.com
