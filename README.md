# Notes API

## 📌 Overview

A RESTful backend API that allows users to register, authenticate, and manage personal notes.
Each user can only access their own notes using JWT-based authentication.

This project demonstrates backend development, authentication, database integration, containerization, and cloud deployment.

---

## 🚀 Features

* User registration and login
* Password hashing with bcrypt
* JWT authentication
* Create, read, update, and delete notes
* **User-specific data isolation** (users can only access their own notes)
* Pagination support
* Docker containerization
* Deployment on AWS EC2

---

## 🛠 Tech Stack

* **Backend:** Python (Flask)
* **Database:** PostgreSQL
* **Authentication:** JWT (JSON Web Tokens)
* **Containerization:** Docker
* **Cloud:** AWS EC2

---

## 🌍 Live API

Base URL:
http://3.19.211.97:5000

---

## 🔐 Authentication

All protected routes require a JWT token.

Include it in requests like this:

Authorization: Bearer YOUR_TOKEN

---

## 📡 API Endpoints

### 🧑‍💻 Register

POST /register
Creates a new user

```json
{
  "username": "user1",
  "password": "123456"
}
```

---

### 🔑 Login

POST /login
Returns a JWT token

```json
{
  "username": "user1",
  "password": "123456"
}
```

---

### 📝 Get Notes

GET /notes
Returns notes for the authenticated user

---

### ➕ Create Note

POST /notes

```json
{
  "content": "My note"
}
```

---

### ✏️ Update Note

PUT /notes/{id}

```json
{
  "content": "Updated note"
}
```

---

### ❌ Delete Note

DELETE /notes/{id}

---

## 🧠 Key Concepts Demonstrated

* REST API design
* Token-based authentication
* Secure password storage
* Multi-user data isolation
* Docker networking between services
* Cloud deployment and configuration

---

## ⚙️ Running Locally (Optional)

1. Clone the repository

2. Install dependencies:
   pip install -r requirements.txt

3. Run the server:
   python notesAPI.py

---

## 🐳 Running with Docker

Build the image:
docker build -t notes-api .

Run the container:
docker run -d -p 5000:5000 notes-api



## 📈 Future Improvements

* Add frontend (React or simple UI)
* Use environment variables for secrets
* Add refresh tokens
* Deploy with HTTPS and domain name
* Use AWS RDS for managed database






