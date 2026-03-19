# Get Started with Cursor CLI

This guide provides instructions on how to install and integrate the Cursor CLI, including working with agents and MCP integrations.

## Using Headless CLI
Use the Cursor CLI in scripts and automation workflows. The headless CLI enables you to run Cursor commands without opening the graphical interface, making it perfect for CI/CD pipelines, automated testing, and background tasks.

Example:
```bash
cursor --headless --command "run-agent my-script.py"
```

## Shell Mode
Run shell commands directly from agents with safety checks and output display. Shell Mode gives your agents the ability to interact with the underlying operating system securely.

To enable shell mode:
```bash
cursor shell --enable-safety-checks
```
*Note: Always review the output displayed when running commands in Shell Mode to ensure safety.*

## GitHub Actions
Integrate Cursor CLI with GitHub Actions for automated CI/CD workflows. You can trigger agents, run tests, and format your codebase directly from your GitHub repository.

Example `.github/workflows/cursor-ci.yml`:
```yaml
name: Cursor Automation
on: [push]
jobs:
  run-cursor:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install Cursor CLI
        run: npm install -g cursor-cli
      - name: Run Cursor Agent
        run: cursor run-agent --headless
```

For more information, tools, and enterprise-grade IDE features, visit [Anysphere](https://anysphere.inc/).
