[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$root = (git rev-parse --show-toplevel).Trim()
if ([string]::IsNullOrWhiteSpace($root)) {
    throw 'Run this script inside the Git repository.'
}

$tracked = @(git -C $root ls-files)
$blockedExtensions = @(
    '.zip', '.rar', '.7z', '.tar', '.gz', '.tgz', '.bz2', '.xz', '.cab',
    '.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv', '.wmv', '.m4v',
    '.mpg', '.mpeg', '.exe', '.msi', '.msix', '.appx', '.apk', '.dmg',
    '.pkg', '.deb', '.rpm', '.iso', '.whl'
)
$blockedPathPattern = '(?i)(^|/)(node_modules|venv|\.venv|site-packages|__pycache__|\.vs|\.idea|\.next)(/|$)'

$blockedFiles = [System.Collections.Generic.List[string]]::new()
$largeFiles = [System.Collections.Generic.List[string]]::new()
$secretFiles = [System.Collections.Generic.List[string]]::new()

foreach ($relativePath in $tracked) {
    $extension = [System.IO.Path]::GetExtension($relativePath).ToLowerInvariant()
    if ($blockedExtensions -contains $extension -or $relativePath -match $blockedPathPattern) {
        $blockedFiles.Add($relativePath)
    }

    if ($relativePath -match '(^|/)(\.env|\.env\..+)$' -and $relativePath -notmatch '(^|/)\.env\.example$') {
        $secretFiles.Add($relativePath)
    }

    $absolutePath = Join-Path $root $relativePath
    if ((Get-Item -LiteralPath $absolutePath).Length -ge 49MB) {
        $largeFiles.Add($relativePath)
    }
}

$secretPatterns = @(
    'AKIA[0-9A-Z]{16}',
    'github_pat_[A-Za-z0-9_]{20,}',
    'gh[pousr]_[A-Za-z0-9]{20,}',
    'sk-[A-Za-z0-9_-]{20,}',
    '-----BEGIN ([A-Z ]+ )?PRIVATE KEY-----',
    '(?i)(api[_-]?key|client[_-]?secret|access[_-]?token)\s*[:=]\s*["''][^"'']{8,}["'']'
)
$rgArguments = @('-l', '-uu', '--no-messages')
foreach ($pattern in $secretPatterns) {
    $rgArguments += @('-e', $pattern)
}
$rgArguments += $root
$secretMatches = @(& rg @rgArguments)
foreach ($match in $secretMatches) {
    $secretFiles.Add($match)
}

$failures = 0
if ($blockedFiles.Count -gt 0) {
    Write-Error "Blocked file or dependency path found ($($blockedFiles.Count))."
    $blockedFiles | ForEach-Object { Write-Host "  $_" }
    $failures++
}
if ($largeFiles.Count -gt 0) {
    Write-Error "File at or above 49 MiB found ($($largeFiles.Count))."
    $largeFiles | ForEach-Object { Write-Host "  $_" }
    $failures++
}
if ($secretFiles.Count -gt 0) {
    Write-Error "Potential credential found ($($secretFiles.Count)). Values are not displayed."
    $secretFiles | Sort-Object -Unique | ForEach-Object { Write-Host "  $_" }
    $failures++
}

if ($failures -gt 0) {
    exit 1
}

$bytes = [int64]0
foreach ($relativePath in $tracked) {
    $bytes += (Get-Item -LiteralPath (Join-Path $root $relativePath)).Length
}

[pscustomobject]@{
    Result = 'pass'
    TrackedFiles = $tracked.Count
    WorkingTreeGiB = [math]::Round($bytes / 1GB, 3)
} | ConvertTo-Json
