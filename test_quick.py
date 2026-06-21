from unittest.mock import patch
from anthropic import Anthropic
import os

client = Anthropic(api_key="fake-key-for-test")

with patch.object(client, "request", return_value="FAKE_RESPONSE") as mock_request:
    result = client.post("/v1/messages", cast_to=dict, body={"messages": [{"role": "user", "content": "hello"}]})
    assert result == "FAKE_RESPONSE", f"Bug pas réglé, post() a retourné: {result}"
    print("OK: post() fonctionne normalement (guard off)")

os.environ["ANTHROPIC_ENABLE_HEURISTIC_GUARD"] = "1"
with patch.object(client, "request", return_value="FAKE_RESPONSE") as mock_request:
    result = client.post("/v1/messages", cast_to=dict, body={"messages": [{"role": "user", "content": "hello, valid prompt"}]})
    assert result == "FAKE_RESPONSE"
    print("OK: post() fonctionne avec guard activé + message valide")

print("Tous les tests passent")
