# backend/chatbot/generate.py
# Minimal deterministic generator for offline use (replace with real model)
def generate_text(prompt: str, max_new_tokens: int = 80) -> str:
    # Very simple echo-style fallback: return a short reply based on prompt
    # Replace with your MiniGPT generate_text when available
    if "integrate" in prompt.lower():
        return "I can help integrate expressions. Example: integrate x^2 -> x^3/3 + C"
    if "invoice" in prompt.lower():
        return "I can generate an invoice. Provide: CustomerName | item=price,item=price"
    # default
    return "Thanks — I received your message. (Replace this stub with a generative model.)"
