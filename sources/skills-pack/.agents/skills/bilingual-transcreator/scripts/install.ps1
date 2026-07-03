[CmdletBinding()]
param([switch]$Force)
$ErrorActionPreference = "Stop"
$SkillDir = Split-Path -Parent $PSScriptRoot
$Dest = Join-Path $HOME ".agents/skills/bilingual-transcreator"
if ((Test-Path $Dest) -and -not $Force) { throw "Refusing to overwrite $Dest. Re-run with -Force." }
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $Dest) | Out-Null
Remove-Item -Recurse -Force $Dest -ErrorAction SilentlyContinue
Copy-Item -Recurse -Force $SkillDir $Dest
Write-Host "Installed for Codex: $Dest"
