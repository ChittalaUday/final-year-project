# 🧭 Skill Compass AI Project

A comprehensive AI-driven platform for career recommendation and visual analysis, composed of a modern microservices architecture.

## 🏗 High-Level Architecture

The system is split into three main components:

1.  **Client (`skill_compass_ai/`)**:
    - **Tech**: Flutter (Mobile/Web)
    - **Role**: User Interface
    - **Port**: N/A (Runs on device/browser)
2.  **Backend Server (`server/`)**:
    - **Tech**: Node.js, Express, TypeScript, Prisma
    - **Role**: API Gateway, Auth, Business Logic
    - **Port**: `5003`

3.  **AI/ML Service (`fastapi_server/`)**:
    - **Tech**: Python, FastAPI, PyTorch
    - **Role**: Machine Learning (Career Prediction, CLIP Image Analysis)
    - **Port**: `8000`

### 🔄 Service Interaction Flow

```
[ User (Flutter) ] <---> [ Node.js Gateway (5003) ] <---> [ FastAPI ML (8000) ]
                                      |
                                  [ Database ]
```

## 📁 Repository Structure

- **/server**: Node.js Backend API. [Read more](./server/README.md)
- **/fastapi_server**: Python AI/ML Service. [Read more](./fastapi_server/README.md)
- **/skill_compass_ai**: Flutter Frontend. [Read more](./skill_compass_ai/README.md)
- **/research**: Data Science notebooks, datasets, and raw model training files.

## 🚀 Getting Started

### 1. Prerequisites

Ensure you have the following installed:

- **Node.js** (v18+)
- **Python** (3.10+)
- **PostgreSQL**
- **Flutter SDK**

### 2. Setup Order (Crucial!)

To run the full stack locally, follow this order:

#### Step 1: Install Dependencies

Run this command in the root to install dependencies for Node.js, Python, and Flutter at once:

```bash
npm run install:all
```

#### Step 2: Start Services

You can run the Backend and ML Service concurrently with one command:

```bash
npm run dev
```

#### Step 3: Run the Client

```bash
npm run dev:client
```

### Manual Setup (If preferred)

#### ML Service

```bash
cd fastapi_server
# (Setup venv and install requirements first)
python -m uvicorn app.main:app --reload
```

✅ Verifies on `http://localhost:8000/health`

#### Step 2: Start the Backend Server

Requires Database and ML Service to be ready.

```bash
cd server
# (Setup .env and install dependencies first)
npm run dev
```

✅ Runs on `http://localhost:5003`

#### Step 3: Run the Client

```bash
cd skill_compass_ai
flutter run
```

## ⚠️ Common Developer Mistakes

1.  **Forgot to start FastAPI**: The Node.js server will error out when trying to compare images if port 8000 is not reachable.
2.  **Missing .env**: Each service (`server` and `fastapi_server`) has its own `.env` file. You must configure **BOTH**.
3.  **CORS Issues**: If accessing from a physical device, ensure your backend `.env` allows the specific IP or use `*` for testing.
4.  **Database URL**: Ensure the `DATABASE_URL` in `server/.env` matches your local Postgres credentials.

## 🔮 Future Improvements

- **Docker Compose**: Add a `docker-compose.yml` to orchestrate all 3 services + DB with a single command.
- **Shared Types**: Generate TypeScript interfaces from Pydantic models to ensure type safety across Python and Node.js.

## 🛡️ Git Hooks & Code Quality

This project uses **Husky** to enforce code quality and commit message standards.

### Pre-commit Hooks

The `pre-commit` hook uses **lint-staged** to automatically format code before it is committed:

- **Prettier**: Formats `js`, `ts`, `json`, `md`, `html`, `css`.
- **Dart Format**: Formats `*.dart` files in the Flutter project.
- **Black**: Formats `*.py` files in Python projects.

### Commit Message Linting

We use **Commitlint** with the [Conventional Commits](https://www.conventionalcommits.org/) specification.
All commit messages must follow this format:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Common Examples:**

- `feat: add new career prediction endpoint`
- `fix: resolve cors issue in express server`
- `chore: update dependencies`
- `docs: update readme with setup instructions`
- `refactor: clean up user controller`

If your commit message does not follow this standard, the commit will be rejected.
