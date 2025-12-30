import joblib
import numpy as np
from pathlib import Path
import sys

try:
    # Load scaler
    sc_path = r'd:\Projects\Project\research\Models\sc.sav'
    sc = joblib.load(sc_path)
    
    # Get feature names
    if hasattr(sc, 'feature_names_in_'):
        feature_names = sc.feature_names_in_
        print(f"Found {len(feature_names)} features")
        print("First 5:", feature_names[:5])
        
        # Save to file
        np.save('expected_features.npy', feature_names)
        print("Saved to expected_features.npy")
        
        # Also save as text for easy reading
        with open('expected_features.txt', 'w', encoding='utf-8') as f:
            for feat in feature_names:
                f.write(f"{feat}\n")
    else:
        print("Scaler does not have feature_names_in_ attribute")
        
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
