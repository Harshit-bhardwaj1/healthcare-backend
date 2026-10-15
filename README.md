# Healthcare Backend API

A healthcare management backend built using Django REST Framework and PostgreSQL. It provides APIs for user authentication, patient management, doctor management, and patient-doctor assignments.

## Tech Stack

- Python
- Django
- Django REST Framework
- PostgreSQL
- Django REST Framework Simple JWT
- psycopg
- python-dotenv
- dj-database-url

## Features

- User registration and JWT-based login
- Create, view, update, and delete patient records
- Create and view doctor records
- Update and delete doctor records created by the logged-in user
- Assign doctors to patients
- View and remove patient-doctor assignments
- Restrict patient records according to user ownership
- Validate requests and handle errors
- Store data in PostgreSQL using Django ORM

## Project Setup

### 1. Requirements

Install Python 3.10 or later and PostgreSQL.

### 2. Open the Project

Open the project folder in VS Code and navigate to the folder containing `manage.py`.

Activate the existing virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

If the virtual environment does not exist, create it first:

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root, in the same folder as `manage.py`.

Add the following configuration:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:YOUR_PORT/healthcare_db
```

Replace `YOUR_PASSWORD` with your PostgreSQL password and `YOUR_PORT` with the port on which PostgreSQL is running.

Create a PostgreSQL database named `healthcare_db` if it does not already exist.

For example, if PostgreSQL is running on port `5000`, use `5000` in `DATABASE_URL`. If it is running on port `5432`, use `5432`.

### 5. Apply Migrations

```powershell
python manage.py migrate
```

### 6. Start the Development Server

```powershell
python manage.py runserver
```

The application will be available at:

`http://127.0.0.1:8000/`

## Authentication

All patient, doctor, and mapping endpoints require a valid JWT access token.

### Register a User

**Method:** `POST`

**Endpoint:** `/api/auth/register/`

Request body:

```json
{
  "name": "Example User",
  "email": "user@example.com",
  "password": "StrongPass123!"
}
```

### Login

**Method:** `POST`

**Endpoint:** `/api/auth/login/`

Request body:

```json
{
  "username": "user@example.com",
  "password": "StrongPass123!"
}
```

The response contains an access token and a refresh token.

For protected requests, select **Authorization → Bearer Token** in Postman and provide the access token.

Alternatively, send this HTTP header:

```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### Refresh Access Token

**Method:** `POST`

**Endpoint:** `/api/auth/token/refresh/`

Request body:

```json
{
  "refresh": "YOUR_REFRESH_TOKEN"
}
```

## API Endpoints

All patient, doctor, and mapping endpoints require authentication.

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register/` | Register a user |
| POST | `/api/auth/login/` | Login and obtain JWT tokens |
| POST | `/api/auth/token/refresh/` | Refresh an access token |

### Patients

Patient records are associated with the user who creates them.

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/patients/` | Create a patient |
| GET | `/api/patients/` | List your patients |
| GET | `/api/patients/{id}/` | Retrieve a patient |
| PUT | `/api/patients/{id}/` | Update a patient |
| PATCH | `/api/patients/{id}/` | Partially update a patient |
| DELETE | `/api/patients/{id}/` | Delete a patient |

Example patient request:

```json
{
  "name": "Aman Sharma",
  "age": 25,
  "gender": "Male",
  "address": "Mathura, Uttar Pradesh",
  "phone": "9876543210"
}
```

### Doctors

Authenticated users can view doctor records. Only the creator can update or delete their doctor records.

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/doctors/` | Create a doctor |
| GET | `/api/doctors/` | List all doctors |
| GET | `/api/doctors/{id}/` | Retrieve a doctor |
| PUT | `/api/doctors/{id}/` | Update a doctor |
| PATCH | `/api/doctors/{id}/` | Partially update a doctor |
| DELETE | `/api/doctors/{id}/` | Delete a doctor |

Example doctor request:

```json
{
  "name": "Dr. Neha Gupta",
  "specialization": "Cardiology",
  "email": "doctor@example.com",
  "phone": "9876543210"
}
```

### Patient-Doctor Mappings

Mappings connect patients with doctors. Users can access mappings associated with their own patients.

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/mappings/` | Assign a doctor to a patient |
| GET | `/api/mappings/` | List your patient-doctor mappings |
| GET | `/api/mappings/{patient_id}/` | List assignments for a specific patient |
| DELETE | `/api/mappings/{id}/` | Remove a mapping |

Example mapping request:

```json
{
  "patient": 1,
  "doctor": 1
}
```

Use the actual patient and doctor IDs returned by the API.

## Authorization and Data Access

- Patient records are accessible only to their owner.
- Authenticated users can view doctor records.
- Only the creator can update or delete a doctor record.
- Mapping access is restricted according to patient ownership.
- Requests without valid authentication credentials are rejected.

## Testing with Postman

1. Register a user using `POST /api/auth/register/`.
2. Log in using `POST /api/auth/login/`.
3. Copy the access token from the response.
4. Set **Authorization → Bearer Token** in Postman.
5. Create a patient using `POST /api/patients/`.
6. Create a doctor using `POST /api/doctors/`.
7. Assign the doctor to the patient using `POST /api/mappings/`.
8. Test GET, PUT, PATCH, and DELETE requests.
9. Retrieve assignments for a patient using `GET /api/mappings/{patient_id}/`.
10. Register another user and verify patient ownership restrictions.
11. Test missing or invalid tokens and invalid input.

## Database

The application uses PostgreSQL for persistent storage and Django ORM for database operations. Database credentials and connection settings are loaded from environment variables.

## License

Developed as a healthcare backend project.
