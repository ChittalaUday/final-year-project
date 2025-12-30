import sys
import traceback

print("="*60)
print("Testing imports...")
print("="*60)

try:
    print("\n1. Testing app.config import...")
    from app.config import settings
    print(f"   ✓ Config imported successfully")
except Exception as e:
    print(f"   ✗ Error: {e}")
    with open("error_details.txt", "w") as f:
        f.write(f"Config error:\n{traceback.format_exc()}\n\n")
    traceback.print_exc()

try:
    print("\n2. Testing app.models import...")
    from app.models import career
    print(f"   ✓ Models imported successfully")
except Exception as e:
    print(f"   ✗ Error: {e}")
    with open("error_details.txt", "a") as f:
        f.write(f"Models error:\n{traceback.format_exc()}\n\n")
    traceback.print_exc()

try:
    print("\n3. Testing app.services import...")
    from app.services import career_service
    print(f"   ✓ Services imported successfully")
except Exception as e:
    print(f"   ✗ Error: {e}")
    with open("error_details.txt", "a") as f:
        f.write(f"Services error:\n{traceback.format_exc()}\n\n")
    traceback.print_exc()

try:
    print("\n4. Testing app.main import...")
    from app import main
    print(f"   ✓ Main imported successfully")
except Exception as e:
    print(f"   ✗ Error: {e}")
    with open("error_details.txt", "a") as f:
        f.write(f"Main error:\n{traceback.format_exc()}\n\n")
    traceback.print_exc()

print("\n" + "="*60)
print("Import test complete. Check error_details.txt for full trace")
print("="*60)
