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

LANGUAGES = {
    "zh": {"short": "CN", "name": "简体中文"},
    "ja": {"short": "JP", "name": "日本語"},
    "en": {"short": "EN", "name": "English"},
}

I18N = {
    "zh": {
        "app_title": "多智能体协作分析平台",
        "app_subtitle": "基于 LangGraph + Groq 的智能协作系统",
        "language_label": "LANGUAGE / 语言",
        "sidebar_label": "编排模式",
        "sidebar_hint": "点击卡片选择协作方式 👇",
        "coming_soon": "即将推出，敬请期待...",
        "status_pending": "⏳ 等待中",
        "status_running": "🔄 运行中",
        "status_done": "✅ 完成",
        "start_run": "🚀 开始执行",
        "start_review": "🚀 开始审查",
        "start_debate": "🚀 开始辩论",
        "mode.supervisor": "顺序流水线",
        "mode.supervisor_desc": "每个 Agent 处理前一个的输出",
        "mode.conditional": "条件分支",
        "mode.conditional_desc": "根据代码特征动态选择审查路径",
        "mode.loop": "循环反馈",
        "mode.loop_desc": "代码生成→审查→修复，直到通过",
        "mode.parallel": "并行执行",
        "mode.parallel_desc": "多维度同时分析后汇总报告",
        "mode.debate": "辩论模式",
        "mode.debate_desc": "支持方 vs 反对方，裁判给出建议",
        "mode.nested": "嵌套 Agent",
        "mode.nested_desc": "Orchestrator 召唤子 Agent 并行执行",
        "mode.hybrid_a": "混合模式 A",
        "mode.hybrid_a_desc": "并行生成 + 循环质检 + 条件分支",
        "mode.hybrid_b": "混合模式 B",
        "mode.hybrid_b_desc": "辩论 + 嵌套 Agent 综合协作",
        "agent.supervisor": "监督者",
        "agent.requirement": "需求分析",
        "agent.analyst": "需求分析",
        "agent.architect": "架构师",
        "agent.coder": "程序员",
        "agent.reviewer": "代码审查",
        "agent.tester": "测试员",
        "agent.documenter": "文档员",
        "agent.security": "安全审查",
        "agent.performance": "性能分析",
        "agent.maintainability": "可维护性分析",
        "agent.merge": "汇总报告",
        "agent.pro": "支持方",
        "agent.con": "反对方",
        "agent.judge": "裁判",
        "agent.orchestrator": "协调者",
        "agent.lf_reviewer": "审查员",
        "agent.lf_fixer": "修复员",
        "agent.cost": "成本分析",
        "supervisor.title": "#### 🔄 顺序流水线",
        "supervisor.input": "需求描述",
        "supervisor.placeholder": "例如：开发一个用户登录模块，支持 JWT 认证...",
        "supervisor.done": "🎉 顺序流水线执行完成！",
        "supervisor.empty_warning": "⚠️ 请先输入需求描述再开始执行。",
        "supervisor.help": "监督者流水线模式：顺序执行，每个 Agent 处理前一个的输出<br><span style=\"color:#6C63FF;font-weight:500;\">📋 需求分析 → 🏗️ 架构师 → 💻 程序员 → 🔍 代码审查</span>",
        "conditional.title": "#### 🔀 条件分支",
        "conditional.input": "请描述你的需求、代码或技术问题",
        "conditional.placeholder": "例如：\n[新功能] 我想加一个微信支付模块...\n[代码审查] 帮我看看这段 React 代码有没有坑...\n[技术问题] Next.js 和 Nuxt.js 选哪个好？",
        "conditional.routing": "🤔 正在分析需求类型...",
        "conditional.detected": "检测到：{route}，原因：{reason}",
        "conditional.route_info": "🧭 **条件分支路由决策:** {reason}",
        "conditional.done": "🎉 分支执行完成！",
        "conditional.empty_warning": "⚠️ 请先输入内容再执行。",
        "conditional.running": "_🔄 {agent}中…_",
        "conditional.waiting": "_⏳ 等待执行…_",
        "conditional.no_result": "_暂无结果_",
        "conditional.help": "Router 自动识别输入类型并激活对应 Agent：<br><span style=\"color:#6366f1\">新功能</span> | <span style=\"color:#7c3aed\">代码审查</span> | <span style=\"color:#0ea5e9\">技术方案</span>",
        "conditional.router": "路由分配",
        "conditional.code_opt": "代码优化",
        "conditional.research": "技术调研",
        "conditional.advisor": "技术顾问",
        "loop.title": "#### 🔁 循环反馈",
        "loop.input": "请描述你需要编写的代码",
        "loop.placeholder": "例如：写一个用 requests 抓取网页并解析标题的函数",
        "loop.iteration": "### 第 {n} 轮迭代",
        "loop.code": "💻 编码生成",
        "loop.review": "🔍 代码审查",
        "loop.review_pass": "🔍 代码审查 ✅ 通过",
        "loop.review_fail": "🔍 代码审查 ❌ 不通过",
        "loop.reviewing": "_🔄 审查中…_",
        "loop.pass": "质检通过！",
        "loop.fail": "质检不通过，打回重做。\n\n**反馈意见：**\n{feedback}",
        "loop.max": "⚠️ 达到最大迭代次数 (3次)，循环终止。",
        "loop.done": "🎉 循环反馈执行完成！",
        "loop.empty_warning": "⚠️ 请先输入需求再执行。",
        "loop.help": "💻 编码生成 → 🔍 代码审查 → 🔧 反馈修复<br>最多迭代 3 次，直到代码满足标准",
        "parallel.title": "#### 🔱 并行执行",
        "parallel.input": "输入代码",
        "parallel.placeholder": "例如：def process_data(data): import os; os.system('rm -rf /')...",
        "parallel.done": "🎉 并行审查完成！",
        "parallel.empty_warning": "⚠️ 请先输入代码再开始审查。",
        "parallel.help": "🔒 安全审查 + ⚡ 性能分析 + 🔧 可维护性分析<br>并行执行后由 📊 汇总报告",
        "debate.title": "#### ⚔️ 辩论模式",
        "debate.input": "输入代码",
        "debate.placeholder": "例如：def login(user, pwd): return True...",
        "debate.rounds": "辩论轮次",
        "debate.side": "{side} (第{round}轮)",
        "debate.verdict": "⚖️ 裁判最终裁决",
        "debate.running": "🤔 Agent 正在激烈辩论中...",
        "debate.done": "🎉 辩论结束！",
        "debate.empty_warning": "⚠️ 请先输入代码再开始辩论。",
        "debate.help": "🟢 支持方 vs 🔴 反对方<br>多轮辩论后由 ⚖️ 裁判给出最终建议",
        "nested.title": "#### 🪆 嵌套 Agent",
        "nested.input": "需求描述",
        "nested.placeholder": "例如：开发一个电商网站，支持用户注册、商品浏览、购物车...",
        "nested.planning": "🎼 Orchestrator 正在规划任务...",
        "nested.output": "🧠 {agent} 输出",
        "nested.final": "📦 最终项目交付成果",
        "nested.done": "🎉 嵌套 Agent 执行完成！",
        "nested.empty_warning": "⚠️ 请先输入需求描述再开始执行。",
        "nested.help": "🎼 Orchestrator 召唤子 Agent 并行执行：<br>💻 程序员 + 🧪 测试员 + 🔒 安全审查 + 📝 文档员<br>最后 📦 汇总交付成果",
        "hybrid_a.title": "#### 🎛️ 混合模式 A",
        "hybrid_a.input": "需求描述",
        "hybrid_a.placeholder": "例如：写一个用户认证模块，支持 JWT...",
        "hybrid_a.code_round": "💻 代码生成（第{n}轮）",
        "hybrid_a.review_pass": "✅ 代码审查通过！",
        "hybrid_a.review_fail": "❌ 代码审查未通过，正在修复...",
        "hybrid_a.security": "🔒 安全审查报告",
        "hybrid_a.final": "📋 项目交付报告",
        "hybrid_a.running": "🔄 正在执行中...",
        "hybrid_a.done": "🎉 混合模式 A 执行完成！",
        "hybrid_a.empty_warning": "⚠️ 请先输入需求描述再开始执行。",
        "hybrid_a.help": "Phase 1: 💻📝🧪 并行生成代码/测试/文档<br>Phase 2: 🔍 循环质检（直到通过）<br>Phase 3: 🔀 条件分支（安全/性能/可维护性）<br>Phase 4: 📋 项目交付报告",
        "hybrid_b.title": "#### 🎭 混合模式 B",
        "hybrid_b.input": "请输入架构方案",
        "hybrid_b.placeholder": "例如：用 Redis 做主数据库，存储用户会话和购物车数据...",
        "hybrid_b.rounds": "辩论轮次",
        "hybrid_b.analyzing": "{icon} {side}第{round}轮分析中...",
        "hybrid_b.call_perf": "⚡ 召唤性能Agent... {status}",
        "hybrid_b.call_cost": "💰 召唤成本Agent... {status}",
        "hybrid_b.call_security": "🔒 召唤安全Agent... {status}",
        "hybrid_b.call_maint": "🔧 召唤可维护性Agent... {status}",
        "hybrid_b.waiting": "⏳ 召唤中...",
        "hybrid_b.done_status": "✅ 完成",
        "hybrid_b.perf_data": "**⚡ 性能分析数据**",
        "hybrid_b.cost_data": "**💰 成本分析数据**",
        "hybrid_b.security_data": "**🔒 安全分析数据**",
        "hybrid_b.maint_data": "**🔧 可维护性分析数据**",
        "hybrid_b.argument": "**论点：**",
        "hybrid_b.done": "🎉 辩论结束！",
        "hybrid_b.empty_warning": "⚠️ 请先输入架构方案再开始辩论。",
        "hybrid_b.help": "输入架构方案，支持方/反对方召唤子 Agent 收集数据后辩论<br><span style=\"color:#10b981\">🟢 支持方</span> → 召唤 ⚡性能 + 💰成本 Agent<br><span style=\"color:#ef4444\">🔴 反对方</span> → 召唤 🔒安全 + 🔧可维护性 Agent<br>⚖️ 裁判综合所有数据给出最终建议",
    },
    "ja": {},
    "en": {},
}

