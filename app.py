"""
Multi-Agent Demo — 统一 Streamlit 入口
侧边栏切换编排模式，目前仅 supervisor_pipeline 可用。
"""
import streamlit as st
from config import AGENT_NAMES, AGENT_ORDER

# ── 页面配置 ──────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Agent Demo",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 编排模式注册表 ─────────────────────────────────────────
MODES = {
    "🔁 Supervisor Pipeline": {
        "key": "supervisor_pipeline",
        "desc": "Supervisor 统一调度，四个子 Agent 顺序流转",
        "available": True,
    },
    "🔀 Conditional Branch": {
        "key": "conditional_branch",
        "desc": "根据条件动态路由到不同 Agent 分支",
        "available": True,
    },
    "🔄 Loop Feedback": {
        "key": "loop_feedback",
        "desc": "Agent 输出反馈回自身，迭代优化直至收敛",
        "available": True,
    },
    "⚡ Parallel": {
        "key": "parallel",
        "desc": "多个 Agent 并行执行，结果汇总合并",
        "available": True,
    },
    "🗣️ Debate": {
        "key": "debate",
        "desc": "多个 Agent 相互辩论，通过对抗得出最优解",
        "available": True,
    },
    "🪆 Nested Agent": {
        "key": "nested_agent",
        "desc": "Agent 内部动态召唤子 Agent，形成嵌套调用",
        "available": True,
    },
}

# ── 自定义样式（亮色主题）────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* ── 全局背景 ───────────────────── */
.stApp {
    background-color: #F5F5F5;
}

/* ── 侧边栏 ─────────────────────── */
section[data-testid="stSidebar"] {
    background-color: #EFEFEF;
    border-right: 1px solid #DCDCDC;
}
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown li {
    color: #555555;
}

