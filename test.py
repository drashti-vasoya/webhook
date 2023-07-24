import hashlib
import hmac
import json

import requests


def generate_hash_signature(
        secret: str,
        payload: str = "",
        digest_method=hashlib.sha256,
):
    return hmac.new(secret.encode("utf-8"), payload.encode("utf-8"), digest_method).hexdigest()


def call_webhook():
    webhook_url = "http://127.0.0.1:8000/webhook"  # Webhook URL

    secret = "secret"  # Webhook secret key
    payload = {}  # Webhook payload
    signature = generate_hash_signature(secret, json.dumps(payload))
    headers = {
        "Content-Type": "application/json",
        "x_hub_signature": signature
    }
    r = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
    return r.json()


if __name__ == "__main__":
    call_webhook()
