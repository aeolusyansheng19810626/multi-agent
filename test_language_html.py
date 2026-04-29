# -*- coding: utf-8 -*-
# Test language switching HTML generation
LANGUAGES = {
    "zh": {"short": "CN", "name": "Simplified Chinese"},
    "ja": {"short": "JP", "name": "Japanese"},
    "en": {"short": "EN", "name": "English"},
}

current_language = "zh"

# Current version (broken)
print("=== Current Version (BROKEN) ===")
language_options_html = ''.join(
    f'<div class="language-option {"active" if code == current_language else ""}" '
    f'onclick="window.location.href="?lang={code}"" style="cursor: pointer;">'
    f'<span class="language-code">{meta["short"]}</span><span>{meta["name"]}</span>'
    f'<span class="language-check">{"V" if code == current_language else ""}</span></div>'
    for code, meta in LANGUAGES.items()
)
print(language_options_html)
print()

# Fix version 1: Escaped double quotes
print("=== Fix Version 1: Escaped quotes ===")
language_options_html = ''.join(
    f'<div class="language-option {"active" if code == current_language else ""}" '
    f"onclick=\"window.location.href='?lang={code}'\" style=\"cursor: pointer;\">"
    f'<span class="language-code">{meta["short"]}</span><span>{meta["name"]}</span>'
    f'<span class="language-check">{"V" if code == current_language else ""}</span></div>'
    for code, meta in LANGUAGES.items()
)
print(language_options_html)
print()

# Fix version 2: Single quotes for onclick
print("=== Fix Version 2: Single quotes ===")
language_options_html = ''.join(
    f"<div class=\"language-option {'active' if code == current_language else ''}\" "
    f"onclick='window.location.href=\"?lang={code}\"' style='cursor: pointer;'>"
    f"<span class=\"language-code\">{meta['short']}</span><span>{meta['name']}</span>"
    f"<span class=\"language-check\">{'V' if code == current_language else ''}</span></div>"
    for code, meta in LANGUAGES.items()
)
print(language_options_html)

# Made with Bob
