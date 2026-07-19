# backend/chatbot/chatbot.py
import json
from .memory import ConversationMemory
from .persona import get_persona_prompt, set_persona
from ..kb.retriever_faiss import DenseRetriever
from ..resume_analyzer.analyzer import analyze_resume
from ..integrations.integrations import place_order_via_api, generate_invoice_via_api
from .generate import generate_text  # generative fallback

memory = ConversationMemory()
try:
    retriever = DenseRetriever()
except Exception:
    retriever = None

# load FAQ
try:
    with open("backend/faq.json", "r", encoding="utf-8") as f:
        FAQ = json.load(f)
except Exception:
    FAQ = {"faqs": []}

def check_faq(message: str):
    m = message.lower()
    for item in FAQ.get("faqs", []):
        if item["q"].lower() in m:
            return item["a"]
    return None

def check_persona_command(message: str):
    m = message.lower()
    if "switch to professional" in m:
        set_persona("professional"); return "Persona switched to professional."
    if "switch to creative" in m:
        set_persona("creative"); return "Persona switched to creative."
    if "switch to friendly" in m:
        set_persona("friendly"); return "Persona switched to friendly."
    return None

def check_kb(message: str):
    if retriever is None:
        return None
    hits = retriever.query(message, top_k=2)
    if not hits:
        return None
    snippets = []
    for h in hits:
        snippets.append(f"From {h['name']} (score {h['score']:.2f}): {h['text'][:300]}")
    return "\n\n".join(snippets)

def check_action_commands(message: str):
    m = message.lower()
    if m.startswith("order product"):
        # format: order product <id> qty <n>
        import re
        match = re.search(r"order product\s+(\d+)\s+qty\s+(\d+)", m)
        if match:
            pid = int(match.group(1)); qty = int(match.group(2))
            return place_order_via_api(user_id=1, product_id=pid, quantity=qty)
        return {"error": "Use: order product <id> qty <n>"}
    if m.startswith("generate invoice"):
        # format: generate invoice: Name | item=price,item=price
        try:
            parts = message.split(":",1)[1].strip()
            name, items_raw = parts.split("|",1)
            items = []
            for it in items_raw.split(","):
                n,p = it.split("=")
                items.append({"name": n.strip(), "price": float(p.strip())})
            return generate_invoice_via_api(customer=name.strip(), items=items)
        except Exception:
            return {"error": "Format: generate invoice: CustomerName | item=12.5,item2=7"}
    return None

def compose_prompt(user_id: str, message: str):
    ctx = memory.get_context(user_id)
    ctx_text = ""
    for turn in ctx:
        ctx_text += f"User: {turn['user']}\nAssistant: {turn['bot']}\n"
    persona = get_persona_prompt()
    prompt = f"{persona}\n{ctx_text}User: {message}\nAssistant:"
    return prompt

def chat(user_id: str, message: str) -> str:
    # 1. persona commands
    p = check_persona_command(message)
    if p:
        return p
    # 2. action commands
    action = check_action_commands(message)
    if action:
        return json.dumps(action)
    # 3. FAQ
    f = check_faq(message)
    if f:
        memory.update(user_id, message, f)
        return f
    # 4. KB
    k = check_kb(message)
    if k:
        memory.update(user_id, message, k)
        return k
    # 5. generative fallback
    prompt = compose_prompt(user_id, message)
    gen = generate_text(prompt)
    memory.update(user_id, message, gen)
    return gen
