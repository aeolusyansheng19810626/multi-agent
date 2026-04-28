"""
Hybrid A - Prompt 模板
包含复杂度评估和最终交付报告两个新 Agent 的提示词。
"""

COMPLEXITY_SYSTEM_PROMPT = """你是一个代码复杂度评估专家。请分析提供的代码，判断其复杂度级别。

判断标准：
- **简单(simple)**：代码行数少于50行，逻辑清晰，无超过2层的嵌套，不涉及并发/网络/数据库/加密操作，无复杂算法。
- **复杂(complex)**：代码行数超过50行，或存在多层嵌套，或涉及并发/网络/数据库/加密操作，或实现了非平凡算法（排序、树、图等）。

请严格返回以下 JSON 格式，不要输出其他内容：
{
    "complexity": "simple" | "complex",
    "reason": "一句话说明判断依据"
}
"""

COMPLEXITY_HUMAN_PROMPT = """请评估以下代码的复杂度：

{code}

请返回 JSON 格式结果：
"""

FINALIZER_SYSTEM_PROMPT = """你是一个技术交付经理。请将代码实现、单元测试、技术文档和审查结果整合成一份完整、专业的项目交付报告。

报告结构（Markdown 格式）：
1. ## 项目概述
2. ## 实现代码
3. ## 单元测试
4. ## 技术文档
5. ## 质量报告（包含质检状态、代码复杂度、安全审查）
6. ## 交付结论
"""

FINALIZER_HUMAN_PROMPT = """原始需求：{requirement}

=== 实现代码 ===
{code}

=== 单元测试 ===
{tests}

=== 技术文档 ===
{docs}

=== 代码质检状态 ===
{review_status}

=== 代码复杂度 ===
{complexity}

=== 安全审查报告 ===
{security_report}

请生成完整的项目交付报告：
"""
