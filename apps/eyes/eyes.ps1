param(
    [int]$fps = 1,
    [int]$bufferSeconds = 60,
    [string]$outDir = "C:\Users\Sean\screenshots\eyes"
)

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# Create output directory
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

$frameInterval = 1000 / $fps
$maxFrames = $fps * $bufferSeconds
$frameCount = 0

Write-Host "Eyes online. ${fps}fps, ${bufferSeconds}s buffer ($maxFrames frames max)"
Write-Host "Output: $outDir"
Write-Host "Press Ctrl+C to stop"

while ($true) {
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss_fff"
    $filename = "$outDir\frame_$timestamp.png"

    $screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
    $bitmap = New-Object System.Drawing.Bitmap($screen.Width, $screen.Height)
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.CopyFromScreen($screen.Location, [System.Drawing.Point]::Empty, $screen.Size)
    $bitmap.Save($filename)
    $graphics.Dispose()
    $bitmap.Dispose()

    $frameCount++

    # Rolling buffer - delete oldest if over max
    $files = Get-ChildItem "$outDir\frame_*.png" | Sort-Object Name
    if ($files.Count -gt $maxFrames) {
        $toDelete = $files.Count - $maxFrames
        $files | Select-Object -First $toDelete | Remove-Item -Force
    }

    Start-Sleep -Milliseconds $frameInterval
}
