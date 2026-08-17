"""Test the responder-loaded hook logic outside the gateway."""
import sys
from pathlib import Path

# Force reload in case it's already imported
hook_path = Path(r"C:\Users\User\AppData\Local\hermes\hooks\whatsapp-customer-gate\handler.py")
sys.path.insert(0, str(hook_path.parent))

# We need to mock the _is_owner and platform checks
import importlib.util
spec = importlib.util.spec_from_file_location("hook_handler", hook_path)
mod = importlib.util.module_from_spec(spec)

# Patch the _is_owner from the module after load - first set to False for customer tests
loaded_mod = None
try:
    spec.loader.exec_module(mod)
    loaded_mod = mod
except Exception as e:
    print("HOOK LOAD FAILED:", e)
    sys.exit(1)

# Mock WhatsApp source object
class MockPlatform:
    value = "whatsapp"

class MockSource:
    platform = MockPlatform()
    user_id = "233204252252"  # non-owner
    chat_id = "234803XXXXXXX@s.whatsapp.net"
    chat_type = "dm"

class MockEvent:
    def __init__(self, text):
        self.text = text
        self.source = MockSource()

# Test 1: Jiji item
print("=== Test 1: Jiji item ===")
event1 = MockEvent("Do you have the Flopro hose spray gun?")
result1 = loaded_mod.handle("pre_gateway_dispatch", {"event": event1})
print("Result:", result1)
assert result1.get("action") == "rewrite", "Expected rewrite"
assert "Flopro 8 Head Hose Spray Gun" in result1.get("text", ""), "Expected Jiji title in reply"
print("PASS\n")

# Test 2: Unknown item
print("=== Test 2: Unknown item ===")
event2 = MockEvent("Can you do me a Samsung S25 ultra 512gb")
result2 = loaded_mod.handle("pre_gateway_dispatch", {"event": event2})
print("Result:", result2)
assert result2.get("action") == "rewrite", "Expected rewrite"
assert result2.get("text") == "We will get back to you shortly.", "Expected placeholder"
print("PASS\n")

# Test 3: Zobaze item
print("=== Test 3: Zobaze item ===")
event3 = MockEvent("How much is hydraulic bottle jack?")
result3 = loaded_mod.handle("pre_gateway_dispatch", {"event": event3})
print("Result:", result3)
assert result3.get("action") == "rewrite", "Expected rewrite"
assert "Hydraulic Bottle Jack HBJ602" in result3.get("text", ""), "Expected Zobaze item name"
assert "GHS 450" in result3.get("text", ""), "Expected price"
print("PASS\n")

# Test 4: Owner number gets through
print("=== Test 4: Owner number bypass ===")
# Temporarily patch _is_owner to return True
orig_is_owner = loaded_mod._is_owner
loaded_mod._is_owner = lambda s: True
event4 = MockEvent("Do you have the Flopro hose spray gun?")
result4 = loaded_mod.handle("pre_gateway_dispatch", {"event": event4})
print("Result:", result4)
assert result4 is None, "Expected None for owner"
print("PASS\n")
loaded_mod._is_owner = orig_is_owner

# Test 5: Non-WhatsApp platform passes through
print("=== Test 5: Non-WhatsApp bypass ===")
class MockSourceTG:
    platform = type('P', (), {'value': 'telegram'})()
    user_id = "123"
    chat_id = "456"
    chat_type = "dm"

class MockEventTG:
    def __init__(self, text):
        self.text = text
        self.source = MockSourceTG()

event5 = MockEventTG("Do you have the Flopro hose spray gun?")
result5 = loaded_mod.handle("pre_gateway_dispatch", {"event": event5})
print("Result:", result5)
assert result5 is None, "Expected None for telegram"
print("PASS\n")

print("All hook integration tests passed.")