/* ── 模式卡片（敬请期待） ─────────── */
.mode-card {
    padding: 10px 14px;
    border-radius: 10px;
    margin-bottom: 6px;
    border: 1px solid #DCDCDC;
    background: #F8F8F8;
    cursor: default;
    transition: all 0.2s ease;
}
.mode-card:hover { background: #F0F0F0; }
.mode-card.active {
    background: rgba(99,102,241,0.08);
    border-color: rgba(99,102,241,0.4);
}
.mode-card-title { color: #444444; font-weight: 600; font-size: 13px; }
.mode-card-desc  { color: #888888; font-size: 11px; margin-top: 2px; }
.mode-badge-soon {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 10px;
    font-size: 10px;
    font-weight: 600;
    background: #E0E0E0;
    color: #888888;
    margin-left: 6px;
    vertical-align: middle;
}

/* ── 输入区 ─────────────────────── */
.stTextArea textarea {
    background: #FFFFFF !important;
    border: 1px solid #CCCCCC !important;
    border-radius: 12px !important;
    color: #333333 !important;
    font-size: 14px !important;
    padding: 16px !important;
    transition: border-color 0.3s ease;
}
.stTextArea textarea:focus {
    border-color: rgba(99,102,241,0.6) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.12) !important;
}

/* ── 按钮（紫色系保留）────────────── */
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 32px !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(99,102,241,0.25) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(99,102,241,0.35) !important;
}

/* ── Expander ───────────────────── */
.streamlit-expanderHeader {
    background: #FFFFFF !important;
    border: 1px solid #DCDCDC !important;
    border-radius: 12px !important;
    color: #333333 !important;
    font-weight: 500 !important;
    padding: 14px 18px !important;
    transition: all 0.3s ease;
}
.streamlit-expanderHeader:hover {
    background: #F0F0F0 !important;
    border-color: rgba(99,102,241,0.4) !important;
}
.streamlit-expanderContent {
    background: #FAFAFA !important;
    border: 1px solid #DCDCDC !important;
    border-top: none !important;
    border-radius: 0 0 12px 12px !important;
    padding: 20px !important;
}

/* ── Status 徽章 ─────────────────── */
.agent-status {
    display: inline-flex; align-items: center; gap: 8px;
    padding: 6px 14px; border-radius: 20px;
    font-size: 13px; font-weight: 500;
}
.status-pending { background: #EBEBEB; color: #888888; }
.status-running { background: rgba(99,102,241,0.10); color: #6366f1; animation: pulse 1.5s infinite; }
.status-done    { background: rgba(34,197,94,0.12);  color: #16a34a; }
@keyframes pulse { 0%,100% { opacity:1; } 50% { opacity:0.55; } }

/* ── 模型名称徽章 ───────────────── */
.model-badge {
    display: inline-flex; align-items: center; gap: 5px;
    padding: 4px 12px; border-radius: 16px;
    font-size: 12px; font-weight: 500;
    background: linear-gradient(135deg, rgba(99,102,241,0.07), rgba(139,92,246,0.07));
    color: #6366f1;
    border: 1px solid rgba(99,102,241,0.25);
    margin-bottom: 12px;
    letter-spacing: 0.3px;
}

/* ── 标题（紫色渐变保留）────────── */
.main-title {
    background: linear-gradient(135deg, #7c3aed, #6366f1, #0ea5e9);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    font-size: 2rem; font-weight: 700; margin-bottom: 0;
}
.sub-title { color: #777777; font-size: 0.95rem; margin-top: 4px; margin-bottom: 28px; }

/* ── 敬请期待占位 ────────────────── */
.coming-soon-box {
    text-align: center;
    padding: 80px 20px;
    color: #AAAAAA;
    border: 1px dashed #CCCCCC;
    border-radius: 16px;
    margin-top: 24px;
    background: #FAFAFA;
}

/* ── Markdown 文字 ───────────────── */
.stMarkdown { color: #333333; }
.stMarkdown h1,.stMarkdown h2,.stMarkdown h3 { color: #222222; }
.stMarkdown code {
    background: #F0F0F0;
    color: #5b21b6;
    padding: 2px 6px;
    border-radius: 4px;
}
.stMarkdown pre {
    background: #F0F0F0 !important;
    border: 1px solid #DCDCDC;
    border-radius: 10px;
    padding: 16px !important;
    color: #333333;
}
footer { visibility: hidden; }
</style>
""",
    unsafe_allow_html=True,
)

# ── 侧边栏：模式选择 ──────────────────────────────────────
with st.sidebar:
    st.markdown("## 🤖 Multi-Agent Demo")
    st.markdown(
        '<p style="color:#888888;font-size:13px;">LangGraph 编排 · Groq 推理</p>',
        unsafe_allow_html=True,
    )
    st.divider()

    st.markdown(
        '<p style="color:#666666;font-size:12px;font-weight:600;letter-spacing:1px;margin-bottom:10px;">编排模式</p>',
        unsafe_allow_html=True,
    )

    available_labels = [k for k, v in MODES.items() if v["available"]]
    unavailable_labels = [k for k, v in MODES.items() if not v["available"]]

    selected_mode_label = st.radio(
        label="选择编排模式",
        options=available_labels,
        label_visibility="collapsed",
    )

    for label in unavailable_labels:
        info = MODES[label]
        st.markdown(
            f'<div class="mode-card">'
            f'<div class="mode-card-title">{label}'
            f'<span class="mode-badge-soon">敬请期待</span></div>'
            f'<div class="mode-card-desc">{info["desc"]}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.divider()

    current_mode = MODES[selected_mode_label]
    st.markdown(
        f'<div style="color:#666666;font-size:12px;line-height:1.8;">'
        f'<b style="color:#444444;">当前模式</b><br>'
        f'{current_mode["desc"]}'
        f'</div>',
        unsafe_allow_html=True,
    )

# ── 主区域顶部 ────────────────────────────────────────────
st.markdown('<p class="main-title">Multi-Agent Demo</p>', unsafe_allow_html=True)
st.markdown(
    f'<p class="sub-title">{selected_mode_label} · {current_mode["desc"]}</p>',
    unsafe_allow_html=True,
)


# ════════════════════════════════════════════════════════════
# ── 模式渲染函数（定义在路由调用之前）
# ════════════════════════════════════════════════════════════

def _render_coming_soon(label: str, desc: str):
    st.markdown(
        f"""
        <div class="coming-soon-box">
            <div style="font-size:48px;margin-bottom:16px;">🚧</div>
            <div style="font-size:18px;font-weight:500;color:#888888;margin-bottom:8px;">{label}</div>
            <div style="font-size:14px;color:#AAAAAA;">{desc}<br><br>敬请期待…</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_supervisor_pipeline():
    from supervisor_pipeline import stream_supervisor

    AGENT_ICONS = {
        "analyst": "📋", "architect": "🏗️", "coder": "💻", "reviewer": "🔍",
    }
    AGENT_STATUS_LABELS = {
        "analyst": "需求分析", "architect": "架构设计", "coder": "编码生成", "reviewer": "代码审查",
    }
    RESULT_KEYS = {
        "analyst": "analysis_result", "architect": "architecture_result",
        "coder": "code_result", "reviewer": "review_result",
    }

    def _status_badge(agent_key: str, status: str) -> str:
        icon = AGENT_ICONS[agent_key]
        label = AGENT_STATUS_LABELS[agent_key]
        if status == "running":
            return f'<span class="agent-status status-running">{icon} {label}中…</span>'
        elif status == "done":
            return f'<span class="agent-status status-done">{icon} {label} ✓</span>'
        return f'<span class="agent-status status-pending">{icon} {label} 待执行</span>'

    # ── 输入区 ────────────────────────────────────────────
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        requirement = st.text_area(
            label="请描述你的软件需求",
            placeholder="例如：开发一个在线教育平台，支持视频课程、作业提交和实时答疑…",
            height=120,
            label_visibility="collapsed",
            key="sp_requirement",
        )
    with col_btn:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        run_btn = st.button("🚀 开始执行", use_container_width=True, type="primary", key="sp_run")

    st.divider()

    # ── session state 初始化 ─────────────────────────────
    for key, default in [
        ("sp_results", {}),
        ("sp_agent_status", {k: "pending" for k in AGENT_ORDER}),
        ("sp_model_used", {}),
        ("sp_is_running", False),
    ]:
        if key not in st.session_state:
            st.session_state[key] = default

    # ── 状态概览条 ───────────────────────────────────────
    status_cols = st.columns(4)
    for i, agent_key in enumerate(AGENT_ORDER):
        with status_cols[i]:
            st.markdown(
                _status_badge(agent_key, st.session_state.sp_agent_status[agent_key]),
                unsafe_allow_html=True,
            )
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # ── 执行逻辑 ─────────────────────────────────────────
    if run_btn and requirement.strip():
        st.session_state.sp_results = {}
        st.session_state.sp_agent_status = {k: "pending" for k in AGENT_ORDER}
        st.session_state.sp_model_used = {}
        st.session_state.sp_is_running = True

        expanders, placeholders = {}, {}
        for agent_key in AGENT_ORDER:
            label = f"{AGENT_ICONS[agent_key]} {AGENT_NAMES[agent_key]}"
            exp = st.expander(label, expanded=(agent_key == "analyst"))
            with exp:
                placeholders[agent_key] = st.empty()
                placeholders[agent_key].markdown("_⏳ 等待执行…_")
            expanders[agent_key] = exp

        for node_name, state_update in stream_supervisor(requirement.strip()):
            st.session_state.sp_agent_status[node_name] = "done"
            result_key = RESULT_KEYS.get(node_name, "")
            result_content = state_update.get(result_key, "")

            model_map = state_update.get("model_used_by", {})
            model_name = model_map.get(node_name, "unknown")
            st.session_state.sp_model_used[node_name] = model_name
            st.session_state.sp_results[node_name] = result_content

            with expanders[node_name]:
                badge = f'<span class="model-badge">🧠 {model_name}</span>'
                placeholders[node_name].markdown(
                    badge + "\n\n" + result_content, unsafe_allow_html=True
                )

            idx = AGENT_ORDER.index(node_name)
            if idx + 1 < len(AGENT_ORDER):
                next_agent = AGENT_ORDER[idx + 1]
                st.session_state.sp_agent_status[next_agent] = "running"
                with expanders[next_agent]:
                    placeholders[next_agent].markdown(
                        f"_🔄 {AGENT_STATUS_LABELS[next_agent]}中…_"
                    )

        st.session_state.sp_is_running = False
        st.markdown("---")
        st.success("🎉 所有 Agent 执行完成！")

    elif run_btn and not requirement.strip():
        st.warning("⚠️ 请先输入需求再执行。")

    elif not st.session_state.sp_is_running and st.session_state.sp_results:
        for agent_key in AGENT_ORDER:
            label = f"{AGENT_ICONS[agent_key]} {AGENT_NAMES[agent_key]}"
            with st.expander(label, expanded=False):
                content = st.session_state.sp_results.get(agent_key, "")
                model_name = st.session_state.sp_model_used.get(agent_key, "")
                if content:
                    if model_name:
                        st.markdown(
                            f'<span class="model-badge">🧠 {model_name}</span>',
                            unsafe_allow_html=True,
                        )
                    st.markdown(content)
                else:
                    st.markdown("_暂无结果_")

    else:
        st.markdown(
            """
            <div style="text-align:center;padding:60px 20px;color:#AAAAAA;">
                <div style="font-size:40px;margin-bottom:16px;">🤖</div>
                <div style="font-size:16px;font-weight:500;color:#888888;margin-bottom:8px;">准备就绪</div>
                <div style="font-size:13px;line-height:1.8;">
                    在上方输入软件需求，点击「开始执行」<br>
                    <span style="color:#6366f1">需求分析</span> →
                    <span style="color:#7c3aed">架构设计</span> →
                    <span style="color:#8b5cf6">编码生成</span> →
                    <span style="color:#0ea5e9">代码审查</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_conditional_branch():
    from conditional_branch import stream_conditional

    AGENT_ICONS = {
        "router": "🧭", "cb_analyst": "📋", "cb_architect": "🏗️", "cb_coder": "💻",
        "cb_reviewer": "🔍", "cb_optimizer": "✨",
        "cb_researcher": "🕵️", "cb_advisor": "💡"
    }
    AGENT_NAMES = {
        "router": "路由分配", "cb_analyst": "需求分析", "cb_architect": "架构设计", "cb_coder": "编码生成",
        "cb_reviewer": "代码审查", "cb_optimizer": "代码优化",
        "cb_researcher": "技术调研", "cb_advisor": "技术顾问"
    }
    RESULT_KEYS = {
        "router": "router_decision", "cb_analyst": "analysis_result", "cb_architect": "architecture_result", "cb_coder": "code_result",
        "cb_reviewer": "review_result", "cb_optimizer": "optimization_result",
        "cb_researcher": "research_result", "cb_advisor": "advice_result"
    }

    # ── 输入区 ────────────────────────────────────────────
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        requirement = st.text_area(
            label="请描述你的需求、代码或技术问题",
            placeholder="例如：\\n[新功能] 我想加一个微信支付模块...\\n[代码审查] 帮我看看这段 React 代码有没有坑...\\n[技术问题] Next.js 和 Nuxt.js 选哪个好？",
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
                    st.info(f"🧭 **Supervisor 路由决策:** {st.session_state.cb_router_reason}")
                
                for agent_key in st.session_state.cb_active_path:
                    status = st.session_state.cb_agent_status.get(agent_key, "pending")
                    label = f"{AGENT_ICONS[agent_key]} {AGENT_NAMES[agent_key]}"
                    exp = st.expander(label, expanded=(status=="running"))
                    with exp:
                        if status == "running":
                            st.markdown(f"_🔄 {AGENT_NAMES[agent_key]}中…_")
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
            st.info(f"🧭 **Supervisor 路由决策:** {st.session_state.cb_router_reason}")
            for agent_key in st.session_state.cb_active_path:
                label = f"{AGENT_ICONS[agent_key]} {AGENT_NAMES[agent_key]}"
                with st.expander(label, expanded=False):
                    content = st.session_state.cb_results.get(agent_key, "")
                    model_name = st.session_state.cb_model_used.get(agent_key, "")
                    if content:
                        if model_name:
                            st.markdown(
                                f'<span class="model-badge">🧠 {model_name}</span>',
                                unsafe_allow_html=True,
                            )
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


def _render_loop_feedback():
    from loop_feedback import stream_loop

    AGENT_ICONS = {"lf_coder": "💻", "lf_reviewer": "🔍"}
    AGENT_NAMES = {"lf_coder": "编码生成", "lf_reviewer": "代码审查"}

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

    for key, default in [
        ("lf_history", []),
        ("lf_is_running", False)
    ]:
        if key not in st.session_state:
            st.session_state[key] = default

    path_container = st.empty()

    if run_btn and requirement.strip():
        st.session_state.lf_history = []
        st.session_state.lf_is_running = True
        
        current_iteration = 0
        current_status = "running" # running, done

        for node_name, state_update in stream_loop(requirement.strip()):
            
            # 记录历史
            # 由于是循环，每次 node 运行完都作为一个事件记录
            if node_name == "lf_coder":
                iteration = state_update.get("iteration", 1)
                code_result = state_update.get("code_result", "")
                model_map = state_update.get("model_used_by", {})
                model_name = model_map.get("lf_coder", "unknown")
                
                # 新的迭代轮次开始
                st.session_state.lf_history.append({
                    "iteration": iteration,
                    "coder_result": code_result,
                    "coder_model": model_name,
                    "reviewer_result": None,
                    "reviewer_model": None,
                    "status": None, # pass, fail
                    "feedback": None
                })
                current_iteration = iteration
                
            elif node_name == "lf_reviewer":
                # 更新当前轮次的评审结果
                status = state_update.get("status", "fail")
                feedback = state_update.get("feedback", "")
                model_map = state_update.get("model_used_by", {})
                model_name = model_map.get("lf_reviewer", "unknown")
                
                if st.session_state.lf_history:
                    st.session_state.lf_history[-1]["reviewer_result"] = feedback
                    st.session_state.lf_history[-1]["reviewer_model"] = model_name
                    st.session_state.lf_history[-1]["status"] = status
                    st.session_state.lf_history[-1]["feedback"] = feedback

            # 动态渲染
            with path_container.container():
                for i, history in enumerate(st.session_state.lf_history):
                    iter_num = history["iteration"]
                    
                    st.markdown(f"### 第 {iter_num} 轮迭代")
                    
                    # 渲染 Coder 结果
                    with st.expander(f"💻 编码生成", expanded=(i == len(st.session_state.lf_history)-1 and history["reviewer_result"] is None)):
                        st.markdown(f'<span class="model-badge">🧠 {history["coder_model"]}</span>', unsafe_allow_html=True)
                        st.markdown(history["coder_result"])
                    
                    # 渲染 Reviewer 结果 (如果有的话)
                    if history["reviewer_result"] is not None:
                        # 确定 expander 是否展开
                        # 如果是 fail 并且是最后一轮，可以展开看 feedback
                        # 如果是 pass，也可以展开看最终确认
                        exp_label = "🔍 代码审查 ✅ 通过" if history["status"] == "pass" else "🔍 代码审查 ❌ 不通过"
                        with st.expander(exp_label, expanded=(i == len(st.session_state.lf_history)-1)):
                            st.markdown(f'<span class="model-badge">🧠 {history["reviewer_model"]}</span>', unsafe_allow_html=True)
                            if history["status"] == "pass":
                                st.success("质检通过！")
                            else:
                                st.error(f"质检不通过，打回重做。\\n\\n**反馈意见：**\\n{history['feedback']}")
                    else:
                        with st.expander("🔍 代码审查", expanded=True):
                            st.markdown("_🔄 审查中…_")
                    
                    st.markdown("<hr style='margin: 1em 0; border: none; border-top: 1px dashed #DCDCDC;'/>", unsafe_allow_html=True)
                
                # 如果超过3轮仍然fail
                if len(st.session_state.lf_history) >= 3 and st.session_state.lf_history[-1].get("status") == "fail":
                    st.error("⚠️ 达到最大迭代次数 (3次)，循环终止。")

        st.session_state.lf_is_running = False
        st.success("🎉 循环反馈执行完成！")

    elif run_btn and not requirement.strip():
        st.warning("⚠️ 请先输入需求再执行。")
        
    elif not st.session_state.lf_is_running and st.session_state.lf_history:
        # 显示历史记录
        with path_container.container():
            for i, history in enumerate(st.session_state.lf_history):
                iter_num = history["iteration"]
                
                st.markdown(f"### 第 {iter_num} 轮迭代")
                
                with st.expander(f"💻 编码生成", expanded=False):
                    st.markdown(f'<span class="model-badge">🧠 {history["coder_model"]}</span>', unsafe_allow_html=True)
                    st.markdown(history["coder_result"])
                
                if history["reviewer_result"] is not None:
                    exp_label = "🔍 代码审查 ✅ 通过" if history["status"] == "pass" else "🔍 代码审查 ❌ 不通过"
                    with st.expander(exp_label, expanded=(history["status"] == "pass" or i == len(st.session_state.lf_history)-1)):
                        st.markdown(f'<span class="model-badge">🧠 {history["reviewer_model"]}</span>', unsafe_allow_html=True)
                        if history["status"] == "pass":
                            st.success("质检通过！")
                        else:
                            st.error(f"质检不通过，打回重做。\\n\\n**反馈意见：**\\n{history['feedback']}")
                
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


def _render_parallel_review():
    """Parallel Review 模式渲染函数 - 并行代码审查"""
    from parallel import stream_parallel

    AGENT_ICONS = {
        "dispatcher": "📡",
        "security_agent": "🔒",
        "performance_agent": "⚡",
        "maintainability_agent": "🔧",
        "merge_agent": "📋"
    }
    AGENT_NAMES = {
        "dispatcher": "分发器",
        "security_agent": "安全审查",
        "performance_agent": "性能审查",
        "maintainability_agent": "可维护性审查",
        "merge_agent": "合并报告"
    }

    # ── 输入区 ────────────────────────────────────────────
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        code_input = st.text_area(
            label="请输入需要审查的代码",
            placeholder="例如：粘贴你的 Python/JavaScript 代码...",
            height=120,
            label_visibility="collapsed",
            key="pr_code_input",
        )
    with col_btn:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        run_btn = st.button("🚀 开始执行", use_container_width=True, type="primary", key="pr_run")

    # 语言选择
    language = st.selectbox(
        "代码语言",
        options=["python", "javascript", "java", "cpp", "go", "rust", "其他"],
        index=0,
        key="pr_language"
    )

    st.divider()

    # ── session state 初始化 ─────────────────────────────
    for key, default in [
        ("pr_results", {}),
        ("pr_agent_status", {}),
        ("pr_model_used", {}),
        ("pr_is_running", False),
        ("pr_issues", {}),
    ]:
        if key not in st.session_state:
            st.session_state[key] = default

    # ── 执行逻辑 ─────────────────────────────────────────
    if run_btn and code_input.strip():
        st.session_state.pr_results = {}
        st.session_state.pr_agent_status = {
            "security_agent": "pending",
            "performance_agent": "pending",
            "maintainability_agent": "pending",
            "merge_agent": "pending",
        }
        st.session_state.pr_model_used = {}
        st.session_state.pr_issues = {}
        st.session_state.pr_is_running = True

        # 创建状态显示区域
        status_cols = st.columns(4)
        status_placeholders = {}
        for i, agent_key in enumerate(["security_agent", "performance_agent", "maintainability_agent", "merge_agent"]):
            with status_cols[i]:
                status_placeholders[agent_key] = st.empty()
                status_placeholders[agent_key].markdown(
                    f'<span class="agent-status status-pending">{AGENT_ICONS[agent_key]} {AGENT_NAMES[agent_key]} 待执行</span>',
                    unsafe_allow_html=True
                )

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        # 创建结果 expander
        expanders = {}
        for agent_key in ["security_agent", "performance_agent", "maintainability_agent"]:
            label = f"{AGENT_ICONS[agent_key]} {AGENT_NAMES[agent_key]}"
            expanders[agent_key] = st.expander(label, expanded=True)

        # merge expander
        expanders["merge_agent"] = st.expander(f"📋 {AGENT_NAMES['merge_agent']}", expanded=False)

        # 流式执行
        for node_name, state_update in stream_parallel(code_input.strip(), language):
            # 更新状态
            if node_name in st.session_state.pr_agent_status:
                st.session_state.pr_agent_status[node_name] = "done"
                status_placeholders[node_name].markdown(
                    f'<span class="agent-status status-done">{AGENT_ICONS[node_name]} {AGENT_NAMES[node_name]} ✓</span>',
                    unsafe_allow_html=True
                )

            # 获取模型信息
            model_map = state_update.get("model_used_by", {})
            if node_name in model_map:
                st.session_state.pr_model_used[node_name] = model_map[node_name]

            # 处理各节点结果
            if node_name == "security_agent":
                result = state_update.get("security_result", "")
                issues = state_update.get("security_issues", [])
                st.session_state.pr_results["security"] = result
                st.session_state.pr_issues["security"] = issues
                with expanders["security_agent"]:
                    badge = f'<span class="model-badge">🧠 {model_map.get("security", "unknown")}</span>'
                    st.markdown(badge, unsafe_allow_html=True)
                    st.markdown(f"**完成（{len(issues)}个问题）**")
                    st.markdown(result)

            elif node_name == "performance_agent":
                result = state_update.get("performance_result", "")
                issues = state_update.get("performance_issues", [])
                st.session_state.pr_results["performance"] = result
                st.session_state.pr_issues["performance"] = issues
                with expanders["performance_agent"]:
                    badge = f'<span class="model-badge">🧠 {model_map.get("performance", "unknown")}</span>'
                    st.markdown(badge, unsafe_allow_html=True)
                    st.markdown(f"**完成（{len(issues)}个问题）**")
                    st.markdown(result)

            elif node_name == "maintainability_agent":
                result = state_update.get("maintainability_result", "")
                issues = state_update.get("maintainability_issues", [])
                st.session_state.pr_results["maintainability"] = result
                st.session_state.pr_issues["maintainability"] = issues
                with expanders["maintainability_agent"]:
                    badge = f'<span class="model-badge">🧠 {model_map.get("maintainability", "unknown")}</span>'
                    st.markdown(badge, unsafe_allow_html=True)
                    st.markdown(f"**完成（{len(issues)}个问题）**")
                    st.markdown(result)

            elif node_name == "merge_agent":
                result = state_update.get("merged_report", "")
                st.session_state.pr_results["merged"] = result
                with expanders["merge_agent"]:
                    badge = f'<span class="model-badge">🧠 {model_map.get("merger", "unknown")}</span>'
                    st.markdown(badge, unsafe_allow_html=True)
                    st.markdown(result)

        st.session_state.pr_is_running = False
        st.markdown("---")
        st.success("🎉 并行审查完成！")

    elif run_btn and not code_input.strip():
        st.warning("⚠️ 请先输入代码再执行。")

    elif not st.session_state.pr_is_running and st.session_state.pr_results:
        # 显示历史结果
        status_cols = st.columns(4)
        for i, agent_key in enumerate(["security_agent", "performance_agent", "maintainability_agent", "merge_agent"]):
            with status_cols[i]:
                if agent_key in st.session_state.pr_agent_status:
                    st.markdown(
                        f'<span class="agent-status status-done">{AGENT_ICONS[agent_key]} {AGENT_NAMES[agent_key]} ✓</span>',
                        unsafe_allow_html=True
                    )

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        for agent_key in ["security_agent", "performance_agent", "maintainability_agent"]:
            label = f"{AGENT_ICONS[agent_key]} {AGENT_NAMES[agent_key]}"
            with st.expander(label, expanded=False):
                content = st.session_state.pr_results.get(agent_key.replace("_agent", ""), "")
                model_name = st.session_state.pr_model_used.get(agent_key, "")
                issues = st.session_state.pr_issues.get(agent_key.replace("_agent", ""), [])
                if content:
                    if model_name:
                        st.markdown(f'<span class="model-badge">🧠 {model_name}</span>', unsafe_allow_html=True)
                    st.markdown(f"**完成（{len(issues)}个问题）**")
                    st.markdown(content)

        with st.expander(f"📋 {AGENT_NAMES['merge_agent']}", expanded=True):
            content = st.session_state.pr_results.get("merged", "")
            model_name = st.session_state.pr_model_used.get("merge_agent", "")
            if content:
                if model_name:
                    st.markdown(f'<span class="model-badge">🧠 {model_name}</span>', unsafe_allow_html=True)
                st.markdown(content)

    else:
        st.markdown(
            """
            <div style="text-align:center;padding:60px 20px;color:#AAAAAA;">
                <div style="font-size:40px;margin-bottom:16px;">⚡</div>
                <div style="font-size:16px;font-weight:500;color:#888888;margin-bottom:8px;">并行审查模式已就绪</div>
                <div style="font-size:13px;line-height:1.8;">
                    输入代码，3个 Agent 并行审查<br>
                    <span style="color:#ef4444">安全审查</span> |
                    <span style="color:#f59e0b">性能审查</span> |
                    <span style="color:#10b981">可维护性审查</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_debate():
    """Debate 模式渲染函数 - 多 Agent 对抗辩论"""
    from debate import stream_debate

    AGENT_ICONS = {"pro": "🟢", "con": "🔴", "judge": "⚖️"}
    AGENT_NAMES = {"pro": "支持方", "con": "反对方", "judge": "裁判 Agent"}

    # ── 输入区 ────────────────────────────────────────────
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        code_input = st.text_area(
            label="请输入需要辩论的代码",
            placeholder="例如：这段单例模式的实现是否优雅？",
            height=120,
            label_visibility="collapsed",
            key="db_code_input",
        )
    with col_btn:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        run_btn = st.button("🚀 开始辩论", use_container_width=True, type="primary", key="db_run")

    rounds = st.slider("辩论轮次", min_value=1, max_value=3, value=2, key="db_rounds")

    # 语言选择
    language = st.selectbox(
        "代码语言",
        options=["python", "javascript", "java", "cpp", "go", "rust", "其他"],
        index=0,
        key="db_language"
    )

    st.divider()

    # ── session state 初始化 ─────────────────────────────
    for key, default in [
        ("db_history", []),
        ("db_conclusion", None),
        ("db_model_used", {}),
        ("db_is_running", False),
    ]:
        if key not in st.session_state:
            st.session_state[key] = default

    path_container = st.empty()

    # ── 执行逻辑 ─────────────────────────────────────────
    if run_btn and code_input.strip():
        st.session_state.db_history = []
        st.session_state.db_conclusion = None
        st.session_state.db_model_used = {}
        st.session_state.db_is_running = True

        for node_name, state_update in stream_debate(code_input.strip(), language=language, max_rounds=rounds):
            
            # 更新模型信息
            model_map = state_update.get("model_used_by", {})
            st.session_state.db_model_used.update(model_map)

            # 处理历史记录
            if node_name in ["pro_agent", "con_agent"]:
                history_items = state_update.get("debate_history", [])
                st.session_state.db_history.extend(history_items)
            
            # 处理最终结论
            if node_name == "judge_agent":
                st.session_state.db_conclusion = state_update.get("final_conclusion", "")

            # 动态渲染
            with path_container.container():
                for i, item in enumerate(st.session_state.db_history):
                    role = item["role"]
                    round_num = item["round"]
                    content = item["content"]
                    icon = AGENT_ICONS[role]
                    name = f"{AGENT_NAMES[role]} (第{round_num}轮)"
                    
                    is_last = (i == len(st.session_state.db_history) - 1) and not st.session_state.db_conclusion
                    with st.expander(f"{icon} {name}", expanded=is_last):
                        model_name = st.session_state.db_model_used.get(role, "")
                        if model_name:
                            st.markdown(f'<span class="model-badge">🧠 {model_name}</span>', unsafe_allow_html=True)
                        st.markdown(content)
                
                if st.session_state.db_conclusion:
                    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
                    with st.expander(f"⚖️ 最终裁决", expanded=True):
                        model_name = st.session_state.db_model_used.get("judge", "")
                        if model_name:
                            st.markdown(f'<span class="model-badge">🧠 {model_name}</span>', unsafe_allow_html=True)
                        st.success(st.session_state.db_conclusion)
                elif st.session_state.db_is_running:
                    st.info("🤔 Agent 正在激烈博弈中...")

        st.session_state.db_is_running = False
        st.success("🎉 辩论结束！")

    elif run_btn and not code_input.strip():
        st.warning("⚠️ 请先输入代码再开始辩论。")

    elif not st.session_state.db_is_running and st.session_state.db_history:
        with path_container.container():
            for i, item in enumerate(st.session_state.db_history):
                role, round_num, content = item["role"], item["round"], item["content"]
                with st.expander(f"{AGENT_ICONS[role]} {AGENT_NAMES[role]} (第{round_num}轮)", expanded=False):
                    model_name = st.session_state.db_model_used.get(role, "")
                    if model_name: st.markdown(f'<span class="model-badge">🧠 {model_name}</span>', unsafe_allow_html=True)
                    st.markdown(content)
            
            if st.session_state.db_conclusion:
                st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
                with st.expander(f"⚖️ 最终裁决", expanded=True):
                    model_name = st.session_state.db_model_used.get("judge", "")
                    if model_name: st.markdown(f'<span class="model-badge">🧠 {model_name}</span>', unsafe_allow_html=True)
                    st.success(st.session_state.db_conclusion)
    else:
        st.markdown('<div style="text-align:center;padding:60px 20px;color:#AAAAAA;">🗣️ 辩论模式已就绪</div>', unsafe_allow_html=True)


def _render_nested_agent():
    """Nested Agent 模式渲染函数 - 动态任务编排"""
    from nested_agent import stream_nested

    AGENT_ICONS = {"orchestrator": "🧠", "coder": "⚙️", "tester": "🧪", "documenter": "📜", "finalizer": "📦"}
    AGENT_LABELS = {"orchestrator": "Orchestrator (规划)", "coder": "代码生成 Agent", "tester": "测试生成 Agent", "documenter": "文档生成 Agent", "finalizer": "Orchestrator (整合交付)"}

    col_input, col_btn = st.columns([5, 1])
    with col_input:
        requirement = st.text_area(label="需求描述", placeholder="例如：写一个 Python 单例模式，包含单元测试...", height=100, label_visibility="collapsed", key="ns_requirement")
    with col_btn:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        run_btn = st.button("🚀 开始执行", use_container_width=True, type="primary", key="ns_run")

    st.divider()

    for key, default in [("ns_plan", None), ("ns_reason", ""), ("ns_outputs", {}), ("ns_model_used", {}), ("ns_is_running", False)]:
        if key not in st.session_state: st.session_state[key] = default

    results_container = st.empty()

    if run_btn and requirement.strip():
        st.session_state.ns_plan = None; st.session_state.ns_reason = ""; st.session_state.ns_outputs = {}; st.session_state.ns_model_used = {}; st.session_state.ns_is_running = True
        for node_name, state_update in stream_nested(requirement.strip()):
            model_map = state_update.get("model_used_by", {})
            st.session_state.ns_model_used.update(model_map)
            if node_name == "orchestrator_agent":
                st.session_state.ns_plan = state_update.get("plan"); st.session_state.ns_reason = state_update.get("plan_reason")
            elif node_name == "coder_agent": st.session_state.ns_outputs["coder"] = state_update.get("coder_output")
            elif node_name == "tester_agent": st.session_state.ns_outputs["tester"] = state_update.get("tester_output")
            elif node_name == "documenter_agent": st.session_state.ns_outputs["documenter"] = state_update.get("documenter_output")
            elif node_name == "finalizer_agent": st.session_state.ns_outputs["finalizer"] = state_update.get("final_output")

            with results_container.container():
                if st.session_state.ns_plan:
                    with st.expander(f"🧠 Orchestrator 规划理由", expanded=True):
                        st.info(st.session_state.ns_reason)
                        cols = st.columns(3)
                        for idx, (agent, needed) in enumerate(st.session_state.ns_plan.items()):
                            cols[idx].markdown(f"**{'✅' if needed else '➖'} {agent.capitalize()}**")
                for k in ["coder", "tester", "documenter"]:
                    if st.session_state.ns_outputs.get(k):
                        with st.expander(f"{AGENT_ICONS[k]} {AGENT_LABELS[k]}", expanded=False):
                            model_name = st.session_state.ns_model_used.get(k, "")
                            if model_name: st.markdown(f'<span class="model-badge">🧠 {model_name}</span>', unsafe_allow_html=True)
                            st.code(st.session_state.ns_outputs[k])
                if st.session_state.ns_outputs.get("finalizer"):
                    with st.expander(f"📦 最终项目交付成果", expanded=True):
                        model_name = st.session_state.ns_model_used.get("orchestrator", "")
                        if model_name: st.markdown(f'<span class="model-badge">🧠 {model_name}</span>', unsafe_allow_html=True)
                        st.markdown(st.session_state.ns_outputs["finalizer"])
                    st.success("🎉 任务执行完毕！"); st.balloons()
        st.session_state.ns_is_running = False
    elif not st.session_state.ns_is_running and st.session_state.ns_plan:
        with results_container.container():
            for k in ["coder", "tester", "documenter"]:
                if st.session_state.ns_outputs.get(k):
                    with st.expander(f"{AGENT_ICONS[k]} {AGENT_LABELS[k]}", expanded=False): st.code(st.session_state.ns_outputs[k])
            if st.session_state.ns_outputs.get("finalizer"):
                with st.expander("📦 最终项目交付成果", expanded=True): st.markdown(st.session_state.ns_outputs["finalizer"])
    else:
        st.markdown('<div style="text-align:center;padding:60px 20px;color:#AAAAAA;">🪆 嵌套模式已就绪</div>', unsafe_allow_html=True)


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
else:
    _render_coming_soon(selected_mode_label, current_mode["desc"])
