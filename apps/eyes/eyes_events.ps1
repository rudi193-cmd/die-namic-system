param(
    [int]$heartbeatSeconds = 12,
    [string]$outDir = "C:\Users\Sean\screenshots",
    [switch]$secure
)

# GOVERNANCE: This script must be started by human action only.
# AI cannot invoke this script directly.

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Win32 {
    [DllImport("user32.dll")]
    public static extern IntPtr GetForegroundWindow();

    [DllImport("user32.dll", CharSet = CharSet.Auto)]
    public static extern int GetWindowText(IntPtr hWnd, System.Text.StringBuilder lpString, int nMaxCount);

    [DllImport("user32.dll")]
    public static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint lpdwProcessId);
}
"@

# Consent
$consent = Read-Host "Eyes (event-triggered) will capture your screen. Continue? (yes/no)"
if ($consent -ne "yes") {
    Write-Host "Aborted."
    exit 0
}

New-Item -ItemType Directory -Force -Path $outDir | Out-Null

$auditLog = "$outDir\eyes_audit.log"
$startTime = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Add-Content $auditLog "EYES_ON | $startTime | heartbeat=${heartbeatSeconds}s | mode=events | user=$env:USERNAME"

# State tracking
$lastWindow = [IntPtr]::Zero
$lastTitle = ""
$lastClipboard = ""
$lastHeartbeat = Get-Date
$frameCount = 0

function Get-WindowTitle($hwnd) {
    $sb = New-Object System.Text.StringBuilder 256
    [Win32]::GetWindowText($hwnd, $sb, 256) | Out-Null
    return $sb.ToString()
}

function Capture-Screen($reason) {
    $script:frameCount++
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss_fff"
    $outFile = "$outDir\screen_${timestamp}.png"

    $screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
    $bitmap = New-Object System.Drawing.Bitmap($screen.Width, $screen.Height)
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.CopyFromScreen($screen.Location, [System.Drawing.Point]::Empty, $screen.Size)
    $bitmap.Save($outFile)
    $graphics.Dispose()
    $bitmap.Dispose()

    Write-Host "[$reason] $outFile"
}

Write-Host "Eyes online. Heartbeat: ${heartbeatSeconds}s + event triggers"
Write-Host "Triggers: window focus, title change, clipboard"
Write-Host "Press Ctrl+C to stop"

try {
    while ($true) {
        $now = Get-Date
        $currentWindow = [Win32]::GetForegroundWindow()
        $currentTitle = Get-WindowTitle $currentWindow

        # Event: Window focus changed
        if ($currentWindow -ne $lastWindow) {
            Capture-Screen "FOCUS"
            $lastWindow = $currentWindow
            $lastTitle = $currentTitle
            $lastHeartbeat = $now
        }
        # Event: Window title changed (dialog opened, tab switched, etc)
        elseif ($currentTitle -ne $lastTitle -and $currentTitle -ne "") {
            Capture-Screen "TITLE"
            $lastTitle = $currentTitle
            $lastHeartbeat = $now
        }

        # Event: Clipboard changed
        try {
            $clipText = [System.Windows.Forms.Clipboard]::GetText()
            if ($clipText -ne $lastClipboard -and $clipText -ne "") {
                Capture-Screen "CLIPBOARD"
                $lastClipboard = $clipText
                $lastHeartbeat = $now
            }
        } catch { }

        # Heartbeat: Capture every N seconds regardless
        if (($now - $lastHeartbeat).TotalSeconds -ge $heartbeatSeconds) {
            Capture-Screen "HEARTBEAT"
            $lastHeartbeat = $now
        }

        Start-Sleep -Milliseconds 100
    }
} finally {
    $stopTime = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Add-Content $auditLog "EYES_OFF | $stopTime | frames=$frameCount"
    Write-Host "`nEyes off. $frameCount frames captured."
}
