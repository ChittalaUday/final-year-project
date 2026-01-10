# 📱 Client / Frontend Application

The mobile/web client cross-platform application for Skill Compass, built with Flutter.

## 1️⃣ Overview

**Purpose**: Provides the user interface for students and users to interact with the Career Recommendation system and Image Analysis tools.  
**Role**: It is the presentation layer that consumes data from the Node.js Backend API.

## 2️⃣ Tech Stack

- **Framework**: Flutter (Dart)
- **Platforms**: Android, iOS, Web, Windows
- **State Management**: (Not yet established, likely Provider/Riverpod planned)
- **Networking**: `http` or `dio` (Planned)

## 3️⃣ Folder Structure

```
skill_compass_ai/
├── lib/
│   └── main.dart        # Entry point of the application
├── android/             # Android native scaffolding
├── ios/                 # iOS native scaffolding
├── web/                 # Web support files
├── pubspec.yaml         # Dependencies and Assets
└── analysis_options.yaml # Linter rules
```

## 4️⃣ Current Features (Implemented)

- **Project Skeleton**: Initial Flutter project structure generated.
- **Basic UI**: Default counter example (currently acting as placeholder).

## 5️⃣ Partially Implemented / In Progress

- **Authentication Screens**: Login/Signup UI integration with Backend.
- **Dashboard**: Main user interface for accessing tools.
- **Image Upload**: functionality to send images to the backend.
- **API Integration**: Connection to `http://localhost:5003` is planned.

## 6️⃣ Environment Variables

- Currently, no `.env` setup in the Flutter app.
- **Future**: API Base URL will likely be configured in a `consts.dart` or `.env` file depending on the build flavor (Dev/Prod).

## 7️⃣ How to Run This Service

### Prerequisites

- Flutter SDK (Latest Stable)
- Android Studio / VS Code with Flutter extensions
- Active Emulator or Physical Device

### Setup

1.  Navigate to the directory:
    ```bash
    cd skill_compass_ai
    ```
2.  Install dependencies:
    ```bash
    flutter pub get
    ```

### Start App

```bash
# Run on connected device/emulator
flutter run
```

## 8️⃣ API / Integration Notes

- **Target Backend**: This app is designed to communicate with the Node.js Server (`server`) on port `5003`.
- **Planned Flow**:
  1.  User Logs in (sends creds to Node.js).
  2.  Token saved securely on device.
  3.  User uploads image -> App sends multipart req to Node.js.

## 9️⃣ Known Limitations

- **Connectivity**: On Android Emulator, `localhost` refers to the device itself. You must use `10.0.2.2` to access the Node.js server running on the host machine.
