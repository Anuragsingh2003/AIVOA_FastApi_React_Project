# Company Management API

This is a FastAPI backend for managing companies. It provides RESTful endpoints to create, read, update, and delete company records in a MySQL database.

## Features

- FastAPI async endpoints
- MySQL database connection pooling
- CORS enabled for React frontend
- CRUD operations for companies

## Requirements

- Python 3.8+
- MySQL server
- `aiomysql`, `fastapi`, `uvicorn`

## Setup

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/yourrepo.git
   cd full_stack_web/backend
   ```

2. **Create and activate a virtual environment:**
   ```sh
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   - Create a `.env` file with your MySQL credentials.

5. **Run the server:**
   ```sh
   uvicorn main:app --reload
   ```

## API Endpoints

- `POST /companies` — Create a company
- `GET /companies` — List all companies
- `GET /companies/{company_id}` — Get a company by ID
- `PUT /companies/{company_id}` — Update a company
- `DELETE /companies/{company_id}` — Delete a company





## Overview
This is a full-stack web application for managing company records, built with a FastAPI backend, React frontend, and MySQL database. It allows users to create, read, update, and delete (CRUD) company entries with fields: `id`, `name`, and `location`. The backend uses asynchronous MySQL connections with a connection pool, and the frontend is styled with Tailwind CSS and built with Vite for fast development.

### Features
- Add new companies with name and location.
- View a list of all companies.
- Edit existing company details.
- Delete companies.
- Responsive UI with Tailwind CSS.
- RESTful API with FastAPI and automatic OpenAPI documentation.
- Robust database connection handling with aiomysql.

### Tech Stack
- **Backend**: Python 3.8, FastAPI, aiomysql, Pydantic
- **Frontend**: React, Vite, Tailwind CSS, JavaScript
- **Database**: MySQL (patient_db, company table)
- **Tools**: Node.js 18.8.0, npm, Git

## Project Structure

## License

MIT
