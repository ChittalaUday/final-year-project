# Onboarding API Implementation Guide

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                   Flutter Client                        │
│            (skill_compass_ai)                           │
└──────────────┬──────────────────────────────────────────┘
               │
               │ HTTP/REST
               ▼
┌─────────────────────────────────────────────────────────┐
│              Node.js Backend (Port 5003)                │
│  ┌──────────────────────────────────────────────────┐   │
│  │         API Gateway & Business Logic             │   │
│  │  - Authentication (JWT)                          │   │
│  │  - Request Validation                            │   │
│  │  - Data Orchestration                            │   │
│  └─────────┬────────────────────────┬────────────────┘   │
└────────────┼────────────────────────┼────────────────────┘
             │                        │
             │                        │ HTTP
             │                        ▼
             │            ┌────────────────────────────────┐
             │            │  FastAPI ML Service (8000)     │
             │            │  - Career Prediction           │
             │            │  - Feature Preprocessing        │
             │            │  - Model Inference              │
             │            └────────────────────────────────┘
             │
             │ Prisma ORM
             ▼
┌─────────────────────────────────────────────────────────┐
│                   PostgreSQL Database                    │
└─────────────────────────────────────────────────────────┘
```

---

## API Endpoints Structure

### 1. Authentication APIs

#### POST /api/auth/signup

```typescript
Request Body:
{
  email: string;
  password: string;
  name: string;
  role: "LEARNER" | "INSTRUCTOR" | "INSTITUTION" | "ADMIN";
}

Response:
{
  success: boolean;
  message: string;
  data: {
    user: {
      id: string;
      email: string;
      name: string;
      role: string;
    };
    token: string;
  }
}
```

#### POST /api/auth/login

```typescript
Request Body:
{
  email: string;
  password: string;
}

Response:
{
  success: boolean;
  data: {
    user: User;
    token: string;
    onboardingStatus: OnboardingProgress;
  }
}
```

---

### 2. Onboarding APIs

#### GET /api/onboarding/status

_Check if user has completed onboarding_

```typescript
Headers: { Authorization: "Bearer <token>" }

Response:
{
  success: boolean;
  data: {
    status: "NOT_STARTED" | "IN_PROGRESS" | "COMPLETED";
    currentStep: number;
    totalSteps: number;
    ageGroup?: string;
    completedSteps: {
      roleSelected: boolean;
      ageDetected: boolean;
      interestsCollected: boolean;
      skillsCollected: boolean;
      assessmentComplete: boolean;
      careerRecommended: boolean;
      pathGenerated: boolean;
    }
  }
}
```

#### POST /api/onboarding/age-group

_Detect and save age group_

```typescript
Request Body:
{
  dateOfBirth: string; // ISO date
}

Response:
{
  success: boolean;
  data: {
    ageGroup: "CHILD" | "SCHOOL" | "COLLEGE" | "GRADUATE" | "PROFESSIONAL";
    nextStep: string;
  }
}
```

#### POST /api/onboarding/learner-profile

_Save learner-specific information based on age group_

```typescript
// For CHILD
Request Body:
{
  parentEmail: string;
  parentConsent: boolean;
}

// For SCHOOL
Request Body:
{
  schoolName: string;
  grade: number;
}

// For COLLEGE
Request Body:
{
  collegeName: string;
  course: string;
  specialization: string;
  currentYear: number;
  cgpaPercentage: number;
}

// For GRADUATE
Request Body:
{
  highestEducation: string;
  yearsOfExperience: number;
  currentJobTitle?: string;
  currentCompany?: string;
  currentIndustry?: string;
}

// For PROFESSIONAL
Request Body:
{
  totalExperience: number;
  currentJobTitle: string;
  currentCompany: string;
  domainShiftIntent: boolean;
  targetDomain?: string;
}

Response:
{
  success: boolean;
  data: {
    profileId: string;
    nextStep: string;
  }
}
```

#### POST /api/onboarding/interests

_Collect user interests_

```typescript
Request Body:
{
  interests: Array<{
    name: string;
    category?: string;
    priority?: number;
  }>;
}

Response:
{
  success: boolean;
  data: {
    interestsCount: number;
    nextStep: string;
  }
}
```

#### POST /api/onboarding/skills

_Collect user skills_

```typescript
Request Body:
{
  skills: Array<{
    name: string;
    category?: string;
    proficiencyLevel?: number; // 1-5
  }>;
}

