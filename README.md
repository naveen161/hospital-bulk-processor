# Hospital Bulk Processing System

This project implements a FastAPI service for bulk hospital data processing.
It integrates with the existing Hospital Directory API to create and activate hospitals in batch from a CSV file upload.
The goal is to provide an automated way to handle multiple hospital records efficiently.

---

## Overview

The service receives a CSV file containing hospital details, validates it, and makes API calls to the existing Hospital Directory system.
Each hospital record is created using the directory’s API, grouped under a unique batch ID.
After all records are created, the batch is activated so that all hospitals become active in the directory.

---

## Features

* Accepts a CSV file with up to 20 hospitals
* Creates hospital records in the external directory API
* Generates a unique batch ID for each upload
* Automatically activates the batch once creation is complete
* Returns a detailed JSON response with results
* Includes optional endpoints for individual hospital CRUD operations (create, read, update, delete)

---

## Technology Stack

* Python 3.10+
* FastAPI
* httpx (for async API calls)
* uvicorn (server)
* python-multipart (for CSV upload)
* Docker (optional for deployment)

---

## Project Structure

```
app/
├── main.py
├── hospital_client.py
├── csv_utils.py
└── models.py
requirements.txt
Dockerfile
README.md
```

---

## Running Locally

1. Clone the repository

   ```bash
   git clone https://github.com/<your-username>/hospital-bulk-processor.git
   cd hospital-bulk-processor
   ```

2. Create and activate a virtual environment

   ```bash
   python -m venv venv
   source venv/bin/activate        # Mac/Linux
   venv\Scripts\activate           # Windows
   ```

3. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application

   ```bash
   uvicorn app.main:app --reload
   ```

5. Open the API documentation in your browser
   [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Example CSV File

```
name,address,phone
General Hospital,123 Main St,555-1111
City Medical,45 Elm Ave,555-2222
Sunrise Clinic,77 Lake Road,555-3333
```

---

## Bulk Upload Endpoint

**POST** `/hospitals/bulk`

Uploads a CSV file and processes the records.

**Response Example:**

```json
{
  "batch_id": "550e8400-e29b-41d4-a716-446655440000",
  "total_hospitals": 3,
  "processed_hospitals": 3,
  "failed_hospitals": 0,
  "batch_activated": true,
  "hospitals": [
    {
      "row": 1,
      "hospital_id": 101,
      "name": "General Hospital",
      "status": "created_and_activated"
    }
  ]
}
```

---

## Individual Hospital Endpoints

These endpoints act as proxies to the external Hospital Directory API.

| Method | Endpoint                   | Description                 |
| ------ | -------------------------- | --------------------------- |
| POST   | `/hospitals/`              | Create a hospital           |
| GET    | `/hospitals/{hospital_id}` | Get hospital details        |
| PUT    | `/hospitals/{hospital_id}` | Update hospital information |
| DELETE | `/hospitals/{hospital_id}` | Delete a hospital           |

---

## Deployment on Render

1. Push your project to a public GitHub repository.
2. Sign in to [https://render.com](https://render.com).
3. Create a new **Web Service** and connect your repository.
4. Set the following configuration:

   ```
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn app.main:app --host 0.0.0.0 --port 10000
   ```
5. Deploy the service and open the generated URL, for example:

   ```
   https://hospital-bulk-processor.onrender.com/docs
   ```

---

## Postman Collection

A Postman collection is available in the project files for testing all endpoints, including:

* Bulk upload
* CRUD operations
* Batch activation and deletion

---

## Example Response Summary

```json
{
  "batch_id": "b2a11dc3-5cc2-4d45-bc6b-fc223fe5526a",
  "total_hospitals": 3,
  "processed_hospitals": 3,
  "failed_hospitals": 0,
  "batch_activated": true
}
```

---

## Credits

Developed by Naveen Satyarthi, email : naveensatyarthi@gmail.com
Assignment: Senior Python Developer Assessment – Hospital Bulk Processing System
External API: Hospital Directory API ([https://hospital-directory.onrender.com/docs](https://hospital-directory.onrender.com/docs))

