"""
Multi-Agent 协作分析平台
支持 6 种 Agent 协作模式：
1. Supervisor Pipeline（监督者流水线）
2. Conditional Branch（条件分支）
3. Loop Feedback（循环反馈）
4. Parallel Review（并行审查）
5. Debate（辩论对抗）
6. Nested Agent（嵌套 Agent）
7. Hybrid A（混合模式 A：并行生成 + 循环质检 + 条件分支）
8. Hybrid B（混合模式 B：辩论 + 嵌套 Agent）
"""

import streamlit as st
import sys
import os

# ── 路径设置 ───────────────────────────────────────────
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ── 页面配置 ───────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Agent 协作分析平台",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 全局 CSS ───────────────────────────────────────────
st.markdown(
    """
    <style>
    /* 全局样式 */
    .stApp {
        background-color: #F8F9FA;
    }
    
    /* 顶部导航栏 */
    .top-navbar {
        background: linear-gradient(135deg, #1D4ED8 0%, #3B82F6 100%);
        padding: 14px 40px;
        margin: -8px -80px 30px -80px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .navbar-left {
        display: flex;
        align-items: center;
        gap: 15px;
    }

    .navbar-logo {
        font-size: 32px;
    }

    .navbar-title {
        color: #FFFFFF !important;
        font-size: 24px;
        font-weight: 700;
        margin: 0;
    }

    .navbar-right {
        color: rgba(255, 255, 255, 0.9);
        font-size: 14px;
        font-weight: 400;
    }
    
    /* 模式卡片样式 */
    .mode-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
        border: 2px solid #E5E7EB;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    .mode-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 16px rgba(108, 99, 255, 0.2);
        border-color: #6C63FF;
    }
    
    .mode-card.selected {
        border-color: #6C63FF;
        background: linear-gradient(135deg, #F5F3FF 0%, #FFFFFF 100%);
        box-shadow: 0 4px 12px rgba(108, 99, 255, 0.3);
    }
    
    .mode-card-icon {
        font-size: 48px;
        margin-bottom: 12px;
        text-align: center;
    }
    
    .mode-card-title {
        font-size: 16px;
        font-weight: 700;
        color: #1F2937;
        margin-bottom: 8px;
        text-align: center;
    }
    
    .mode-card-desc {
        font-size: 13px;
        color: #6B7280;
        line-height: 1.5;
        text-align: center;
        margin-bottom: 12px;
    }
    
    .mode-card-status {
        text-align: center;
        font-size: 12px;
        font-weight: 600;
    }
    
    .status-ready {
        color: #10B981;
    }
    
    .status-coming {
        color: #F59E0B;
    }
    
    /* 输入框样式 */
    .stTextArea textarea {
        border-radius: 12px !important;
        border: 2px solid #E5E7EB !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1) !important;
        padding: 16px !important;
        font-size: 14px !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #6C63FF !important;
        box-shadow: 0 0 0 3px rgba(108, 99, 255, 0.1) !important;
    }
    
    /* 按钮样式 */
    .stButton > button {
        background: linear-gradient(135deg, #6C63FF 0%, #8B7FFF 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        box-shadow: 0 4px 6px rgba(108, 99, 255, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 12px rgba(108, 99, 255, 0.4) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* Agent状态卡片 */
    .agent-status-card {
        background: white;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .agent-status-card:hover {
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }
    
    /* 折叠面板样式 */
    .streamlit-expanderHeader {
        background: white !important;
        border-radius: 8px !important;
        border: 1px solid #E5E7EB !important;
        padding: 12px 16px !important;
        font-weight: 600 !important;
        color: #1F2937 !important;
    }
    
    .streamlit-expanderHeader:hover {
        border-color: #6C63FF !important;
        background: #F9FAFB !important;
    }
    
    .streamlit-expanderContent {
        border: 1px solid #E5E7EB !important;
        border-top: none !important;
        border-radius: 0 0 8px 8px !important;
        background: white !important;
    }
    
    /* Model Badge */
    .model-badge {
        display: inline-block;
        background: linear-gradient(135deg, #6C63FF 0%, #8B7FFF 100%);
        color: white;
        font-size: 11px;
        padding: 4px 10px;
        border-radius: 12px;
        margin-bottom: 8px;
        font-family: 'Courier New', monospace;
        font-weight: 600;
        box-shadow: 0 2px 4px rgba(108, 99, 255, 0.3);
    }
    
    /* 状态徽章 */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
    }
    
    .status-pending {
        background: #F3F4F6;
        color: #6B7280;
    }
    
    .status-running {
        background: #DBEAFE;
        color: #2563EB;
    }
    
    .status-done {
        background: #D1FAE5;
        color: #059669;
    }
    
    /* 隐藏 Streamlit 默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden; height: 0 !important; min-height: 0 !important;}
    [data-testid="stDecoration"] {visibility: hidden; height: 0 !important;}
    header[data-testid="stHeader"] {height: 0 !important; min-height: 0 !important;}
    
    /* 侧边栏样式 - 与主区域一致的浅色背景 */
    [data-testid="stSidebar"] {
        background-color: #F8F9FA !important;
        border-right: 1px solid #E5E7EB !important;
        padding: 6px 12px !important;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: transparent !important;
    }
    
    
    /* 主内容区域 */
    .main .block-container {
        padding-top: 0 !important;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    [data-testid="stMainBlockContainer"] {
        padding-top: 0 !important;
    }
    
    /* 信息提示框 */
    .stAlert {
        border-radius: 8px !important;
        border-left: 4px solid #6C63FF !important;
    }
    
    /* 成功提示框 */
    .stSuccess {
        background-color: #D1FAE5 !important;
        border-left-color: #10B981 !important;
    }
    
    /* 警告提示框 */
    .stWarning {
        background-color: #FEF3C7 !important;
        border-left-color: #F59E0B !important;
    }
    
    /* 错误提示框 */
    .stError {
        background-color: #FEE2E2 !important;
        border-left-color: #EF4444 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── 顶部导航栏 ───────────────────────────────────────────
st.markdown(
    """
    <div class="top-navbar">
        <div class="navbar-left">
            <h1 class="navbar-title">多智能体协作分析平台</h1>
        </div>
        <div class="navbar-right">
            基于 LangGraph + Groq 的智能协作系统
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── 侧边栏：模式选择 ──────────────────────────────────
st.sidebar.markdown("""
<div style="margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid #E5E7EB;">
    <div style="font-size: 12px; color: #9CA3AF; font-weight: 600; letter-spacing: 1.2px; text-transform: uppercase; margin-bottom: 5px;">编排模式</div>
    <div style="font-size: 16px; color: #374151; font-weight: 700;">点击卡片选择协作方式 👇</div>
</div>
""", unsafe_allow_html=True)

MODES = [
    {"key": "supervisor_pipeline", "label": "顺序流水线", "icon": "🔄", "desc": "每个 Agent 处理前一个的输出", "status": "Ready"},
    {"key": "conditional_branch", "label": "条件分支", "icon": "🔀", "desc": "根据代码特征动态选择审查路径", "status": "Ready"},
    {"key": "loop_feedback", "label": "循环反馈", "icon": "🔁", "desc": "代码生成→审查→修复，直到通过", "status": "Ready"},
    {"key": "parallel", "label": "并行执行", "icon": "🔱", "desc": "多维度同时分析后汇总报告", "status": "Ready"},
    {"key": "debate", "label": "辩论模式", "icon": "⚔️", "desc": "支持方 vs 反对方，裁判给出建议", "status": "Ready"},
    {"key": "nested_agent", "icon": "🪆", "label": "嵌套 Agent", "desc": "Orchestrator 召唤子 Agent 并行执行", "status": "Ready"},
    {"key": "hybrid_a", "icon": "🎛️", "label": "混合模式 A", "desc": "并行生成 + 循环质检 + 条件分支", "status": "Ready"},
    {"key": "hybrid_b", "icon": "🎭", "label": "混合模式 B", "desc": "辩论 + 嵌套 Agent 综合协作", "status": "Coming"},
]

# 初始化选中的模式
if "selected_mode_key" not in st.session_state:
    st.session_state.selected_mode_key = "supervisor_pipeline"

# 注入侧边栏核心 CSS
st.sidebar.markdown(
    """
    <style>
    /* 侧边栏容器 */
    [data-testid="stSidebar"] {
        background-color: #F8F9FA !important;
        border-right: 1px solid #E5E7EB !important;
    }
    
    /* 侧边栏标题 */
    [data-testid="stSidebar"] h3 {
        color: #374151 !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        margin-bottom: 20px !important;
        border-left: 4px solid #6C63FF;
        padding-left: 12px !important;
    }

    /* 视觉卡片层 */
    .mode-card-visual {
        background: rgba(255, 255, 255, 0.8);
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 16px 20px; /* 显著增加内边距 */
        height: 100px; /* 匹配精确高度 */
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        position: relative;
        z-index: 1;
        pointer-events: none;
        transition: all 0.3s ease;
    }

    .mode-card-visual.selected {
        border-left: 5px solid #6C63FF !important;
        background: white;
        border-color: #6C63FF;
        box-shadow: 0 4px 20px rgba(108, 99, 255, 0.15);
    }

    /* 当覆盖在上面的按钮被 hover 时，下方的视觉卡片触发动效 */
    [data-testid="stSidebar"] .element-container:has(+ .element-container .stButton button:hover) .mode-card-visual {
        border-color: #6C63FF !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 25px rgba(108, 99, 255, 0.12) !important;
    }

    .card-row-1 {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .card-title-group {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .card-icon { font-size: 18px; }
    .card-title-text { 
        font-weight: 600; 
        font-size: 15px; 
        color: #1F2937; 
    }

    .card-row-2 {
        font-size: 12px;
        color: #6B7280;
        line-height: 1.5;
        margin-top: 6px;
        text-align: left;
    }

    /* 按钮交互层（完全透明） */
    [data-testid="stSidebar"] .stMarkdown {
        margin-bottom: 0px !important;
    }

    [data-testid="stSidebar"] .stButton {
        height: 100px !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    [data-testid="stSidebar"] .element-container:has(.stButton) {
        margin-top: -116px !important; /* 向上拉 100px高度 + 16px gap 覆盖卡片 */
        margin-bottom: 12px !important; /* 控制卡片间的间距 */
    }

    [data-testid="stSidebar"] .stButton > button {
        height: 100px !important;
        background: transparent !important;
        border: none !important;
        color: transparent !important;
        box-shadow: none !important;
        width: 100% !important;
        z-index: 10 !important;
        outline: none !important;
        padding: 0 !important;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover,
    [data-testid="stSidebar"] .stButton > button:active,
    [data-testid="stSidebar"] .stButton > button:focus {
        background: transparent !important;
        border: none !important;
        color: transparent !important;
        box-shadow: none !important;
        outline: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 渲染卡片循环
for mode in MODES:
    is_selected = st.session_state.selected_mode_key == mode["key"]
    
    # 1. 渲染视觉外观
    st.sidebar.markdown(f"""
        <div class="mode-card-visual {'selected' if is_selected else ''}">
            <div class="card-row-1">
                <span class="card-title-group">
                    <span class="card-icon">{mode['icon']}</span>
                    <span class="card-title-text">{mode['label']}</span>
                </span>
            </div>
            <div class="card-row-2">{mode['desc']}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # 2. 渲染透明按钮覆盖层
    if st.sidebar.button("", key=f"nav_btn_{mode['key']}", use_container_width=True):
        st.session_state.selected_mode_key = mode["key"]
        st.rerun()

# ── 获取当前选中的模式数据 ──────────────────────────────
current_mode = next((m for m in MODES if m["key"] == st.session_state.selected_mode_key), MODES[0])
selected_mode_label = f"{current_mode['icon']} {current_mode['label']}"

# ── Agent 图标和名称映射 ─────────────────────────────
AGENT_ICONS = {
    "supervisor": "🎯",
    "requirement": "📋",
    "architect": "🏗️",
    "coder": "💻",
    "tester": "🧪",
    "documenter": "📝",
    "security_agent": "🔒",
    "performance_agent": "⚡",
    "maintainability_agent": "🔧",
    "merge_agent": "📊",
    "pro": "🟢",
    "con": "🔴",
    "judge": "⚖️",
    "orchestrator": "🎼",
    "lf_coder": "💻",
    "lf_reviewer": "🔍",
    "lf_fixer": "🔧",
    "pro_orchestrator": "🎼",
    "con_orchestrator": "🎼",
    "performance_agent": "⚡",
    "cost_agent": "💰",
    "security_agent": "🔒",
    "maintainability_agent": "🔧",
    "pro_summarizer": "🟢",
    "con_summarizer": "🔴",
    "judge_agent": "⚖️",
}

AGENT_NAMES = {
    "supervisor": "监督者",
    "requirement": "需求分析",
    "architect": "架构师",
    "coder": "程序员",
    "tester": "测试员",
    "documenter": "文档员",
    "security_agent": "安全审查",
    "performance_agent": "性能分析",
    "maintainability_agent": "可维护性分析",
    "merge_agent": "汇总报告",
    "pro": "支持方",
    "con": "反对方",
    "judge": "裁判",
    "analyst": "需求分析",
    "reviewer": "代码审查",
    "orchestrator": "协调者",
    "lf_coder": "程序员",
    "lf_reviewer": "审查员",
    "lf_fixer": "修复员",
    "pro_orchestrator": "支持方协调者",
    "con_orchestrator": "反对方协调者",
    "performance_agent": "性能分析",
    "cost_agent": "成本分析",
    "security_agent": "安全审查",
    "maintainability_agent": "可维护性分析",
    "pro_summarizer": "支持方",
    "con_summarizer": "反对方",
    "judge_agent": "裁判",
}

# ── 通用组件 ───────────────────────────────────────────

def _status_badge(status: str) -> str:
    """返回状态徽章 HTML（使用新的紫色主题样式）"""
    badges = {
        "pending": '<span class="status-badge status-pending">⏳ 等待中</span>',
        "running": '<span class="status-badge status-running">🔄 运行中</span>',
        "done": '<span class="status-badge status-done">✅ 完成</span>',
    }
    return badges.get(status, status)


def _render_coming_soon(label: str, desc: str):
    """渲染“即将推出”占位页"""
    st.markdown(
        f"""
        <div style="text-align:center;padding:80px 20px;color:#AAAAAA;">
            <div style="font-size:48px;margin-bottom:16px;">🚧</div>
            <div style="font-size:20px;font-weight:600;margin-bottom:8px;">{label}</div>
            <div style="font-size:14px;">{desc}</div>
            <div style="font-size:13px;margin-top:16px;color:#888;">即将推出，敬请期待...</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ── Supervisor Pipeline 模式 ────────────────────────────
def _render_supervisor_pipeline():
    """Supervisor Pipeline 模式渲染函数"""
    from supervisor_pipeline import stream_supervisor

    AGENT_ORDER = ["analyst", "architect", "coder", "reviewer"]
    AGENT_ICONS_LOCAL = {"analyst": "📋", "architect": "🏗️", "coder": "💻", "reviewer": "🔍"}
    RESULT_KEYS = {"analyst": "analysis_result", "architect": "architecture_result", "coder": "code_result", "reviewer": "review_result"}

    st.markdown("#### 🔄 顺序流水线")
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        req_input = st.text_area("需求描述", height=120, placeholder="例如：开发一个用户登录模块，支持 JWT 认证...", label_visibility="collapsed", key="sp_req")
    with col_btn:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        run_btn = st.button("🚀 开始执行", use_container_width=True, type="primary", key="sp_run")

    st.divider()

    if "sp_agent_status" not in st.session_state:
        st.session_state.sp_agent_status = {k: "pending" for k in AGENT_ORDER}
    if "sp_results" not in st.session_state:
        st.session_state.sp_results = {}
    if "sp_model_used" not in st.session_state:
        st.session_state.sp_model_used = {}
    if "sp_is_running" not in st.session_state:
        st.session_state.sp_is_running = False

    path_container = st.empty()

    def _render_sp_state():
        with path_container.container():
            status_cols = st.columns(4)
            for i, agent_key in enumerate(AGENT_ORDER):
                with status_cols[i]:
                    icon = AGENT_ICONS_LOCAL[agent_key]
                    name = AGENT_NAMES[agent_key]
                    badge = _status_badge(st.session_state.sp_agent_status[agent_key])
                    st.markdown(
                        f"""
                        <div class="agent-status-card">
                            <div style='font-size:32px;margin-bottom:8px'>{icon}</div>
                            <div style='font-size:13px;font-weight:600;color:#1F2937;margin-bottom:8px'>{name}</div>
                            <div style='font-size:11px'>{badge}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            for agent_key in AGENT_ORDER:
                result = st.session_state.sp_results.get(agent_key, "")
                with st.expander(f"{AGENT_ICONS_LOCAL[agent_key]} {AGENT_NAMES[agent_key]}", expanded=False):
                    model_name = st.session_state.sp_model_used.get(agent_key, "")
                    if model_name:
                        st.markdown(f'<span class="model-badge">🧠 {model_name}</span>', unsafe_allow_html=True)
                    if result:
                        st.markdown(result)

    if run_btn and req_input.strip():
        st.session_state.sp_agent_status = {k: "pending" for k in AGENT_ORDER}
        st.session_state.sp_results = {}
        st.session_state.sp_model_used = {}
        st.session_state.sp_is_running = True

        for node_name, state_update in stream_supervisor(req_input.strip()):
            st.session_state.sp_model_used.update(state_update.get("model_used_by", {}))
            if node_name in st.session_state.sp_agent_status:
                result_key = RESULT_KEYS[node_name]
                st.session_state.sp_results[node_name] = state_update.get(result_key, "")
                st.session_state.sp_agent_status[node_name] = "done"
                next_idx = AGENT_ORDER.index(node_name) + 1
                if next_idx < len(AGENT_ORDER):
                    st.session_state.sp_agent_status[AGENT_ORDER[next_idx]] = "running"

            _render_sp_state()

        st.session_state.sp_is_running = False
        st.success("🎉 顺序流水线执行完成！")

    elif run_btn and not req_input.strip():
        st.warning("⚠️ 请先输入需求描述再开始执行。")

    elif not st.session_state.sp_is_running and st.session_state.sp_results:
        _render_sp_state()
    else:
        st.markdown(
            """
            <div style="padding:20px 0;color:#6B7280;font-size:14px;line-height:1.8;">
                监督者流水线模式：顺序执行，每个 Agent 处理前一个的输出<br>
                <span style="color:#6C63FF;font-weight:500;">📋 需求分析 → 🏗️ 架构师 → 💻 程序员 → 🔍 代码审查</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ── Conditional Branch 模式 ─────────────────────────────
def _render_conditional_branch():
    from conditional_branch import stream_conditional

    AGENT_ICONS = {
        "router": "🧭", "cb_analyst": "📋", "cb_architect": "🏗️", "cb_coder": "💻",
        "cb_reviewer": "🔍", "cb_optimizer": "✨",
        "cb_researcher": "🕵️", "cb_advisor": "💡"
    }
    AGENT_NAMES_LOCAL = {
        "router": "路由分配", "cb_analyst": "需求分析", "cb_architect": "架构设计", "cb_coder": "编码生成",
        "cb_reviewer": "代码审查", "cb_optimizer": "代码优化",
        "cb_researcher": "技术调研", "cb_advisor": "技术顾问"
    }
    RESULT_KEYS = {
        "router": "router_decision", "cb_analyst": "analysis_result", "cb_architect": "architecture_result", "cb_coder": "code_result",
        "cb_reviewer": "review_result", "cb_optimizer": "optimization_result",
        "cb_researcher": "research_result", "cb_advisor": "advice_result"
    }

    col_input, col_btn = st.columns([5, 1])
    with col_input:
        requirement = st.text_area(
            label="请描述你的需求、代码或技术问题",
            placeholder="例如：\n[新功能] 我想加一个微信支付模块...\n[代码审查] 帮我看看这段 React 代码有没有坑...\n[技术问题] Next.js 和 Nuxt.js 选哪个好？",
            height=120,
            label_visibility="collapsed",
            key="cb_requirement",
        )
    with col_btn:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        run_btn = st.button("🚀 开始执行", use_container_width=True, type="primary", key="cb_run")

    st.divider()

    for key, default in [
        ("cb_results", {}),
        ("cb_agent_status", {}),
        ("cb_model_used", {}),
        ("cb_is_running", False),
        ("cb_active_path", []),
        ("cb_router_reason", "")
    ]:
        if key not in st.session_state:
            st.session_state[key] = default

    path_container = st.empty()

    if run_btn and requirement.strip():
        st.session_state.cb_results = {}
        st.session_state.cb_agent_status = {"router": "running"}
        st.session_state.cb_model_used = {}
        st.session_state.cb_is_running = True
        st.session_state.cb_active_path = []
        st.session_state.cb_router_reason = "🤔 正在分析需求类型..."

        for node_name, state_update in stream_conditional(requirement.strip()):
            st.session_state.cb_agent_status[node_name] = "done"
            result_key = RESULT_KEYS.get(node_name, "")

            model_map = state_update.get("model_used_by", {})
            model_name = model_map.get(node_name, "unknown")
            st.session_state.cb_model_used[node_name] = model_name

            if node_name == "router":
                decision = state_update.get("router_decision", {})
                route = decision.get("route", "new_feature")
                reason = decision.get("reason", "")
                st.session_state.cb_router_reason = f"检测到：{route}，原因：{reason}"

                if route == "new_feature":
                    st.session_state.cb_active_path = ["cb_analyst", "cb_architect", "cb_coder"]
                elif route == "code_review":
                    st.session_state.cb_active_path = ["cb_reviewer", "cb_optimizer"]
                elif route == "tech_question":
                    st.session_state.cb_active_path = ["cb_researcher", "cb_advisor"]
                else:
                    st.session_state.cb_active_path = ["cb_analyst", "cb_architect", "cb_coder"]

                for i, agent in enumerate(st.session_state.cb_active_path):
                    st.session_state.cb_agent_status[agent] = "running" if i == 0 else "pending"
            else:
                result_content = state_update.get(result_key, "")
                st.session_state.cb_results[node_name] = result_content

                if node_name in st.session_state.cb_active_path:
                    idx = st.session_state.cb_active_path.index(node_name)
                    if idx + 1 < len(st.session_state.cb_active_path):
                        next_agent = st.session_state.cb_active_path[idx + 1]
                        st.session_state.cb_agent_status[next_agent] = "running"

            with path_container.container():
                if st.session_state.cb_router_reason:
                    st.info(f"🧭 **条件分支路由决策:** {st.session_state.cb_router_reason}")

                for agent_key in st.session_state.cb_active_path:
                    status = st.session_state.cb_agent_status.get(agent_key, "pending")
                    label = f"{AGENT_ICONS[agent_key]} {AGENT_NAMES_LOCAL[agent_key]}"
                    with st.expander(label, expanded=(status == "running")):
                        if status == "running":
                            st.markdown(f"_🔄 {AGENT_NAMES_LOCAL[agent_key]}中…_")
                        elif status == "done":
                            m_name = st.session_state.cb_model_used.get(agent_key, "")
                            if m_name:
                                st.markdown(f'<span class="model-badge">🧠 {m_name}</span>', unsafe_allow_html=True)
                            st.markdown(st.session_state.cb_results.get(agent_key, ""))
                        else:
                            st.markdown("_⏳ 等待执行…_")

        st.session_state.cb_is_running = False
        st.markdown("---")
        st.success("🎉 分支执行完成！")

    elif run_btn and not requirement.strip():
        st.warning("⚠️ 请先输入内容再执行。")

    elif not st.session_state.cb_is_running and st.session_state.cb_results:
        with path_container.container():
            st.info(f"🧭 **条件分支路由决策:** {st.session_state.cb_router_reason}")
            for agent_key in st.session_state.cb_active_path:
                label = f"{AGENT_ICONS[agent_key]} {AGENT_NAMES_LOCAL[agent_key]}"
                with st.expander(label, expanded=False):
                    content = st.session_state.cb_results.get(agent_key, "")
                    model_name = st.session_state.cb_model_used.get(agent_key, "")
                    if content:
                        if model_name:
                            st.markdown(f'<span class="model-badge">🧠 {model_name}</span>', unsafe_allow_html=True)
                        st.markdown(content)
                    else:
                        st.markdown("_暂无结果_")
    else:
        with path_container.container():
            st.markdown(
                """
                <div style="text-align:center;padding:60px 20px;color:#AAAAAA;">
                    <div style="font-size:40px;margin-bottom:16px;">🔀</div>
                    <div style="font-size:16px;font-weight:500;color:#888888;margin-bottom:8px;">条件分支模式已就绪</div>
                    <div style="font-size:13px;line-height:1.8;">
                        输入你的问题，Supervisor 将自动识别类型并激活对应 Agent<br>
                        <span style="color:#6366f1">新功能</span> |
                        <span style="color:#7c3aed">代码审查</span> |
                        <span style="color:#0ea5e9">技术方案</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ── Loop Feedback 模式 ─────────────────────────────────
def _render_loop_feedback():
    from loop_feedback import stream_loop

    col_input, col_btn = st.columns([5, 1])
    with col_input:
        requirement = st.text_area(
            label="请描述你需要编写的代码",
            placeholder="例如：写一个用 requests 抓取网页并解析标题的函数",
            height=120,
            label_visibility="collapsed",
            key="lf_requirement",
        )
    with col_btn:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        run_btn = st.button("🚀 开始执行", use_container_width=True, type="primary", key="lf_run")

    st.divider()

    for key, default in [("lf_history", []), ("lf_is_running", False)]:
        if key not in st.session_state:
            st.session_state[key] = default

    path_container = st.empty()

    if run_btn and requirement.strip():
        st.session_state.lf_history = []
        st.session_state.lf_is_running = True

        for node_name, state_update in stream_loop(requirement.strip()):
            if node_name == "lf_coder":
                iteration = state_update.get("iteration", 1)
                code_result = state_update.get("code_result", "")
                model_name = state_update.get("model_used_by", {}).get("lf_coder", "unknown")
                st.session_state.lf_history.append({
                    "iteration": iteration,
                    "coder_result": code_result,
                    "coder_model": model_name,
                    "reviewer_result": None,
                    "reviewer_model": None,
                    "status": None,
                    "feedback": None,
                })
            elif node_name == "lf_reviewer":
                status = state_update.get("status", "fail")
                feedback = state_update.get("feedback", "")
                model_name = state_update.get("model_used_by", {}).get("lf_reviewer", "unknown")
                if st.session_state.lf_history:
                    st.session_state.lf_history[-1]["reviewer_result"] = feedback
                    st.session_state.lf_history[-1]["reviewer_model"] = model_name
                    st.session_state.lf_history[-1]["status"] = status
                    st.session_state.lf_history[-1]["feedback"] = feedback

            with path_container.container():
                for i, history in enumerate(st.session_state.lf_history):
                    iter_num = history["iteration"]
                    st.markdown(f"### 第 {iter_num} 轮迭代")

                    with st.expander("💻 编码生成", expanded=(i == len(st.session_state.lf_history) - 1 and history["reviewer_result"] is None)):
                        st.markdown(f'<span class="model-badge">🧠 {history["coder_model"]}</span>', unsafe_allow_html=True)
                        st.markdown(history["coder_result"])

                    if history["reviewer_result"] is not None:
                        exp_label = "🔍 代码审查 ✅ 通过" if history["status"] == "pass" else "🔍 代码审查 ❌ 不通过"
                        with st.expander(exp_label, expanded=(i == len(st.session_state.lf_history) - 1)):
                            st.markdown(f'<span class="model-badge">🧠 {history["reviewer_model"]}</span>', unsafe_allow_html=True)
                            if history["status"] == "pass":
                                st.success("质检通过！")
                            else:
                                st.error(f"质检不通过，打回重做。\n\n**反馈意见：**\n{history['feedback']}")
                    else:
                        with st.expander("🔍 代码审查", expanded=True):
                            st.markdown("_🔄 审查中…_")

                    st.markdown("<hr style='margin: 1em 0; border: none; border-top: 1px dashed #DCDCDC;'/>", unsafe_allow_html=True)

                if len(st.session_state.lf_history) >= 3 and st.session_state.lf_history[-1].get("status") == "fail":
                    st.error("⚠️ 达到最大迭代次数 (3次)，循环终止。")

        st.session_state.lf_is_running = False
        st.success("🎉 循环反馈执行完成！")

    elif run_btn and not requirement.strip():
        st.warning("⚠️ 请先输入需求再执行。")

    elif not st.session_state.lf_is_running and st.session_state.lf_history:
        with path_container.container():
            for i, history in enumerate(st.session_state.lf_history):
                iter_num = history["iteration"]
                st.markdown(f"### 第 {iter_num} 轮迭代")

                with st.expander("💻 编码生成", expanded=False):
                    st.markdown(f'<span class="model-badge">🧠 {history["coder_model"]}</span>', unsafe_allow_html=True)
                    st.markdown(history["coder_result"])

                if history["reviewer_result"] is not None:
                    exp_label = "🔍 代码审查 ✅ 通过" if history["status"] == "pass" else "🔍 代码审查 ❌ 不通过"
                    with st.expander(exp_label, expanded=(history["status"] == "pass" or i == len(st.session_state.lf_history) - 1)):
                        st.markdown(f'<span class="model-badge">🧠 {history["reviewer_model"]}</span>', unsafe_allow_html=True)
                        if history["status"] == "pass":
                            st.success("质检通过！")
                        else:
                            st.error(f"质检不通过，打回重做。\n\n**反馈意见：**\n{history['feedback']}")

                st.markdown("<hr style='margin: 1em 0; border: none; border-top: 1px dashed #DCDCDC;'/>", unsafe_allow_html=True)

            if len(st.session_state.lf_history) >= 3 and st.session_state.lf_history[-1].get("status") == "fail":
                st.error("⚠️ 达到最大迭代次数 (3次)，循环终止。")

    else:
        with path_container.container():
            st.markdown(
                """
                <div style="text-align:center;padding:60px 20px;color:#AAAAAA;">
                    <div style="font-size:40px;margin-bottom:16px;">🔄</div>
                    <div style="font-size:16px;font-weight:500;color:#888888;margin-bottom:8px;">循环反馈模式已就绪</div>
                    <div style="font-size:13px;line-height:1.8;">
                        输入代码需求，Agent 将自动进行"编码-审查-修改"循环<br>
                        最多迭代 3 次，直到代码满足标准（异常处理、类型注解、注释）
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ── Parallel Review 模式 ────────────────────────────────
def _render_parallel_review():
    """Parallel Review 模式渲染函数 - 并行代码审查"""
    from parallel import stream_parallel

    st.markdown("#### 🔱 并行执行")
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        code_input = st.text_area("输入代码", height=120, placeholder="例如：def process_data(data): import os; os.system('rm -rf /')...", label_visibility="collapsed", key="pr_code")
    with col_btn:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        run_btn = st.button("🚀 开始审查", use_container_width=True, type="primary", key="pr_run")

    st.divider()

    PR_MODEL_KEYS = {"security_agent": "security", "performance_agent": "performance", "maintainability_agent": "maintainability", "merge_agent": "merger"}
    PR_RESULT_KEYS = {"security_agent": "security_result", "performance_agent": "performance_result", "maintainability_agent": "maintainability_result", "merge_agent": "merged_report"}
    PR_AGENTS = ["security_agent", "performance_agent", "maintainability_agent", "merge_agent"]

    if "pr_agent_status" not in st.session_state:
        st.session_state.pr_agent_status = {k: "pending" for k in PR_AGENTS}
    if "pr_results" not in st.session_state:
        st.session_state.pr_results = {}
    if "pr_model_used" not in st.session_state:
        st.session_state.pr_model_used = {}
    if "pr_is_running" not in st.session_state:
        st.session_state.pr_is_running = False

    path_container = st.empty()

    def _render_pr_state():
        with path_container.container():
            status_cols = st.columns(4)
            for i, agent_key in enumerate(PR_AGENTS):
                with status_cols[i]:
                    icon = AGENT_ICONS[agent_key]
                    name = AGENT_NAMES[agent_key]
                    badge = _status_badge(st.session_state.pr_agent_status[agent_key])
                    st.markdown(f"<div style='text-align:center'><div style='font-size:24px'>{icon}</div><div style='font-size:12px;font-weight:500'>{name}</div><div style='font-size:11px;margin-top:4px'>{badge}</div></div>", unsafe_allow_html=True)

            for agent_key in ["security_agent", "performance_agent", "maintainability_agent"]:
                result = st.session_state.pr_results.get(agent_key, "")
                with st.expander(f"{AGENT_ICONS[agent_key]} {AGENT_NAMES[agent_key]}", expanded=False):
                    model_name = st.session_state.pr_model_used.get(PR_MODEL_KEYS[agent_key], "")
                    if model_name:
                        st.markdown(f'<span class="model-badge">🧠 {model_name}</span>', unsafe_allow_html=True)
                    if result:
                        st.markdown(result)

            merge_result = st.session_state.pr_results.get("merge_agent", "")
            with st.expander(f"📋 {AGENT_NAMES['merge_agent']}", expanded=bool(merge_result)):
                model_name = st.session_state.pr_model_used.get("merger", "")
                if model_name:
                    st.markdown(f'<span class="model-badge">🧠 {model_name}</span>', unsafe_allow_html=True)
                if merge_result:
                    st.markdown(merge_result)

    if run_btn and code_input.strip():
        st.session_state.pr_agent_status = {k: "pending" for k in PR_AGENTS}
        st.session_state.pr_results = {}
        st.session_state.pr_model_used = {}
        st.session_state.pr_is_running = True

        for node_name, state_update in stream_parallel(code_input.strip(), "python"):
            st.session_state.pr_model_used.update(state_update.get("model_used_by", {}))
            if node_name in st.session_state.pr_agent_status:
                st.session_state.pr_agent_status[node_name] = "done"
                result_key = PR_RESULT_KEYS.get(node_name, "")
                result = state_update.get(result_key, "")
                if result:
                    st.session_state.pr_results[node_name] = result
            _render_pr_state()

        st.session_state.pr_is_running = False
        st.success("🎉 并行审查完成！")

    elif run_btn and not code_input.strip():
        st.warning("⚠️ 请先输入代码再开始审查。")

    elif not st.session_state.pr_is_running and st.session_state.pr_results:
        _render_pr_state()

    else:
        st.markdown(
            """<div style="padding:20px 0;color:#6B7280;font-size:14px;line-height:1.8;">
            🔒 安全审查 + ⚡ 性能分析 + 🔧 可维护性分析<br>
            并行执行后由 📊 汇总报告
            </div>""",
            unsafe_allow_html=True,
        )


# ── Debate 模式 ────────────────────────────────────────
def _render_debate():
    """Debate 模式渲染函数 - 多 Agent 对抗辩论"""
    from debate import stream_debate

    st.markdown("#### ⚔️ 辩论模式")
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        code_input = st.text_area("输入代码", height=120, placeholder="例如：def login(user, pwd): return True...", label_visibility="collapsed", key="db_code")
    with col_btn:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        run_btn = st.button("🚀 开始辩论", use_container_width=True, type="primary", key="db_run")

    rounds = st.slider("辩论轮次", min_value=1, max_value=3, value=2, key="db_rounds")

    st.divider()

    if "db_history" not in st.session_state:
        st.session_state.db_history = []
    if "db_conclusion" not in st.session_state:
        st.session_state.db_conclusion = None
    if "db_model_used" not in st.session_state:
        st.session_state.db_model_used = {}
    if "db_is_running" not in st.session_state:
        st.session_state.db_is_running = False

    path_container = st.empty()

    if run_btn and code_input.strip():
        st.session_state.db_history = []
        st.session_state.db_conclusion = None
        st.session_state.db_model_used = {}
        st.session_state.db_is_running = True

        for node_name, state_update in stream_debate(code_input.strip(), "python", max_rounds=rounds):
            model_map = state_update.get("model_used_by", {})
            st.session_state.db_model_used.update(model_map)

            if node_name in ["pro_agent", "con_agent"]:
                history_items = state_update.get("debate_history", [])
                st.session_state.db_history.extend(history_items)

            if node_name == "judge_agent":
                st.session_state.db_conclusion = state_update.get("final_conclusion", "")

            with path_container.container():
                for i, item in enumerate(st.session_state.db_history):
                    role = item["role"]
                    round_num = item["round"]
                    content = item["content"]
                    icon = "🟢" if role == "pro" else "🔴"
                    name = f"{'支持方' if role == 'pro' else '反对方'} (第{round_num}轮)"

                    is_last = (i == len(st.session_state.db_history) - 1) and not st.session_state.db_conclusion

                    with st.expander(f"{icon} {name}", expanded=is_last):
                        model_key = "pro" if role == "pro" else "con"
                        model_name = st.session_state.db_model_used.get(model_key, "")
                        if model_name:
                            st.markdown(f'<span class="model-badge">🧠 {model_name}</span>', unsafe_allow_html=True)
                        st.markdown(content)

                if st.session_state.db_conclusion:
                    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
                    with st.expander("⚖️ 裁判最终裁决", expanded=True):
                        model_name = st.session_state.db_model_used.get("judge", "")
                        if model_name:
                            st.markdown(f'<span class="model-badge">🧠 {model_name}</span>', unsafe_allow_html=True)
                        st.success(st.session_state.db_conclusion)
                elif st.session_state.db_is_running:
                    st.info("🤔 Agent 正在激烈辩论中...")

        st.session_state.db_is_running = False
        st.success("🎉 辩论结束！")

    elif run_btn and not code_input.strip():
        st.warning("⚠️ 请先输入代码再开始辩论。")

    elif not st.session_state.db_is_running and st.session_state.db_history:
        with path_container.container():
            for i, item in enumerate(st.session_state.db_history):
                role = item["role"]
                round_num = item["round"]
                content = item["content"]
                icon = "🟢" if role == "pro" else "🔴"
                name = f"{'支持方' if role == 'pro' else '反对方'} (第{round_num}轮)"

                with st.expander(f"{icon} {name}", expanded=False):
                    model_key = "pro" if role == "pro" else "con"
                    model_name = st.session_state.db_model_used.get(model_key, "")
                    if model_name:
                        st.markdown(f'<span class="model-badge">🧠 {model_name}</span>', unsafe_allow_html=True)
                    st.markdown(content)

            if st.session_state.db_conclusion:
                st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
                with st.expander("⚖️ 裁判最终裁决", expanded=True):
                    model_name = st.session_state.db_model_used.get("judge", "")
                    if model_name:
                        st.markdown(f'<span class="model-badge">🧠 {model_name}</span>', unsafe_allow_html=True)
                    st.success(st.session_state.db_conclusion)
    else:
        st.markdown(
            """<div style="padding:20px 0;color:#6B7280;font-size:14px;line-height:1.8;">
            🟢 支持方 vs 🔴 反对方<br>
            多轮辩论后由 ⚖️ 裁判给出最终建议
            </div>""",
            unsafe_allow_html=True,
        )


# ── Nested Agent 模式 ──────────────────────────────────
def _render_nested_agent():
    """Nested Agent 模式渲染函数"""
    from nested_agent import stream_nested

    st.markdown("#### 🪆 嵌套 Agent")
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        req_input = st.text_area("需求描述", height=120, placeholder="例如：开发一个电商网站，支持用户注册、商品浏览、购物车...", label_visibility="collapsed", key="na_req")
    with col_btn:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        run_btn = st.button("🚀 开始执行", use_container_width=True, type="primary", key="na_run")

    st.divider()

    AGENT_LABELS = {
        "coder": "💻 程序员",
        "tester": "🧪 测试员",
        "security_reviewer": "🔒 安全审查",
        "documenter": "📝 文档员",
    }

    if "na_result" not in st.session_state:
        st.session_state.na_result = None
    if "na_model_used" not in st.session_state:
        st.session_state.na_model_used = {}
    if "na_is_running" not in st.session_state:
        st.session_state.na_is_running = False

    results_container = st.empty()

    if run_btn and req_input.strip():
        st.session_state.na_result = None
        st.session_state.na_model_used = {}
        st.session_state.na_is_running = True

        for node_name, state_update in stream_nested(req_input.strip()):
            st.session_state.na_model_used.update(state_update.get("model_used_by", {}))

            with results_container.container():
                if node_name == "orchestrator":
                    st.info("🎼 Orchestrator 正在规划任务...")

                elif node_name in ["coder", "tester", "security_reviewer", "documenter"]:
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.markdown(f"### {AGENT_LABELS.get(node_name, node_name)}")
                        model_name = st.session_state.na_model_used.get(node_name, "")
                        if model_name:
                            st.markdown(f'<span class="model-badge">🧠 {model_name}</span>', unsafe_allow_html=True)
                    with col2:
                        result = state_update.get(f"{node_name}_result", "")
                        if result:
                            with st.expander(f"🧠 {AGENT_LABELS.get(node_name, node_name)} 输出", expanded=True):
                                st.markdown(result)

                elif node_name == "merge":
                    st.session_state.na_result = state_update.get("final_deliverable", "")
                    if st.session_state.na_result:
                        with st.expander("📦 最终项目交付成果", expanded=True):
                            st.success(st.session_state.na_result)

        st.session_state.na_is_running = False
        st.success("🎉 嵌套 Agent 执行完成！")

    elif run_btn and not req_input.strip():
        st.warning("⚠️ 请先输入需求描述再开始执行。")

    elif not st.session_state.na_is_running and st.session_state.na_result:
        with results_container.container():
            st.markdown("### 📦 最终项目交付成果")
            st.success(st.session_state.na_result)

    else:
        st.markdown(
            """<div style="padding:20px 0;color:#6B7280;font-size:14px;line-height:1.8;">
            🎼 Orchestrator 召唤子 Agent 并行执行：<br>
            💻 程序员 + 🧪 测试员 + 🔒 安全审查 + 📝 文档员<br>
            最后 📦 汇总交付成果
            </div>""",
            unsafe_allow_html=True,
        )


# ── Hybrid A 模式 ───────────────────────────────────────
def _render_hybrid_a():
    """Hybrid A 模式渲染函数 - 混合模式 A：并行生成 + 循环质检 + 条件分支"""
    from hybrid_a import stream_hybrid_a

    st.markdown("#### 🎛️ 混合模式 A")
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        req_input = st.text_area("需求描述", height=120, placeholder="例如：写一个用户认证模块，支持 JWT...", label_visibility="collapsed", key="ha_req")
    with col_btn:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        run_btn = st.button("🚀 开始执行", use_container_width=True, type="primary", key="ha_run")

    st.divider()

    if "ha_history" not in st.session_state:
        st.session_state.ha_history = []
    if "ha_final" not in st.session_state:
        st.session_state.ha_final = None
    if "ha_model_used" not in st.session_state:
        st.session_state.ha_model_used = {}
    if "ha_security_model" not in st.session_state:
        st.session_state.ha_security_model = ""
    if "ha_is_running" not in st.session_state:
        st.session_state.ha_is_running = False

    path_container = st.empty()

    def _phase1_badge(node: str) -> str:
        if st.session_state.ha_model_used.get(node):
            return f'<span class="model-badge">🧠 {st.session_state.ha_model_used[node]}</span>'
        return ""

    def _render_current_state():
        with path_container.container():
            for i, entry in enumerate(st.session_state.ha_history):
                phase = entry.get("phase", "")
                if phase == "phase1_parallel":
                    iter_num = entry.get("iteration", 1)
                    status = entry.get("status", "unknown")
                    code = entry.get("code", "")
                    is_last = (i == len(st.session_state.ha_history) - 1)

                    with st.expander(f"💻 代码生成（第{iter_num}轮）", expanded=is_last):
                        model = st.session_state.ha_model_used.get("lf_coder", "")
                        if model:
                            st.markdown(f'<span class="model-badge">🧠 {model}</span>', unsafe_allow_html=True)
                        st.code(code, language="python")
                        if status == "pass":
                            st.success("✅ 代码审查通过！")
                        else:
                            st.error("❌ 代码审查未通过，正在修复...")

                elif phase == "phase2_security":
                    with st.expander("🔒 安全审查报告", expanded=True):
                        smodel = st.session_state.ha_security_model
                        if smodel:
                            st.markdown(f'<span class="model-badge">🧠 {smodel}</span>', unsafe_allow_html=True)
                        st.markdown(entry.get("security_report", ""))

                elif phase == "phase3_final":
                    with st.expander("📋 项目交付报告", expanded=True):
                        st.success(entry.get("final_report", ""))

            if st.session_state.ha_is_running:
                st.info("🔄 正在执行中...")

    if run_btn and req_input.strip():
        st.session_state.ha_history = []
        st.session_state.ha_final = None
        st.session_state.ha_model_used = {}
        st.session_state.ha_security_model = ""
        st.session_state.ha_is_running = True

        for node_name, state_update in stream_hybrid_a(req_input.strip()):
            st.session_state.ha_model_used.update(state_update.get("model_used_by", {}))

            if node_name == "lf_coder":
                st.session_state.ha_history.append({
                    "phase": "phase1_parallel",
                    "iteration": len([e for e in st.session_state.ha_history if e.get("phase") == "phase1_parallel"]) + 1,
                    "code": state_update.get("code", ""),
                    "status": state_update.get("status", "unknown"),
                })

            if node_name == "security_reviewer":
                st.session_state.ha_security_model = st.session_state.ha_model_used.get("security_reviewer", "")
                st.session_state.ha_history.append({
                    "phase": "phase2_security",
                    "security_report": state_update.get("security_report", ""),
                })

            if node_name == "final_merge":
                st.session_state.ha_final = state_update.get("final_report", "")
                st.session_state.ha_history.append({
                    "phase": "phase3_final",
                    "final_report": st.session_state.ha_final,
                })

            _render_current_state()

        st.session_state.ha_is_running = False
        st.success("🎉 混合模式 A 执行完成！")

    elif run_btn and not req_input.strip():
        st.warning("⚠️ 请先输入需求描述再开始执行。")

    elif not st.session_state.ha_is_running and st.session_state.ha_history:
        _render_current_state()

    else:
        st.markdown(
            """<div style="padding:20px 0;color:#6B7280;font-size:14px;line-height:1.8;">
            Phase 1: 💻📝🧪 并行生成代码/测试/文档<br>
            Phase 2: 🔍 循环质检（直到通过）<br>
            Phase 3: 🔀 条件分支（安全/性能/可维护性）<br>
            Phase 4: 📋 项目交付报告
            </div>""",
            unsafe_allow_html=True,
        )


# ── Hybrid B 模式 ───────────────────────────────────────
def _render_hybrid_b():
    """Hybrid B 模式渲染函数 - 辩论 + 嵌套 Agent"""
    from hybrid_b import stream_hybrid_b

    # ── 输入区 ───────────────────────────────────────────
    st.markdown("#### 🎭 混合模式 B")
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        scheme_input = st.text_area(
            label="请输入架构方案",
            placeholder="例如：用 Redis 做主数据库，存储用户会话和购物车数据...",
            height=120,
            label_visibility="collapsed",
            key="hb_scheme_input",
        )
    with col_btn:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        run_btn = st.button("🚀 开始辩论", use_container_width=True, type="primary", key="hb_run")

    rounds = st.slider("辩论轮次", min_value=1, max_value=3, value=2, key="hb_rounds")

    st.divider()

    # ── session state 初始化 ───────────────────────────────
    for key, default in [
        ("hb_history", []),
        ("hb_conclusion", None),
        ("hb_model_used", {}),
        ("hb_is_running", False),
        ("hb_sub_agent_status", None),  # 子Agent状态
    ]:
        if key not in st.session_state:
            st.session_state[key] = default

    path_container = st.empty()

    # ── 执行逻辑 ──────────────────────────────────────────
    if run_btn and scheme_input.strip():
        st.session_state.hb_history = []
        st.session_state.hb_conclusion = None
        st.session_state.hb_model_used = {}
        st.session_state.hb_is_running = True
        st.session_state.hb_sub_agent_status = None

        for node_name, state_update in stream_hybrid_b(scheme_input.strip(), max_rounds=rounds):
            # 更新模型信息
            model_map = state_update.get("model_used_by", {})
            st.session_state.hb_model_used.update(model_map)

            # 跟踪子Agent状态
            if node_name == "pro_orchestrator":
                current_round = state_update.get("current_round", 1)
                st.session_state.hb_sub_agent_status = {
                    "side": "pro",
                    "round": current_round,
                    "performance": "⏳ 召唤中...",
                    "cost": "⏳ 召唤中...",
                    "done": False
                }
            elif node_name == "performance_agent":
                if st.session_state.hb_sub_agent_status:
                    st.session_state.hb_sub_agent_status["performance"] = "✅ 完成"
            elif node_name == "cost_agent":
                if st.session_state.hb_sub_agent_status:
                    st.session_state.hb_sub_agent_status["cost"] = "✅ 完成"
            elif node_name == "pro_summarizer":
                if st.session_state.hb_sub_agent_status:
                    st.session_state.hb_sub_agent_status["done"] = True
            elif node_name == "con_orchestrator":
                current_round = state_update.get("current_round", 1)
                st.session_state.hb_sub_agent_status = {
                    "side": "con",
                    "round": current_round,
                    "security": "⏳ 召唤中...",
                    "maintainability": "⏳ 召唤中...",
                    "done": False
                }
            elif node_name == "security_agent":
                if st.session_state.hb_sub_agent_status:
                    st.session_state.hb_sub_agent_status["security"] = "✅ 完成"
            elif node_name == "maintainability_agent":
                if st.session_state.hb_sub_agent_status:
                    st.session_state.hb_sub_agent_status["maintainability"] = "✅ 完成"
            elif node_name == "con_summarizer":
                if st.session_state.hb_sub_agent_status:
                    st.session_state.hb_sub_agent_status["done"] = True

            # 处理辩论历史
            if node_name in ["pro_summarizer", "con_summarizer"]:
                history_items = state_update.get("debate_history", [])
                st.session_state.hb_history.extend(history_items)

            # 处理最终结论
            if node_name == "judge_agent":
                st.session_state.hb_conclusion = state_update.get("final_conclusion", "")

            # 动态渲染
            with path_container.container():
                # 显示子Agent召唤状态
                status = st.session_state.hb_sub_agent_status
                if status and not status.get("done"):
                    side_icon = "🟢" if status["side"] == "pro" else "🔴"
                    side_name = "支持方" if status["side"] == "pro" else "反对方"
                    st.info(f"{side_icon} {side_name}第{status['round']}轮分析中...")

                    if status["side"] == "pro":
                        col1, col2 = st.columns(2)
                        with col1:
                            st.caption(f"⚡ 召唤性能Agent... {status.get('performance', '⏳')}")
                        with col2:
                            st.caption(f"💰 召唤成本Agent... {status.get('cost', '⏳')}")
                    else:
                        col1, col2 = st.columns(2)
                        with col1:
                            st.caption(f"🔒 召唤安全Agent... {status.get('security', '⏳')}")
                        with col2:
                            st.caption(f"🔧 召唤可维护性Agent... {status.get('maintainability', '⏳')}")

                # 显示辩论历史
                for i, item in enumerate(st.session_state.hb_history):
                    role = item["role"]
                    round_num = item["round"]
                    content = item["content"]
                    icon = "🟢" if role == "pro" else "🔴"
                    name = f"{'支持方' if role == 'pro' else '反对方'} (第{round_num}轮)"

                    is_last = (i == len(st.session_state.hb_history) - 1) and not st.session_state.hb_conclusion

                    with st.expander(f"{icon} {name}", expanded=is_last):
                        # 显示模型信息
                        model_key = "pro_summarizer" if role == "pro" else "con_summarizer"
                        model_name = st.session_state.hb_model_used.get(model_key, "")
                        if model_name:
                            st.markdown(f'<span class="model-badge">🧠 {model_name}</span>', unsafe_allow_html=True)

                        # 显示子Agent数据
                        if role == "pro":
                            if item.get("performance_result"):
                                st.markdown("**⚡ 性能分析数据**")
                                st.caption(item["performance_result"][:500] + "...")
                            if item.get("cost_result"):
                                st.markdown("**💰 成本分析数据**")
                                st.caption(item["cost_result"][:500] + "...")
                        else:
                            if item.get("security_result"):
                                st.markdown("**🔒 安全分析数据**")
                                st.caption(item["security_result"][:500] + "...")
                            if item.get("maintainability_result"):
                                st.markdown("**🔧 可维护性分析数据**")
                                st.caption(item["maintainability_result"][:500] + "...")

                        # 显示论点
                        st.markdown("**论点：**")
                        st.markdown(content)

                # 显示裁判裁决
                if st.session_state.hb_conclusion:
                    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
                    with st.expander("⚖️ 裁判最终裁决", expanded=True):
                        model_name = st.session_state.hb_model_used.get("judge", "")
                        if model_name:
                            st.markdown(f'<span class="model-badge">🧠 {model_name}</span>', unsafe_allow_html=True)
                        st.success(st.session_state.hb_conclusion)
                elif st.session_state.hb_is_running:
                    st.info("🤔 Agent 正在激烈辩论中...")

        st.session_state.hb_is_running = False
        st.success("🎉 辩论结束！")

    elif run_btn and not scheme_input.strip():
        st.warning("⚠️ 请先输入架构方案再开始辩论。")

    elif not st.session_state.hb_is_running and st.session_state.hb_history:
        with path_container.container():
            for i, item in enumerate(st.session_state.hb_history):
                role = item["role"]
                round_num = item["round"]
                content = item["content"]
                icon = "🟢" if role == "pro" else "🔴"
                name = f"{'支持方' if role == 'pro' else '反对方'} (第{round_num}轮)"

                with st.expander(f"{icon} {name}", expanded=False):
                    # 显示模型信息
                    model_key = "pro_summarizer" if role == "pro" else "con_summarizer"
                    model_name = st.session_state.hb_model_used.get(model_key, "")
                    if model_name:
                        st.markdown(f'<span class="model-badge">🧠 {model_name}</span>', unsafe_allow_html=True)

                    # 显示子Agent数据（折叠）
                    if role == "pro":
                        if item.get("performance_result"):
                            with st.expander("⚡ 性能分析数据", expanded=False):
                                st.caption(item["performance_result"])
                        if item.get("cost_result"):
                            with st.expander("💰 成本分析数据", expanded=False):
                                st.caption(item["cost_result"])
                    else:
                        if item.get("security_result"):
                            with st.expander("🔒 安全分析数据", expanded=False):
                                st.caption(item["security_result"])
                        if item.get("maintainability_result"):
                            with st.expander("🔧 可维护性分析数据", expanded=False):
                                st.caption(item["maintainability_result"])

                    st.markdown("**论点：**")
                    st.markdown(content)

            if st.session_state.hb_conclusion:
                st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
                with st.expander("⚖️ 裁判最终裁决", expanded=True):
                    model_name = st.session_state.hb_model_used.get("judge", "")
                    if model_name:
                        st.markdown(f'<span class="model-badge">🧠 {model_name}</span>', unsafe_allow_html=True)
                    st.success(st.session_state.hb_conclusion)
    else:
        st.markdown(
            """<div style="padding:20px 0;color:#6B7280;font-size:14px;line-height:1.8;">
            输入架构方案，支持方/反对方召唤子 Agent 收集数据后辩论<br>
            <span style="color:#10b981">🟢 支持方</span> → 召唤 ⚡性能 + 💰成本 Agent<br>
            <span style="color:#ef4444">🔴 反对方</span> → 召唤 🔒安全 + 🔧可维护性 Agent<br>
            ⚖️ 裁判综合所有数据给出最终建议
            </div>""",
            unsafe_allow_html=True,
        )


# ── 路由入口（函数定义后执行）───────────────────────────
mode_key = current_mode["key"]
if mode_key == "supervisor_pipeline":
    _render_supervisor_pipeline()
elif mode_key == "conditional_branch":
    _render_conditional_branch()
elif mode_key == "loop_feedback":
    _render_loop_feedback()
elif mode_key == "parallel":
    _render_parallel_review()
elif mode_key == "debate":
    _render_debate()
elif mode_key == "nested_agent":
    _render_nested_agent()
elif mode_key == "hybrid_a":
    _render_hybrid_a()
elif mode_key == "hybrid_b":
    _render_hybrid_b()
else:
    _render_coming_soon(selected_mode_label, current_mode["desc"])