Response:
{
  success: boolean;
  data: {
    skillsCount: number;
    nextStep: string;
  }
}
```

#### POST /api/onboarding/career-goals

_Set career goals (optional)_

```typescript
Request Body:
{
  goals: Array<{
    goalTitle: string;
    description?: string;
    targetDate?: string;
    priority?: number;
  }>;
}

Response:
{
  success: boolean;
  data: {
    goalsCount: number;
    nextStep: string;
  }
}
```

---

### 3. ML Integration APIs

#### POST /api/ml/predict-career

_Get career recommendations from ML model_

```typescript
Headers: { Authorization: "Bearer <token>" }

Request Body:
{
  userId: string;
  forceRecompute?: boolean; // Optional: force new prediction
}

Backend Flow:
1. Fetch user's learner profile
2. Fetch interests and skills
3. Call FastAPI endpoint: POST http://localhost:8000/predict
4. Process response
5. Save MLPrediction record
6. Create CareerRecommendation records
7. Return formatted response

Response:
{
  success: boolean;
  data: {
    prediction: {
      predictedCareer: string;
      confidence: "HIGH" | "MEDIUM" | "LOW" | "INSUFFICIENT";
      confidenceScore: number;
      alternativeCareers: string[];
      alternativeScores: number[];
    };
    recommendations: Array<{
      careerTitle: string;
      careerDescription: string;
      requiredSkills: string[];
      educationPath: string[];
      industryDemand: string;
      avgSalaryRange: string;
    }>;
  }
}
```

**FastAPI Endpoint:**

```python
# POST http://localhost:8000/predict
{
  "gender": 1,  # encoded
  "course": 14,  # encoded
  "grades": 75.5,
  "interests": ["technology", "programming", "ai"],
  "skills": ["python", "sql", "machine learning"]
}

Response:
{
  "predicted_course": "Computer Science Engineering",
  "confidence_score": 0.87,
  "alternative_courses": [
    "Information Technology",
    "Data Science"
  ],
  "alternative_scores": [0.72, 0.65]
}
```

#### POST /api/ml/accept-recommendation

_Accept a career recommendation_

```typescript
Request Body:
{
  recommendationId: string;
}

Response:
{
  success: boolean;
  data: {
    learningPath: {
      pathId: string;
      pathName: string;
      targetCareer: string;
      estimatedDuration: number;
      modules: Array<{...}>;
    }
  }
}
```

#### POST /api/ml/explore-careers

_Enter exploration mode for multiple careers_

```typescript
Request Body:
{
  careerIds: string[];
}

Response:
{
  success: boolean;
  data: {
    explorationMode: boolean;
    careers: Array<{...}>;
  }
}
```

---

### 4. Learning Path APIs

#### GET /api/learning-path/my-paths

_Get user's learning paths_

```typescript
Response:
{
  success: boolean;
  data: {
    activePaths: Array<{
      pathId: string;
      pathName: string;
      targetCareer: string;
      completionPercent: number;
      modules: Array<{...}>;
    }>;
  }
}
```

#### POST /api/learning-path/generate

_Generate personalized learning path_

```typescript
Request Body:
{
  targetCareer: string;
  userLevel?: "beginner" | "intermediate" | "advanced";
}

Response:
{
  success: boolean;
  data: {
    learningPath: {...}
  }
}
```

#### GET /api/learning-path/:pathId/content

_Get content for a specific path_

```typescript
Response: {
  success: boolean;
  data: {
    modules: Array<{
      moduleId: string;
      title: string;
      content: Array<{
        contentId: string;
        title: string;
        contentType: string;
        contentUrl: string;
        duration: number;
        isCompleted: boolean;
      }>;
    }>;
  }
}
```

---

### 5. Progress Tracking APIs

#### POST /api/progress/update

_Update learning progress_

```typescript
Request Body:
{
  contentId: string;
  progressPercent: number;
  timeSpent: number; // seconds
  isCompleted: boolean;
}