I18N["ja"] = {
    **I18N["zh"],
    "app_title": "Multi-Agent 分析ﾌﾟﾗｯﾄﾌｫｰﾑ",
    "app_subtitle": "LangGraph + Groq ﾍﾞｰｽのｲﾝﾃﾘｼﾞｪﾝﾄ協調ｼｽﾃﾑ",
    "sidebar_label": "編成ﾓｰﾄﾞ",
    "sidebar_hint": "ｶｰﾄﾞをｸﾘｯｸして協調方式を選択 👇",
    "coming_soon": "近日公開予定です...",
    "status_pending": "⏳ 待機中",
    "status_running": "🔄 実行中",
    "status_done": "✅ 完了",
    "start_run": "🚀 実行開始",
    "start_review": "🚀 レビュー開始",
    "start_debate": "🚀 討論開始",
    "mode.supervisor": "順次ﾊﾟｲﾌﾟﾗｲﾝ",
    "mode.supervisor_desc": "各 Agent が前段の出力を処理",
    "mode.conditional": "条件分岐",
    "mode.conditional_desc": "入力特徴に応じてﾚﾋﾞｭｰ経路を選択",
    "mode.loop": "ﾌｨｰﾄﾞﾊﾞｯｸﾙｰﾌﾟ",
    "mode.loop_desc": "生成→ﾚﾋﾞｭｰ→修正を合格まで反復",
    "mode.parallel": "並列実行",
    "mode.parallel_desc": "複数観点で同時分析して集約",
    "mode.debate": "討論ﾓｰﾄﾞ",
    "mode.debate_desc": "賛成派 vs 反対派、審判が提案",
    "mode.nested": "ﾈｽﾄ Agent",
    "mode.nested_desc": "Orchestrator が子 Agent を並列呼び出し",
    "mode.hybrid_a": "ﾊｲﾌﾞﾘｯﾄﾞ A",
    "mode.hybrid_a_desc": "並列生成 + 反復品質確認 + 条件分岐",
    "mode.hybrid_b": "ﾊｲﾌﾞﾘｯﾄﾞ B",
    "mode.hybrid_b_desc": "討論 + ﾈｽﾄ Agent の複合協調",
    "agent.supervisor": "監督者",
    "agent.requirement": "要件分析",
    "agent.analyst": "要件分析",
    "agent.architect": "ｱｰｷﾃｸﾄ",
    "agent.coder": "ﾌﾟﾛｸﾞﾗﾏｰ",
    "agent.reviewer": "ｺｰﾄﾞﾚﾋﾞｭｰ",
    "agent.tester": "ﾃｽﾀｰ",
    "agent.documenter": "ﾄﾞｷｭﾒﾝﾄ担当",
    "agent.security": "ｾｷｭﾘﾃｨﾚﾋﾞｭｰ",
    "agent.performance": "性能分析",
    "agent.maintainability": "保守性分析",
    "agent.merge": "集約ﾚﾎﾟｰﾄ",
    "agent.pro": "賛成派",
    "agent.con": "反対派",
    "agent.judge": "審判",
    "agent.orchestrator": "調整者",
    "agent.lf_reviewer": "ﾚﾋﾞｭｱｰ",
    "agent.lf_fixer": "修正担当",
    "agent.cost": "ｺｽﾄ分析",
    "supervisor.title": "#### 🔄 順次ﾊﾟｲﾌﾟﾗｲﾝ",
    "supervisor.input": "要件説明",
    "supervisor.placeholder": "例：JWT 認証対応のﾕｰｻﾞｰﾛｸﾞｲﾝ機能を開発...",
    "supervisor.done": "🎉 順次ﾊﾟｲﾌﾟﾗｲﾝが完了しました！",
    "supervisor.empty_warning": "⚠️ 要件を入力してから実行してください。",
    "supervisor.help": "監督者ﾊﾟｲﾌﾟﾗｲﾝ：各 Agent が前段の出力を順に処理します<br><span style=\"color:#6C63FF;font-weight:500;\">📋 要件分析 → 🏗️ ｱｰｷﾃｸﾄ → 💻 ﾌﾟﾛｸﾞﾗﾏｰ → 🔍 ｺｰﾄﾞﾚﾋﾞｭｰ</span>",
    "conditional.title": "#### 🔀 条件分岐",
    "conditional.input": "要件・ｺｰﾄﾞ・技術質問を入力してください",
    "conditional.placeholder": "例：\n[新機能] WeChat Pay ﾓｼﾞｭｰﾙを追加したい...\n[ｺｰﾄﾞﾚﾋﾞｭｰ] この React ｺｰﾄﾞを見てほしい...\n[技術質問] Next.js と Nuxt.js どちらがよい？",
    "conditional.routing": "🤔 入力ﾀｲﾌﾟを分析中...",
    "conditional.detected": "検出：{route}、理由：{reason}",
    "conditional.route_info": "🧭 **条件分岐ﾙｰﾃｨﾝｸﾞ:** {reason}",
    "conditional.done": "🎉 分岐実行が完了しました！",
    "conditional.empty_warning": "⚠️ 内容を入力してから実行してください。",
    "conditional.running": "_🔄 {agent} 実行中…_",
    "conditional.waiting": "_⏳ 待機中…_",
    "conditional.no_result": "_結果はまだありません_",
    "conditional.help": "Router が入力ﾀｲﾌﾟを識別して対応する Agent を起動します：<br><span style=\"color:#6366f1\">新機能</span> | <span style=\"color:#7c3aed\">ｺｰﾄﾞﾚﾋﾞｭｰ</span> | <span style=\"color:#0ea5e9\">技術質問</span>",
    "conditional.router": "ﾙｰﾃｨﾝｸﾞ",
    "conditional.code_opt": "ｺｰﾄﾞ最適化",
    "conditional.research": "技術調査",
    "conditional.advisor": "技術ｱﾄﾞﾊﾞｲｻﾞｰ",
    "loop.title": "#### 🔁 ﾌｨｰﾄﾞﾊﾞｯｸﾙｰﾌﾟ",
    "loop.input": "作成したいｺｰﾄﾞを説明してください",
    "loop.placeholder": "例：requests でﾍﾟｰｼﾞを取得しﾀｲﾄﾙを解析する関数",
    "loop.iteration": "### 第 {n} 回ｲﾃﾚｰｼｮﾝ",
    "loop.code": "💻 ｺｰﾄﾞ生成",
    "loop.review": "🔍 ｺｰﾄﾞﾚﾋﾞｭｰ",
    "loop.review_pass": "🔍 ｺｰﾄﾞﾚﾋﾞｭｰ ✅ 合格",
    "loop.review_fail": "🔍 ｺｰﾄﾞﾚﾋﾞｭｰ ❌ 不合格",
    "loop.reviewing": "_🔄 ﾚﾋﾞｭｰ中…_",
    "loop.pass": "品質ﾁｪｯｸ合格！",
    "loop.fail": "品質ﾁｪｯｸ不合格。修正に戻します。\n\n**ﾌｨｰﾄﾞﾊﾞｯｸ：**\n{feedback}",
    "loop.max": "⚠️ 最大反復回数（3回）に達したため終了します。",
    "loop.done": "🎉 ﾌｨｰﾄﾞﾊﾞｯｸﾙｰﾌﾟが完了しました！",
    "loop.empty_warning": "⚠️ 要件を入力してから実行してください。",
    "loop.help": "💻 ｺｰﾄﾞ生成 → 🔍 ｺｰﾄﾞﾚﾋﾞｭｰ → 🔧 ﾌｨｰﾄﾞﾊﾞｯｸ修正<br>最大 3 回まで反復します",
    "parallel.title": "#### 🔱 並列実行",
    "parallel.input": "ｺｰﾄﾞを入力",
    "parallel.placeholder": "例：def process_data(data): import os; os.system('rm -rf /')...",
    "parallel.done": "🎉 並列ﾚﾋﾞｭｰが完了しました！",
    "parallel.empty_warning": "⚠️ ｺｰﾄﾞを入力してからﾚﾋﾞｭｰしてください。",
    "parallel.help": "🔒 ｾｷｭﾘﾃｨ + ⚡ 性能 + 🔧 保守性<br>並列実行後に 📊 ﾚﾎﾟｰﾄを集約",
    "debate.title": "#### ⚔️ 討論ﾓｰﾄﾞ",
    "debate.input": "ｺｰﾄﾞを入力",
    "debate.placeholder": "例：def login(user, pwd): return True...",
    "debate.rounds": "討論ﾗｳﾝﾄﾞ",
    "debate.side": "{side}（第{round}ﾗｳﾝﾄﾞ）",
    "debate.verdict": "⚖️ 審判の最終判断",
    "debate.running": "🤔 Agent が討論中...",
    "debate.done": "🎉 討論が終了しました！",
    "debate.empty_warning": "⚠️ ｺｰﾄﾞを入力してから討論してください。",
    "debate.help": "🟢 賛成派 vs 🔴 反対派<br>複数ﾗｳﾝﾄﾞ後に ⚖️ 審判が提案します",
    "nested.title": "#### 🪆 ﾈｽﾄ Agent",
    "nested.input": "要件説明",
    "nested.placeholder": "例：ﾕｰｻﾞｰ登録、商品閲覧、ｶｰﾄ対応のECｻｲﾄを開発...",
    "nested.planning": "🎼 Orchestrator がﾀｽｸを計画中...",
    "nested.output": "🧠 {agent} 出力",
    "nested.final": "📦 最終成果物",
    "nested.done": "🎉 ﾈｽﾄ Agent が完了しました！",
    "nested.empty_warning": "⚠️ 要件を入力してから実行してください。",
    "nested.help": "🎼 Orchestrator が子 Agent を並列呼び出し：<br>💻 ﾌﾟﾛｸﾞﾗﾏｰ + 🧪 ﾃｽﾀｰ + 🔒 ｾｷｭﾘﾃｨﾚﾋﾞｭｰ + 📝 ﾄﾞｷｭﾒﾝﾄ担当<br>最後に 📦 集約します",
    "hybrid_a.title": "#### 🎛️ ﾊｲﾌﾞﾘｯﾄﾞ A",
    "hybrid_a.input": "要件説明",
    "hybrid_a.placeholder": "例：JWT 対応のﾕｰｻﾞｰ認証ﾓｼﾞｭｰﾙを書く...",
    "hybrid_a.code_round": "💻 ｺｰﾄﾞ生成（第{n}回）",
    "hybrid_a.review_pass": "✅ ｺｰﾄﾞﾚﾋﾞｭｰ合格！",
    "hybrid_a.review_fail": "❌ ｺｰﾄﾞﾚﾋﾞｭｰ不合格、修正中...",
    "hybrid_a.security": "🔒 ｾｷｭﾘﾃｨﾚﾋﾞｭｰﾚﾎﾟｰﾄ",
    "hybrid_a.final": "📋 ﾌﾟﾛｼﾞｪｸﾄ納品ﾚﾎﾟｰﾄ",
    "hybrid_a.running": "🔄 実行中...",
    "hybrid_a.done": "🎉 ﾊｲﾌﾞﾘｯﾄﾞ A が完了しました！",
    "hybrid_a.empty_warning": "⚠️ 要件を入力してから実行してください。",
    "hybrid_a.help": "Phase 1: 💻📝🧪 ｺｰﾄﾞ/ﾃｽﾄ/文書を並列生成<br>Phase 2: 🔍 反復品質確認（合格まで）<br>Phase 3: 🔀 条件分岐（安全/性能/保守性）<br>Phase 4: 📋 納品ﾚﾎﾟｰﾄ",
    "hybrid_b.title": "#### 🎭 ﾊｲﾌﾞﾘｯﾄﾞ B",
    "hybrid_b.input": "ｱｰｷﾃｸﾁｬ案を入力",
    "hybrid_b.placeholder": "例：Redis を主ﾃﾞｰﾀﾍﾞｰｽとしてﾕｰｻﾞｰｾｯｼｮﾝとｶｰﾄを保存...",
    "hybrid_b.rounds": "討論ﾗｳﾝﾄﾞ",
    "hybrid_b.analyzing": "{icon} {side} 第{round}ﾗｳﾝﾄﾞ分析中...",
    "hybrid_b.call_perf": "⚡ 性能Agentを呼び出し中... {status}",
    "hybrid_b.call_cost": "💰 ｺｽﾄAgentを呼び出し中... {status}",
    "hybrid_b.call_security": "🔒 ｾｷｭﾘﾃｨAgentを呼び出し中... {status}",
    "hybrid_b.call_maint": "🔧 保守性Agentを呼び出し中... {status}",
    "hybrid_b.waiting": "⏳ 呼び出し中...",
    "hybrid_b.done_status": "✅ 完了",
    "hybrid_b.perf_data": "**⚡ 性能分析ﾃﾞｰﾀ**",
    "hybrid_b.cost_data": "**💰 ｺｽﾄ分析ﾃﾞｰﾀ**",
    "hybrid_b.security_data": "**🔒 ｾｷｭﾘﾃｨ分析ﾃﾞｰﾀ**",
    "hybrid_b.maint_data": "**🔧 保守性分析ﾃﾞｰﾀ**",
    "hybrid_b.argument": "**論点：**",
    "hybrid_b.done": "🎉 討論が終了しました！",
    "hybrid_b.empty_warning": "⚠️ ｱｰｷﾃｸﾁｬ案を入力してから討論してください。",
    "hybrid_b.help": "ｱｰｷﾃｸﾁｬ案を入力し、賛成派/反対派が子 Agent でﾃﾞｰﾀ収集後に討論します<br><span style=\"color:#10b981\">🟢 賛成派</span> → ⚡性能 + 💰ｺｽﾄ Agent<br><span style=\"color:#ef4444\">🔴 反対派</span> → 🔒安全 + 🔧保守性 Agent<br>⚖️ 審判が総合判断します",
}

