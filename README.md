# Authentication Microservice

## Overview
The Authentication Microservice provides user management and authentication functionality using **Keycloak** and **FastAPI**. It handles user registration, login, token verification, user information, resource management and logout.

---

## Features
- **User Registration**: Register users in Keycloak with roles and details.
- **Token Management**: Authenticate users, generate access/refresh tokens, and verify them.
- **Logout**: Invalidate tokens and log out users securely.
- **User Info**: Retrieves user information in exchange for JWT.
- **Health Check**: Monitor service health with a simple endpoint.

---

## Architecture
- **Keycloak**: Handles authentication and user management.
- **FastAPI**: Provides API endpoints for interaction with Keycloak.
- **SQL**: Database for storing user information.
- **Docker Compose**: Manages the deployment of the microservice.
- **Helm Charts**: Manages the deployment of the microservice on Kubernetes.

---

## Setup Instructions

### Prerequisites
- Docker and Docker Compose installed.
- Python 3.10+ installed.
- Access to a Keycloak server or deploy using the included `docker-compose.yml`.

### Installation

1. Clone the repository:
    ```bash
    git clone <repository-url>
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up the `.env` file with the following variables:
    ```dotenv
    SQLALCHEMY_DATABASE_URL=
    KEYCLOAK_SERVER_URL=
    KEYCLOAK_REALM=
    KEYCLOAK_CLIENT_ID=
    KEYCLOAK_CLIENT_SECRET=
    KEYCLOAK_ADMIN_USERNAME=
    KEYCLOAK_ADMIN_PASSWORD=
    ```

4. Run the service using Docker Compose:
    ```bash
    docker-compose up --build
    ```

---

## Usage

### API Endpoints

#### 1. **Endpoint**
- Fast-api web-auth: <ip>:8000/web-auth/docs
- keycloak admin dashboard: <ip>:8080/keycloak

#### 2. **Swagger Docs**
- All usage examples on <ip>:8000/web-auth/docs

   
