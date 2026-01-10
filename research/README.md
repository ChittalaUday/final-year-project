# Career Recommendation System - Research & AI Models

This directory contains the machine learning research, datasets, and trained models for the Career Recommendation System. The goal of this component is to analyze student profiles (interests, skills, grades) and predict suitable career courses or paths.

## 📂 Directory Structure

| File/Folder                                    | Description                                                                                                      |
| ---------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| `career-recommendation-dataset-notebook.ipynb` | Main Jupyter Notebook containing the end-to-end ML workflow: EDA, preprocessing, model training, and evaluation. |
| `career_recommender.csv`                       | The dataset used for training and testing the models.                                                            |
| `Models/`                                      | Directory containing serialized (pickled) model artifacts and encoders.                                          |
| `temp_notebook.py`                             | Python script export of the notebook logic.                                                                      |

## 📊 Dataset: `career_recommender.csv`

The dataset contains student profiles with various attributes used to predict the most suitable course.

**Key Features:**

- **Demographics:** Gender
- **Academic:** UG Course, Specialization, Grades (CGPA/Percentage)
- **Interests & Skills:** User interests (e.g., "Technology", "Research") and technical skills (e.g., "Python", "SQL"), often provided as comma-separated lists.
- **Target Variable:** `Course` (The recommended course/career path).

## 🧠 Machine Learning Workflow

The `career-recommendation-dataset-notebook.ipynb` performs the following steps:

1.  **Data Loading & Cleaning**:
    - Loads data from CSV.
    - Renames columns for better readability.
    - Handles missing values (Imputation with Mode).
    - Uses `klib` for efficient data cleaning and type conversion.

2.  **Preprocessing**:
    - **Label Encoding**: attributes like `Gender` and `Course` are label encoded.
    - **Multi-Hot Encoding**: `Interests` and `Skills` columns (containing lists of items) are transformed using `MultiLabelBinarizer` to create binary vectors for each unique interest/skill.
    - **Standardization**: Numerical features are scaled using `StandardScaler`.

3.  **Model Training**:
    - **Linear Regression**: Utilized as a baseline model.
    - **Random Forest Regressor**: The primary model used for predictions.
    - **Hyperparameter Tuning**: `GridSearchCV` is used to optimize Random Forest parameters (`n_estimators`, `max_depth`, etc.).

4.  **Evaluation**:
    - Models are evaluated using R2 Score, Mean Absolute Error (MAE), and Root Mean Squared Error (RMSE).

## 📦 Model Artifacts (`/Models`)

The trained components are saved as pickle/joblib files for use in the production application (FastAPI server).

- **Encoders:**
  - `le.pkl`: Label Encoder (for decoding predictions back to course names).
  - `mlb_interest.pkl`: MultiLabelizer for Interest column.
  - `mlb_skills.pkl`: MultiLabelizer for Skills column.
  - `sc.sav`: StandardScaler for normalizing input data.
- **Models:**
  - `rf.sav`: The trained Random Forest model.
  - `random_forest_grid2.sav`: The best estimator from Grid Search.
  - `lr.sav`: Linear Regression model (baseline).

## 🚀 Usage

To use these models in the backend (FastAPI):

1.  Load the necessary artifacts using `joblib`.
2.  Preprocess the input data (User profile) using the loaded `le`, `mlb`, and `sc` objects.
3.  Pass the processed feature vector to the loaded model (`rf.sav`) to get a prediction.
4.  Decode the prediction using the inverse transform of the Label Encoder if classification was performed (note: the notebook uses Regressors, so output might need nearest-neighbor mapping or thresholding if it was treated as a regression problem on encoded labels).

## 🛠️ Requirements

To run the notebook or retraining scripts, install the following:

```bash
pip install pandas numpy matplotlib seaborn scikit-learn klib joblib
```
