# 🌐 Backend API Server

The primary backend service for the Skill Compass platform, serving as the API Gateway and business logic handler.

## 1️⃣ Overview

**Purpose**: Manages user authentication, data persistence, and coordinates communication between the Client (Flutter) and the AI/ML Service (FastAPI).  
**Role**: It is the central hub. Clients only talk to this server; they do not access the Database or ML services directly.

## 2️⃣ Tech Stack

*   **Runtime**: Node.js
*   **Language**: TypeScript
*   **Framework**: Express.js
*   **Database**: PostgreSQL
*   **ORM**: Prisma
*   **Authentication**: JWT (JSON Web Tokens) & Bcrypt
*   **File Handling**: Multer (Uploads), Sharp/Jimp (Image Processing)
*   **Validation**: Joi
*   **Testing**: None currently integrated.

## 3️⃣ Folder Structure

```
server/
├── src/
│   ├── config/          # Database & App configuration
│   ├── controllers/     # Request handlers (Auth, CLIP proxy)
│   ├── middleware/      # Auth checks, error handling, logging
│   ├── routes/          # API route definitions
│   │   ├── api/         # V1 routes (auth, clip, users)
│   ├── services/        # Business logic abstraction
│   ├── models/          # (Mostly handled by Prisma schemas)
│   └── app.ts           # Express app setup
├── prisma/              # Database schema & migrations
├── .env.example         # Environment variables template
└── index.ts             # Server entry point
```

## 4️⃣ Current Features (Implemented)

*   **User Authentication**: Register/Login endpoints with JWT issuance.
*   **Secure Password Storage**: Hashing using Bcrypt.
*   **Proxy to ML Service**: Receives file uploads/requests for Image Comparison (CLIP) and securely forwards them to the Python FastAPI server.
*   **Request Logging**: using Morgan.
*   **Global Error Handling**: Centralized error middleware.

## 5️⃣ Partially Implemented / In Progress

*   **User Profile Management**: Routes exist but basic CRUD is minimal.
*   **Authorization Levels**: Role-based access control (Admin vs User) is scaffolding.

## 6️⃣ Environment Variables

Create a `.env` file in `server/` based on `.env.example`:

| Key | Description | Default |
| :--- | :--- | :--- |
| `PORT` | API Server Port | `5003` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://...` |
| `JWT_SECRET` | Secret key for signing tokens | (Set a strong secret) |
| `FASTAPI_URL` | URL of the running Python ML service | `http://localhost:8000` |
| `NODE_ENV` | Environment (development/production) | `development` |

## 7️⃣ How to Run This Service

### Prerequisites
*   Node.js (v18+)
*   PostgreSQL Database running

### Setup
1.  Navigate to the directory:
    ```bash
    cd server
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Configure Environment:
    Copy `.env.example` to `.env` and fill in your DB credentials and JWT secret.
4.  Database Migration:
    ```bash
    npx prisma generate
    # If migrations needed:
    # npx prisma migrate dev
    ```

### Start Server
```bash
# Development (with auto-restart)
npm run dev

# Production Build
npm run build
npm start
```
Server runs on `http://localhost:5003`.

## 8️⃣ API / Integration Notes

*   **Auth**: Most endpoints require `Authorization: Bearer <token>` header.
*   **Integration with ML**:
    *   The `POST /api/clip/compare` endpoint accepts `multipart/form-data`.
    *   It temporarily saves files -> sends to FastAPI -> cleans up files -> returns ML result.

## 9️⃣ Known Limitations

*   **File Cleanup**: If the server crashes mid-process, temp files in `uploads/` might remain.