# FlyRank Assignment 4 – Authentication API

## About the Project

This project is made using Python and FastAPI. It uses Supabase for user authentication.

Users can create an account, log in, and log out. Some API endpoints need a valid access token, while public endpoints can be used without logging in.

## Technologies Used

- Python
- FastAPI
- Supabase
- Pydantic
- Uvicorn
- Python-dotenv

## Project Features

- User signup
- User login
- User logout
- Access-token verification
- Protected profile
- Protected dashboard
- Public information
- API testing with Swagger UI

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/auth/signup` | Create a new account |
| POST | `/auth/login` | Log in to an account |
| POST | `/auth/logout` | Log out |
| GET | `/protected/profile` | Get user details |
| GET | `/protected/dashboard` | Open the protected dashboard |
| GET | `/public/info` | Get public information |

## How to Run the Project

### 1. Download the Project

Clone the GitHub repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd flyrank-auth-assignment4
```

### 2. Create a Virtual Environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install the Required Packages

```bash
pip install fastapi "uvicorn[standard]" supabase python-dotenv email-validator
```

### 4. Set Up Supabase

Create a `.env` file and add your Supabase project URL and publishable or anon key.

Use `.env.example` as a guide. Do not upload your real `.env` file to GitHub.

### 5. Start the Server

```bash
uvicorn main:app --reload
```

### 6. Open Swagger UI

Open this address in your browser:

`http://127.0.0.1:8000/docs`

You can use Swagger UI to test the API endpoints.

## Testing Results

I tested the API using Swagger UI.

- Login returned `200 OK`.
- Protected profile returned `200 OK` with a valid token.
- Protected dashboard returned `200 OK`.
- Public information returned `200 OK`.
- Logout returned `204 No Content`.
- After logout, the protected profile returned `401 Unauthorized`.

## Security

- Supabase settings are stored in environment variables.
- The `.env` file should not be uploaded to GitHub.
- Protected endpoints require a valid access token.

## Author

FlyRank Backend AI Engineering – Assignment 4