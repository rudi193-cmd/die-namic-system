param(
    [int]$frames = 1,
    [string]$eyesDir = "C:\Users\Sean\screenshots\eyes_secure",
    [string]$outputDir = "C:\Users\Sean\screenshots\eyes_secure\decrypted"
)

# GOVERNANCE: Decrypted frames are temporary and must be deleted after viewing.
# AI can request this script be run, but human must provide passphrase.

Add-Type -AssemblyName System.Security

$auditLog = "$eyesDir\audit.log"

# Get decryption key from human
$key = Read-Host "Enter decryption passphrase" -AsSecureString
$keyBytes = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($key)
)
$aesKey = [System.Text.Encoding]::UTF8.GetBytes($keyBytes.PadRight(32).Substring(0,32))

# Get latest encrypted frames
$files = Get-ChildItem "$eyesDir\frame_*.enc" -ErrorAction SilentlyContinue |
    Sort-Object Name -Descending |
    Select-Object -First $frames

if ($files.Count -eq 0) {
    Write-Host "No frames. Eyes offline or buffer empty."
    exit 1
}

# Create temp output dir
New-Item -ItemType Directory -Force -Path $outputDir | Out-Null

$decryptedFiles = @()

foreach ($file in $files) {
    try {
        $encData = [System.IO.File]::ReadAllBytes($file.FullName)

        # Extract IV (first 16 bytes) and ciphertext
        $iv = $encData[0..15]
        $ciphertext = $encData[16..($encData.Length - 1)]

        # Decrypt
        $aes = [System.Security.Cryptography.Aes]::Create()
        $aes.Key = $aesKey
        $aes.IV = $iv
        $decryptor = $aes.CreateDecryptor()
        $plainBytes = $decryptor.TransformFinalBlock($ciphertext, 0, $ciphertext.Length)

        # Write decrypted frame
        $outFile = "$outputDir\$($file.BaseName).png"
        [System.IO.File]::WriteAllBytes($outFile, $plainBytes)
        $decryptedFiles += $outFile
        Write-Host $outFile

    } catch {
        Write-Host "Failed to decrypt $($file.Name): Wrong passphrase or corrupted frame"
    }
}

# Log access
$accessTime = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Add-Content $auditLog "LOOK | $accessTime | frames=$($decryptedFiles.Count) | user=$env:USERNAME"

Write-Host "`nFrames decrypted to $outputDir"
Write-Host "WARNING: Delete these files after viewing. They contain unencrypted screen data."
Write-Host "Run: Remove-Item '$outputDir\*.png' -Force"
