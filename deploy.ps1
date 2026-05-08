# =============================================================
#  deploy.ps1 -- one-time deployment script for jiehu-research.github.io
# -------------------------------------------------------------
#  Run this once from PowerShell, in this folder, after you've authed
#  to GitHub via `gh auth login` (see MAINTAINER.md, step 2).
#
#  Usage (from PowerShell, in this folder):
#      .\deploy.ps1
#
#  What it does:
#    1. Initialises git if not yet initialised.
#    2. Sets the remote to your repo.
#    3. Stages and commits everything.
#    4. Force-pushes to the master branch (replaces the live site).
#
#  After this initial deploy, day-to-day work uses normal git commands:
#      git add -A
#      git commit -m "describe your edit"
#      git push
# =============================================================

$ErrorActionPreference = "Stop"

$RepoUrl    = "https://github.com/jiehu-research/jiehu-research.github.io.git"
$Branch     = "master"      # GitHub Pages source branch -- update if yours is "main"
$UserName   = "Jie Hu"
$UserEmail  = "jiehu@oakland.edu"

Write-Host ""
Write-Host "-> Setting up git in $(Get-Location)" -ForegroundColor Cyan

if (-not (Test-Path ".git")) {
    git init -b $Branch
}

git config user.name  $UserName
git config user.email $UserEmail

# Remote
$existingRemote = git remote get-url origin 2>$null
if ($null -eq $existingRemote) {
    git remote add origin $RepoUrl
} elseif ($existingRemote -ne $RepoUrl) {
    Write-Warning "origin already set to $existingRemote"
    Write-Warning "Re-pointing to $RepoUrl"
    git remote set-url origin $RepoUrl
}

# Fetch what's there so we're not pushing into a vacuum
Write-Host "-> Fetching remote..." -ForegroundColor Cyan
git fetch origin $Branch

Write-Host ""
Write-Host "-> Staging files..." -ForegroundColor Cyan
git add -A
git status --short | Select-Object -First 30

Write-Host ""
$ans = Read-Host "Proceed with commit and FORCE PUSH to origin/$Branch? This replaces the live site. (yes/no)"
if ($ans -ne "yes") {
    Write-Host "Aborted. No changes pushed." -ForegroundColor Yellow
    exit 0
}

git commit -m "Polish homepage: clean minimal redesign with full content + tooling" --allow-empty

Write-Host ""
Write-Host "-> Force-pushing to origin/$Branch..." -ForegroundColor Cyan
git push --force-with-lease origin HEAD:$Branch

Write-Host ""
Write-Host "Done. Watch the build at:" -ForegroundColor Green
Write-Host "https://github.com/jiehu-research/jiehu-research.github.io/actions" -ForegroundColor Green
Write-Host ""
Write-Host "Live site (refreshes in ~60s):" -ForegroundColor Green
Write-Host "https://jiehu-research.github.io" -ForegroundColor Green
