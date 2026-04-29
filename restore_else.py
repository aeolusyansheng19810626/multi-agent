import re

with open('original_app.py', 'r', encoding='utf-16') as f:
    orig = f.read()

with open('app.py', 'r', encoding='utf-8') as f:
    curr = f.read()

functions = [
    "_render_supervisor_pipeline",
    "_render_conditional_branch",
    "_render_loop_feedback",
    "_render_parallel_review",
    "_render_debate",
    "_render_nested_agent",
    "_render_hybrid_a",
    "_render_hybrid_b"
]

for func in functions:
    pattern = rf'def {func}\(\):.*?(\n    else:\n        st\.markdown\(\n            """\n            <div style="text-align:center;padding:[^`]*?unsafe_allow_html=True,\n        \))'
    match = re.search(pattern, orig, flags=re.DOTALL)
    if match:
        else_block = match.group(1)
        
        # Regex to remove those two lines. Example:
        # <div style="font-size:40px;margin-bottom:16px;">图标</div>
        # <div style="font-size:16px;font-weight:500;color:#888888;margin-bottom:8px;">标题</div>
        
        modified_else = re.sub(r'(\s+)<div style="font-size:(?:40|64)px;[^>]*>.*?</div>\n\s+<div style="font-size:(?:16|20)px;[^>]*>.*?</div>\n', r'\1', else_block)
        
        # In `curr`, we need to find the function definition and replace it up to the next `# ──` or `def _render`.
        func_pattern = rf'(def {func}\(\):.*?)(?=\n# ── |\ndef _render)'
        curr_match = re.search(func_pattern, curr, flags=re.DOTALL)
        if curr_match:
            func_content = curr_match.group(1)
            # The current content doesn't have the `else:` block.
            new_func_content = func_content.rstrip() + modified_else + '\n\n\n'
            curr = curr.replace(func_content, new_func_content)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(curr)
print("Restored modified else blocks.")
