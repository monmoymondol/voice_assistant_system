# backend/integrations/integrations.py
import requests

ECOMMERCE_BASE = "http://localhost:5000/api"  # change to your e-commerce backend
INVOICE_SERVICE = "http://localhost:5001"     # change to your invoice service

def place_order_via_api(user_id: int, product_id: int, quantity: int):
    try:
        r = requests.post(f"{ECOMMERCE_BASE}/orders", json={"user_id": user_id, "product_id": product_id, "quantity": quantity}, timeout=8)
        return r.json()
    except Exception as e:
        return {"error": str(e)}

def generate_invoice_via_api(customer: str, items: list):
    try:
        r = requests.post(f"{INVOICE_SERVICE}/generate", json={"customer": customer, "items": items}, timeout=12)
        return r.json()
    except Exception as e:
        return {"error": str(e)}
