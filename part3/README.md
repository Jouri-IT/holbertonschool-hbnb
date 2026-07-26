# HBnB Evolution Phase 3: Authentication and Database Integration

---

# Overview

This phase extends the HBnB Evolution project by introducing secure authentication, authorization, and persistent database integration.

The project transitions from the in-memory repository implemented in Phase 2 to a database-backed architecture using SQLAlchemy and SQLite for development, while preparing the application for MySQL in production.

---

# Project Scope

The implementation includes the following major features:

- User Authentication (JWT)
- Role-Based Authorization
- Persistent Database Integration
- SQLAlchemy ORM
- SQLite Development Database
- MySQL Production Support
- Entity Relationship Mapping
- Database Validation

The project is organized into the following layers:

- Presentation Layer (Flask REST API)
- Business Logic Layer
- Persistence Layer (SQLAlchemy Repository)
- Database Layer (SQLite / MySQL)

Communication between these layers continues through the HBnBFacade.

---

# Deliverables

This project includes:

- Application Configuration
- JWT Authentication
- Password Hashing
- Authorization
- SQLAlchemy Repository
- SQLite Integration
- MySQL Configuration
- Entity Mapping
- Database Relationships
- ER Diagram
- Technical Documentation

---

# Technologies

- Python 3
- Flask
- Flask-RESTX
- Flask-JWT-Extended
- SQLAlchemy
- SQLite
- MySQL
- bcrypt
- REST API

---

# Repository Structure

```
.
├── README.md
├── requirements.txt
├── config.py
├── run.py
├── app/
│   ├── __init__.py
│   ├── api/
│   │   └── v1/
│   ├── models/
│   ├── services/
│   └── persistence/
```

---

# Installation and Running the Application

1. (Optional) Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the application

```bash
python run.py
```

4. Open Swagger

```
http://127.0.0.1:5000/api/v1/
```

---

# Team Members

- Razan Kashr
- Reema Almujalli
- Jouri AlSulaiman

---

# Goal

The goal of this phase is to transform the HBnB application into a secure, database-backed REST API by implementing authentication, authorization, persistent storage, and relational database management while maintaining the layered architecture developed in the previous phases.
