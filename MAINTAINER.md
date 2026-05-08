# Maintainer guide

This file explains how the site is wired up and how to handle git for someone
new to GitHub.

---

## One-time setup (Windows)

You only do this once on each computer where you want to edit the site locally.

### Step 1 -- install Git

If `git --version` doesn't work in PowerShell, download Git for Windows:
<https://git-scm.com/download/win>. Accept all defaults.

### Step 2 -- install GitHub CLI

This is the easiest way to authenticate without dealing with passwords or
tokens.

```powershell
winget install --id GitHub.cli
```

Then in a fresh PowerShell window:

```powershell
gh auth login
```

Pick:

- GitHub.com
- HTTPS
- Y to authenticate Git with your GitHub credentials
- Login with a web browser
- Copy the one-time code, paste it in the browser, click Authorize.

Once you see "Logged in as jiehu-research", you're done forever -- Claude can
push and pull on your behalf without prompting.

### Step 3 -- have the project folder linked to the repo

Open PowerShell, then:

```powershell
cd "$env:USERPROFILE\Documents\Claude\Projects\Reconstruct Academic Homepage"
git init -b main
git remote add origin https://github.com/jiehu-research/jiehu-research.github.io.git
git fetch origin main
git reset --hard origin/main           # makes your local match the remote
```

Important: this **discards** any uncommitted local files in favour of the
remote. Don't run it if you have edits you want to keep -- ask Claude first.

After this, the folder is a normal git working copy. You don't need to run
those commands again.

---

## Daily workflow

### To pull the latest from GitHub

```powershell
cd "$env:USERPROFILE\Documents\Claude\Projects\Reconstruct Academic Homepage"
git pull
```

Or just say to Claude: **"Pull the latest from my homepage repo."**

### To push your changes

```powershell
git add -A
git commit -m "describe what you changed"
git push
```

Or say to Claude: **"Commit and push my changes with the message 'added X'."**

GitHub Pages rebuilds the site automatically; the new version is live in
about 60 seconds. You can watch progress at:

<https://github.com/jiehu-research/jiehu-research.github.io/actions>

---

## What goes where

| To change                          | Edit this file                       |
|------------------------------------|--------------------------------------|
| Name, title, social links          | `_config.yml`                        |
| Recruiting blurb                   | `_config.yml` (recruiting: section)  |
| News items                         | `_data/news.yml`                     |
| Publications                       | `_data/publications.yml`             |
| Teaching list (homepage)           | `_data/teaching.yml`                 |
| Profile photo                      | `assets/images/profile.png` (replace) |
| CV                                 | `assets/files/cv.pdf` (replace)      |
| Site styling / colours             | `assets/css/main.css`                |
| Page layout / sections             | `index.md`                           |

Most of the time you'll only touch the YAML files in `_data/`.

---

## Troubleshooting

### "Site says 'page not found' after I pushed"

Wait 60 seconds for the GitHub Pages build to finish. If it still doesn't
work, check the **Actions** tab on GitHub for build errors.

### "I edited a YAML file and the site is broken"

YAML is whitespace-sensitive. Most likely:

- A line is indented with tabs instead of spaces (always use spaces).
- A quoted string contains an unescaped `"`.
- A `>` or `|` block doesn't have its content indented further than the key.

To validate locally before pushing:

```powershell
python -c "import yaml; yaml.safe_load(open('_data/publications.yml'))"
```

If that prints nothing, the file is valid. If it prints an error, fix the
line it points to.

### "I want to discard all my local changes"

```powershell
git fetch origin main
git reset --hard origin/main
```

Warning: this deletes any uncommitted edits.

### "I accidentally pushed something I shouldn't have"

Don't try to fix it yourself. Tell Claude: *"I just pushed a commit by
mistake -- the wrong CV / wrong photo / wrong info. Please revert it."*
Reverting in git is safe but easy to mess up by hand.

---

## Anatomy of a Jekyll site (very brief)

When you push, GitHub Pages does the following:

1. Reads `_config.yml` to get site-wide settings.
2. Renders each `.md` and `.html` file through the Liquid template engine,
   substituting `{{ ... }}` and `{% ... %}` tags with values from your data.
3. Wraps each rendered file in the layout specified by its front-matter
   (e.g. `layout: default`, found in `_layouts/default.html`).
4. Drops the result into the `_site/` folder, which is what people see.

Files starting with `_` are templates / data; everything else becomes a real
page on the site. The folder structure under the project root maps directly
to URLs (so `publications/index.md` is served at `/publications/`).