I18N["en"] = {
    **I18N["zh"],
    "app_title": "Multi-Agent Platform",
    "app_subtitle": "Intelligent workflow system powered by LangGraph + Groq",
    "sidebar_label": "Workflow Modes",
    "sidebar_hint": "Click a card to choose a workflow 👇",
    "coming_soon": "Coming soon...",
    "status_pending": "⏳ Pending",
    "status_running": "🔄 Running",
    "status_done": "✅ Done",
    "start_run": "🚀 Run",
    "start_review": "🚀 Review",
    "start_debate": "🚀 Debate",
    "mode.supervisor": "Sequential Pipeline",
    "mode.supervisor_desc": "Each Agent processes the previous output",
    "mode.conditional": "Conditional Branch",
    "mode.conditional_desc": "Route by input type and code features",
    "mode.loop": "Feedback Loop",
    "mode.loop_desc": "Generate → review → fix until accepted",
    "mode.parallel": "Parallel Review",
    "mode.parallel_desc": "Analyze in parallel and merge the report",
    "mode.debate": "Debate Mode",
    "mode.debate_desc": "Pro vs Con, judged by a final Agent",
    "mode.nested": "Nested Agent",
    "mode.nested_desc": "Orchestrator invokes child Agents",
    "mode.hybrid_a": "Hybrid Mode A",
    "mode.hybrid_a_desc": "Parallel generation + quality loop + branch",
    "mode.hybrid_b": "Hybrid Mode B",
    "mode.hybrid_b_desc": "Debate + nested Agent collaboration",
    "agent.supervisor": "Supervisor",
    "agent.requirement": "Requirement Analysis",
    "agent.analyst": "Requirement Analysis",
    "agent.architect": "Architect",
    "agent.coder": "Coder",
    "agent.reviewer": "Code Review",
    "agent.tester": "Tester",
    "agent.documenter": "Documenter",
    "agent.security": "Security Review",
    "agent.performance": "Performance Analysis",
    "agent.maintainability": "Maintainability Analysis",
    "agent.merge": "Merged Report",
    "agent.pro": "Pro",
    "agent.con": "Con",
    "agent.judge": "Judge",
    "agent.orchestrator": "Orchestrator",
    "agent.lf_reviewer": "Reviewer",
    "agent.lf_fixer": "Fixer",
    "agent.cost": "Cost Analysis",
    "supervisor.title": "#### 🔄 Sequential Pipeline",
    "supervisor.input": "Requirement",
    "supervisor.placeholder": "Example: Build a user login module with JWT authentication...",
    "supervisor.done": "🎉 Sequential pipeline completed!",
    "supervisor.empty_warning": "⚠️ Enter a requirement before running.",
    "supervisor.help": "Supervisor pipeline: each Agent processes the previous output<br><span style=\"color:#6C63FF;font-weight:500;\">📋 Requirements → 🏗️ Architect → 💻 Coder → 🔍 Code Review</span>",
    "conditional.title": "#### 🔀 Conditional Branch",
    "conditional.input": "Describe a requirement, code snippet, or technical question",
    "conditional.placeholder": "Example:\n[Feature] Add a WeChat Pay module...\n[Code Review] Review this React code...\n[Technical Question] Next.js or Nuxt.js?",
    "conditional.routing": "🤔 Detecting input type...",
    "conditional.detected": "Detected: {route}; reason: {reason}",
    "conditional.route_info": "🧭 **Conditional routing:** {reason}",
    "conditional.done": "🎉 Branch completed!",
    "conditional.empty_warning": "⚠️ Enter content before running.",
    "conditional.running": "_🔄 {agent} running…_",
    "conditional.waiting": "_⏳ Waiting…_",
    "conditional.no_result": "_No result yet_",
    "conditional.help": "Router detects the input type and activates the matching Agents:<br><span style=\"color:#6366f1\">Feature</span> | <span style=\"color:#7c3aed\">Code review</span> | <span style=\"color:#0ea5e9\">Technical question</span>",
    "conditional.router": "Router",
    "conditional.code_opt": "Code Optimization",
    "conditional.research": "Technical Research",
    "conditional.advisor": "Technical Advisor",
    "loop.title": "#### 🔁 Feedback Loop",
    "loop.input": "Describe the code you need",
    "loop.placeholder": "Example: Write a function that fetches a page and parses its title",
    "loop.iteration": "### Iteration {n}",
    "loop.code": "💻 Code Generation",
    "loop.review": "🔍 Code Review",
    "loop.review_pass": "🔍 Code Review ✅ Passed",
    "loop.review_fail": "🔍 Code Review ❌ Failed",
    "loop.reviewing": "_🔄 Reviewing…_",
    "loop.pass": "Quality check passed!",
    "loop.fail": "Quality check failed. Sending back for revision.\n\n**Feedback:**\n{feedback}",
    "loop.max": "⚠️ Maximum iterations reached (3). Loop stopped.",
    "loop.done": "🎉 Feedback loop completed!",
    "loop.empty_warning": "⚠️ Enter a requirement before running.",
    "loop.help": "💻 Code generation → 🔍 Review → 🔧 Feedback fix<br>Up to 3 iterations until the code meets the standard",
    "parallel.title": "#### 🔱 Parallel Review",
    "parallel.input": "Code",
    "parallel.placeholder": "Example: def process_data(data): import os; os.system('rm -rf /')...",
    "parallel.done": "🎉 Parallel review completed!",
    "parallel.empty_warning": "⚠️ Enter code before reviewing.",
    "parallel.help": "🔒 Security + ⚡ Performance + 🔧 Maintainability<br>Run in parallel and merge into a 📊 report",
    "debate.title": "#### ⚔️ Debate Mode",
    "debate.input": "Code",
    "debate.placeholder": "Example: def login(user, pwd): return True...",
    "debate.rounds": "Debate rounds",
    "debate.side": "{side} (Round {round})",
    "debate.verdict": "⚖️ Final Verdict",
    "debate.running": "🤔 Agents are debating...",
    "debate.done": "🎉 Debate finished!",
    "debate.empty_warning": "⚠️ Enter code before starting the debate.",
    "debate.help": "🟢 Pro vs 🔴 Con<br>After multiple rounds, ⚖️ Judge gives the final recommendation",
    "nested.title": "#### 🪆 Nested Agent",
    "nested.input": "Requirement",
    "nested.placeholder": "Example: Build an ecommerce site with registration, product browsing, and cart...",
    "nested.planning": "🎼 Orchestrator is planning tasks...",
    "nested.output": "🧠 {agent} Output",
    "nested.final": "📦 Final Deliverable",
    "nested.done": "🎉 Nested Agent completed!",
    "nested.empty_warning": "⚠️ Enter a requirement before running.",
    "nested.help": "🎼 Orchestrator invokes child Agents in parallel:<br>💻 Coder + 🧪 Tester + 🔒 Security Review + 📝 Documenter<br>Then 📦 merges the deliverable",
    "hybrid_a.title": "#### 🎛️ Hybrid Mode A",
    "hybrid_a.input": "Requirement",
    "hybrid_a.placeholder": "Example: Write a JWT-based user authentication module...",
    "hybrid_a.code_round": "💻 Code Generation (Round {n})",
    "hybrid_a.review_pass": "✅ Code review passed!",
    "hybrid_a.review_fail": "❌ Code review failed, fixing...",
    "hybrid_a.security": "🔒 Security Review Report",
    "hybrid_a.final": "📋 Project Delivery Report",
    "hybrid_a.running": "🔄 Running...",
    "hybrid_a.done": "🎉 Hybrid Mode A completed!",
    "hybrid_a.empty_warning": "⚠️ Enter a requirement before running.",
    "hybrid_a.help": "Phase 1: 💻📝🧪 Generate code/tests/docs in parallel<br>Phase 2: 🔍 Quality loop until accepted<br>Phase 3: 🔀 Conditional branch (security/performance/maintainability)<br>Phase 4: 📋 Delivery report",
    "hybrid_b.title": "#### 🎭 Hybrid Mode B",
    "hybrid_b.input": "Architecture proposal",
    "hybrid_b.placeholder": "Example: Use Redis as the primary database for sessions and cart data...",
    "hybrid_b.rounds": "Debate rounds",
    "hybrid_b.analyzing": "{icon} {side} round {round} analysis...",
    "hybrid_b.call_perf": "⚡ Calling Performance Agent... {status}",
    "hybrid_b.call_cost": "💰 Calling Cost Agent... {status}",
    "hybrid_b.call_security": "🔒 Calling Security Agent... {status}",
    "hybrid_b.call_maint": "🔧 Calling Maintainability Agent... {status}",
    "hybrid_b.waiting": "⏳ Calling...",
    "hybrid_b.done_status": "✅ Done",
    "hybrid_b.perf_data": "**⚡ Performance Data**",
    "hybrid_b.cost_data": "**💰 Cost Data**",
    "hybrid_b.security_data": "**🔒 Security Data**",
    "hybrid_b.maint_data": "**🔧 Maintainability Data**",
    "hybrid_b.argument": "**Argument:**",
    "hybrid_b.done": "🎉 Debate finished!",
    "hybrid_b.empty_warning": "⚠️ Enter an architecture proposal before debating.",
    "hybrid_b.help": "Enter an architecture proposal. Pro/Con sides call child Agents for data before debating<br><span style=\"color:#10b981\">🟢 Pro</span> → ⚡Performance + 💰Cost Agent<br><span style=\"color:#ef4444\">🔴 Con</span> → 🔒Security + 🔧Maintainability Agent<br>⚖️ Judge gives the final recommendation",
}

