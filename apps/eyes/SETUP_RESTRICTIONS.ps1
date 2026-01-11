# EYES SECURITY SETUP
# Run as Administrator for full functionality
# This script helps configure OS-level restrictions on screen capture

try {

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  EYES SECURITY SETTINGS" -ForegroundColor Cyan
Write-Host "  OS-Level Screen Capture Restrictions" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as admin
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "WARNING: Not running as Administrator." -ForegroundColor Yellow
    Write-Host "Some options require admin privileges." -ForegroundColor Yellow
    Write-Host ""
}

# Check current states
function Get-ProfileRestrictionStatus {
    $profilePath = $PROFILE.CurrentUserAllHosts
    if (Test-Path $profilePath) {
        $content = Get-Content $profilePath -Raw -ErrorAction SilentlyContinue
        if ($content -match "EYES SECURITY") {
            return $true
        }
    }
    return $false
}

function Get-ScriptLoggingStatus {
    try {
        $val = Get-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging" -Name "EnableScriptBlockLogging" -ErrorAction SilentlyContinue
        return ($val.EnableScriptBlockLogging -eq 1)
    } catch {
        return $false
    }
}

function Get-CLMStatus {
    $val = [Environment]::GetEnvironmentVariable("__PSLockdownPolicy", "Machine")
    return ($val -eq "4")
}

# Display current status
function Show-Status {
    Write-Host ""
    Write-Host "CURRENT STATUS:" -ForegroundColor Cyan
    Write-Host "===============" -ForegroundColor Cyan

    $profileStatus = Get-ProfileRestrictionStatus
    $loggingStatus = Get-ScriptLoggingStatus
    $clmStatus = Get-CLMStatus

    if ($profileStatus) {
        Write-Host "[1] Profile Restriction:    ON  " -ForegroundColor Green -NoNewline
        Write-Host "(Screen capture assemblies blocked)"
    } else {
        Write-Host "[1] Profile Restriction:    OFF " -ForegroundColor Red -NoNewline
        Write-Host "(Screen capture assemblies available)"
    }

    if ($loggingStatus) {
        Write-Host "[2] Script Block Logging:   ON  " -ForegroundColor Green -NoNewline
        Write-Host "(PowerShell commands logged)"
    } else {
        Write-Host "[2] Script Block Logging:   OFF " -ForegroundColor Red -NoNewline
        Write-Host "(No audit trail)"
    }

    if ($clmStatus) {
        Write-Host "[3] Constrained Language:   ON  " -ForegroundColor Green -NoNewline
        Write-Host "(PowerShell heavily restricted)"
    } else {
        Write-Host "[3] Constrained Language:   OFF " -ForegroundColor Red -NoNewline
        Write-Host "(Full PowerShell access)"
    }

    Write-Host ""
    Write-Host "[4] Run Audit (check capabilities)"
    Write-Host "[Q] Quit"
    Write-Host ""
}

# Toggle functions
function Toggle-ProfileRestriction {
    $profilePath = $PROFILE.CurrentUserAllHosts
    $profileDir = Split-Path $profilePath

    if (Get-ProfileRestrictionStatus) {
        # Turn OFF
        Write-Host "Removing profile restriction..." -ForegroundColor Yellow
        if (Test-Path $profilePath) {
            $content = Get-Content $profilePath -Raw
            $pattern = "(?s)# EYES SECURITY:.*?function Add-Type \{.*?\}"
            $newContent = $content -replace $pattern, ""
            $newContent = $newContent.Trim()
            if ($newContent) {
                Set-Content $profilePath $newContent
            } else {
                Remove-Item $profilePath
            }
        }
        Write-Host "Profile restriction DISABLED." -ForegroundColor Red
    } else {
        # Turn ON
        Write-Host "Adding profile restriction..." -ForegroundColor Yellow

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
        Add-Content -Path $profilePath -Value $restriction
        Write-Host "Profile restriction ENABLED." -ForegroundColor Green
        Write-Host "Takes effect in new PowerShell sessions." -ForegroundColor Yellow
    }
}

