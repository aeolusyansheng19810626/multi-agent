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
    .model-badge {
        display: inline-block;
        background: #1e293b;
        color: #60a5fa;
        font-size: 12px;
        padding: 2px 8px;
        border-radius: 10px;
        margin-bottom: 8px;
        font-family: 'Courier New', monospace;
    }
    /* 隐藏 Streamlit 默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ── 侧边栏：模式选择 ──────────────────────────────────
st.sidebar.title("🤖 Multi-Agent 平台")
st.sidebar.markdown("---")

MODES = [
    {"key": "supervisor_pipeline", "label": "Supervisor Pipeline", "icon": "🔄", "desc": "监督者流水线：顺序执行，每个 Agent 处理前一个的输出"},
    {"key": "conditional_branch", "label": "Conditional Branch", "icon": "🔀", "desc": "条件分支：根据代码特征动态选择审查路径"},
    {"key": "loop_feedback", "label": "Loop Feedback", "icon": "🔁", "desc": "循环反馈：代码生成 → 审查 → 修复，直到通过"},
    {"key": "parallel", "label": "Parallel Review", "icon": "⚡", "desc": "并行审查：安全、性能、可维护性同时分析后汇总"},
    {"key": "debate", "label": "Debate", "icon": "⚔️", "desc": "辩论对抗：支持方 vs 反对方，裁判给出最终建议"},
    {"key": "nested_agent", "icon": "🪆", "label": "Nested Agent", "desc": "嵌套 Agent：Orchestrator 召唤子 Agent 并行执行后汇总"},
    {"key": "hybrid_a", "icon": "🌀", "label": "Hybrid A", "desc": "混合模式 A：并行生成 + 循环质检 + 条件分支"},
    {"key": "hybrid_b", "icon": "🔀", "label": "Hybrid B", "desc": "辩论 + 嵌套 Agent：支持方/反对方召唤子Agent收集数据后辩论"},
]

mode_labels = [f"{m['icon']} {m['label']}" for m in MODES]
mode_keys = [m["key"] for m in MODES]

selected_label = st.sidebar.radio("选择协作模式", mode_labels)
current_mode = MODES[mode_labels.index(selected_label)]
selected_mode_label = selected_label

st.sidebar.markdown("---")
st.sidebar.caption(current_mode["desc"])

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
    """返回状态徽章 HTML"""
    badges = {
        "pending": '<span style="color:#888;">⏳ 等待中</span>',
        "running": '<span style="color:#3b82f6;">🔄 运行中</span>',
        "done": '<span style="color:#10b981;">✅ 完成</span>',
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

    AGENT_ORDER = ["requirement", "architect", "coder", "tester", "documenter"]
    AGENT_ICONS_LOCAL = {"requirement": "📋", "architect": "🏗️", "coder": "💻", "tester": "🧪", "documenter": "📝"}

    st.markdown("#### 🔄 Supervisor Pipeline")
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        req_input = st.text_area("需求描述", height=120, placeholder="例如：开发一个用户登录模块，支持 JWT 认证...", label_visibility="collapsed", key="sp_req")
    with col_btn:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        run_btn = st.button("🚀 开始执行", use_container_width=True, type="primary", key="sp_run")

    st.divider()

    if "sp_agent_status" not in st.session_state:
        st.session_state.sp_agent_status = {k: "pending" for k in AGENT_ORDER}
    if "sp_final" not in st.session_state:
        st.session_state.sp_final = None
    if "sp_is_running" not in st.session_state:
        st.session_state.sp_is_running = False

    path_container = st.empty()

    if run_btn and req_input.strip():
        st.session_state.sp_agent_status = {k: "pending" for k in AGENT_ORDER}
        st.session_state.sp_final = None
        st.session_state.sp_is_running = True

        for node_name, state_update in stream_supervisor(req_input.strip()):
            if node_name in st.session_state.sp_agent_status:
                st.session_state.sp_agent_status[node_name] = "done"
                next_idx = AGENT_ORDER.index(node_name) + 1
                if next_idx < len(AGENT_ORDER):
                    st.session_state.sp_agent_status[AGENT_ORDER[next_idx]] = "running"

            with path_container.container():
                status_cols = st.columns(5)
                for i, agent_key in enumerate(AGENT_ORDER):
                    with status_cols[i]:
                        icon = AGENT_ICONS_LOCAL[agent_key]
                        name = AGENT_NAMES[agent_key]
                        badge = _status_badge(st.session_state.sp_agent_status[agent_key])
                        st.markdown(f"<div style='text-align:center'><div style='font-size:24px'>{icon}</div><div style='font-size:12px;font-weight:500'>{name}</div><div style='font-size:11px;margin-top:4px'>{badge}</div></div>", unsafe_allow_html=True)

                expanders = {}
                for agent_key in AGENT_ORDER:
                    expanders[agent_key] = st.expander(f"{AGENT_ICONS_LOCAL[agent_key]} {AGENT_NAMES[agent_key]}", expanded=False)

                if node_name in expanders:
                    with expanders[node_name]:
                        result = state_update.get(f"{node_name}_result", "")
                        if result:
                            st.markdown(result)

                if node_name == "documenter":
                    st.session_state.sp_final = state_update.get("final_report", "")
                    if st.session_state.sp_final:
                        with st.expander("📦 最终项目交付成果", expanded=True):
                            st.success(st.session_state.sp_final)

        st.session_state.sp_is_running = False
        st.success("🎉 Supervisor Pipeline 执行完成！")

    elif run_btn and not req_input.strip():
        st.warning("⚠️ 请先输入需求描述再开始执行。")

    elif not st.session_state.sp_is_running and st.session_state.sp_final:
        with path_container.container():
            status_cols = st.columns(5)
            for i, agent_key in enumerate(AGENT_ORDER):
                with status_cols[i]:
                    icon = AGENT_ICONS_LOCAL[agent_key]
                    name = AGENT_NAMES[agent_key]
                    st.markdown(f"<div style='text-align:center'><div style='font-size:24px'>{icon}</div><div style='font-size:12px;font-weight:500'>{name}</div><div style='font-size:11px;margin-top:4px'>{_status_badge('done')}</div></div>", unsafe_allow_html=True)

            for agent_key in AGENT_ORDER:
                with st.expander(f"{AGENT_ICONS_LOCAL[agent_key]} {AGENT_NAMES[agent_key]}", expanded=False):
                    st.caption(f"Agent {agent_key} 的输出（静态展示）")

            with st.expander("📦 最终项目交付成果", expanded=True):
                st.success(st.session_state.sp_final)
    else:
        st.markdown(
            """
            <div style="text-align:center;padding:60px 20px;color:#AAAAAA;">
                <div style="font-size:40px;margin-bottom:16px;">🔄</div>
                <div style="font-size:16px;font-weight:500;color:#888888;margin-bottom:8px;">Supervisor Pipeline 已就绪</div>
                <div style="font-size:13px;line-height:1.8;">
                    监督者流水线模式：<br>
                    📋 需求分析 → 🏗️ 架构师 → 💻 程序员 → 🧪 测试员 → 📝 文档员
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ── Conditional Branch 模式 ─────────────────────────────
def _render_conditional_branch():
    """Conditional Branch 模式渲染函数"""
    from conditional_branch import stream_conditional

    NODE_LIST = ["input", "analyzer", "security_path", "performance_path", "maintainability_path", "merge"]
    NODE_ICONS = {"input": "📥", "analyzer": "🔍", "security_path": "🔒", "performance_path": "⚡", "maintainability_path": "🔧", "merge": "📊"}

    st.markdown("#### 🔀 Conditional Branch")
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        code_input = st.text_area("输入代码", height=120, placeholder="例如：def login(user, pwd): return True...", label_visibility="collapsed", key="cb_code")
    with col_btn:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        run_btn = st.button("🚀 开始分析", use_container_width=True, type="primary", key="cb_run")

    st.divider()

    if "cb_agent_status" not in st.session_state:
        st.session_state.cb_agent_status = {k: "pending" for k in NODE_LIST}
    if "cb_is_running" not in st.session_state:
        st.session_state.cb_is_running = False

    path_container = st.empty()

    if run_btn and code_input.strip():
        st.session_state.cb_agent_status = {k: "pending" for k in NODE_LIST}
        st.session_state.cb_is_running = True

        active_path = []

        for node_name, state_update in stream_conditional(code_input.strip(), "python"):
            if node_name in st.session_state.cb_agent_status:
                st.session_state.cb_agent_status[node_name] = "done"
                if node_name not in active_path:
                    active_path.append(node_name)

            with path_container.container():
                st.info(f"🔍 当前执行路径：{' → '.join([NODE_ICONS.get(n, n) for n in active_path])}")

                for node_name_key in NODE_LIST:
                    status = st.session_state.cb_agent_status[node_name_key]
                    icon = NODE_ICONS[node_name_key]
                    name = AGENT_NAMES.get(node_name_key, node_name_key)
                    if status == "done" or node_name_key in active_path:
                        with st.expander(f"{icon} {name}", expanded=(node_name_key == node_name)):
                            result = state_update.get(f"{node_name_key}_result", "") if node_name_key == node_name else ""
                            if result:
                                st.caption(result[:500])

        st.session_state.cb_is_running = False
        st.success("🎉 条件分支分析完成！")

    elif run_btn and not code_input.strip():
        st.warning("⚠️ 请先输入代码再开始分析。")

    else:
        st.markdown(
            """
            <div style="text-align:center;padding:60px 20px;color:#AAAAAA;">
                <div style="font-size:40px;margin-bottom:16px;">🔀</div>
                <div style="font-size:16px;font-weight:500;color:#888888;margin-bottom:8px;">Conditional Branch 已就绪</div>
                <div style="font-size:13px;line-height:1.8;">
                    根据代码特征动态选择审查路径：<br>
                    🔍 分析器 → （🔒 安全 / ⚡ 性能 / 🔧 可维护性）→ 📊 汇总
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ── Loop Feedback 模式 ─────────────────────────────────
def _render_loop_feedback():
    """Loop Feedback 模式渲染函数"""
    from loop_feedback import stream_loop

    st.markdown("#### 🔁 Loop Feedback")
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        req_input = st.text_area("需求描述", height=120, placeholder="例如：写一个 Python 函数，计算斐波那契数列...", label_visibility="collapsed", key="lf_req")
    with col_btn:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        run_btn = st.button("🚀 开始生成", use_container_width=True, type="primary", key="lf_run")

    st.divider()

    if "lf_history" not in st.session_state:
        st.session_state.lf_history = []
    if "lf_is_running" not in st.session_state:
        st.session_state.lf_is_running = False

    path_container = st.empty()

    if run_btn and req_input.strip():
        st.session_state.lf_history = []
        st.session_state.lf_is_running = True

        for node_name, state_update in stream_loop(req_input.strip()):
            if node_name == "lf_coder":
                code = state_update.get("code", "")
                status = state_update.get("status", "unknown")
                st.session_state.lf_history.append({
                    "iteration": len(st.session_state.lf_history) + 1,
                    "code": code,
                    "status": status,
                })

            with path_container.container():
                for i, entry in enumerate(st.session_state.lf_history):
                    iter_num = entry["iteration"]
                    status = entry["status"]
                    code = entry["code"]

                    is_last = (i == len(st.session_state.lf_history) - 1)

                    with st.expander(f"💻 代码生成（第{iter_num}轮）", expanded=is_last):
                        st.code(code, language="python")
                        if status == "pass":
                            st.success("✅ 代码审查通过！")
                        else:
                            st.error("❌ 代码审查未通过，正在修复...")

                if st.session_state.lf_is_running:
                    st.info("🔄 正在生成/修复代码中...")

        st.session_state.lf_is_running = False
        st.success("🎉 代码生成完成并通过审查！")

    elif run_btn and not req_input.strip():
        st.warning("⚠️ 请先输入需求描述再开始生成。")

    elif not st.session_state.lf_is_running and st.session_state.lf_history:
        with path_container.container():
            for i, entry in enumerate(st.session_state.lf_history):
                iter_num = entry["iteration"]
                status = entry["status"]
                code = entry["code"]

                with st.expander(f"💻 代码生成（第{iter_num}轮）", expanded=False):
                    st.code(code, language="python")
                    if status == "pass":
                        st.success("✅ 代码审查通过！")
                    else:
                        st.error("❌ 代码审查未通过")

    else:
        st.markdown(
            """
            <div style="text-align:center;padding:60px 20px;color:#AAAAAA;">
                <div style="font-size:40px;margin-bottom:16px;">🔁</div>
                <div style="font-size:16px;font-weight:500;color:#888888;margin-bottom:8px;">Loop Feedback 已就绪</div>
                <div style="font-size:13px;line-height:1.8;">
                    💻 代码生成 → 🔍 代码审查 → 🔧 修复<br>
                    循环直到审查通过
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ── Parallel Review 模式 ────────────────────────────────
def _render_parallel_review():
    """Parallel Review 模式渲染函数 - 并行代码审查"""
    from parallel import stream_parallel

    st.markdown("#### ⚡ Parallel Review")
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        code_input = st.text_area("输入代码", height=120, placeholder="例如：def process_data(data): import os; os.system('rm -rf /')...", label_visibility="collapsed", key="pr_code")
    with col_btn:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        run_btn = st.button("🚀 开始审查", use_container_width=True, type="primary", key="pr_run")

    st.divider()

    if "pr_agent_status" not in st.session_state:
        st.session_state.pr_agent_status = {
            "security_agent": "pending",
            "performance_agent": "pending",
            "maintainability_agent": "pending",
            "merge_agent": "pending",
        }
    if "pr_is_running" not in st.session_state:
        st.session_state.pr_is_running = False

    path_container = st.empty()

    if run_btn and code_input.strip():
        st.session_state.pr_agent_status = {k: "pending" for k in ["security_agent", "performance_agent", "maintainability_agent", "merge_agent"]}
        st.session_state.pr_is_running = True

        for node_name, state_update in stream_parallel(code_input.strip(), "python"):
            if node_name in st.session_state.pr_agent_status:
                st.session_state.pr_agent_status[node_name] = "done"

            with path_container.container():
                status_cols = st.columns(4)
                agents = ["security_agent", "performance_agent", "maintainability_agent", "merge_agent"]
                for i, agent_key in enumerate(agents):
                    with status_cols[i]:
                        icon = AGENT_ICONS[agent_key]
                        name = AGENT_NAMES[agent_key]
                        badge = _status_badge(st.session_state.pr_agent_status[agent_key])
                        st.markdown(f"<div style='text-align:center'><div style='font-size:24px'>{icon}</div><div style='font-size:12px;font-weight:500'>{name}</div><div style='font-size:11px;margin-top:4px'>{badge}</div></div>", unsafe_allow_html=True)

                expanders = {}
                for agent_key in ["security_agent", "performance_agent", "maintainability_agent"]:
                    expanders[agent_key] = st.expander(f"{AGENT_ICONS[agent_key]} {AGENT_NAMES[agent_key]}", expanded=False)

                if node_name in expanders:
                    with expanders[node_name]:
                        result = state_update.get(f"{node_name}_result", "")
                        if result:
                            st.markdown(result[:500] + "...")

                if node_name == "merge_agent":
                    with st.expander(f"📋 {AGENT_NAMES['merge_agent']}", expanded=True):
                        result = state_update.get("merged_report", "")
                        if result:
                            st.success(result)

        st.session_state.pr_is_running = False
        st.success("🎉 并行审查完成！")

    elif run_btn and not code_input.strip():
        st.warning("⚠️ 请先输入代码再开始审查。")

    elif not st.session_state.pr_is_running and st.session_state.pr_agent_status["merge_agent"] == "done":
        with path_container.container():
            status_cols = st.columns(4)
            for i, agent_key in enumerate(["security_agent", "performance_agent", "maintainability_agent", "merge_agent"]):
                with status_cols[i]:
                    icon = AGENT_ICONS[agent_key]
                    name = AGENT_NAMES[agent_key]
                    st.markdown(f"<div style='text-align:center'><div style='font-size:24px'>{icon}</div><div style='font-size:12px;font-weight:500'>{name}</div><div style='font-size:11px;margin-top:4px'>{_status_badge('done')}</div></div>", unsafe_allow_html=True)

            for agent_key in ["security_agent", "performance_agent", "maintainability_agent"]:
                with st.expander(f"{AGENT_ICONS[agent_key]} {AGENT_NAMES[agent_key]}", expanded=False):
                    st.caption("审查结果（静态展示）")

            with st.expander(f"📋 {AGENT_NAMES['merge_agent']}", expanded=True):
                st.success("审查报告已完成（静态展示）")

    else:
        st.markdown(
            """
            <div style="text-align:center;padding:60px 20px;color:#AAAAAA;">
                <div style="font-size:40px;margin-bottom:16px;">⚡</div>
                <div style="font-size:16px;font-weight:500;color:#888888;margin-bottom:8px;">Parallel Review 已就绪</div>
                <div style="font-size:13px;line-height:1.8;">
                    🔒 安全审查 + ⚡ 性能分析 + 🔧 可维护性分析<br>
                    并行执行后由 📊 汇总报告
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ── Debate 模式 ────────────────────────────────────────
def _render_debate():
    """Debate 模式渲染函数 - 多 Agent 对抗辩论"""
    from debate import stream_debate

    st.markdown("#### ⚔️ 代码辩论")
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
                        model_map = state_update.get("model_used_by", {})
                        model_key = "pro_agent" if role == "pro" else "con_agent"
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
                    model_key = "pro_agent" if role == "pro" else "con_agent"
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
            """
            <div style="text-align:center;padding:60px 20px;color:#AAAAAA;">
                <div style="font-size:40px;margin-bottom:16px;">⚔️</div>
                <div style="font-size:16px;font-weight:500;color:#888888;margin-bottom:8px;">Debate 模式已就绪</div>
                <div style="font-size:13px;line-height:1.8;">
                    🟢 支持方 vs 🔴 反对方<br>
                    多轮辩论后由 ⚖️ 裁判给出最终建议
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ── Nested Agent 模式 ──────────────────────────────────
def _render_nested_agent():
    """Nested Agent 模式渲染函数"""
    from nested_agent import stream_nested

    st.markdown("#### 🪆 Nested Agent")
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
        st.success("🎉 Nested Agent 执行完成！")

    elif run_btn and not req_input.strip():
        st.warning("⚠️ 请先输入需求描述再开始执行。")

    elif not st.session_state.na_is_running and st.session_state.na_result:
        with results_container.container():
            st.markdown("### 📦 最终项目交付成果")
            st.success(st.session_state.na_result)

    else:
        st.markdown(
            """
            <div style="text-align:center;padding:60px 20px;color:#AAAAAA;">
                <div style="font-size:40px;margin-bottom:16px;">🪆</div>
                <div style="font-size:16px;font-weight:500;color:#888888;margin-bottom:8px;">Nested Agent 已就绪</div>
                <div style="font-size:13px;line-height:1.8;">
                    🎼 Orchestrator 召唤子 Agent 并行执行：<br>
                    💻 程序员 + 🧪 测试员 + 🔒 安全审查 + 📝 文档员<br>
                    最后 📦 汇总交付成果
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ── Hybrid A 模式 ───────────────────────────────────────
def _render_hybrid_a():
    """Hybrid A 模式渲染函数 - 混合模式 A：并行生成 + 循环质检 + 条件分支"""
    from hybrid_a import stream_hybrid_a

    st.markdown("#### 🌀 Hybrid A · 并行生成 + 循环质检 + 条件分支")
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
        st.success("🎉 Hybrid A 执行完成！")

    elif run_btn and not req_input.strip():
        st.warning("⚠️ 请先输入需求描述再开始执行。")

    elif not st.session_state.ha_is_running and st.session_state.ha_history:
        _render_current_state()

    else:
        st.markdown(
            """
            <div style="text-align:center;padding:60px 20px;color:#AAAAAA;">
                <div style="font-size:40px;margin-bottom:16px;">🌀</div>
                <div style="font-size:16px;font-weight:500;color:#888888;margin-bottom:8px;">Hybrid A 模式已就绪</div>
                <div style="font-size:13px;line-height:1.8;">
                    Phase 1: 💻💰📝 并行生成代码/测试/文档<br>
                    Phase 2: 🔍 循环质检（直到通过）<br>
                    Phase 3: 🔀 条件分支（安全/性能/可维护性）<br>
                    Phase 4: 📋 项目交付报告
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ── Hybrid B 模式 ───────────────────────────────────────
def _render_hybrid_b():
    """Hybrid B 模式渲染函数 - 辩论 + 嵌套 Agent"""
    from hybrid_b import stream_hybrid_b

    # ── 输入区 ───────────────────────────────────────────
    st.markdown("#### 🏗️ 架构方案评审")
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
            """
            <div style="text-align:center;padding:60px 20px;color:#AAAAAA;">
                <div style="font-size:40px;margin-bottom:16px;">🔀</div>
                <div style="font-size:16px;font-weight:500;color:#888888;margin-bottom:8px;">Hybrid B 模式已就绪</div>
                <div style="font-size:13px;line-height:1.8;">
                    输入架构方案，支持方/反对方召唤子Agent收集数据后辩论<br>
                    <span style="color:#10b981">🟢 支持方</span> → 召唤 ⚡性能 + 💰成本 Agent<br>
                    <span style="color:#ef4444">🔴 反对方</span> → 召唤 🔒安全 + 🔧可维护性 Agent<br>
                    ⚖️ 裁判综合所有数据给出最终建议
                </div>
            </div>
            """,
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