lang_from_url = st.query_params.get("lang", "zh")
if lang_from_url not in LANGUAGES:
    lang_from_url = "zh"
st.session_state.ui_language = lang_from_url


def t(key: str, **kwargs) -> str:
    text = I18N.get(st.session_state.ui_language, I18N["zh"]).get(key, I18N["zh"].get(key, key))
    return text.format(**kwargs) if kwargs else text

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
        flex-wrap: wrap;
        gap: 12px;
    }

    .navbar-left {
        display: flex;
        align-items: center;
        gap: 15px;
        flex: 1;
        min-width: 300px;
    }

    .navbar-logo {
        font-size: 32px;
    }

    .navbar-title {
        color: #FFFFFF !important;
        font-size: 22px;
        font-weight: 700;
        margin: 0;
        line-height: 1.3;
        word-break: keep-all;
    }

    .navbar-right {
        color: rgba(255, 255, 255, 0.9);
        font-size: 13px;
        font-weight: 400;
        line-height: 1.4;
        max-width: 400px;
    }

    .navbar-actions {
        display: flex;
        align-items: center;
        gap: 18px;
        flex-shrink: 0;
    }

    .language-menu {
        position: relative;
    }

    .language-trigger {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 12px;
        border: 1.5px solid rgba(255, 255, 255, 0.8);
        border-radius: 999px;
        color: #FFFFFF;
        font-size: 13px;
        font-weight: 600;
        background: rgba(255, 255, 255, 0.14);
        box-shadow: 0 2px 6px rgba(0,0,0,0.15);
        cursor: pointer;
    }

    .language-dropdown {
        display: none;
        position: absolute;
        right: 0;
        top: 40px;
        width: 200px;
        background: #FFFFFF;
        border-radius: 12px;
        padding: 12px 10px;
        box-shadow: 0 12px 28px rgba(31, 41, 55, 0.2);
        z-index: 1000;
    }

    .language-menu:hover .language-dropdown,
    .language-dropdown:hover {
        display: block;
    }

    .language-title {
        color: #8B8DA2;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 0.08em;
        margin: 4px 10px 8px;
        pointer-events: none;
    }

    .language-option {
        display: grid;
        grid-template-columns: 36px 1fr 24px;
        align-items: center;
        gap: 6px;
        padding: 8px 10px;
        border-radius: 8px;
        color: #111827;
        text-decoration: none !important;
        font-size: 12px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .language-option:hover,
    .language-option.active {
        background: #F0ECFF;
        color: #4F46E5;
    }

    .language-code {
        font-size: 12px;
        color: #374151;
        font-weight: 800;
    }

    .language-check {
        color: #6C3FE8;
        font-weight: 900;
        text-align: center;
        font-size: 14px;
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
language_options_html = ''.join(
    f"<a href='?lang={code}' target='_self' class=\"language-option {'active' if code == st.session_state.ui_language else ''}\" "
    f"style='text-decoration: none; display: grid; grid-template-columns: 36px 1fr 24px; align-items: center; gap: 6px; padding: 8px 10px; border-radius: 8px; color: #111827; font-size: 12px; font-weight: 500; cursor: pointer; transition: all 0.2s ease;'>"
    f"<span class=\"language-code\">{meta['short']}</span><span>{meta['name']}</span>"
    f"<span class=\"language-check\">{'✓' if code == st.session_state.ui_language else ''}</span></a>"
    for code, meta in LANGUAGES.items()
)

st.markdown(
    f"""
    <div class="top-navbar">
        <div class="navbar-left">
            <h1 class="navbar-title">{t("app_title")}</h1>
        </div>
        <div class="navbar-actions">
            <div class="navbar-right">{t("app_subtitle")}</div>
            <div class="language-menu">
                <div class="language-trigger">🌐 {LANGUAGES[st.session_state.ui_language]["short"]}⌃</div>
                <div class="language-dropdown">
                    <div class="language-title">{t("language_label")}</div>
                    {language_options_html}
                </div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── 侧边栏：模式选择 ──────────────────────────────────
st.sidebar.markdown(f"""
<div style="margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid #E5E7EB;">
    <div style="font-size: 12px; color: #9CA3AF; font-weight: 600; letter-spacing: 1.2px; text-transform: uppercase; margin-bottom: 5px;">{t("sidebar_label")}</div>
    <div style="font-size: 16px; color: #374151; font-weight: 700;">{t("sidebar_hint")}</div>
</div>
""", unsafe_allow_html=True)

MODES = [
    {"key": "supervisor_pipeline", "label": t("mode.supervisor"), "icon": "🔄", "desc": t("mode.supervisor_desc"), "status": "Ready"},
    {"key": "conditional_branch", "label": t("mode.conditional"), "icon": "🔀", "desc": t("mode.conditional_desc"), "status": "Ready"},
    {"key": "loop_feedback", "label": t("mode.loop"), "icon": "🔁", "desc": t("mode.loop_desc"), "status": "Ready"},
    {"key": "parallel", "label": t("mode.parallel"), "icon": "🔱", "desc": t("mode.parallel_desc"), "status": "Ready"},
    {"key": "debate", "label": t("mode.debate"), "icon": "⚔️", "desc": t("mode.debate_desc"), "status": "Ready"},
    {"key": "nested_agent", "icon": "🪆", "label": t("mode.nested"), "desc": t("mode.nested_desc"), "status": "Ready"},
    {"key": "hybrid_a", "icon": "🎛️", "label": t("mode.hybrid_a"), "desc": t("mode.hybrid_a_desc"), "status": "Ready"},
    {"key": "hybrid_b", "icon": "🎭", "label": t("mode.hybrid_b"), "desc": t("mode.hybrid_b_desc"), "status": "Coming"},
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

st.sidebar.markdown(
    """
    <div style="margin-top:24px;padding-top:16px;border-top:1px solid #E5E7EB;text-align:center;color:#9CA3AF;font-size:13px;line-height:1.8;">
        Built by <span style="color:#6366F1;font-weight:500;">Sheng Yan</span>
        &nbsp;·&nbsp;
        <a href="https://github.com/aeolusyansheng19810626" target="_blank"
           style="color:#6366F1;text-decoration:none;font-weight:500;">GitHub</a>
    </div>
    """,
    unsafe_allow_html=True,
)

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
    "supervisor": t("agent.supervisor"),
    "requirement": t("agent.requirement"),
    "architect": t("agent.architect"),
    "coder": t("agent.coder"),
    "tester": t("agent.tester"),
    "documenter": t("agent.documenter"),
    "security_agent": t("agent.security"),
    "performance_agent": t("agent.performance"),
    "maintainability_agent": t("agent.maintainability"),
    "merge_agent": t("agent.merge"),
    "pro": t("agent.pro"),
    "con": t("agent.con"),
    "judge": t("agent.judge"),
    "analyst": t("agent.analyst"),
    "reviewer": t("agent.reviewer"),
    "orchestrator": t("agent.orchestrator"),
    "lf_coder": t("agent.coder"),
    "lf_reviewer": t("agent.lf_reviewer"),
    "lf_fixer": t("agent.lf_fixer"),
    "pro_orchestrator": f'{t("agent.pro")} {t("agent.orchestrator")}',
    "con_orchestrator": f'{t("agent.con")} {t("agent.orchestrator")}',
    "cost_agent": t("agent.cost"),
    "pro_summarizer": t("agent.pro"),
    "con_summarizer": t("agent.con"),
    "judge_agent": t("agent.judge"),
}

# ── 通用组件 ───────────────────────────────────────────

def _status_badge(status: str) -> str:
    """返回状态徽章 HTML（使用新的紫色主题样式）"""
    badges = {
        "pending": f'<span class="status-badge status-pending">{t("status_pending")}</span>',
        "running": f'<span class="status-badge status-running">{t("status_running")}</span>',
        "done": f'<span class="status-badge status-done">{t("status_done")}</span>',
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
            <div style="font-size:13px;margin-top:16px;color:#888;">{t("coming_soon")}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _remember_text_area(widget_key: str, saved_key: str):
    """Keep text_area content when its widget is temporarily unmounted."""
    if saved_key not in st.session_state:
        st.session_state[saved_key] = ""
    if widget_key not in st.session_state:
        st.session_state[widget_key] = st.session_state[saved_key]
    return lambda: st.session_state.__setitem__(saved_key, st.session_state.get(widget_key, ""))


# ── Supervisor Pipeline 模式 ────────────────────────────
def _render_supervisor_pipeline():
    """Supervisor Pipeline 模式渲染函数"""
    from supervisor_pipeline import stream_supervisor

    AGENT_ORDER = ["analyst", "architect", "coder", "reviewer"]
    AGENT_ICONS_LOCAL = {"analyst": "📋", "architect": "🏗️", "coder": "💻", "reviewer": "🔍"}
    RESULT_KEYS = {"analyst": "analysis_result", "architect": "architecture_result", "coder": "code_result", "reviewer": "review_result"}

    st.markdown(t("supervisor.title"))
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        req_input = st.text_area(t("supervisor.input"), height=120, placeholder=t("supervisor.placeholder"), label_visibility="collapsed", key="sp_req", on_change=_remember_text_area("sp_req", "sp_req_saved"))
    with col_btn:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        run_btn = st.button(t("start_run"), use_container_width=True, type="primary", key="sp_run")

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
        st.success(t("supervisor.done"))

    elif run_btn and not req_input.strip():
        st.warning(t("supervisor.empty_warning"))

    elif not st.session_state.sp_is_running and st.session_state.sp_results:
        _render_sp_state()
    else:
        st.markdown(
            f"""
            <div style="padding:20px 0;color:#6B7280;font-size:14px;line-height:1.8;">
                {t("supervisor.help")}
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
        "router": t("conditional.router"), "cb_analyst": t("agent.analyst"), "cb_architect": t("agent.architect"), "cb_coder": t("agent.coder"),
        "cb_reviewer": t("agent.reviewer"), "cb_optimizer": t("conditional.code_opt"),
        "cb_researcher": t("conditional.research"), "cb_advisor": t("conditional.advisor")
    }
    RESULT_KEYS = {
        "router": "router_decision", "cb_analyst": "analysis_result", "cb_architect": "architecture_result", "cb_coder": "code_result",
        "cb_reviewer": "review_result", "cb_optimizer": "optimization_result",
        "cb_researcher": "research_result", "cb_advisor": "advice_result"
    }

    st.markdown(t("conditional.title"))
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        requirement = st.text_area(
            label=t("conditional.input"),
            placeholder=t("conditional.placeholder"),
            height=120,
            label_visibility="collapsed",
            key="cb_requirement",
            on_change=_remember_text_area("cb_requirement", "cb_requirement_saved"),
        )
    with col_btn:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        run_btn = st.button(t("start_run"), use_container_width=True, type="primary", key="cb_run")

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
        st.session_state.cb_router_reason = t("conditional.routing")

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
                st.session_state.cb_router_reason = t("conditional.detected", route=route, reason=reason)

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
                    st.info(t("conditional.route_info", reason=st.session_state.cb_router_reason))

                for agent_key in st.session_state.cb_active_path:
                    status = st.session_state.cb_agent_status.get(agent_key, "pending")
                    label = f"{AGENT_ICONS[agent_key]} {AGENT_NAMES_LOCAL[agent_key]}"
                    with st.expander(label, expanded=(status == "running")):
                        if status == "running":
                            st.markdown(t("conditional.running", agent=AGENT_NAMES_LOCAL[agent_key]))
                        elif status == "done":
                            m_name = st.session_state.cb_model_used.get(agent_key, "")
                            if m_name:
                                st.markdown(f'<span class="model-badge">🧠 {m_name}</span>', unsafe_allow_html=True)
                            st.markdown(st.session_state.cb_results.get(agent_key, ""))
                        else:
                            st.markdown(t("conditional.waiting"))

        st.session_state.cb_is_running = False
        st.markdown("---")
        st.success(t("conditional.done"))

    elif run_btn and not requirement.strip():
        st.warning(t("conditional.empty_warning"))

    elif not st.session_state.cb_is_running and st.session_state.cb_results:
        with path_container.container():
            st.info(t("conditional.route_info", reason=st.session_state.cb_router_reason))
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
                        st.markdown(t("conditional.no_result"))
    else:
        with path_container.container():
            st.markdown(
                f"""
                <div style="padding:20px 0;color:#6B7280;font-size:14px;line-height:1.8;">
                    {t("conditional.help")}
                </div>
                """,
                unsafe_allow_html=True,
            )


# ── Loop Feedback 模式 ─────────────────────────────────
def _render_loop_feedback():
    from loop_feedback import stream_loop

    st.markdown(t("loop.title"))
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        requirement = st.text_area(
            label=t("loop.input"),
            placeholder=t("loop.placeholder"),
            height=120,
            label_visibility="collapsed",
            key="lf_requirement",
            on_change=_remember_text_area("lf_requirement", "lf_requirement_saved"),
        )
    with col_btn:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        run_btn = st.button(t("start_run"), use_container_width=True, type="primary", key="lf_run")

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
                    st.markdown(t("loop.iteration", n=iter_num))

                    with st.expander(t("loop.code"), expanded=(i == len(st.session_state.lf_history) - 1 and history["reviewer_result"] is None)):
                        st.markdown(f'<span class="model-badge">🧠 {history["coder_model"]}</span>', unsafe_allow_html=True)
                        st.markdown(history["coder_result"])

                    if history["reviewer_result"] is not None:
                        exp_label = t("loop.review_pass") if history["status"] == "pass" else t("loop.review_fail")
                        with st.expander(exp_label, expanded=(i == len(st.session_state.lf_history) - 1)):
                            st.markdown(f'<span class="model-badge">🧠 {history["reviewer_model"]}</span>', unsafe_allow_html=True)
                            if history["status"] == "pass":
                                st.success(t("loop.pass"))
                            else:
                                st.error(t("loop.fail", feedback=history["feedback"]))
                    else:
                        with st.expander(t("loop.review"), expanded=True):
                            st.markdown(t("loop.reviewing"))

                    st.markdown("<hr style='margin: 1em 0; border: none; border-top: 1px dashed #DCDCDC;'/>", unsafe_allow_html=True)

                if len(st.session_state.lf_history) >= 3 and st.session_state.lf_history[-1].get("status") == "fail":
                    st.error(t("loop.max"))

        st.session_state.lf_is_running = False
        st.success(t("loop.done"))

    elif run_btn and not requirement.strip():
        st.warning(t("loop.empty_warning"))

    elif not st.session_state.lf_is_running and st.session_state.lf_history:
        with path_container.container():
            for i, history in enumerate(st.session_state.lf_history):
                iter_num = history["iteration"]
                st.markdown(t("loop.iteration", n=iter_num))

                with st.expander(t("loop.code"), expanded=False):
                    st.markdown(f'<span class="model-badge">🧠 {history["coder_model"]}</span>', unsafe_allow_html=True)
                    st.markdown(history["coder_result"])

                if history["reviewer_result"] is not None:
                    exp_label = t("loop.review_pass") if history["status"] == "pass" else t("loop.review_fail")
                    with st.expander(exp_label, expanded=(history["status"] == "pass" or i == len(st.session_state.lf_history) - 1)):
                        st.markdown(f'<span class="model-badge">🧠 {history["reviewer_model"]}</span>', unsafe_allow_html=True)
                        if history["status"] == "pass":
                            st.success(t("loop.pass"))
                        else:
                            st.error(t("loop.fail", feedback=history["feedback"]))

                st.markdown("<hr style='margin: 1em 0; border: none; border-top: 1px dashed #DCDCDC;'/>", unsafe_allow_html=True)

            if len(st.session_state.lf_history) >= 3 and st.session_state.lf_history[-1].get("status") == "fail":
                st.error(t("loop.max"))

    else:
        with path_container.container():
            st.markdown(
                f"""
                <div style="padding:20px 0;color:#6B7280;font-size:14px;line-height:1.8;">
                    {t("loop.help")}
                </div>
                """,
                unsafe_allow_html=True,
            )


# ── Parallel Review 模式 ────────────────────────────────
def _render_parallel_review():
    """Parallel Review 模式渲染函数 - 并行代码审查"""
    from parallel import stream_parallel

    st.markdown(t("parallel.title"))
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        code_input = st.text_area(t("parallel.input"), height=120, placeholder=t("parallel.placeholder"), label_visibility="collapsed", key="pr_code", on_change=_remember_text_area("pr_code", "pr_code_saved"))
    with col_btn:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        run_btn = st.button(t("start_review"), use_container_width=True, type="primary", key="pr_run")

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
        st.success(t("parallel.done"))

    elif run_btn and not code_input.strip():
        st.warning(t("parallel.empty_warning"))

    elif not st.session_state.pr_is_running and st.session_state.pr_results:
        _render_pr_state()

    else:
        st.markdown(
            f"""<div style="padding:20px 0;color:#6B7280;font-size:14px;line-height:1.8;">
            {t("parallel.help")}
            </div>""",
            unsafe_allow_html=True,
        )


# ── Debate 模式 ────────────────────────────────────────
def _render_debate():
    """Debate 模式渲染函数 - 多 Agent 对抗辩论"""
    from debate import stream_debate

    st.markdown(t("debate.title"))
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        code_input = st.text_area(t("debate.input"), height=120, placeholder=t("debate.placeholder"), label_visibility="collapsed", key="db_code", on_change=_remember_text_area("db_code", "db_code_saved"))
    with col_btn:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        run_btn = st.button(t("start_debate"), use_container_width=True, type="primary", key="db_run")

    rounds = st.slider(t("debate.rounds"), min_value=1, max_value=3, value=2, key="db_rounds")

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
                    name = t("debate.side", side=t("agent.pro") if role == "pro" else t("agent.con"), round=round_num)

                    is_last = (i == len(st.session_state.db_history) - 1) and not st.session_state.db_conclusion

                    with st.expander(f"{icon} {name}", expanded=is_last):
                        model_key = "pro" if role == "pro" else "con"
                        model_name = st.session_state.db_model_used.get(model_key, "")
                        if model_name:
                            st.markdown(f'<span class="model-badge">🧠 {model_name}</span>', unsafe_allow_html=True)
                        st.markdown(content)

                if st.session_state.db_conclusion:
                    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
                    with st.expander(t("debate.verdict"), expanded=True):
                        model_name = st.session_state.db_model_used.get("judge", "")
                        if model_name:
                            st.markdown(f'<span class="model-badge">🧠 {model_name}</span>', unsafe_allow_html=True)
                        st.success(st.session_state.db_conclusion)
                elif st.session_state.db_is_running:
                    st.info(t("debate.running"))

        st.session_state.db_is_running = False
        st.success(t("debate.done"))

    elif run_btn and not code_input.strip():
        st.warning(t("debate.empty_warning"))

    elif not st.session_state.db_is_running and st.session_state.db_history:
        with path_container.container():
            for i, item in enumerate(st.session_state.db_history):
                role = item["role"]
                round_num = item["round"]
                content = item["content"]
                icon = "🟢" if role == "pro" else "🔴"
                name = t("debate.side", side=t("agent.pro") if role == "pro" else t("agent.con"), round=round_num)

                with st.expander(f"{icon} {name}", expanded=False):
                    model_key = "pro" if role == "pro" else "con"
                    model_name = st.session_state.db_model_used.get(model_key, "")
                    if model_name:
                        st.markdown(f'<span class="model-badge">🧠 {model_name}</span>', unsafe_allow_html=True)
                    st.markdown(content)

            if st.session_state.db_conclusion:
                st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
                with st.expander(t("debate.verdict"), expanded=True):
                    model_name = st.session_state.db_model_used.get("judge", "")
                    if model_name:
                        st.markdown(f'<span class="model-badge">🧠 {model_name}</span>', unsafe_allow_html=True)
                    st.success(st.session_state.db_conclusion)
    else:
        st.markdown(
            f"""<div style="padding:20px 0;color:#6B7280;font-size:14px;line-height:1.8;">
            {t("debate.help")}
            </div>""",
            unsafe_allow_html=True,
        )


# ── Nested Agent 模式 ──────────────────────────────────
def _render_nested_agent():
    """Nested Agent 模式渲染函数"""
    from nested_agent import stream_nested

    st.markdown(t("nested.title"))
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        req_input = st.text_area(t("nested.input"), height=120, placeholder=t("nested.placeholder"), label_visibility="collapsed", key="na_req", on_change=_remember_text_area("na_req", "na_req_saved"))
    with col_btn:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        run_btn = st.button(t("start_run"), use_container_width=True, type="primary", key="na_run")

    st.divider()

    AGENT_LABELS = {
        "coder_agent": f"💻 {t('agent.coder')}",
        "tester_agent": f"🧪 {t('agent.tester')}",
        "documenter_agent": f"📝 {t('agent.documenter')}",
    }

    if "na_result" not in st.session_state:
        st.session_state.na_result = None
    if "na_model_used" not in st.session_state:
        st.session_state.na_model_used = {}
    if "na_is_running" not in st.session_state:
        st.session_state.na_is_running = False
    if "na_plan" not in st.session_state:
        st.session_state.na_plan = None
    if "na_plan_reason" not in st.session_state:
        st.session_state.na_plan_reason = None
    if "na_coder_output" not in st.session_state:
        st.session_state.na_coder_output = None
    if "na_tester_output" not in st.session_state:
        st.session_state.na_tester_output = None
    if "na_documenter_output" not in st.session_state:
        st.session_state.na_documenter_output = None

    def _render_nested_results():
        """渲染嵌套Agent的所有结果"""
        if st.session_state.na_plan:
            with st.expander("📋 执行规划", expanded=False):
                st.markdown(f"**规划**: {st.session_state.na_plan}")
                st.markdown(f"**理由**: {st.session_state.na_plan_reason}")
        
        if st.session_state.na_coder_output:
            with st.expander(f"{AGENT_LABELS['coder_agent']} 输出", expanded=True):
                model_name = st.session_state.na_model_used.get("coder", "")
                if model_name:
                    st.markdown(f'<span class="model-badge">🧠 {model_name}</span>', unsafe_allow_html=True)
                st.code(st.session_state.na_coder_output, language="python")
        
        if st.session_state.na_tester_output:
            with st.expander(f"{AGENT_LABELS['tester_agent']} 输出", expanded=False):
                model_name = st.session_state.na_model_used.get("tester", "")
                if model_name:
                    st.markdown(f'<span class="model-badge">🧠 {model_name}</span>', unsafe_allow_html=True)
                st.code(st.session_state.na_tester_output, language="python")
        
        if st.session_state.na_documenter_output:
            with st.expander(f"{AGENT_LABELS['documenter_agent']} 输出", expanded=False):
                model_name = st.session_state.na_model_used.get("documenter", "")
                if model_name:
                    st.markdown(f'<span class="model-badge">🧠 {model_name}</span>', unsafe_allow_html=True)
                st.markdown(st.session_state.na_documenter_output)
        
        if st.session_state.na_result:
            with st.expander(t("nested.final"), expanded=True):
                model_name = st.session_state.na_model_used.get("finalizer", "")
                if model_name:
                    st.markdown(f'<span class="model-badge">🧠 {model_name}</span>', unsafe_allow_html=True)
                st.success(st.session_state.na_result)

    if run_btn and req_input.strip():
        st.session_state.na_result = None
        st.session_state.na_model_used = {}
        st.session_state.na_plan = None
        st.session_state.na_plan_reason = None
        st.session_state.na_coder_output = None
        st.session_state.na_tester_output = None
        st.session_state.na_documenter_output = None
        st.session_state.na_is_running = True

        progress_placeholder = st.empty()

        for node_name, state_update in stream_nested(req_input.strip()):
            st.session_state.na_model_used.update(state_update.get("model_used_by", {}))

            if node_name == "orchestrator_agent":
                st.session_state.na_plan = state_update.get("plan", {})
                st.session_state.na_plan_reason = state_update.get("plan_reason", "")
                progress_placeholder.info(f"📋 规划完成: {st.session_state.na_plan}")

            elif node_name == "coder_agent":
                st.session_state.na_coder_output = state_update.get("coder_output", "")
                progress_placeholder.info("💻 代码生成完成")

            elif node_name == "tester_agent":
                st.session_state.na_tester_output = state_update.get("tester_output", "")
                progress_placeholder.info("🧪 测试生成完成")

            elif node_name == "documenter_agent":
                st.session_state.na_documenter_output = state_update.get("documenter_output", "")
                progress_placeholder.info("📝 文档生成完成")

            elif node_name == "finalizer_agent":
                st.session_state.na_result = state_update.get("final_output", "")
                progress_placeholder.info("📦 最终整合完成")

        st.session_state.na_is_running = False
        progress_placeholder.empty()
        _render_nested_results()
        st.success(t("nested.done"))

    elif run_btn and not req_input.strip():
        st.warning(t("nested.empty_warning"))

    elif not st.session_state.na_is_running and st.session_state.na_result:
        _render_nested_results()

    else:
        st.markdown(
            f"""<div style="padding:20px 0;color:#6B7280;font-size:14px;line-height:1.8;">
            {t("nested.help")}
            </div>""",
            unsafe_allow_html=True,
        )


# ── Hybrid A 模式 ───────────────────────────────────────
def _render_hybrid_a():
    """Hybrid A 模式渲染函数 - 混合模式 A：并行生成 + 循环质检 + 条件分支"""
    from hybrid_a import stream_hybrid_a

    st.markdown(t("hybrid_a.title"))
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        req_input = st.text_area(t("hybrid_a.input"), height=120, placeholder=t("hybrid_a.placeholder"), label_visibility="collapsed", key="ha_req", on_change=_remember_text_area("ha_req", "ha_req_saved"))
    with col_btn:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        run_btn = st.button(t("start_run"), use_container_width=True, type="primary", key="ha_run")

    st.divider()

    if "ha_iterations" not in st.session_state:
        st.session_state.ha_iterations = []  # [{code, reviewer_status, reviewer_feedback}]
    if "ha_parallel_results" not in st.session_state:
        st.session_state.ha_parallel_results = {}  # {tester: ..., documenter: ...}
    if "ha_complexity" not in st.session_state:
        st.session_state.ha_complexity = None
    if "ha_security_result" not in st.session_state:
        st.session_state.ha_security_result = None
    if "ha_final" not in st.session_state:
        st.session_state.ha_final = None
    if "ha_model_used" not in st.session_state:
        st.session_state.ha_model_used = {}
    if "ha_is_running" not in st.session_state:
        st.session_state.ha_is_running = False

    def _render_ha_results():
        """渲染混合模式A的完整结果"""
        # 阶段1：代码生成与质检循环
        st.markdown("### 📝 阶段1：代码生成与质检")
        for i, iter_data in enumerate(st.session_state.ha_iterations):
            iter_num = i + 1
            code = iter_data.get("code", "")
            status = iter_data.get("reviewer_status")
            feedback = iter_data.get("reviewer_feedback", "")
            
            # 代码生成
            with st.expander(f"💻 代码生成（第{iter_num}轮）", expanded=(i == len(st.session_state.ha_iterations) - 1)):
                model = st.session_state.ha_model_used.get("ha_coder", "")
                if model:
                    st.markdown(f'<span class="model-badge">🧠 {model}</span>', unsafe_allow_html=True)
                st.code(code, language="python")
            
            # 第1轮后显示并行生成（测试+文档）
            if i == 0 and st.session_state.ha_parallel_results:
                st.markdown("#### 🔀 并行生成（测试 + 文档）")
                
                if "tester" in st.session_state.ha_parallel_results:
                    with st.expander("🧪 单元测试", expanded=False):
                        model = st.session_state.ha_model_used.get("ha_tester", "")
                        if model:
                            st.markdown(f'<span class="model-badge">🧠 {model}</span>', unsafe_allow_html=True)
                        st.code(st.session_state.ha_parallel_results["tester"], language="python")
                
                if "documenter" in st.session_state.ha_parallel_results:
                    with st.expander("📝 技术文档", expanded=False):
                        model = st.session_state.ha_model_used.get("ha_documenter", "")
                        if model:
                            st.markdown(f'<span class="model-badge">🧠 {model}</span>', unsafe_allow_html=True)
                        st.markdown(st.session_state.ha_parallel_results["documenter"])
            
            # 质检结果
            if status:
                if status == "pass":
                    with st.expander(f"✅ 代码质检通过（第{iter_num}轮）", expanded=False):
                        model = st.session_state.ha_model_used.get("ha_reviewer", "")
                        if model:
                            st.markdown(f'<span class="model-badge">🧠 {model}</span>', unsafe_allow_html=True)
                        st.success("代码质量合格，通过审查")
                else:
                    with st.expander(f"❌ 代码质检不通过（第{iter_num}轮）", expanded=False):
                        model = st.session_state.ha_model_used.get("ha_reviewer", "")
                        if model:
                            st.markdown(f'<span class="model-badge">🧠 {model}</span>', unsafe_allow_html=True)
                        st.error(f"**反馈**: {feedback}")
        
        # 阶段2：复杂度分析与安全审查
        if st.session_state.ha_complexity:
            st.markdown("### 🔍 阶段2：复杂度分析与安全审查")
            complexity = st.session_state.ha_complexity
            model = st.session_state.ha_model_used.get("ha_complexity", "")
            
            if complexity == "complex":
                st.warning(f"🔴 复杂度：**高** → 触发安全审查")
                if model:
                    st.markdown(f'<span class="model-badge">🧠 {model}</span>', unsafe_allow_html=True)
            else:
                st.info(f"🟢 复杂度：**低** → 跳过安全审查")
                if model:
                    st.markdown(f'<span class="model-badge">🧠 {model}</span>', unsafe_allow_html=True)
        
        # 安全审查（如果有）
        if st.session_state.ha_security_result:
            with st.expander("🔒 安全审查报告", expanded=False):
                model = st.session_state.ha_model_used.get("ha_security", "")
                if model:
                    st.markdown(f'<span class="model-badge">🧠 {model}</span>', unsafe_allow_html=True)
                st.markdown(st.session_state.ha_security_result)
        
        # 阶段3：最终交付
        if st.session_state.ha_final:
            st.markdown("### 📦 阶段3：最终交付")
            with st.expander("项目交付报告", expanded=True):
                model = st.session_state.ha_model_used.get("ha_finalizer", "")
                if model:
                    st.markdown(f'<span class="model-badge">🧠 {model}</span>', unsafe_allow_html=True)
                st.success(st.session_state.ha_final)

    results_container = st.empty()

    if run_btn and req_input.strip():
        st.session_state.ha_iterations = []
        st.session_state.ha_parallel_results = {}
        st.session_state.ha_complexity = None
        st.session_state.ha_security_result = None
        st.session_state.ha_final = None
        st.session_state.ha_model_used = {}
        st.session_state.ha_is_running = True

        for node_name, state_update in stream_hybrid_a(req_input.strip()):
            # 跳过中转节点或空更新
            if not state_update or node_name == "dispatcher":
                continue
                
            st.session_state.ha_model_used.update(state_update.get("model_used_by", {}))

            if node_name == "ha_coder":
                code = state_update.get("code_result", "")
                st.session_state.ha_iterations.append({
                    "code": code,
                    "reviewer_status": None,
                    "reviewer_feedback": None,
                })

            elif node_name == "ha_reviewer":
                status = state_update.get("status", "fail")
                feedback = state_update.get("feedback", "")
                if st.session_state.ha_iterations:
                    st.session_state.ha_iterations[-1]["reviewer_status"] = status
                    st.session_state.ha_iterations[-1]["reviewer_feedback"] = feedback

            elif node_name == "ha_tester":
                test_output = state_update.get("tester_output", "")
                if test_output:
                    st.session_state.ha_parallel_results["tester"] = test_output

            elif node_name == "ha_documenter":
                doc_output = state_update.get("documenter_output", "")
                if doc_output:
                    st.session_state.ha_parallel_results["documenter"] = doc_output

            elif node_name == "ha_complexity":
                complexity = state_update.get("complexity", "simple")
                st.session_state.ha_complexity = complexity

            elif node_name == "ha_security":
                security_result = state_update.get("security_result", "")
                if security_result:
                    st.session_state.ha_security_result = security_result

            elif node_name == "ha_finalizer":
                final_output = state_update.get("final_output", "")
                if final_output:
                    st.session_state.ha_final = final_output

            # 实时渲染当前状态
            with results_container.container():
                _render_ha_results()

        st.session_state.ha_is_running = False
        with results_container.container():
            _render_ha_results()
        st.success(t("hybrid_a.done"))

    elif run_btn and not req_input.strip():
        st.warning(t("hybrid_a.empty_warning"))

    elif not st.session_state.ha_is_running and st.session_state.ha_iterations:
        _render_ha_results()

    else:
        st.markdown(
            f"""<div style="padding:20px 0;color:#6B7280;font-size:14px;line-height:1.8;">
            {t("hybrid_a.help")}
            </div>""",
            unsafe_allow_html=True,
        )


# ── Hybrid B 模式 ───────────────────────────────────────
def _render_hybrid_b():
    """Hybrid B 模式渲染函数 - 辩论 + 嵌套 Agent"""
    from hybrid_b import stream_hybrid_b

    # ── 输入区 ───────────────────────────────────────────
    st.markdown(t("hybrid_b.title"))
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        scheme_input = st.text_area(
            label=t("hybrid_b.input"),
            placeholder=t("hybrid_b.placeholder"),
            height=120,
            label_visibility="collapsed",
            key="hb_scheme_input",
            on_change=_remember_text_area("hb_scheme_input", "hb_scheme_input_saved"),
        )
    with col_btn:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        run_btn = st.button(t("start_debate"), use_container_width=True, type="primary", key="hb_run")

    rounds = st.slider(t("hybrid_b.rounds"), min_value=1, max_value=3, value=2, key="hb_rounds")

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
                    "performance": t("hybrid_b.waiting"),
                    "cost": t("hybrid_b.waiting"),
                    "done": False
                }
            elif node_name == "performance_agent":
                if st.session_state.hb_sub_agent_status:
                    st.session_state.hb_sub_agent_status["performance"] = t("hybrid_b.done_status")
            elif node_name == "cost_agent":
                if st.session_state.hb_sub_agent_status:
                    st.session_state.hb_sub_agent_status["cost"] = t("hybrid_b.done_status")
            elif node_name == "pro_summarizer":
                if st.session_state.hb_sub_agent_status:
                    st.session_state.hb_sub_agent_status["done"] = True
            elif node_name == "con_orchestrator":
                current_round = state_update.get("current_round", 1)
                st.session_state.hb_sub_agent_status = {
                    "side": "con",
                    "round": current_round,
                    "security": t("hybrid_b.waiting"),
                    "maintainability": t("hybrid_b.waiting"),
                    "done": False
                }
            elif node_name == "security_agent":
                if st.session_state.hb_sub_agent_status:
                    st.session_state.hb_sub_agent_status["security"] = t("hybrid_b.done_status")
            elif node_name == "maintainability_agent":
                if st.session_state.hb_sub_agent_status:
                    st.session_state.hb_sub_agent_status["maintainability"] = t("hybrid_b.done_status")
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
                    side_name = t("agent.pro") if status["side"] == "pro" else t("agent.con")
                    st.info(t("hybrid_b.analyzing", icon=side_icon, side=side_name, round=status["round"]))

                    if status["side"] == "pro":
                        col1, col2 = st.columns(2)
                        with col1:
                            st.caption(t("hybrid_b.call_perf", status=status.get("performance", "⏳")))
                        with col2:
                            st.caption(t("hybrid_b.call_cost", status=status.get("cost", "⏳")))
                    else:
                        col1, col2 = st.columns(2)
                        with col1:
                            st.caption(t("hybrid_b.call_security", status=status.get("security", "⏳")))
                        with col2:
                            st.caption(t("hybrid_b.call_maint", status=status.get("maintainability", "⏳")))

                # 显示辩论历史
                for i, item in enumerate(st.session_state.hb_history):
                    role = item["role"]
                    round_num = item["round"]
                    content = item["content"]
                    icon = "🟢" if role == "pro" else "🔴"
                    name = t("debate.side", side=t("agent.pro") if role == "pro" else t("agent.con"), round=round_num)

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
                                st.markdown(t("hybrid_b.perf_data"))
                                st.caption(item["performance_result"][:500] + "...")
                            if item.get("cost_result"):
                                st.markdown(t("hybrid_b.cost_data"))
                                st.caption(item["cost_result"][:500] + "...")
                        else:
                            if item.get("security_result"):
                                st.markdown(t("hybrid_b.security_data"))
                                st.caption(item["security_result"][:500] + "...")
                            if item.get("maintainability_result"):
                                st.markdown(t("hybrid_b.maint_data"))
                                st.caption(item["maintainability_result"][:500] + "...")

                        # 显示论点
                        st.markdown(t("hybrid_b.argument"))
                        st.markdown(content)

                # 显示裁判裁决
                if st.session_state.hb_conclusion:
                    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
                    with st.expander(t("debate.verdict"), expanded=True):
                        model_name = st.session_state.hb_model_used.get("judge", "")
                        if model_name:
                            st.markdown(f'<span class="model-badge">🧠 {model_name}</span>', unsafe_allow_html=True)
                        st.success(st.session_state.hb_conclusion)
                elif st.session_state.hb_is_running:
                    st.info(t("debate.running"))

        st.session_state.hb_is_running = False
        st.success(t("hybrid_b.done"))

    elif run_btn and not scheme_input.strip():
        st.warning(t("hybrid_b.empty_warning"))

    elif not st.session_state.hb_is_running and st.session_state.hb_history:
        with path_container.container():
            for i, item in enumerate(st.session_state.hb_history):
                role = item["role"]
                round_num = item["round"]
                content = item["content"]
                icon = "🟢" if role == "pro" else "🔴"
                name = t("debate.side", side=t("agent.pro") if role == "pro" else t("agent.con"), round=round_num)

                with st.expander(f"{icon} {name}", expanded=False):
                    # 显示模型信息
                    model_key = "pro_summarizer" if role == "pro" else "con_summarizer"
                    model_name = st.session_state.hb_model_used.get(model_key, "")
                    if model_name:
                        st.markdown(f'<span class="model-badge">🧠 {model_name}</span>', unsafe_allow_html=True)

                    # 显示子Agent数据（折叠）
                    if role == "pro":
                        if item.get("performance_result"):
                            with st.expander(t("hybrid_b.perf_data").strip("*"), expanded=False):
                                st.caption(item["performance_result"])
                        if item.get("cost_result"):
                            with st.expander(t("hybrid_b.cost_data").strip("*"), expanded=False):
                                st.caption(item["cost_result"])
                    else:
                        if item.get("security_result"):
                            with st.expander(t("hybrid_b.security_data").strip("*"), expanded=False):
                                st.caption(item["security_result"])
                        if item.get("maintainability_result"):
                            with st.expander(t("hybrid_b.maint_data").strip("*"), expanded=False):
                                st.caption(item["maintainability_result"])

                    st.markdown(t("hybrid_b.argument"))
                    st.markdown(content)

            if st.session_state.hb_conclusion:
                st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
                with st.expander(t("debate.verdict"), expanded=True):
                    model_name = st.session_state.hb_model_used.get("judge", "")
                    if model_name:
                        st.markdown(f'<span class="model-badge">🧠 {model_name}</span>', unsafe_allow_html=True)
                    st.success(st.session_state.hb_conclusion)
    else:
        st.markdown(
            f"""<div style="padding:20px 0;color:#6B7280;font-size:14px;line-height:1.8;">
            {t("hybrid_b.help")}
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
