#!/usr/bin/env python
# coding: utf-8

# In[84]:


import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


# In[85]:


#loading the dataset
df_test = pd.read_csv(r'career_recommender.csv')


# In[86]:


df_test.head()


# ## Checking for Null Values and filling them

# In[87]:


df_test.isnull().sum()


# In[88]:


df_test['What are your skills ? (Select multiple if necessary)'].mode()


# In[89]:


df_test['What are your skills ? (Select multiple if necessary)'].fillna(df_test['What are your skills ? (Select multiple if necessary)'].mode()[0],inplace=True)


# In[90]:


df_test['If yes, then what is/was your first Job title in your current field of work? If not applicable, write NA.               '].mode()


# In[91]:


df_test['If yes, then what is/was your first Job title in your current field of work? If not applicable, write NA.               '].fillna(df_test['If yes, then what is/was your first Job title in your current field of work? If not applicable, write NA.               '].mode()[0],inplace=True)


# In[92]:


df_test['Have you done masters after undergraduation? If yes, mention your field of masters.(Eg; Masters in Mathematics)'].mode()


# In[93]:


df_test['Have you done masters after undergraduation? If yes, mention your field of masters.(Eg; Masters in Mathematics)'].fillna(df_test['Have you done masters after undergraduation? If yes, mention your field of masters.(Eg; Masters in Mathematics)'].mode()[0],inplace=True)


# In[94]:


df_test.isnull().sum()


# In[ ]:





# In[ ]:





# In[95]:


# Create a dictionary of the old column names and new column names
column_dict= {'What is your name?': 'Name',
               'What is your gender?': 'Gender',
               'What was your course in UG?': 'Course',
               'What is your UG specialization? Major Subject (Eg; Mathematics)': 'Specialization',
               'What are your interests?': 'Interest',
               'What are your skills ? (Select multiple if necessary)': 'Skills',
               'What was the average CGPA or Percentage obtained in under graduation?': 'Grades',
               'Did you do any certification courses additionally?': 'Any_Add_Cert_Courses',
               'If yes, please specify your certificate course title.': 'Cert_Courses_Desc',
               'Are you working?': 'Working?',
               'If yes, then what is/was your first Job title in your current field of work? If not applicable, write NA.               ': 'Job_Title',
               'Have you done masters after undergraduation? If yes, mention your field of masters.(Eg; Masters in Mathematics)': 'Masters_Desc'}

# Rename the columns using the dictionary
df_test = df_test.rename(columns=column_dict)


# In[96]:


print(df_test.columns)


# In[ ]:





# In[97]:


df_test.drop(['Name', 'Specialization', 'Any_Add_Cert_Courses', 'Cert_Courses_Desc', 'Working?', 'Job_Title', 'Masters_Desc'], axis=1, inplace=True)


# In[98]:


print(df_test.columns)


# In[ ]:





# ## Data Cleaning using Klib Library

# In[99]:


# CELL 1: Import required libraries
get_ipython().system('pip install klib')
import klib


# In[100]:


klib.convert_datatypes(df_test) # converts existing to more efficient dtypes, also called inside data_cleaning()


# In[101]:


klib.clean_column_names(df_test) # cleans and standardizes column names, also called inside data_cleaning()


# In[102]:


klib.data_cleaning(df_test) # performs datacleaning (drop duplicates & empty rows/cols, adjust dtypes,...)


# In[103]:


klib.mv_col_handling(df_test)


# In[ ]:





# In[ ]:





# In[ ]:





# ## Preprocessing Task before Model Building¶
# Label Encoding

# In[104]:


from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()


# In[105]:


df_test['gender'] = le.fit_transform(df_test['gender'])
df_test['course'] = le.fit_transform(df_test['course'])


# In[ ]:





# In[106]:


# convert input strings to lower case,remove any leading/trailing spaces, replace any semicolons by comms and split the input strings by comma to create a list
df_test['interest'] = df_test['interest'].apply(lambda x: [interest.lower().strip() for interest in x.replace(';', ',').split(',')])
df_test['skills'] = df_test['skills'].apply(lambda x: [skill.lower().strip() for skill in x.replace(';', ',').split(',')])


