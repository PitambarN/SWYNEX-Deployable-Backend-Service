# Swynex API Project Setup

A RESTful API built using Python, Flask, and PostgreSQL to manage patient records through CRUD (Create, Read, Update, and Delete) operations.
This project was developed as part of the internship at SWYNEX Technologies. It demonstrates database integration, API key authentication, 
request validation, error handling, and environment-based configuration.

## 📌 Project Overview
The Swynex Patient Management API provides HTTP endpoints to create, retrieve, update, and delete patient records stored in a PostgreSQL database.
The API also includes a health check endpoint, a database connectivity test, environment variable configuration, and JSON-based request validation and error responses.

## Features

1. [ ] REST API development using Flask.
1. [ ] PostgreSQL database integration using Psycopg2.
2. [ ] Patient CRUD operations.
3. [ ] API key authentication for the protected endpoint.
4. [ ] JSON payload validation.
5. [ ] Patient ID, name, department, and appointment date validation.
6. [ ] Consistent JSON error responses.
7. [ ] Database exception handling and transaction rollback.
8. [ ] Health check and database connectivity endpoints.
9. [ ] Environment-based application configuration using python-dotenv.

##  Project Structure
**Swenex-API-project-setup/**
|
---app.py 
___.env 
---.gitignore 
--- README.md  
---requirements.txt 

## 🛠️ Technologies Used

Language: Python
Framework: Flask
Database: PostgreSQL
Database Driver: Psycopg2
Configuration: python-dotenv
API Format: JSON
Testing: Postman and curl
Version Control: Git and GitHub

## PROJECT STRUCTURE
Swynex-API-project-setup/
├── app.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
The .env file contains local configuration and must not be committed to GitHub. A .env.example file can be added to document the required environment variables without exposing secrets.

## ⚙️ Prerequisites

Install the following software before running the project:

* Python 3.13.4, or another version supported by the project dependencies.
* pip(Python package Installer)
* PostgreSQL
* Git (optional)
* Postman (optional, for API testing)

## 🚀 Installation and Setup
1. Clone the Repository
If your project is hosted on GitHub, clone it using:

git clone <your-repository-url>
cd Swenex-API-project-setup
Alternatively, navigate directly to your existing project directory.
Alternatively, download the repository and open the project directory.

## **2. Create a Virtual Environment**

Create an isolated Python environment:

python -m venv venv
Activate the virtual environment.

Windows (Command Prompt):

venv\Scripts\activate
Windows (PowerShell):

.\venv\Scripts\Activate.ps1
Linux/macOS:

source venv/bin/activate

## 3. Install Dependencies

Install the required packages:

pip install Flask python-dotenv psycopg2-binary


pip install -r requirements.txt

or If you have not yet added the dependencies to requirements.txt, include:
flask
python dotenv

## 4. Configure Environment Variables
Create a .env file in the root directory of your project.

Example configuration:


APP_NAME="BACKEND APPLICATION"
SECRET_KEY=DEBAS
API_SECRET_KEY=my_api_key_0000
PORT="4070"
DEBUG="True"
DB_NAME="patient_db"

DB_USER="postgres"
DB_PASSWORD="1122"
HOST="localhost"
DB_PORT="5432"
Environment variable descriptions:

**Variable**	**Description**
APP_NAME:	    Name displayed by the health check endpoint
SECRETE_KEY:	Secret key configured for the Flask application,Flask application secret key
PORT:	        PostgreSQL server port
DEBUG:      	Enables or disables Flask debug mode
API_SECRET_KEY: API key used to authenticate protected requests
HOST:           PostgreSQL server HOST name
DB_USER:        PostgreSQL Username
DB_PASSWORD:    PostgreSQL Password
DB_NAME:        PostgreSQL Database Name
keep your .env file private and do not commit real secrets to Git.
# NOTE:
These variable names must match the names actually read by app.py. The example values are placeholders, not production credentials.
Keep .env private and add it to .gitignore. Never upload real passwords, API keys, or secret keys to GitHub.

# Database Setup
Open PostgreSQL or pgAdmin and execute:


CREATE DATABASE patient_db;
Connect to the patient_db database before creating the table.

## 5. Create the patient table

Create a database named patient_db using PostgreSQL or pgAdmin.

Create the patient table using the following SQL:

CREATE TABLE patient (
    patient_id VARCHAR(5) primary key ,
    patient_name VARCHAR(30) NOT NULL,
    department VARCHAR(20) NOT NULL,
    appointment_date VARCHAR(10) NOT NULL,
    transaction_id SERIAL unique
);

# NOTE:
This schema stores the appointment date as text. If the application uses PostgreSQL's DATE type instead, update the table definition and application queries accordingly.


## **5. Run the Application**
Start the Flask application using:


python app.py
If the application is configured to listen on port 4070, the local base URL is:


http://127.0.0.1:4070
Otherwise, use the port configured in app.py and your environment settings.

The API is now ready for local testing.

http://127.0.0.1:5000
The port may differ depending on your .env configuration.

## 🔗 API DOCUMENTATION
Base URL for local development:


http://127.0.0.1:4070
The following endpoint descriptions are based on the current project implementation. Verify the accepted methods, request fields, and response formats against app.py.

# API authentication END-POINT

### /add_patient(protected end point)

I have protected this end-point by x-api-key  Authentication.
IF the clent enter the correct API-key with valid data and valid request method then 
access this end point.If the client entered the wrong Api key they the response is Unauthorized Access.Enter a valid API key.

# END-POINT Sumaary:

### HTTP METHODS  End-Point **Method_Endpoint_Description**           Authentication

* GET	        /health_check	        Check API status              As configured
  * GET	        /test_db	        Test PostgreSQL connectivity      As configured
* POST	      /add_patient	         Create a patient record          API key required
* GET	      /get_patient	         Retrieve a patient by ID         As configured 
* PUT	    /update_patient         	Update patient details        As configured
* DELETE	/delete_patient	           Delete a patient record        As configured


# health_check ENDPOINT

EXAMPLE request using postman
http://127.0.0.1:5000/health_check
Example response:

{
  "WELCOME TO MY": "BACKEND APPLICATION"
}
The response value depends on the APP_NAME variable configured in your .env file.

Sample API Requests
Use Postman to test the following endpoints. Set the request header to:

Content-Type: application/json

1. **Health_Check**
Request

GET http://127.0.0.1:4070/health_check
Example response

{
  "message": "ok",
  "WELCOME TO MY": "SWYNEX Patient API"
}
2**. Test Database Connection**
Request

GET http://127.0.0.1:4070/test_db
Successful response

{
  "status": "success",
  "message": "PostgreSQL connection successful"
}
3. **Create a Patient**

## END POINT:post/add_patient
Creates a new patient record. This endpoint requires API key authentication.

Request headers:
Content-Type: application/json
x-api-key: YOUR_API_KEY


Request

POST http://127.0.0.1:4070/add_patient
Request body

{
  "id": "12345",
  "name": "Rahul Sharma",
  "department": "Cardiology",
  "date": "2026-10-20"
}
The id must be a five-digit numeric string. The appointment date should use the YYYY-MM-DD format when the database column is of type DATE.

Example response

{
  "message": "data inserted successfully",
  "patient_id": "12345",
  "patient_name": "Rahul Sharma",
  "department": "Cardiology",
  "appointment_date": "2026-10-20",
  "transaction_id": 1
}
The transaction ID shown is illustrative; the database generates the actual value.

4. **Retrieve a Patient**
Endpoint: GET /get_patient

Example request body, if the current implementation accepts JSON in a GET request:

Request

GET http://127.0.0.1:4070/get_patient
Request body

{
  "id": "12345"
}
The endpoint currently expects a JSON body with a GET request. In production APIs, a path parameter or query parameter is generally preferable.
 GET request bodies are not consistently supported by HTTP clients and intermediaries. A path parameter such as /patients/12345 or a query parameter such as /get_patient?id=12345 is generally preferable when revising the API.

5. **Update a Patient**
Endpoint: PUT /update_patient
Request

PUT http://127.0.0.1:4070/update_patient
Request body

{
  "id": "12345",
  "name": "Rahul Kumar",
  "department": "Neurology",
  "date": "2026-10-22"
}
This request is intended to update an existing patient record.

6. **Delete a Patient**
Request

DELETE http://127.0.0.1:4070/delete_patient
Request body

{
  "id": "12345"
}
This request deletes the matching patient record.

# Sample Data

Use the following fictional patient record to test the API in a local development database.


### Field	          Sample value

Patient ID	            12345
Patient Name	      Rahul Sharma
Department	          Cardiology
Appointment Date	  2026-10-20


The sample record can be created using POST /add_patient with the JSON body documented above.
The following SQL statement can also be used to insert sample data directly into PostgreSQL, if the record does not already exist:


INSERT INTO patient
    (patient_id, patient_name, department, appointment_date)
VALUES
    ('12345', 'Rahul Sharma', 'Cardiology', '2026-10-20');
Use fictional records only. Do not include real patient information in the public repository

## Authentication
The POST /add_patient endpoint is documented as protected by API key authentication.
Send the key using the x-api-key request header:


x-api-key: YOUR_API_KEY
Configure the expected key using the environment variable used by your application, documented here as API_SECRET_KEY.

A valid API key should allow the request to proceed to the normal validation and database processing steps.
A missing or invalid key should be rejected if the authentication check is correctly implemented.
Keep the key confidential and never commit it to the repository.
Authentication requirements for the remaining endpoints should be documented according to the actual code.

# **Validation and Error Handling**

The project documents validation for the following fields and conditions:

* Required patient fields.
* Five-digit numeric patient IDs.
* Patient names up to 30 characters.
* Department names up to 20 characters.
* Appointment date validation.
* Invalid JSON payloads.
* Database errors and transaction rollback.
* Unsupported HTTP methods and HTTP 405 responses.
* Authentication failures on protected endpoints.

Example error response format, if supported by the application:


{
  "error": "Invalid request",
  "message": "A required field is missing"
}
Error messages and HTTP status codes may vary depending on the implemented handlers. Use the actual response formats from app.py when documenting specific errors.

# Testing

Test the endpoints using Postman or curl.

Recommended test cases:

Call GET /health_check and verify that the API returns a response.
Call GET /test_db and verify database connectivity.
Create a patient using a valid API key and valid JSON.
Try creating a patient with an invalid or missing API key.
Test validation using missing fields and invalid patient IDs.
Retrieve an existing patient.
Update an existing patient.
Delete a test patient.
Try an unsupported HTTP method and verify the error response.
Use a development database for testing destructive operations such as DELETE.

## Deployments Notes
The application can be run locally using Flask and PostgreSQL. For remote deployment, the application needs a hosting environment and a reachable PostgreSQL database.

Before deploying:
* Confirm that requirements.txt contains all required dependencies.
* Configure the environment variables through the hosting provider's secret or environment configuration.
* Provision a PostgreSQL database and configure its connection details.
* Ensure that the application listens on the port provided by the hosting platform, if required.
* Disable Flask debug mode in production.
* Use a production WSGI server, such as Gunicorn, where supported.
* Configure HTTPS and restrict access to credentials.
* Verify the health check and CRUD endpoints after deployment.

A possible production start command for a Flask application whose entry-point module is app.py and whose Flask instance is named app is:


gunicorn app:app
This command requires Gunicorn to be installed and the Flask instance to be named app. Adjust it if your application uses a different entry point or instance name.

Live deployment status: Deploy succeeded.

GitHub Repository: <https://github.com/PitambarN/SWYNEX-API-Project-Setup.git>
Live API Base URL: < https://swynex-api-project-setup.onrender.com>

## Security Considerations

* Keep .env out of version control.
* Use strong, unique API keys and secret keys.
* Never expose database passwords in source code or README examples.
* Disable debug mode in production.
* Use HTTPS for deployed API traffic.
* Use fictional sample data in public documentation.
* Restrict database access and use appropriately scoped database credentials.

## Learning Outcomes

Through this project, I practised:

Building REST APIs with Flask
Connecting Python applications to PostgreSQL
Executing SQL queries using Psycopg2
Implementing CRUD operations
Validating incoming JSON data
Handling database exceptions and transactions
Managing configuration using environment variables
Testing endpoints using Postman

## Updated Learning Outcomes
Through this project, I practised:

* Developing REST APIs with Flask.
* Integrating PostgreSQL with Python.
* Executing SQL queries using Psycopg2.
* Implementing CRUD operations.
* Validating JSON request payloads.
* Handling database exceptions and transactions.
* Managing environment-based configuration.
* Testing endpoints using Postman and curl.

# Internship Task

Organization: SWYNEX Technologies
Task: Task 2 — Database Integration and CRUD Operations
Project: Patient Management REST API

## **Testing with a Browser or API Client**

You can test the health check endpoint using:

A web browser
Postman
curl
Send a GET request to /health_check and verify that the API returns a JSON response.

## 👨‍💻 Author

** Name**:Debasis Nayak

**Project Name**: Swynex API Project setup

**Description:** This project demonstrates a basic patient management API with PostgreSQL integration and API request handling, developed as part of an internship learning project.



