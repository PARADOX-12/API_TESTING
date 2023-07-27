# Flask REST API 

## Overview

The Flask REST API is a backend application developed for Testing purpose to provide various endpoints for managing user data and performing CRUD (Create, Read, Update, Delete) operations. The API is built using Flask, a lightweight web framework for Python.

## Features

- User Authentication: The API uses JSON Web Tokens (JWT) for user authentication, providing secure access to protected endpoints.
- User Management: The API allows registration of new users, updating user profiles, and deleting user accounts.
- Data Operations: Users with appropriate privileges can perform CRUD operations on data resources.
- Error Handling: The API includes robust error handling to provide informative responses for invalid requests.

## Endpoints

1. `/register` (POST): Register a new user with the system.
2. `/login` (POST): Obtain access and refresh tokens upon successful authentication.
3. `/user`(POST) : To create new users(admin-only)
4. `/users/<user_id>` (GET, PUT, DELETE): Fetch, update, or delete a specific user's information (GET - all users, (PUT,DELETE) -admin-only).
5. `/users/<name>` (GET, PUT, DELETE): Fetch, update, or delete using name of a specific user(GET - all users, (PUT,DELETE) -admin-only).
6. `/users/<email>` (GET, PUT, DELETE): Fetch, update, or delete using email of a specific user(GET - all users, (PUT,DELETE) -admin-only).

## Authentication and Authorization

- Users must provide valid credentials to obtain access to protected endpoints.
- Upon successful login, users receive an access token and a refresh token.
- Access tokens must be included in the Authorization header of requests to access protected endpoints.
- The API uses different roles (e.g., "user" and "admin") to manage different levels of access to resources.

## Installation and Usage

1. Clone the project from the GitHub repository.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Set up the environment configuration by copying `.env.example` to `.env` and customizing the settings.
4. Run the Flask API using `python run.py`. The API will be available at `http://localhost:5000`.


# Configuration
The API uses configuration settings to manage JWT tokens and other parameters. The configuration can be found in the config.py file.





---

Thank you for exploring the Flask API project! The API provides powerful user management and data operations functionalities. 