# In[ ]:





# Multi-Hot Encoding

# In[107]:


from sklearn.preprocessing import MultiLabelBinarizer
mlb = MultiLabelBinarizer()


# In[108]:


# create a separate instance of MultiLabelBinarizer for each column
mlb_interest = MultiLabelBinarizer()
mlb_skills = MultiLabelBinarizer()

# perform multihot encoding on each column separately
encoded_interest = mlb_interest.fit_transform(df_test['interest'])
encoded_skills = mlb_skills.fit_transform(df_test['skills'])

# concatenate the encoded arrays with the original dataframe
df_test = pd.concat([df_test, pd.DataFrame(encoded_interest, columns=mlb_interest.classes_), pd.DataFrame(encoded_skills, columns=mlb_skills.classes_)], axis=1)

# remove the original columns from the encoded dataframe
df_test.drop(['interest', 'skills'], axis=1, inplace=True)


# In[ ]:





# In[109]:


df_test.shape


# In[110]:


df_test


# In[ ]:





# In[111]:


import joblib


# In[112]:


# Save label encoders
joblib.dump(le,r'D:\Projects\Project\research\Models\le.pkl')
joblib.dump(mlb,r'D:\Projects\Project\research\Models\mlb.pkl')


# In[ ]:





# In[113]:


# Check the correlation between columns
corr_matrix = df_test.corr()

# Display the correlation matrix
print(corr_matrix)


# In[ ]:





# In[ ]:





# ## Splitting our data into train and test

# In[114]:


X=df_test.drop('course',axis=1)


# In[115]:


Y=df_test['course']


# In[116]:


from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X,Y, random_state=101, test_size=0.2)


# In[ ]:





# In[ ]:





# ## Standarization

# In[117]:


X.describe()


# In[118]:


from sklearn.preprocessing import StandardScaler
sc= StandardScaler()


# In[119]:


X_train_std= sc.fit_transform(X_train)


# In[120]:


X_test_std= sc.transform(X_test)


# In[121]:


X_train_std


# In[122]:


X_test_std


# In[123]:


Y_train


# In[124]:


Y_test


# In[ ]:





# In[125]:


joblib.dump(sc,r'D:\Projects\Project\research\Models\sc.sav')


# In[ ]:





# ## Model Building
#   and saving the model(s)

# In[126]:


from sklearn.linear_model import LinearRegression
lr= LinearRegression()


# In[127]:


lr.fit(X_train_std,Y_train)


# In[128]:


X_test.head()


# In[129]:


Y_pred_lr=lr.predict(X_test_std)


# In[130]:


from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error


# In[131]:


print(r2_score(Y_test,Y_pred_lr))
print(mean_absolute_error(Y_test,Y_pred_lr))
print(np.sqrt(mean_squared_error(Y_test,Y_pred_lr)))


# In[ ]:





# In[ ]:





# In[132]:


joblib.dump(lr,r'D:\Projects\Project\research\Models\lr.sav')


# In[ ]:





# In[ ]:





# In[133]:


from sklearn.ensemble import RandomForestRegressor
rf= RandomForestRegressor()


# In[134]:


rf.fit(X_train,Y_train)


# In[135]:


Y_pred_rf= rf.predict(X_test)


# In[136]:


print(r2_score(Y_test,Y_pred_rf))
print(mean_absolute_error(Y_test,Y_pred_rf))
print(np.sqrt(mean_squared_error(Y_test,Y_pred_rf)))


# In[137]:


joblib.dump(rf,r'D:\Projects\Project\research\Models\rf.sav')


# In[ ]:





# ## Hyper Parameter Tuning

# In[138]:


from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.model_selection import GridSearchCV

# define models and parameters
model = RandomForestRegressor()
n_estimators = [10, 100, 1000]
max_depth=range(1,31)
min_samples_leaf=np.linspace(0.1, 1.0)
max_features=["auto", "sqrt", "log2"]
min_samples_split=np.linspace(0.1, 1.0, 10)

