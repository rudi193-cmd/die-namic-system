param(
    [int]$fps = 1,
    [int]$bufferSeconds = 30,
    [string]$outDir = "C:\Users\Sean\screenshots\eyes_secure",
    [SecureString]$key
)

# GOVERNANCE: This script must be started by human action only.
# AI cannot invoke this script directly.

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName System.Security

# Require explicit consent
$consent = Read-Host "Eyes will capture your screen. Passwords and private data may be visible. Continue? (yes/no)"
if ($consent -ne "yes") {
    Write-Host "Aborted. No frames captured."
    exit 0
}

# Get encryption key from user (not stored)
if (-not $key) {
    $key = Read-Host "Enter encryption passphrase" -AsSecureString
}
$keyBytes = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($key)
)
$aesKey = [System.Text.Encoding]::UTF8.GetBytes($keyBytes.PadRight(32).Substring(0,32))

# Create secure output directory
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

# Audit log
$auditLog = "$outDir\audit.log"
$startTime = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Add-Content $auditLog "EYES_ON | $startTime | fps=$fps | buffer=${bufferSeconds}s | user=$env:USERNAME"

$frameInterval = 1000 / $fps
$maxFrames = $fps * $bufferSeconds
$frameCount = 0

Write-Host "Eyes SECURE online. ${fps}fps, ${bufferSeconds}s buffer ($maxFrames frames max)"
Write-Host "Frames encrypted. Auto-purge enabled."
Write-Host "Press Ctrl+C to stop"

# Cleanup handler
$cleanup = {
    $stopTime = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Add-Content $auditLog "EYES_OFF | $stopTime | frames_captured=$frameCount"
    # Secure delete all frames
    Get-ChildItem "$outDir\frame_*.enc" -ErrorAction SilentlyContinue | Remove-Item -Force
    Write-Host "`nEyes off. Frames purged."
}

try {
    while ($true) {
        $timestamp = Get-Date -Format "yyyyMMdd_HHmmss_fff"
        $tempFile = "$outDir\temp_$timestamp.png"
        $encFile = "$outDir\frame_$timestamp.enc"

        # Capture
        $screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
        $bitmap = New-Object System.Drawing.Bitmap($screen.Width, $screen.Height)
        $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
        $graphics.CopyFromScreen($screen.Location, [System.Drawing.Point]::Empty, $screen.Size)

        # Save to temp, encrypt, delete temp
        $bitmap.Save($tempFile)
        $graphics.Dispose()
        $bitmap.Dispose()

        # Encrypt frame
        $plainBytes = [System.IO.File]::ReadAllBytes($tempFile)
        $aes = [System.Security.Cryptography.Aes]::Create()
        $aes.Key = $aesKey
        $aes.GenerateIV()
        $encryptor = $aes.CreateEncryptor()
        $encBytes = $encryptor.TransformFinalBlock($plainBytes, 0, $plainBytes.Length)

        # Write IV + encrypted data
        $output = $aes.IV + $encBytes
        [System.IO.File]::WriteAllBytes($encFile, $output)

        # Secure delete temp
        Remove-Item $tempFile -Force

        $frameCount++

        # Rolling buffer - delete oldest encrypted frames
        $files = Get-ChildItem "$outDir\frame_*.enc" | Sort-Object Name
        if ($files.Count -gt $maxFrames) {
            $toDelete = $files.Count - $maxFrames
            $files | Select-Object -First $toDelete | Remove-Item -Force
        }

        Start-Sleep -Milliseconds $frameInterval
    }
} finally {
    & $cleanup
}
