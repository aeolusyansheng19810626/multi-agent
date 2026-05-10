LANGUAGE_INSTRUCTIONS = {
    "zh": "请使用简体中文输出。",
    "ja": "日本語で出力してください。",
    "en": "Please output in English.",
}


def get_language_instruction(lang: str) -> str:
    return LANGUAGE_INSTRUCTIONS.get(lang, LANGUAGE_INSTRUCTIONS["en"])