# define grid search
grid = dict(n_estimators=n_estimators, max_depth=max_depth)

#cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=3, random_state=101)

grid_search_forest = GridSearchCV(estimator=model, param_grid=grid, n_jobs=-1, 
                           scoring='r2',error_score=0,verbose=2,cv=2)

grid_search_forest.fit(X_train_std, Y_train)

# summarize results
print(f"Best: {grid_search_forest.best_score_:.3f} using {grid_search_forest.best_params_}")
means = grid_search_forest.cv_results_['mean_test_score']
stds = grid_search_forest.cv_results_['std_test_score']
params = grid_search_forest.cv_results_['params']

for mean, stdev, param in zip(means, stds, params):
    print(f"{mean:.3f} ({stdev:.3f}) with: {param}")


# In[139]:


grid_search_forest.best_params_


# In[140]:


grid_search_forest.best_score_


# In[141]:


Y_pred_rf_grid=grid_search_forest.predict(X_test_std)


# In[ ]:





# In[ ]:





# ## Save your model

# In[142]:


#import joblib


# In[ ]:


joblib.dump(grid_search_forest,r'D:\Projects\Project\research\Models\random_forest_grid2.sav')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# # YOU MAY NEED THIS DURING DEPLOYMENT
Interests

Cloud computing
Technology
Understand human behaviour
Sales/Marketing
Trading
Home interior design
Research
Teaching
Understand human body
Content Writing
Govt. Job
Service
Infrastructure
Financial Analysis
Take risk for Profits
Entrepreneurship
Digital marketing
Market research
Agriculture
Construction Management
Data analytics
Data scientist
Industries
Information Technology
News Coverage
Social Justice
Supply Chain Analysis
Game industry
Design
Web Designing
Web development
Social causes
Blockchain
Machine Learning
Excel
Sports Industry
Product Life cycle Management
SAP Consultant in MM
Project Management
Navy Defence related
Oil and Gas
BioTechnology
Software developer
Hospitality
Salesforce Admin
Social media marketing
Software Job
IT
Urban Planning
Data entry or telecalling work
Mobile App Development
Geography
Geology
Statistical Programmer
Software Engineering
Gardening
Operations
Cyber Security
Application Development
Higher Studies
Retailer
Litigation & Legal service<label for="interest">Interest:</label>
<input type="text" id="interest" name="interest" list="interest-list">

<datalist id="interest-list">
  <option value="Cloud computing">
  <option value="Technology">
  <option value="Understand human behaviour">
  <option value="Sales/Marketing">
  <option value="Trading">
  <option value="Home interior design">
  <option value="Research">
  <option value="Teaching">
  <option value="Understand human body">
  <option value="Content Writing">
  <option value="Govt. Job">
  <option value="Service">
  <option value="Infrastructure">
  <option value="Financial Analysis">
  <option value="Take risk for Profits">
  <option value="Entrepreneurship">
  <option value="Digital marketing">
  <option value="Market research">
  <option value="Agriculture">
  <option value="Construction Management">
  <option value="Data analytics">
  <option value="Data scientist">
  <option value="Industries">
  <option value="Information Technology">
  <option value="News Coverage">
  <option value="Social Justice">
  <option value="Supply Chain Analysis">
  <option value="Game industry">
  <option value="Design">
  <option value="Web Designing">
  <option value="Web development">
  <option value="Social causes">
  <option value="Blockchain">
  <option value="Machine Learning">
  <option value="Excel">
  <option value="Sports Industry">
  <option value="Product Life cycle Management">
  <option value="SAP Consultant in MM">
  <option value="Project Management">
  <option value="Navy Defence related">
  <option value="Oil and Gas">
  <option value="BioTechnology">
  <option value="Software developer">
  <option value="Hospitality">
  <option value="Salesforce Admin">
  <option value="Social media marketing">
  <option value="Software Job">
  <option value="IT">
  <option value="Urban Planning">
  <option value="Data entry or telecalling work">
  <option value="Mobile App Development">
  <option value="Geography">
  <option value="Geology">
  <option value="Statistical Programmer">
  <option value="Software Engineering">
  <option value="Gardening">
  <option value="Operations">
  <option value="Cyber Security">
  <option value="Application Development">
  <option value="Higher Studies">
  <option value="Retailer">
  <option value="Litigation & Legal service">
