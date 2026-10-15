# Healthcare Backend API

A healthcare management backend built using Django REST Framework and PostgreSQL. It provides APIs for user authentication, patient management, doctor management, and patient-doctor assignments.

## Tech Stack

- Python
- Django
- Django REST Framework (DRF)
- PostgreSQL
- Django REST Framework Simple JWT
- Django ORM
- psycopg
- python-dotenv
- dj-database-url

## Features

- User registration and JWT-based login
- Create, retrieve, update, and delete patient records
- Restrict patient records according to user ownership
- Create, view, update, and delete doctor records
- Allow only the creator to update or delete their doctor records
- Assign doctors to patients
- View and remove patient-doctor assignments
- Request validation and error handling
- PostgreSQL database integration using Django ORM
- Environment-based configuration

## Project Setup

### 1. Requirements

Install Python 3.10 or later and PostgreSQL.

### 2. Clone the Repository

```bash
git clone https://github.com/Harshit-bhardwaj1/healthcare-backend.git
cd healthcare-backend
```

### 3. Create and Activate a Virtual Environment

On Windows PowerShell:

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
```

If you already have a virtual environment, activate it instead.

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the project root, in the same directory as `manage.py`.

Add the following configuration:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:YOUR_PORT/healthcare_db
```

Replace `YOUR_PASSWORD` with your PostgreSQL password and `YOUR_PORT` with the port on which PostgreSQL is running.

Create a PostgreSQL database named `healthcare_db` if it does not already exist.

For example, if PostgreSQL runs on port `5000`, use port `5000` in `DATABASE_URL`. If it runs on port `5432`, use port `5432`.

Keep your `.env` file private and do not commit it to GitHub.

### 6. Apply Database Migrations

```bash
python manage.py migrate
```

### 7. Start the Development Server

```bash
python manage.py runserver
```

The application will be available at:

`http://127.0.0.1:8000/`

## Authentication APIs

All patient, doctor, and mapping endpoints require a valid JWT access token.

### Register a User

- **Method:** POST
- **Endpoint:** `/api/auth/register/`

Request body:

```json
{
  "name": "Example User",
  "email": "user@example.com",
  "password": "StrongPass123!"
}
```

### Log In

- **Method:** POST
- **Endpoint:** `/api/auth/login/`

Request body:

```json
{
  "username": "user@example.com",
  "password": "StrongPass123!"
}
```

The response contains an access token and a refresh token.

### Refresh an Access Token

- **Method:** POST
- **Endpoint:** `/api/auth/token/refresh/`

Request body:

```json
{
  "refresh": "YOUR_REFRESH_TOKEN"
}
```

For protected requests, select **Authorization → Bearer Token** in Postman and provide the access token.

Alternatively, use this HTTP header:

```text
Authorization: Bearer YOUR_ACCESS_TOKEN
```

## Patient Management APIs

Patient records are associated with the user who creates them.

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/patients/` | Create a patient |
| GET | `/api/patients/` | List your patients |
| GET | `/api/patients/{id}/` | Retrieve a patient |
| PUT | `/api/patients/{id}/` | Update a patient |
| PATCH | `/api/patients/{id}/` | Partially update a patient |
| DELETE | `/api/patients/{id}/` | Delete a patient |

Example request:

```json
{
  "name": "Aman Sharma",
  "age": 25,
  "gender": "Male",
  "address": "Mathura, Uttar Pradesh",
  "phone": "9876543210"
}
```

## Doctor Management APIs

Authenticated users can view doctor records. Only the creator can update or delete their doctor records.

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/doctors/` | Create a doctor |
| GET | `/api/doctors/` | List all doctors |
| GET | `/api/doctors/{id}/` | Retrieve a doctor |
| PUT | `/api/doctors/{id}/` | Update a doctor |
| PATCH | `/api/doctors/{id}/` | Partially update a doctor |
| DELETE | `/api/doctors/{id}/` | Delete a doctor |

Example request:

```json
{
  "name": "Dr. Neha Gupta",
  "specialization": "Cardiology",
  "email": "doctor@example.com",
  "phone": "9876543210"
}
```

## Patient-Doctor Mapping APIs

Mappings connect patients with doctors. Access to mappings is restricted according to patient ownership.

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/mappings/` | Assign a doctor to a patient |
| GET | `/api/mappings/` | List your patient-doctor mappings |
| GET | `/api/mappings/{patient_id}/` | List assignments for a specific patient |
| DELETE | `/api/mappings/{id}/` | Remove a mapping |

Example request:

```json
{
  "patient": 1,
  "doctor": 1
}
```

Replace the example IDs with actual patient and doctor IDs returned by the API. IDs may differ between databases.

## Authorization and Data Access

- All patient, doctor, and mapping endpoints require authentication.
- Users can access only their own patient records.
- Authenticated users can view doctor records.
- Only the creator can update or delete a doctor record.
- Mapping access follows patient ownership restrictions.
- Requests without valid authentication credentials are rejected.

## Testing with Postman

1. Register a user using `POST /api/auth/register/`.
2. Log in using `POST /api/auth/login/`.
3. Copy the access token from the response.
4. Set **Authorization → Bearer Token** in Postman.
5. Create a patient using `POST /api/patients/`.
6. Create a doctor using `POST /api/doctors/`.
7. Assign the doctor to the patient using `POST /api/mappings/`.
8. Test the available GET, PUT, PATCH, and DELETE endpoints.
9. Register another user and verify patient ownership restrictions.
10. Test missing or invalid tokens, duplicate email registration, and invalid request data.

## Database

The application uses PostgreSQL for persistent storage and Django ORM for database operations. Database connection settings are loaded from environment variables.

## Repository

GitHub: https://github.com/Harshit-bhardwaj1/healthcare-backend

## License

Developed as a healthcare backend assignment project.
