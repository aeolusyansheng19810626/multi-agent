import re
import sys

def run():
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Sidebar title
    old_sidebar = 'st.sidebar.markdown("### 🎯 选择协作模式")\nst.sidebar.markdown("<div style=\'height: 10px\'></div>", unsafe_allow_html=True)'
    new_sidebar = '''st.sidebar.markdown(
    """
    <div style="padding: 10px 0 20px 0;">
        <div style="font-size: 18px; font-weight: 700; color: #1F2937; margin-bottom: 8px; display: flex; align-items: center; gap: 8px;">
            🎯 协作模式
        </div>
        <div style="font-size: 13px; color: #6B7280; line-height: 1.5;">
            点击下方卡片，体验不同多智能体架构组合与执行流程
        </div>
    </div>
    """,
    unsafe_allow_html=True
)'''
    if old_sidebar in content:
        content = content.replace(old_sidebar, new_sidebar)
        print("Replaced sidebar successfully.")
    else:
        print("Warning: old sidebar not found.")

    # 2. Banner
    content = content.replace('background: linear-gradient(135deg, #2D1B69 0%, #6C63FF 100%);', 'background: linear-gradient(135deg, #3B82F6 0%, #6C63FF 100%);')
    content = content.replace('.top-navbar {\n        background:', '.top-navbar {\n        color: white !important;\n        background:')
    content = content.replace('.navbar-left {\n        display:', '.navbar-left {\n        color: white !important;\n        display:')
    content = content.replace('.navbar-title {\n        color: white;', '.navbar-title {\n        color: white !important;')
    content = content.replace('.navbar-right {\n        color: rgba(255, 255, 255, 0.9);', '.navbar-right {\n        color: white !important;')
    print("Replaced banner colors successfully.")

    # 3. Headers
    headers_map = {
        'st.markdown("#### 🔄 Supervisor Pipeline")': 'st.markdown("#### 🔄 顺序流水线")',
        'st.markdown("#### 🔀 Conditional Branch")': 'st.markdown("#### 🔀 条件分支")',
        'st.markdown("#### 🔁 Loop Feedback")': 'st.markdown("#### 🔁 循环反馈")',
        'st.markdown("#### ⚡ Parallel Review")': 'st.markdown("#### ⚡ 并行执行")',
        'st.markdown("#### ⚔️ 代码辩论")': 'st.markdown("#### ⚔️ 辩论模式")',
        'st.markdown("#### 🪆 Nested Agent")': 'st.markdown("#### 🪆 嵌套 Agent")',
        'st.markdown("#### 🌀 Hybrid A · 并行生成 + 循环质检 + 条件分支")': 'st.markdown("#### 🌀 混合模式 A")',
        'st.markdown("#### 🏗️ 架构方案评审")': 'st.markdown("#### 🔀 混合模式 B")'
    }
    for k, v in headers_map.items():
        if k in content:
            content = content.replace(k, v)
        else:
            print(f"Warning: Header not found: {k}")

    # 4. Remove icon and title from else blocks
    # Looking for:
    # <div style="text-align:center;padding:80px 20px;">
    #     <div style="font-size:64px;margin-bottom:24px;">🔄</div>
    #     <div style="font-size:20px;font-weight:600;color:#1F2937;margin-bottom:12px;">Supervisor Pipeline</div>
    # OR:
    # <div style="text-align:center;padding:60px 20px;color:#AAAAAA;">
    #     <div style="font-size:40px;margin-bottom:16px;">🔀</div>
    #     <div style="font-size:16px;font-weight:500;color:#888888;margin-bottom:8px;">Conditional Branch 已就绪</div>

    # General regex for these two divs immediately following the padding div:
    pattern = r'(<div style="text-align:center;padding:[^>]*>)\s*<div style="font-size:(?:40|64)px;margin-bottom:(?:16|24)px;">.*?</div>\s*<div style="font-size:(?:16|20)px;[^>]*>.*?</div>'
    
    matches = re.findall(pattern, content)
    print(f"Found {len(matches)} placeholder blocks to trim.")
    content = re.sub(pattern, r'\1', content)

    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("All changes applied successfully to app.py.")

if __name__ == "__main__":
    run()