</datalist>Skills

Python
SQL
Java
Critical Thinking
Analytic Thinking
Programming
Work under Pressure
Logical Skills
Problem Solving skills
People management
Communication skills
Accounting Skills
PLC Allen Bradley
PLC Ladder Logic
LabVIEW
Business Analysis
End-to-End Project Management
Cross-functional Team Leadership
Requirements Gathering
Lean Six Sigma
Lean six sigma blackbelt
Productivity Improvement
C
HTML
Active Listening
Gathering Information
Artistic/Creative Skills
Leadership
Editing
Writing skills
Medical knowledge
HR
Teaching
Cost Accounting
Team work
Tableau
Data Visualization skills( Power Bi/ Tableau )
Machine Learning skills
Artificial Intelligence
MATLAB
R
Designing skills
Proeficiency in Software like STAAD PRO, ETABS
Hardware skills
Product knowledge
Risk management skills
CAD/CAE(autocad/catia/ansys/proE/SeimensNX)
Finance related skills
Negotiation skills
Mass Communication
Sales
Interpersonal skills
Wealth Management
Financial Analysis
Financial Modeling
Marketing Strategy
Financial Services
Design and analysis of automobile components
Vehicle maintenance and reconditioning
Design for manufacturer and assemble
Creativity Skills
Excel
Teamwork
Time Management
Company Secretarial Work
Legal Compliance
Interpersonal Communication
Companies Act
Indirect Taxation
Cloud Computing
Reporting
Observation Skills
Subject Knowledge
Business Knowledge
Market Study
Civil & Criminal Law
Social Media Marketing
Bootstrap
Node.js
Angular
JIRA
TRELLO
Jquery
Javascript
Ajax
PHP

