# EYES SECURITY SETUP
# Run as Administrator for full functionality
# This script helps configure OS-level restrictions on screen capture

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  EYES SECURITY SETUP" -ForegroundColor Cyan
Write-Host "  OS-Level Screen Capture Restrictions" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as admin
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "WARNING: Not running as Administrator." -ForegroundColor Yellow
    Write-Host "Some options require admin privileges." -ForegroundColor Yellow
    Write-Host "Right-click and 'Run as Administrator' for full access." -ForegroundColor Yellow
    Write-Host ""
}

Write-Host "This script helps restrict screen capture capabilities." -ForegroundColor White
Write-Host "AI instances (Claude Code, etc.) use PowerShell to capture screens." -ForegroundColor White
Write-Host "These options limit or audit that capability." -ForegroundColor White
Write-Host ""

# Option 1: Audit current state
Write-Host "============================================" -ForegroundColor Green
Write-Host "OPTION 1: Audit Current State" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host "Check what screen capture capabilities exist."
Write-Host ""

$audit = Read-Host "Run audit? (yes/no)"
if ($audit -eq "yes") {
    Write-Host ""
    Write-Host "Checking PowerShell execution policy..." -ForegroundColor Yellow
    Get-ExecutionPolicy -List | Format-Table -AutoSize

    Write-Host "Checking for screen capture assemblies..." -ForegroundColor Yellow
    $assemblies = @(
        "System.Windows.Forms",
        "System.Drawing"
    )
    foreach ($asm in $assemblies) {
        try {
            Add-Type -AssemblyName $asm -ErrorAction Stop
            Write-Host "  [AVAILABLE] $asm" -ForegroundColor Red
        } catch {
            Write-Host "  [BLOCKED] $asm" -ForegroundColor Green
        }
    }
    Write-Host ""
}

# Option 2: Create restricted PowerShell profile
Write-Host "============================================" -ForegroundColor Green
Write-Host "OPTION 2: Restricted PowerShell Profile" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host "Create a PowerShell profile that blocks screen capture assemblies."
Write-Host "This affects all PowerShell sessions for your user."
Write-Host ""

$profile_opt = Read-Host "Create restricted profile? (yes/no)"
if ($profile_opt -eq "yes") {
    $profilePath = $PROFILE.CurrentUserAllHosts
    $profileDir = Split-Path $profilePath

    if (-not (Test-Path $profileDir)) {
        New-Item -ItemType Directory -Path $profileDir -Force | Out-Null
    }

    $restriction = @'

# EYES SECURITY: Block screen capture assemblies
$Global:__OriginalAddType = ${function:Add-Type}
function Add-Type {
    param([string]$AssemblyName, [string]$TypeDefinition, [switch]$PassThru)

    $blocked = @("System.Windows.Forms", "System.Drawing")
    if ($AssemblyName -in $blocked) {
        Write-Warning "BLOCKED: $AssemblyName is restricted by security policy."
        return
    }
    & $Global:__OriginalAddType @PSBoundParameters
}

'@

    $confirm = Read-Host "This will modify your PowerShell profile. Continue? (yes/no)"
    if ($confirm -eq "yes") {
        Add-Content -Path $profilePath -Value $restriction
        Write-Host "Profile updated: $profilePath" -ForegroundColor Green
        Write-Host "Screen capture assemblies will be blocked in new PowerShell sessions." -ForegroundColor Green
    }
    Write-Host ""
}

# Option 3: Audit log for PowerShell commands
Write-Host "============================================" -ForegroundColor Green
Write-Host "OPTION 3: Enable PowerShell Script Block Logging" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host "Log all PowerShell commands to Windows Event Log."
Write-Host "You can review what AI tried to run."
Write-Host "Requires Administrator."
Write-Host ""

if ($isAdmin) {
    $logging = Read-Host "Enable script block logging? (yes/no)"
    if ($logging -eq "yes") {
        $regPath = "HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging"
        if (-not (Test-Path $regPath)) {
            New-Item -Path $regPath -Force | Out-Null
        }
        Set-ItemProperty -Path $regPath -Name "EnableScriptBlockLogging" -Value 1
        Write-Host "Script block logging enabled." -ForegroundColor Green
        Write-Host "View logs in Event Viewer > Applications and Services > Microsoft > Windows > PowerShell" -ForegroundColor Green
    }
} else {
    Write-Host "SKIPPED: Requires Administrator privileges." -ForegroundColor Yellow
}
Write-Host ""

# Option 4: Constrained Language Mode
Write-Host "============================================" -ForegroundColor Green
Write-Host "OPTION 4: PowerShell Constrained Language Mode" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host "Restrict PowerShell to a limited command set."
Write-Host "This is aggressive - may break legitimate scripts."
Write-Host "Requires Administrator and affects system-wide policy."
Write-Host ""

if ($isAdmin) {
    Write-Host "WARNING: This is a significant restriction." -ForegroundColor Red
    Write-Host "It will limit PowerShell functionality system-wide." -ForegroundColor Red
    $clm = Read-Host "Enable Constrained Language Mode? (yes/no)"
    if ($clm -eq "yes") {
        $confirm2 = Read-Host "Are you SURE? This may break other scripts. (YES to confirm)"
        if ($confirm2 -eq "YES") {
            [Environment]::SetEnvironmentVariable("__PSLockdownPolicy", "4", "Machine")
            Write-Host "Constrained Language Mode enabled." -ForegroundColor Green
            Write-Host "Restart PowerShell sessions for this to take effect." -ForegroundColor Green
        }
    }
} else {
    Write-Host "SKIPPED: Requires Administrator privileges." -ForegroundColor Yellow
}
Write-Host ""

# Summary
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "SETUP COMPLETE" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Current protection layers:" -ForegroundColor White
Write-Host "  1. Governance: AI agrees not to capture (HS-EYES-005)" -ForegroundColor White
Write-Host "  2. Code: Unsecured scripts removed from repo" -ForegroundColor White
Write-Host "  3. OS: Run this script to add restrictions" -ForegroundColor White
Write-Host ""
Write-Host "To undo changes:" -ForegroundColor Yellow
Write-Host "  - Profile: Edit $PROFILE.CurrentUserAllHosts" -ForegroundColor Yellow
Write-Host "  - Logging: Set EnableScriptBlockLogging to 0" -ForegroundColor Yellow
Write-Host "  - CLM: Remove __PSLockdownPolicy environment variable" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