Response:
{
  success: boolean;
  data: {
    progress: {...};
    nextContent?: {...};
  }
}
```

#### GET /api/progress/dashboard

_Get user dashboard data_

```typescript
Response:
{
  success: boolean;
  data: {
    overallProgress: number;
    activePaths: number;
    completedModules: number;
    totalTimeSpent: number;
    achievements: Array<{...}>;
    recentActivity: Array<{...}>;
  }
}
```

---

### 6. Assessment APIs

#### GET /api/assessments/available

_Get available assessments_

```typescript
Query: ?type=APTITUDE|SKILL|KNOWLEDGE

Response:
{
  success: boolean;
  data: {
    assessments: Array<{
      assessmentId: string;
      title: string;
      assessmentType: string;
      duration: number;
      questionCount: number;
    }>;
  }
}
```

#### POST /api/assessments/start

_Start an assessment_

```typescript
Request Body:
{
  assessmentId: string;
}

Response:
{
  success: boolean;
  data: {
    sessionId: string;
    questions: Array<{
      questionId: string;
      questionText: string;
      questionType: string;
      options: string[];
      points: number;
    }>;
  }
}
```

#### POST /api/assessments/submit

_Submit assessment answers_

```typescript
Request Body:
{
  assessmentId: string;
  answers: Array<{
    questionId: string;
    selectedAnswer: string;
  }>;
  timeSpent: number;
}

Response:
{
  success: boolean;
  data: {
    result: {
      score: number;
      maxScore: number;
      percentageScore: number;
      isPassed: boolean;
      aiAnalysis: string;
      strengths: string[];
      weaknesses: string[];
      recommendations: string[];
    }
  }
}
```

---

## Implementation Flow

### Step-by-Step Onboarding Implementation

#### Phase 1: Authentication

1. User signs up → `POST /api/auth/signup`
2. Create user record
3. Create empty `OnboardingProgress` record
4. Return JWT token

#### Phase 2: Age Detection & Profile

1. Client sends date of birth → `POST /api/onboarding/age-group`
2. Backend calculates age group
3. Update `OnboardingProgress.ageDetected = true`
4. Create `LearnerProfile` with age group
5. Return next step based on age group

#### Phase 3: Profile Details Collection

1. Based on age group, show relevant form
2. Submit profile details → `POST /api/onboarding/learner-profile`
3. Update `LearnerProfile` with specific fields
4. Update `OnboardingProgress` step

#### Phase 4: Interests & Skills

1. Collect interests → `POST /api/onboarding/interests`
2. Collect skills → `POST /api/onboarding/skills`
3. Update `OnboardingProgress.interestsCollected = true`
4. Update `OnboardingProgress.skillsCollected = true`

#### Phase 5: Assessment (Optional based on age group)

1. Fetch appropriate assessment → `GET /api/assessments/available`
2. Start assessment → `POST /api/assessments/start`
3. Submit answers → `POST /api/assessments/submit`
4. Update `OnboardingProgress.assessmentComplete = true`

#### Phase 6: ML Prediction

1. Call prediction endpoint → `POST /api/ml/predict-career`
2. Backend prepares data:
   - Encode gender
   - Encode course (if applicable)
   - Format interests array
   - Format skills array
   - Include grades
3. Send to FastAPI: `POST http://localhost:8000/predict`
4. FastAPI returns prediction
5. Backend saves `MLPrediction` record
6. Backend creates `CareerRecommendation` records
7. Update `OnboardingProgress.careerRecommended = true`
8. Return recommendations to client

#### Phase 7: Career Selection

**High Confidence:**

- Show primary recommendation
- User accepts → `POST /api/ml/accept-recommendation`
- Generate learning path automatically

**Low Confidence:**

- Show multiple options
- User selects → `POST /api/ml/explore-careers`
- Allow exploration mode

**Insufficient Data:**

- Request minimal additional inputs
- Re-run prediction
- Or provide generic foundational path

#### Phase 8: Learning Path Generation

1. Based on accepted career → `POST /api/learning-path/generate`
2. Backend creates:
   - `LearningPath` record
   - Multiple `LearningModule` records
   - Associated `Content` records
3. Update `OnboardingProgress.pathGenerated = true`
4. Mark `OnboardingProgress.status = COMPLETED`
5. Return complete learning path

#### Phase 9: Dashboard Navigation

1. User is redirected to dashboard
2. Fetch dashboard data → `GET /api/progress/dashboard`
3. Show personalized learning path
4. Enable progress tracking

---

## FastAPI Integration Details

### Preprocessing Pipeline (Before calling ML model)

