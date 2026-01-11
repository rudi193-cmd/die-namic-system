param(
    [int]$frames = 1,
    [string]$eyesDir = "C:\Users\Sean\screenshots\eyes"
)

$files = Get-ChildItem "$eyesDir\frame_*.png" -ErrorAction SilentlyContinue | Sort-Object Name -Descending | Select-Object -First $frames

if ($files.Count -eq 0) {
    Write-Host "No frames. Eyes offline?"
    exit 1
}

foreach ($file in $files) {
    Write-Host $file.FullName
}
