"# MY NOTES`n" | Out-File README.md

Get-ChildItem -Directory |
Sort-Object Name |
ForEach-Object {
    $encoded = [System.Uri]::EscapeDataString($_.Name)
    "- 📘 [$($_.Name)]($encoded/)"
} | Add-Content README.md