```python
# In fastapi_server/app/services/ml_service.py

def preprocess_user_data(user_data):
    # 1. Label Encoding
    gender_encoded = label_encoder.transform([user_data['gender']])[0]
    course_encoded = label_encoder.transform([user_data['course']])[0] if 'course' in user_data else 0

    # 2. Multi-Label Encoding for interests & skills
    interests_encoded = mlb_interests.transform([user_data['interests']])[0]
    skills_encoded = mlb_skills.transform([user_data['skills']])[0]

    # 3. Combine features
    features = np.concatenate([
        [gender_encoded, course_encoded, user_data.get('grades', 0)],
        interests_encoded,
        skills_encoded
    ])

    # 4. Feature Scaling
    features_scaled = scaler.transform([features])

    return features_scaled
```

### Model Inference

```python
def predict_career(features):
    # Load trained model
    model = load_model('random_forest_grid2.sav')

    # Predict
    prediction = model.predict(features)[0]
    confidence_scores = model.predict_proba(features)[0]

    # Get top N predictions
    top_indices = confidence_scores.argsort()[-3:][::-1]
    top_careers = [reverse_label_encoder(idx) for idx in top_indices]
    top_scores = confidence_scores[top_indices]

    return {
        'predicted_career': reverse_label_encoder(prediction),
        'confidence_score': max(confidence_scores),
        'alternative_careers': top_careers[1:],
        'alternative_scores': top_scores[1:].tolist()
    }
```

---

## Database Migration Strategy

### 1. Initial Setup

```bash
cd server
npx prisma generate
npx prisma migrate dev --name init
```

### 2. Seeding Test Data

```typescript
// server/prisma/seed.ts
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
  // Seed interests
  const interests = [
    'Cloud computing',
    'Technology',
    'Understand human behaviour',
    // ... (all interests from notebook)
  ];

  // Seed skills
  const skills = [
    'Python',
    'SQL',
    'Java',
    'Critical Thinking',
    // ... (all skills from notebook)
  ];

  // Create sample assessments
  const aptitudeTest = await prisma.assessment.create({
    data: {
      title: 'General Aptitude Test',
      assessmentType: 'APTITUDE',
      duration: 60,
      questions: {
        create: [
          // Sample questions
        ],
      },
    },
  });
}

main();
```

---

## Error Handling

### Standard Error Response

```typescript
{
  success: false,
  error: {
    code: string;
    message: string;
    details?: any;
  }
}
```

### Common Error Codes

- `AUTH_INVALID_CREDENTIALS`
- `ONBOARDING_INCOMPLETE`
- `ML_PREDICTION_FAILED`
- `INSUFFICIENT_DATA`
- `RESOURCE_NOT_FOUND`
- `VALIDATION_ERROR`

---

## Testing Strategy

### 1. Unit Tests

- Test individual API endpoints
- Mock database calls
- Mock FastAPI calls

### 2. Integration Tests

- Test complete onboarding flow
- Test ML prediction with real model
- Test progress tracking

### 3. E2E Tests

- Full user journey from signup to dashboard
- Multiple age group scenarios
- Different confidence level scenarios

---

## Performance Considerations

1. **Caching**: Cache ML predictions for 24 hours
2. **Pagination**: Implement pagination for content lists
3. **Lazy Loading**: Load modules on demand
4. **Indexing**: Proper database indexes (already in schema)
5. **Connection Pooling**: Configure Prisma connection pool
6. **Rate Limiting**: Implement rate limiting for ML endpoints

---

## Security Best Practices

1. **JWT Expiry**: Set appropriate token expiration
2. **Input Validation**: Validate all inputs with Zod/Joi
3. **SQL Injection**: Prisma ORM handles this
4. **CORS**: Configure properly in production
5. **Environment Variables**: Never commit .env files
6. **API Rate Limiting**: Prevent abuse
7. **Data Encryption**: Encrypt sensitive profile data

---

## Next Steps

1. ✅ Review and approve database schema
2. ✅ Run Prisma migrations
3. ✅ Implement authentication endpoints
4. ✅ Implement onboarding endpoints
5. ✅ Set up FastAPI communication
6. ✅ Create seed data
7. ✅ Test complete flow
8. ✅ Integrate with Flutter client
9. ✅ Deploy to staging
10. ✅ Production deployment
