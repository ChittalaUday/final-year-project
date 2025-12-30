import sys
import traceback

try:
    from app.main import app
    print("✓ Import successful!")
except Exception as e:
    print(f"✗ Error importing app:")
    print(f"  {type(e).__name__}: {str(e)}")
    traceback.print_exc()
    sys.exit(1)
