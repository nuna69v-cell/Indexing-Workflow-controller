# Kombai Agent - Design to Code Conversion

## Overview

Kombai is an AI-powered tool that converts Figma designs, screenshots, and design files into high-quality frontend code. It can generate HTML, CSS, React, Vue, and other framework code from visual designs.

## Features

- **Figma to Code**: Convert Figma designs directly to code
- **Screenshot to Code**: Generate code from design screenshots
- **Multi-Framework Support**: React, Vue, HTML/CSS, Tailwind CSS
- **Responsive Design**: Automatically generate responsive layouts
- **Component Extraction**: Identify and extract reusable components
- **Design System Integration**: Maintain design system consistency
- **Clean Code Output**: Production-ready, semantic code

## Setup Instructions

### 1. Create Kombai Account

1. Visit [Kombai website](https://kombai.com/)
2. Sign up with email (Lengkundee01@gmail.com)
3. Choose a plan (Free tier available)
4. Complete account setup

### 2. Get API Key (For API Access)

1. Log in to Kombai dashboard
2. Navigate to Settings → API Keys
3. Generate new API key
4. Copy and store securely

### 3. Configure API Key

**Option A: Environment Variable**
```powershell
[System.Environment]::SetEnvironmentVariable('KOMBAI_API_KEY', 'YOUR_API_KEY_HERE', 'User')
```

**Option B: Windows Credential Manager**
```powershell
.\setup-kombai-agent.ps1 -ApiKey "YOUR_API_KEY_HERE"
```

### 4. Install Kombai Plugin

**For Figma:**
1. Open Figma
2. Go to Plugins → Browse Plugins
3. Search for "Kombai"
4. Install plugin
5. Connect with your Kombai account

**For CLI (if available):**
```powershell
npm install -g kombai-cli
```

### 5. Configuration File

Create `kombai-config.json`:

```json
{
  "agent_name": "Kombai",
  "provider": "kombai",
  "features": {
    "figma_integration": true,
    "screenshot_conversion": true,
    "component_extraction": true,
    "responsive_generation": true
  },
  "output_settings": {
    "framework": "react",
    "styling": "tailwind",
    "typescript": true,
    "component_format": "functional"
  },
  "design_tokens": {
    "colors": "auto-extract",
    "spacing": "auto-extract",
    "typography": "auto-extract",
    "breakpoints": ["mobile", "tablet", "desktop"]
  },
  "code_preferences": {
    "semantic_html": true,
    "accessibility": true,
    "bem_naming": false,
    "css_modules": false
  },
  "supported_frameworks": [
    "html",
    "react",
    "vue",
    "angular",
    "svelte"
  ]
}
```

## Usage

### 1. Convert Figma Design to Code

**Using Figma Plugin:**
1. Open design in Figma
2. Run Kombai plugin (Plugins → Kombai)
3. Select frames/components to convert
4. Choose output framework (React, HTML, etc.)
5. Click "Generate Code"
6. Copy or download generated code

**Using API:**
```powershell
# Convert Figma file to React code
.\kombai-convert-figma.ps1 -FigmaFileId "FILE_ID" -Framework "react"
```

### 2. Convert Screenshot to Code

**Web Interface:**
1. Go to Kombai dashboard
2. Upload design screenshot
3. Select output framework
4. Review and adjust generated code
5. Download code

**Using PowerShell Script:**
```powershell
# Convert screenshot to code
.\kombai-screenshot-to-code.ps1 -ImagePath "design.png" -Framework "react"
```

### 3. Extract Components

Kombai automatically identifies reusable components:
- Buttons
- Forms
- Navigation bars
- Cards
- Modals
- Headers/Footers

```powershell
# Extract components from design
.\kombai-extract-components.ps1 -DesignFile "design.fig" -OutputDir "./components"
```

### 4. Generate Responsive Layouts

```json
{
  "responsive": {
    "breakpoints": {
      "mobile": "320px",
      "tablet": "768px",
      "desktop": "1024px",
      "wide": "1440px"
    },
    "auto_scale": true,
    "fluid_typography": true
  }
}
```

## Integration Scripts

### Figma to React Converter

Create `kombai-convert-figma.ps1`:

```powershell
# Convert Figma design to React components
param(
    [Parameter(Mandatory=$true)]
    [string]$FigmaFileId,
    
    [string]$Framework = "react",
    [string]$OutputDir = "./generated-components"
)

Write-Host "[INFO] Converting Figma design to $Framework..." -ForegroundColor Cyan

# Call Kombai API
$ApiKey = $env:KOMBAI_API_KEY
$ApiUrl = "https://api.kombai.com/v1/convert"

$Body = @{
    figma_file_id = $FigmaFileId
    framework = $Framework
    output_format = "typescript"
} | ConvertTo-Json

try {
    $Response = Invoke-RestMethod -Uri $ApiUrl -Method Post -Headers @{
        "Authorization" = "Bearer $ApiKey"
        "Content-Type" = "application/json"
    } -Body $Body
    
    # Save generated code
    New-Item -Path $OutputDir -ItemType Directory -Force | Out-Null
    
    foreach ($Component in $Response.components) {
        $FilePath = Join-Path -Path $OutputDir -ChildPath "$($Component.name).$($Component.extension)"
        $Component.code | Out-File -FilePath $FilePath -Encoding UTF8
        Write-Host "[OK] Generated: $FilePath" -ForegroundColor Green
    }
    
    Write-Host "[OK] Conversion complete!" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Conversion failed: $_" -ForegroundColor Red
    exit 1
}
```

### Screenshot to Code Converter

Create `kombai-screenshot-to-code.ps1`:

```powershell
# Convert screenshot to code
param(
    [Parameter(Mandatory=$true)]
    [string]$ImagePath,
    
    [string]$Framework = "html",
    [string]$OutputFile = "output.html"
)

Write-Host "[INFO] Converting screenshot to $Framework..." -ForegroundColor Cyan

if (-not (Test-Path $ImagePath)) {
    Write-Host "[ERROR] Image file not found: $ImagePath" -ForegroundColor Red
    exit 1
}

# Read image as base64
$ImageBytes = [System.IO.File]::ReadAllBytes($ImagePath)
$ImageBase64 = [Convert]::ToBase64String($ImageBytes)

# Call Kombai API
$ApiKey = $env:KOMBAI_API_KEY
$ApiUrl = "https://api.kombai.com/v1/screenshot-to-code"

$Body = @{
    image = $ImageBase64
    framework = $Framework
} | ConvertTo-Json

try {
    $Response = Invoke-RestMethod -Uri $ApiUrl -Method Post -Headers @{
        "Authorization" = "Bearer $ApiKey"
        "Content-Type" = "application/json"
    } -Body $Body
    
    # Save generated code
    $Response.code | Out-File -FilePath $OutputFile -Encoding UTF8
    Write-Host "[OK] Code saved to: $OutputFile" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Conversion failed: $_" -ForegroundColor Red
    exit 1
}
```

## Use Cases for This Project

### 1. Trading Dashboard UI

Convert Figma designs for trading dashboards:
- Real-time charts
- Order entry forms
- Account balance displays
- Trade history tables

### 2. System Configuration UI

Generate admin panels for:
- VPS management interface
- Git automation dashboard
- Security monitoring UI
- System status displays

### 3. Documentation Website

Create project documentation sites:
- README renderings
- API documentation
- Setup guides
- Architecture diagrams

### 4. Landing Pages

Build landing pages for:
- Trading system features
- Project showcase
- Service offerings

## Supported Frameworks and Technologies

### Frontend Frameworks
- **React**: Functional components, hooks, TypeScript
- **Vue**: Vue 3 composition API
- **Angular**: Component-based architecture
- **Svelte**: Svelte 3+
- **HTML/CSS**: Pure HTML5 and CSS3

### Styling Options
- **CSS**: Plain CSS, CSS modules
- **Tailwind CSS**: Utility-first classes
- **Styled Components**: CSS-in-JS for React
- **SCSS/SASS**: Pre-processor support
- **Bootstrap**: Bootstrap 5 classes

### Output Formats
- TypeScript
- JavaScript (ES6+)
- JSX/TSX
- Single File Components (Vue)

## Best Practices

1. **Clean Designs**: Ensure Figma designs are well-organized with proper naming
2. **Design System**: Use consistent design tokens (colors, spacing, typography)
3. **Component Structure**: Group related elements in Figma frames
4. **Responsive Design**: Design for multiple breakpoints
5. **Accessibility**: Include proper labels and semantic structure
6. **Review Output**: Always review and refine generated code
7. **Version Control**: Commit generated code with clear messages

## Quality Checks

After generating code:

```powershell
# Check code quality
.\qodo-quality-check.ps1 -Files @("generated-components/*.tsx")

# Run linting
npm run lint

# Check accessibility
npm run a11y-check

# Test responsiveness
npm run test:responsive
```

## Integration with Project Workflow

```powershell
# Full workflow
1. Design in Figma
2. .\kombai-convert-figma.ps1 -FigmaFileId "abc123"
3. .\qodo-quality-check.ps1 -Files "./generated-components/*"
4. Review and refine code manually
5. .\auto-install-dependencies.ps1
6. npm run test
7. git add . && git commit -m "feat: add new UI components"
```

## Limitations

- **Complex Interactions**: May need manual refinement for complex interactions
- **State Management**: State logic needs to be added manually
- **API Integration**: Backend integration requires manual coding
- **Custom Logic**: Business logic must be implemented separately
- **Animations**: Complex animations may need adjustment

## Troubleshooting

### API Authentication Failed

**Issue**: 401 Unauthorized error

**Solution**:
1. Verify API key is correct
2. Check key hasn't expired
3. Ensure environment variable is set

### Poor Code Quality

**Issue**: Generated code needs significant refactoring

**Solution**:
1. Improve Figma design organization
2. Use proper naming conventions
3. Adjust Kombai settings for better output
4. Use Qodo to refactor generated code

### Missing Components

**Issue**: Some design elements not converted

**Solution**:
1. Ensure elements are in proper Figma frames
2. Check element visibility and layers
3. Verify design complexity is supported

## Documentation Links

- [Kombai Website](https://kombai.com/)
- [Kombai Documentation](https://docs.kombai.com/)
- [Figma Plugin](https://www.figma.com/community/plugin/kombai)
- [API Reference](https://docs.kombai.com/api)

## Integration with Other Agents

Kombai works well with:
- **Cursor**: Refine generated code with AI assistance
- **Qodo**: Test and analyze generated components
- **Jules**: Review and commit generated code

## Pricing

- **Free Tier**: Limited conversions per month
- **Pro**: Unlimited conversions, advanced features
- **Team**: Collaboration features, API access
- **Enterprise**: Custom solutions, priority support

## Support

For issues or questions:
- Visit Kombai documentation
- Check community forums
- Email: support@kombai.com
- Discord: kombai.com/discord

## Project-Specific Configuration

For this Windows automation project, Kombai is primarily useful for:
- Creating admin dashboards for system management
- Building UI for trading system monitoring
- Generating documentation websites
- Creating landing pages for project showcases
