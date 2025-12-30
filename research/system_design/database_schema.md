# Database Schema

## 1. Overview

This document outlines the proposed database schema for the learning application. The schema is designed to be flexible and scalable to support the application's features.

## 2. ERD Diagram

```mermaid
erDiagram
    USER ||--o{ USER_PROFILE : has
    USER ||--o{ USER_GOAL : has
    USER ||--o{ USER_ACHIEVEMENT : has
    USER ||--o{ USER_ENROLLMENT : has
    USER_ENROLLMENT ||--|{ COURSE : enrolls
    COURSE ||--o{ MODULE : has
    MODULE ||--o{ CONTENT : has
    CONTENT ||--o{ QUIZ : has
    USER ||--o{ QUIZ_ATTEMPT : attempts

    USER {
        int user_id PK
        string username
        string password_hash
        string email
        string role
    }

    USER_PROFILE {
        int user_profile_id PK
        int user_id FK
        int age
        string interests
        string iq_score
    }

    USER_GOAL {
        int user_goal_id PK
        int user_id FK
        string goal_description
        date target_date
        string status
    }

    USER_ACHIEVEMENT {
        int user_achievement_id PK
        int user_id FK
        string achievement_description
        date date_achieved
    }

    COURSE {
        int course_id PK
        string title
        string description
        int instructor_id FK
    }

    USER_ENROLLMENT {
        int enrollment_id PK
        int user_id FK
        int course_id FK
        date enrollment_date
    }

    MODULE {
        int module_id PK
        int course_id FK
        string title
    }

    CONTENT {
        int content_id PK
        int module_id FK
        string title
        string type
        string url
    }

    QUIZ {
        int quiz_id PK
        int content_id FK
        string title
    }

    QUIZ_ATTEMPT {
        int attempt_id PK
        int user_id FK
        int quiz_id FK
        int score
        timestamp attempted_at
    }
```

## 3. Table Descriptions

*   **USER:** Stores user account information.
*   **USER_PROFILE:** Stores additional information about the user, such as age, interests, and IQ.
*   **USER_GOAL:** Stores user-defined learning goals.
*   **USER_ACHIEVEMENT:** Stores user achievements and badges.
*   **COURSE:** Stores information about courses.
*   **USER_ENROLLMENT:** Stores information about user enrollments in courses.
*   **MODULE:** Stores information about modules within a course.
*   **CONTENT:** Stores information about learning content within a module.
*   **QUIZ:** Stores information about quizzes.
*   **QUIZ_ATTEMPT:** Stores user attempts at quizzes.
