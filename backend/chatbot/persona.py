# backend/chatbot/persona.py
persona_styles = {
    "friendly": "You are a friendly assistant. Use warm, helpful tone.",
    "professional": "You are a professional assistant. Be concise and formal.",
    "creative": "You are a creative assistant. Be imaginative and playful."
}
_current = {"style": "friendly"}

def set_persona(style: str):
    if style in persona_styles:
        _current["style"] = style
        return True
    return False

def get_persona_prompt() -> str:
    return persona_styles.get(_current["style"], "")