Codeignitor
Loopback
Hospitality
Polymerase Chain Reaction (PCR)
Life Sciences
protein purification
protein chemistry
Protein Assays
Protein Electrophoresis
Protein Chromatography
Western Blotting
Protein Structure Prediction
Protein Kinases
protein characterization
protein engineering
Phytochemistry
Metabolomics
DNA
Biochemistry
Bioinformatics
Cell Culture
STAAD PRO
ETABS
Data science
SAP
.NET Framework
Transact
Technical machine fitter
C#
Good communication skills
Client management
Business Analytics
Risk Analytics
SAS
Marketing Management
Market Research
Business Strategy
Commercial Banking
Portfolio Management
Supply Chain Management
Business Process Reengineering
Consumer Behaviour
Long-term Customer Relationships
Retail Marketing
Financial Accounting
credit risk modeling
Security Analysis
Working Capital Management
Strategic Marketing
Investment Banking
Structured Finance
Building Rapport<label for="skills">Interest:</label> <input type="text" id="skills" name="skills" list="skills-list">  
<datalist id="skills-list">
  <option value="Python">
  <option value="SQL">
  <option value="Java">
  <option value="Critical Thinking">
  <option value="Analytic Thinking">
  <option value="Programming">
  <option value="Work under Pressure">
  <option value="Logical Skills">
  <option value="Problem Solving skills">
  <option value="People management">
  <option value="Communication skills">
  <option value="Accounting Skills">
  <option value="PLC Allen Bradley">
  <option value="PLC Ladder Logic">
  <option value="LabVIEW">
  <option value="Business Analysis">
  <option value="End-to-End Project Management">
  <option value="Cross-functional Team Leadership">
  <option value="Requirements Gathering">
  <option value="Lean Six Sigma">
  <option value="Lean six sigma blackbelt">
  <option value="Productivity Improvement">
  <option value="C">
  <option value="HTML">
  <option value="Active Listening">
  <option value="Gathering Information">
  <option value="Artistic/Creative Skills">
  <option value="Leadership">
  <option value="Editing">
  <option value="Writing skills">
  <option value="Medical knowledge">
  <option value="HR">
  <option value="Teaching">
  <option value="Cost Accounting">
  <option value="Team work">
  <option value="Tableau">
  <option value="Data Visualization skills( Power Bi/ Tableau )">
  <option value="Machine Learning skills">
  <option value="Artificial Intelligence">
  <option value="MATLAB">
  <option value="R">
  <option value="Designing skills">
  <option value="Proeficiency in Software like STAAD PRO, ETABS">
  <option value="Hardware skills">
  <option value="Product knowledge">
  <option value="Risk management skills">
  <option value="CAD/CAE(autocad/catia/ansys/proE/SeimensNX)">
  <option value="Finance related skills">
  <option value="Negotiation skills">
  <option value="Mass Communication">
  <option value="Sales">
  <option value="Interpersonal skills">
  <option value="Wealth Management">
  <option value="Financial Analysis">
  <option value="Financial Modeling">
  <option value="Marketing Strategy">
  <option value="Financial Services">
  <option value="Design and analysis of automobile components">
  <option value="Vehicle maintenance and reconditioning">
  <option value="Design for manufacturer and assemble">
  <option value="Creativity Skills">
  <option value="Excel">
  <option value="Teamwork">
  <option value="Time Management">   
  <option value="Company Secretarial Work">   
  <option value="Legal Compliance">   
  <option value="Interpersonal Communication">   
  <option value="Companies Act">   
  <option value="Indirect Taxation">   
  <option value="Cloud Computing">   
  <option value="Reporting">   
  <option value="Observation Skills">   
  <option value="Subject Knowledge">   
  <option value="Business Knowledge">   
  <option value="Market Study">   
  <option value="Civil & Criminal Law">   
  <option value="Social Media Marketing">   
  <option value="Bootstrap">   
  <option value="Node.js">   
  <option value="Angular">   
  <option value="JIRA">   
  <option value="TRELLO">   
  <option value="Jquery">   
  <option value="Javascript">   
  <option value="Ajax">   
  <option value="PHP">  
<option value="Codeignitor">
<option value="Loopback">
<option value="Hospitality">
<option value="Polymerase Chain Reaction (PCR)">
<option value="Life Sciences">
<option value="Protein Purification">
<option value="Protein Chemistry">
<option value="Protein Assays">
<option value="Protein Electrophoresis">
<option value="Protein Chromatography">
<option value="Western Blotting">
<option value="Protein Structure Prediction">
<option value="Protein Kinases">
<option value="Protein Characterization">
<option value="Protein Engineering">
<option value="Phytochemistry">
<option value="Metabolomics">
<option value="DNA">
<option value="Biochemistry">
<option value="Bioinformatics">
<option value="Cell Culture">
<option value="STAAD PRO">
<option value="ETABS">
<option value="Data Science">
<option value="SAP">
<option value=".NET Framework">
<option value="Transact">
<option value="Technical Machine Fitter">
<option value="C#">
<option value="Good Communication Skills">
<option value="Client Management">
<option value="Business Analytics">
<option value="Risk Analytics">
<option value="SAS">
<option value="Marketing Management">
<option value="Market Research">
<option value="Business Strategy">
<option value="Commercial Banking">
<option value="Portfolio Management">
<option value="Supply Chain Management">
<option value="Business Process Reengineering">
<option value="Consumer Behaviour">
<option value="Long-term Customer Relationships">
<option value="Retail Marketing">
<option value="Financial Accounting">
<option value="Credit Risk Modeling">
<option value="Security Analysis">
<option value="Working Capital Management">
<option value="Strategic Marketing">
  <option value="Investment Banking">
  <option value="Structured Finance">
  <option value="Building Rapport">
</datalist>