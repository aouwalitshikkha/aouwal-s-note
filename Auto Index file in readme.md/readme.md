# Directory Index Generator (PowerShell)
This repository uses a small PowerShell script to automatically generate a clean, navigable index of subfolders inside README.md.

It’s designed for repos that organize content by folders (notes, projects, experiments, docs, etc.) and want a human-readable table of contents without maintaining it manually.


## ✨ What the Script Does

When run from the repository root, the script:

1. Creates README.md (or overwrites the header if it already exists)

2. Scans all immediate subdirectories

3. Sorts them alphabetically

4. Generates Markdown links pointing to each folder

5. URL-encodes folder names so spaces and special characters work correctly on GitHub

Each directory is listed like this:

```text
- 📘 Folder Name
```
…with a clickable link that navigates into the folder.


## The Script
```bash
"# MY NOTES`n" | Out-File README.md

Get-ChildItem -Directory |
Sort-Object Name |
ForEach-Object {
    $encoded = [System.Uri]::EscapeDataString($_.Name)
    "- 📘 [$($_.Name)]($encoded/)"
} | Add-Content README.md
```
## How to Use

1. Open PowerShell
2. Navigate to the repository root
3. Run the script
4. Commit the updated README.md

