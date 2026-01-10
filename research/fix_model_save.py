"""
Fix for the model saving issue in career-recommendation-dataset-notebook.ipynb

This script provides the corrected code to save the model properly.
Copy and paste this into your Jupyter notebook cells.
"""

# CELL 1: Import required libraries
# Replace cell 65 content with:
"""
import joblib
import os
"""

# CELL 2: Save the model with directory creation
# Replace cell 66 content with:
# """
# # Create the directory if it doesn't exist
# model_path = r'C:\Users\hp\Documents\Course Recommendation System\Models'
# os.makedirs(model_path, exist_ok=True)

# # Save the model
# model_file = os.path.join(model_path, 'random_forest_grid2.sav')
# joblib.dump(grid_search_forest, model_file)
# print(f"Model saved successfully to: {model_file}")
# """

print("Instructions:")
print("=" * 60)
print("1. In your Jupyter notebook, find cell 65 (the one with '#import joblib')")
print("2. Replace its content with:")
print("   import joblib")
print("   import os")
print()
print("3. Find cell 66 (the one throwing FileNotFoundError)")
print("4. Replace its content with:")
print("""
# Create the directory if it doesn't exist
model_path = r'C:\\Users\\hp\\Documents\\Course Recommendation System\\Models'
os.makedirs(model_path, exist_ok=True)

# Save the model
model_file = os.path.join(model_path, 'random_forest_grid2.sav')
joblib.dump(grid_search_forest, model_file)
print(f"Model saved successfully to: {model_file}")
""")
print("=" * 60)
