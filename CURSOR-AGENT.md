# Cursor Agent - AI-Assisted Code Editing

## Overview

Cursor is an AI-powered code editor built on VS Code that provides intelligent code completion, generation, and editing capabilities. This project already uses Cursor with custom rules for PowerShell automation and Windows system management.

## Features

- **AI Code Completion**: Context-aware code suggestions
- **Code Generation**: Generate entire functions or files from descriptions
- **Code Refactoring**: AI-assisted code improvements
- **Natural Language Editing**: Edit code using natural language commands
- **Custom Rules**: Project-specific AI behavior rules
- **Multi-file Editing**: Edit multiple files simultaneously
- **Chat Interface**: Conversational coding assistance

## Setup Instructions

### 1. Install Cursor IDE

1. Download from [Cursor website](https://cursor.sh/)
2. Install for Windows
3. Launch Cursor
4. Sign in or create account

### 2. Configure API Key

Cursor has its own AI model (no separate API key needed for basic features).

**For OpenAI Integration (Optional):**
```powershell
# Set OpenAI API key for enhanced features
[System.Environment]::SetEnvironmentVariable('OPENAI_API_KEY', 'YOUR_API_KEY', 'User')
```

### 3. Cursor Rules Configuration

This project already has Cursor rules configured in `.cursor/rules/`. Current rules:

- `automation-patterns/` - PowerShell automation patterns
- `github-desktop-integration/` - GitHub Desktop integration
- `powershell-standards/` - PowerShell coding standards
- `security-tokens/` - Security and token handling
- `security-trading/` - Trading system security
- `system-configuration/` - Windows system configuration
- `trading-automation/` - Trading automation rules
- `trading-system/` - Trading system rules
- `ai-agents/` - AI agent integration rules (NEW)

### 4. Project-Specific Configuration

Create `.cursorrules` in project root:

```
# Project: Windows Automation and Trading System
# Device: NuNa (Windows 11)
# Organization: A6-9V

## System Configuration
- Device: NuNa
- OS: Windows 11 Home Single Language 25H2 (Build 26220.7344)
- Processor: Intel(R) Core(TM) i3-N305 (1.80 GHz)
- RAM: 8.00 GB (7.63 GB usable)

## Code Style - PowerShell
- Use clear, descriptive variable names
- Add comments for complex logic
- Use Write-Host with -ForegroundColor for user feedback
- Always use try-catch blocks for error handling
- Use consistent status indicators: [OK], [INFO], [WARNING], [ERROR]

## Security Rules
- Never commit tokens or credentials
- All token files must be in .gitignore
- Tokens stored in Windows Credential Manager
- Never log or display token values

## Automation Principles
1. Automated Decision Making: Scripts make intelligent decisions without user prompts
2. Best Practices First: Always choose secure and recommended options
3. Fail-Safe: Skip gracefully if something can't be automated
4. Token Security: GitHub tokens stored locally, never committed

## File Organization
- Scripts: *.ps1 files in project root
- Documentation: *.md files for rules and guides
- Configuration: git-credentials.txt (gitignored)
- Rules: .cursor/rules/ directory for project-specific rules
```

### 5. Keyboard Shortcuts

**Essential Cursor Shortcuts:**
- `Ctrl+K` - Open AI command palette
- `Ctrl+L` - Open AI chat
- `Ctrl+Shift+L` - Edit with AI
- `Ctrl+K Ctrl+D` - Generate code from comment
- `Ctrl+.` - Quick fix/suggestions

### 6. Cursor Settings

Configure in Cursor Settings (File → Preferences → Settings):

```json
{
  "cursor.ai.model": "gpt-4",
  "cursor.ai.temperature": 0.7,
  "cursor.ai.maxTokens": 2048,
  "cursor.rules.enabled": true,
  "cursor.rules.paths": [
    ".cursor/rules",
    ".cursorrules"
  ],
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll": true
  }
}
```

## Usage

### 1. AI Code Completion

Type naturally and Cursor will suggest completions:

```powershell
# Type: "function to check if node is installed"
# Cursor suggests:
function Test-NodeInstalled {
    try {
        $version = node --version 2>$null
        return $LASTEXITCODE -eq 0
    } catch {
        return $false
    }
}
```

### 2. Generate Code from Comments

```powershell
# Generate a script to backup all PowerShell files to USB drive
# (Press Ctrl+K Ctrl+D)

# Cursor generates the complete script based on comment
```

### 3. Natural Language Editing

Open chat (Ctrl+L) and ask:
- "Refactor this function to use modern PowerShell syntax"
- "Add error handling to this script"
- "Generate tests for this function"
- "Explain what this code does"

### 4. Multi-file Operations

```
@file1.ps1 @file2.ps1 Make these scripts follow the same error handling pattern
```

### 5. Code Review with AI

```powershell
# Select code and press Ctrl+L
# Ask: "Review this code for security issues and best practices"
```

## Integration with Project

### Automated Workflows

Cursor integrates with existing scripts:

```powershell
# Use Cursor to generate and review scripts
.\auto-setup.ps1           # System setup
.\complete-device-setup.ps1 # Device configuration
.\review-and-merge-prs.ps1 # PR automation
```

### Custom Rules Usage

The AI will follow rules from `.cursor/rules/`:

1. **PowerShell Standards**: Consistent code style
2. **Security Rules**: Safe token handling
3. **Automation Patterns**: Reliable automation
4. **Trading System Rules**: Trading-specific patterns

### Script Generation

Use Cursor to generate new automation scripts:

```
Prompt: "Create a PowerShell script to monitor disk health and alert if issues detected"

Cursor generates: disk-health-monitor.ps1 (already exists in project)
```

## Advanced Features

### 1. Cursor Composer

Multi-file editing with AI:
- Select multiple files
- Describe changes
- Cursor applies changes across all files

### 2. Symbol Search

Find and navigate code with AI:
- Press `Ctrl+T` for symbol search
- Ask AI: "Where is the git authentication function?"

### 3. Linting Integration

```powershell
# Install PSScriptAnalyzer for PowerShell linting
Install-Module -Name PSScriptAnalyzer -Force

# Cursor will show linting issues inline
```

### 4. Git Integration

Cursor has built-in Git support:
- View changes in sidebar
- Stage/commit with AI-generated messages
- Review diffs with AI explanations

## Best Practices

1. **Use Rules Files**: Define project-specific patterns in `.cursor/rules/`
2. **Clear Prompts**: Be specific in natural language requests
3. **Review AI Output**: Always review generated code
4. **Iterative Refinement**: Refine AI responses through conversation
5. **Context Management**: Include relevant files in context (@mentions)

## Configuration for This Project

### PowerShell Specific

```json
{
  "files.associations": {
    "*.ps1": "powershell",
    "*.psm1": "powershell",
    "*.psd1": "powershell"
  },
  "powershell.scriptAnalysis.enable": true,
  "powershell.codeFormatting.preset": "OTBS"
}
```

### AI Model Selection

```json
{
  "cursor.ai.preferredModel": {
    "default": "gpt-4",
    "code-generation": "gpt-4",
    "chat": "gpt-4",
    "editing": "gpt-3.5-turbo"
  }
}
```

## Troubleshooting

### AI Not Responding

**Issue**: Cursor AI not providing suggestions

**Solution**:
1. Check internet connection
2. Verify account is active
3. Restart Cursor
4. Check API key if using custom models

### Rules Not Applied

**Issue**: Custom rules not being followed

**Solution**:
1. Verify `.cursor/rules/` structure
2. Check rules file syntax
3. Ensure `cursor.rules.enabled` is true
4. Restart Cursor to reload rules

### Slow Performance

**Issue**: Cursor running slowly

**Solution**:
1. Reduce number of indexed files
2. Exclude large directories (node_modules, etc.)
3. Close unused tabs
4. Update to latest version

## Documentation Links

- [Cursor Website](https://cursor.sh/)
- [Cursor Documentation](https://docs.cursor.sh/)
- [Cursor Rules Guide](https://docs.cursor.sh/get-started/rules)
- [VS Code Documentation](https://code.visualstudio.com/docs) (Cursor is based on VS Code)

## Integration Points

Cursor enhances these project workflows:

- **Script Development**: Generate and refine PowerShell scripts
- **Code Review**: AI-assisted PR reviews
- **Documentation**: Auto-generate README and guides
- **Debugging**: AI-powered debugging assistance
- **Refactoring**: Modernize legacy code

## Comparison with Other Editors

| Feature | Cursor | VS Code + Copilot | Standard IDE |
|---------|--------|-------------------|--------------|
| AI Completion | ✓ | ✓ | ✗ |
| Chat Interface | ✓ | Limited | ✗ |
| Multi-file Edit | ✓ | ✗ | ✗ |
| Custom Rules | ✓ | Limited | ✗ |
| Native Git | ✓ | ✓ | Varies |

## Support

For issues or questions:
- Check Cursor documentation
- Visit Cursor community forum
- Email: support@cursor.sh
- Discord: cursor.sh/discord

## Project-Specific Notes

This project uses Cursor for:
- PowerShell script development
- Trading system automation code
- Git automation scripts
- System configuration scripts
- Documentation generation

All scripts follow the rules defined in `.cursor/rules/` for consistency and quality.
