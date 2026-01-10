# Contributing to Skill Compass AI

First off, thanks for taking the time to contribute! 🎉

## Getting Started

### 1. Prerequisites

- Node.js (v18+)
- Python (3.10+)
- Flutter SDK
- PostgreSQL

### 2. Setup

We have streamlined the setup process with root-level scripts.

```bash
# Install dependencies for ALL services (Server, ML, Flutter)
npm run install:all

# VS Code Users:
# Please accept the "Recommended Extensions" popup when opening the project.
# We have Prettier, Python, and Flutter extensions pre-configured.
```

## 🛠 Development Workflow

### Running the Stack

To run the Backend and ML Service concurrently:

```bash
npm run dev
```

- Server: http://localhost:5003
- ML Service: http://localhost:8000

To run the Flutter Client:

```bash
npm run dev:client
```

### Git Hooks

This project uses **Husky** to strict quality control:

- **Pre-commit**: Automatically formats code (Prettier, Black, Dart Format).
- **Commit-msg**: Enforces [Conventional Commits](https://www.conventionalcommits.org/).

**Valid Commit Messages:**

- `feat: add login screen`
- `fix: crash on profile update`
- `chore: update npm dependencies`

**Invalid:**

- `fixed bug`
- `added stuff`

## Branches

- **main**: Production-ready code.
- **feature/your-feature-name**: For new features.
- **fix/bug-name**: For bug fixes.

## Pull Request Process

1. Update usage documentation if needed.
2. The PR description should clearly state what the change does.
3. Ensure the CI checks pass (Linting, Tests).
