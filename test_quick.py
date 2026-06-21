from unittest.mock import patch
from anthropic import Anthropic
import os

client = Anthropic(api_key="fake-key-for-test")

# Cas 1 : guard désactivé -> doit appeler self.request normalement
with patch.object(client, "request", return_value="FAKE_RESPONSE") as mock_request:
    result = client.post("/v1/messages", cast_to=dict, body={"messages": [{"role": "user", "content": "hello"}]})
    assert result == "FAKE_RESPONSE", f"Bug pas réglé, post() a retourné: {result}"
    print("OK: post() fonctionne normalement (guard off)")

os.environ["ANTHROPIC_ENABLE_HEURISTIC_GUARD"] = "1"

# Cas 2 : guard activé, message VALIDE avec verbe opérant -> doit passer
with patch.object(client, "request", return_value="FAKE_RESPONSE") as mock_request:
    result = client.post("/v1/messages", cast_to=dict, body={"messages": [{"role": "user", "content": "Génère un résumé de ce document en français"}]})
    assert result == "FAKE_RESPONSE", f"Bug: message valide bloqué a tort, post() a retourné: {result}"
    print("OK: post() fonctionne avec guard activé + message valide")

# Cas 3 : guard activé, prompt cassé -> doit être bloqué (ValueError)
try:
    client.post("/v1/messages", cast_to=dict, body={"messages": [{"role": "user", "content": "asdkj zzzz xxx"}]})
    print("PROBLEME: un prompt cassé est passé alors qu'il devrait être bloqué!")
except ValueError as e:
    print(f"OK: prompt cassé bien bloqué ({e})")

print("Tous les tests passent")
