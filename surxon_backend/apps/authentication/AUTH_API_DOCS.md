# Authentication API Documentation

This document describes the custom user authentication system implemented with JWT tokens.

## Features

- Custom User model with phone number as unique identifier
- Uzbekistan phone number validation
- JWT-based authentication
- Registration, Login, Logout, and Token Refresh APIs

## User Model Fields

- `username`: User's display name
- `full_name`: Full name (optional)
- `phone_number`: Uzbekistan phone number (unique identifier)

## Phone Number Format

Phone numbers must follow the Uzbekistan standard:
- Format: `+998XXXXXXXXX` or `998XXXXXXXXX`
- Valid operator codes: 90, 91, 93, 94, 95, 97, 98, 99, 33, 71, 77, 88
- Examples: `+998901234567`, `998911234567`

## API Endpoints

### 1. Register
**POST** `/api/auth/register/`

```json
{
    "username": "testuser",
    "full_name": "Test User",
    "phone_number": "+998901234567",
    "password": "testpassword123",
    "password_confirm": "testpassword123"
}
```

**Response:**
```json
{
    "message": "User registered successfully",
    "user": {
        "id": 1,
        "username": "testuser",
        "full_name": "Test User",
        "phone_number": "+998901234567",
        "date_joined": "2025-12-08T06:24:55.624297Z"
    },
    "tokens": {
        "refresh": "...",
        "access": "..."
    }
}
```

### 2. Login
**POST** `/api/auth/login/`

```json
{
    "phone_number": "+998901234567",
    "password": "testpassword123"
}
```

**Response:**
```json
{
    "message": "Login successful",
    "user": {...},
    "tokens": {
        "refresh": "...",
        "access": "..."
    }
}
```

### 3. Refresh Token
**POST** `/api/auth/refresh/`

```json
{
    "refresh": "refresh_token_here"
}
```

**Response:**
```json
{
    "message": "Token refreshed successfully",
    "tokens": {
        "access": "new_access_token",
        "refresh": "new_refresh_token"
    }
}
```

### 4. Logout
**POST** `/api/auth/logout/`
**Headers:** `Authorization: Bearer access_token`

```json
{
    "refresh": "refresh_token_here"
}
```

**Response:**
```json
{
    "message": "Logout successful"
}
```

## Authentication

For protected endpoints, include the access token in the Authorization header:
```
Authorization: Bearer your_access_token_here
```

## Token Configuration

- Access token lifetime: 60 minutes
- Refresh token lifetime: 7 days
- Refresh tokens are rotated on each refresh
- Tokens are blacklisted after logout

## Running the Server

```bash
cd surxon_backend
source ../venv/bin/activate
python manage.py runserver
```

## Admin Access

A superuser has been created:
- Phone: `+998991234567`
- Password: `admin123`

Access admin at: `http://localhost:8000/admin/`