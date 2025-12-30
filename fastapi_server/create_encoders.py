import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
import joblib

# Load the training data
df = pd.read_csv(r'd:\Projects\Project\research\career_recommender.csv')

# Rename columns
df = df.rename(columns={
    'What is your gender?': 'gender',
    'What are your interests?': 'interest',
    'What are your skills ? (Select multiple if necessary)': 'skills'
})

# Process interests and skills exactly as in training
df['interest'] = df['interest'].apply(lambda x: [i.lower().strip() for i in str(x).replace(';', ',').split(',')])
df['skills'] = df['skills'].apply(lambda x: [s.lower().strip() for s in str(x).replace(';', ',').split(',')])

# Fit encoders
mlb_interest = MultiLabelBinarizer()
mlb_skills = MultiLabelBinarizer()

mlb_interest.fit(df['interest'])
mlb_skills.fit(df['skills'])

print(f"Interest features: {len(mlb_interest.classes_)}")
print(f"Skill features: {len(mlb_skills.classes_)}")
print(f"Total with gender+grades: {2 + len(mlb_interest.classes_) + len(mlb_skills.classes_)}")

# Save the encoders to the correct location (research/Models/)
joblib.dump(mlb_interest, r'd:\Projects\Project\research\Models\mlb_interest.pkl')
joblib.dump(mlb_skills, r'd:\Projects\Project\research\Models\mlb_skills.pkl')

print("\n✓ Saved correct encoders to research/Models/")
print(f"  - mlb_interest.pkl ({len(mlb_interest.classes_)} features)")
print(f"  - mlb_skills.pkl ({len(mlb_skills.classes_)} features)")
