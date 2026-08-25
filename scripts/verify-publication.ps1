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
    '.pkg', '.deb', '.rpm', '.iso', '.whl',
    '.dll', '.so', '.dylib', '.pyd', '.node', '.obj', '.o', '.lib', '.pdb',
    '.ipch', '.pch', '.class', '.jar'
)
$blockedPathPattern = '(?i)((^|/)(node_modules|venv|\.venv|site-packages|__pycache__|\.vs|\.idea|\.settings|\.lift|\.vscode|exe|cifar-10-batches-py|\.next)(/|$)|(^|/)[^/]*可执行文件[^/]*(/|$))'
$blockedPrivateDataPattern = '(?i)^大三/大三上/基于Web的编程/Web/(courses|cxzczxc|students|teachers|users)\.json$'
$blockedGeneratedDataPattern = '(?i)^大三/大三下/大模型技术及应用/.+/(code|demo)/(?:[^/]+/)*(data_base|train_data|files|datas|documents)(/|$)'
$blockedThirdPartyAudioPattern = '(?i)(^大一课程/英语/BC_LISTENING.*_Audio\.mp3$|^大三/大三上/图形学/实验/期末大作业/.+/music/.+\.mp3$)'

$blockedFiles = [System.Collections.Generic.List[string]]::new()
$largeFiles = [System.Collections.Generic.List[string]]::new()
$secretFiles = [System.Collections.Generic.List[string]]::new()
$binaryMagicFiles = [System.Collections.Generic.List[string]]::new()
$archiveMagicFiles = [System.Collections.Generic.List[string]]::new()

foreach ($relativePath in $tracked) {
    $extension = [System.IO.Path]::GetExtension($relativePath).ToLowerInvariant()
    if ($blockedExtensions -contains $extension -or $relativePath -match $blockedPathPattern -or $relativePath -match $blockedPrivateDataPattern -or $relativePath -match $blockedGeneratedDataPattern -or $relativePath -match $blockedThirdPartyAudioPattern -or [System.IO.Path]::GetFileName($relativePath) -in @(
        '.classpath', '.project', 'CMakeCache.txt', 'cmake_install.cmake',
        'ALL_BUILD.vcxproj', 'ALL_BUILD.vcxproj.filters',
        'ZERO_CHECK.vcxproj', 'ZERO_CHECK.vcxproj.filters'
    ) -or $extension -eq '.iml') {
        $blockedFiles.Add($relativePath)
    }

    if ($relativePath -match '(^|/)(\.env|\.env\..+)$' -and $relativePath -notmatch '(^|/)\.env\.example$') {
        $secretFiles.Add($relativePath)
    }

    $absolutePath = Join-Path $root $relativePath
    if ((Get-Item -LiteralPath $absolutePath).Length -ge 49MB) {
        $largeFiles.Add($relativePath)
    }

    $stream = $null
    try {
        $stream = [System.IO.File]::OpenRead($absolutePath)
        $bytes = New-Object byte[] 8
        $read = $stream.Read($bytes, 0, $bytes.Length)
        $isCompiledBinary = $false
        if ($read -ge 4 -and $bytes[0] -eq 0x7f -and $bytes[1] -eq 0x45 -and $bytes[2] -eq 0x4c -and $bytes[3] -eq 0x46) {
            $isCompiledBinary = $true
        }
        elseif ($read -ge 2 -and $bytes[0] -eq 0x4d -and $bytes[1] -eq 0x5a) {
            $isCompiledBinary = $true
        }
        elseif ($read -ge 4) {
            $magic = '{0:X2}{1:X2}{2:X2}{3:X2}' -f $bytes[0], $bytes[1], $bytes[2], $bytes[3]
            $isCompiledBinary = $magic -in @('FEEDFACE', 'FEEDFACF', 'CEFAEDFE', 'CFFAEDFE')
        }
        if ($isCompiledBinary) {
            $binaryMagicFiles.Add($relativePath)
        }

        $isArchive = $false
        $allowedZipContainerExtensions = @('.docx', '.xlsx', '.pptx', '.odt', '.ods', '.odp', '.xmind')
        if ($read -ge 4 -and $bytes[0] -eq 0x50 -and $bytes[1] -eq 0x4b -and $bytes[2] -in @(0x03, 0x05, 0x07) -and $bytes[3] -in @(0x04, 0x06, 0x08)) {
            $isArchive = $extension -notin $allowedZipContainerExtensions
        }
        elseif ($read -ge 6 -and $bytes[0] -eq 0x37 -and $bytes[1] -eq 0x7a -and $bytes[2] -eq 0xbc -and $bytes[3] -eq 0xaf -and $bytes[4] -eq 0x27 -and $bytes[5] -eq 0x1c) {
            $isArchive = $true
        }
        elseif ($read -ge 4 -and $bytes[0] -eq 0x52 -and $bytes[1] -eq 0x61 -and $bytes[2] -eq 0x72 -and $bytes[3] -eq 0x21) {
            $isArchive = $true
        }
        elseif ($read -ge 2 -and $bytes[0] -eq 0x1f -and $bytes[1] -eq 0x8b) {
            $isArchive = $true
        }
        elseif ($read -ge 3 -and $bytes[0] -eq 0x42 -and $bytes[1] -eq 0x5a -and $bytes[2] -eq 0x68) {
            $isArchive = $true
        }
        elseif ($read -ge 6 -and $bytes[0] -eq 0xfd -and $bytes[1] -eq 0x37 -and $bytes[2] -eq 0x7a -and $bytes[3] -eq 0x58 -and $bytes[4] -eq 0x5a -and $bytes[5] -eq 0x00) {
            $isArchive = $true
        }
        if ($isArchive) {
            $archiveMagicFiles.Add($relativePath)
        }
    }
    finally {
        if ($null -ne $stream) {
            $stream.Dispose()
        }
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
if ($binaryMagicFiles.Count -gt 0) {
    Write-Error "Compiled executable detected by file signature ($($binaryMagicFiles.Count))."
    $binaryMagicFiles | ForEach-Object { Write-Host "  $_" }
    $failures++
}
if ($archiveMagicFiles.Count -gt 0) {
    Write-Error "Archive detected by file signature ($($archiveMagicFiles.Count))."
    $archiveMagicFiles | ForEach-Object { Write-Host "  $_" }
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
