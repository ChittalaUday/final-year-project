# 📡 API Documentation

This directory details the REST API endpoints available in the Node.js Server (`server`).

**Base URL**: `http://localhost:5003/api`

---

## 🔐 Authentication

### `POST /auth/register`

Create a new user account.

- **Body**:
  ```json
  {
    "name": "John Doe",
    "email": "john@example.com",
    "password": "securepassword123",
    "dob": "2000-01-01" // Optional
  }
  ```
- **Response**: `201 Created` with JWT token.

### `POST /auth/login`

Authenticate existing user.

- **Body**:
  ```json
  {
    "email": "john@example.com",
    "password": "securepassword123"
  }
  ```
- **Response**: `200 OK`
  ```json
  {
    "success": true,
    "token": "ey..."
  }
  ```

---

## 🖼️ Image Analysis (CLIP)

### `POST /clip/compare`

Compare two images to see how similar they are. Proxies request to Python ML Service.

- **Headers**: `Authorization: Bearer <token>`
- **Content-Type**: `multipart/form-data`
- **Body**:
  - `image1`: File (Image) [Required]
  - `image2`: File (Image) [Required]
  - `tag`: String (Optional - e.g. "Cat")
- **Response**: `200 OK`
  ```json
  {
    "success": true,
    "data": {
      "similarity": 0.85,
      "text_similarity": 0.12 // if tag provided
    }
  }
  ```

### `GET /clip/info`

Get details about the CLIP model configuration.

- **Response**: `200 OK` with JSON details.

---

## 👤 Users Management

### `GET /users`

List all users (may be restricted to Admin in future).

- **Headers**: `Authorization: Bearer <token>`
- **Response**: `200 OK` - Array of user objects.

### `POST /users`

Create a user (Admin route).

- **Body**: Same as register.

---

## 🔮 Future / Planned APIs

### Career Recommendation

- `POST /career/predict`: Send academic data -> Get career list.
- `GET /career/history`: Get past predictions for logged-in user.

### Profiles

- `GET /profile/me`: Get current user profile.
- `PUT /profile/me`: Update bio, links, avatar.

---

## error Handling

Standard error format:

```json
{
  "success": false,
  "message": "Error description",
  "error": "Detailed error info (if dev mode)"
}
```

- **400**: Bad Request (Validation failed)
- **401**: Unauthorized (Missing/Invalid Token)
- **404**: Not Found
- **500**: Internal Server Error
