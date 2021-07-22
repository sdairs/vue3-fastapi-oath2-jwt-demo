# vue3-fastapi-oath2-jwt-demo
This is a Demo project to show how to do OAth2 token auth with FastAPI to Vue3 frontend with JWT (with Postgres)

The project consists of:
- A backend API built using Python & FastAPI
- A frontend UI built using Vue.js
- A database using CockroachDB

## Backend API
The backend is a REST API built in Python and using FastAPI.

Uses: 
- Pydantic (validation between frontend input & backend output, conversion from DB ORM models)
- SQLAlchemy (DB abstraction, ORM models)
- python-jose is used for working with JWT
- passlib & argon2 is used for handling password hashing
- Poetry is used for dependency management

The API exposes two endpoints:
- `GET /` returns a JSON Hello World result, protected by OAuth2
- `POST /token` takes multi-part form data providing credentials for logging in & returns an OAuth2 bearer token

You can run the backend using the uvicorn dev server, make sure you're inside the `backend` dir e.g.
`~/vue3-fastapi-oath2-jwt-demo/backend $ uvicorn main:app --reload --host 0.0.0.0 --port 8080` 

## Frontend UI
The frontend is a Vue3.js app that presents a very basic Login form with Username & Password fields.

Uses:
- Vue3.js for app framework 
- Element-Plus as UI framework
- VueX for state management
- Vue-router for handling routing
- Native Fetch API for communication with the backend REST API
- Yarn for dependency management

There is only a single route `/` which presents a simple Login form.
Clicking the Submit button will `POST` to the `/token` backend endpoint, giving the Username & Password as multi-part form data.

## Database
The database used is CockroachDB, which is a PostgreSQL compatible distributed database.
If you aren't familiar with CockroachDB, just pretend it's Postgres.

One database/table exists in the database, `users.users` with 1 existing user entry.
Username: `user1`
Password: `password`

Passwords are stored as STRING representations of an Argon2 hash. 
See [https://passlib.readthedocs.io/en/stable/lib/passlib.hash.argon2.html](this page) for details on Argon2 hashes.

# Setup
Some example commands are provided in the `setup` directory `commands` file.
This is not a script to be executed as is, it's just a dump of commands you might use to set your environment up.