function Toggle-ScriptLogging {
    if (-not $isAdmin) {
        Write-Host "ERROR: Requires Administrator." -ForegroundColor Red
        return
    }

    $regPath = "HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging"

    if (Get-ScriptLoggingStatus) {
        # Turn OFF
        Write-Host "Disabling script block logging..." -ForegroundColor Yellow
        Set-ItemProperty -Path $regPath -Name "EnableScriptBlockLogging" -Value 0
        Write-Host "Script logging DISABLED." -ForegroundColor Red
    } else {
        # Turn ON
        Write-Host "Enabling script block logging..." -ForegroundColor Yellow
        if (-not (Test-Path $regPath)) {
            New-Item -Path $regPath -Force | Out-Null
        }
        Set-ItemProperty -Path $regPath -Name "EnableScriptBlockLogging" -Value 1
        Write-Host "Script logging ENABLED." -ForegroundColor Green
        Write-Host "View: Event Viewer > Applications and Services > Microsoft > Windows > PowerShell" -ForegroundColor Yellow
    }
}

function Toggle-CLM {
    if (-not $isAdmin) {
        Write-Host "ERROR: Requires Administrator." -ForegroundColor Red
        return
    }

    if (Get-CLMStatus) {
        # Turn OFF
        Write-Host "Disabling Constrained Language Mode..." -ForegroundColor Yellow
        [Environment]::SetEnvironmentVariable("__PSLockdownPolicy", $null, "Machine")
        Write-Host "CLM DISABLED." -ForegroundColor Red
        Write-Host "Restart PowerShell for this to take effect." -ForegroundColor Yellow
    } else {
        # Turn ON
        Write-Host "WARNING: This heavily restricts PowerShell!" -ForegroundColor Red
        $confirm = Read-Host "Are you sure? (YES to confirm)"
        if ($confirm -eq "YES") {
            [Environment]::SetEnvironmentVariable("__PSLockdownPolicy", "4", "Machine")
            Write-Host "CLM ENABLED." -ForegroundColor Green
            Write-Host "Restart PowerShell for this to take effect." -ForegroundColor Yellow
        } else {
            Write-Host "Cancelled." -ForegroundColor Yellow
        }
    }
}

function Run-Audit {
    Write-Host ""
    Write-Host "AUDIT: Screen Capture Capabilities" -ForegroundColor Cyan
    Write-Host "===================================" -ForegroundColor Cyan

    Write-Host ""
    Write-Host "PowerShell Execution Policy:" -ForegroundColor Yellow
    Get-ExecutionPolicy -List | Format-Table -AutoSize

    Write-Host "Screen Capture Assemblies:" -ForegroundColor Yellow
    $assemblies = @("System.Windows.Forms", "System.Drawing")
    foreach ($asm in $assemblies) {
        try {
            Add-Type -AssemblyName $asm -ErrorAction Stop
            Write-Host "  [AVAILABLE] $asm" -ForegroundColor Red
        } catch {
            Write-Host "  [BLOCKED]   $asm" -ForegroundColor Green
        }
    }
    Write-Host ""
}

# Main menu loop
do {
    Show-Status
    $choice = Read-Host "Enter option to toggle (1-4) or Q to quit"

    switch ($choice.ToUpper()) {
        "1" { Toggle-ProfileRestriction }
        "2" { Toggle-ScriptLogging }
        "3" { Toggle-CLM }
        "4" { Run-Audit }
        "Q" { break }
        default { Write-Host "Invalid option." -ForegroundColor Red }
    }

    if ($choice.ToUpper() -ne "Q") {
        Write-Host ""
        Read-Host "Press Enter to continue"
    }

} while ($choice.ToUpper() -ne "Q")

Write-Host ""
Write-Host "Settings saved. Goodbye." -ForegroundColor Cyan

} catch {
    Write-Host "ERROR: $_" -ForegroundColor Red
} finally {
    Write-Host ""
    Write-Host "Press any key to exit..." -ForegroundColor Cyan
    cmd /c pause
}
