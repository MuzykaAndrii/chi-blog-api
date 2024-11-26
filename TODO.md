### 1. Develop REST API using Flask
- [ ] **Create Basic Auth System**
  - [ ] Implement login/password authentication.
  - [ ] Users can only be created through management commands/SQL queries.
  - [ ] Assign user roles (Admin, Editor, Viewer) on creation.

- [ ] **Endpoints for Managing User Permissions**
  - **Roles**:
    - Admin:
      - [ ] Can perform CRUD operations on all entities.
    - Editor:
      - [ ] Can view, update, and manage articles created by others.
      - [ ] Can manage their own articles.
    - Viewer:
      - [ ] Can view articles created by others.
      - [ ] Can manage their own articles.

- [ ] **Endpoints for Articles**
  - [ ] Create (POST)
  - [ ] Read (GET)
  - [ ] Update (PUT)
  - [ ] Delete (DELETE)
  - [ ] List all articles
  - [ ] Get article by ID

- [ ] **Endpoints for Users**
  - [ ] Create (POST)
  - [ ] Read (GET)
  - [ ] Update (PUT)
  - [ ] Delete (DELETE)
  - [ ] Retrieve list of all users
  - [ ] Search users by text

- [ ] **Database**
  - [ ] Use PostgreSQL as the database.
  - [ ] Use SQLAlchemy/Peewee as the ORM.

- [ ] **Permissions**
  - [ ] Admin:
    - CRUD on all users and articles.
  - [ ] Editor:
    - View and update any articles.
  - [ ] Viewer:
    - Manage own articles.

- [ ] **Search Functionality**
  - [ ] Endpoints to search users and articles by text.

---

### 2. Populate the Database with Initial Data
- [ ] Develop a script to populate the database with:
  - Sample articles.
  - Users with various roles.

---

### 3. Write Unit Tests for All Endpoints
- [ ] Cover all endpoints with unit tests using `pytest` or `unittest`.

---

### 4. Docker Setup
- [ ] Develop Docker configuration for the application.
- [ ] Ensure the project runs with minimal setup (Docker only).

---

### 5. Write README File
- [ ] Include instructions for:
  - [ ] Building the application.
  - [ ] Running the application.
  - [ ] Running tests.
  - [ ] Loading initial data.

---

## Nice-to-Have Tasks

- [ ] Maximize test coverage (minimum 80% for custom code, excluding tests and auto-generated files).
- [ ] Integrate OpenAPI (Swagger) documentation using [Flasgger](https://github.com/flasgger/flasgger).
- [ ] Create a Postman collection.
- [ ] Develop an SQL script to set up the database:
  - Tables.
  - Data.
  - Users for each role.
  - [ ] Provide a convenient way to run the script (Docker command, shell script, or Python script).
- [ ] Measure test coverage using external tools like `pytest-cov`.

---

## Deployment Tasks

- [ ] Deploy application to AWS/GCP/Azure.
  - [ ] Make it accessible via an IP address.
  - [ ] Use either SSH/manual deployment or automated systems like GitHub Actions/Cloud Formation.

---

## CI/CD

- [ ] Configure GitHub Actions to:
  - [ ] Run tests on every commit.
  - [ ] Deploy the application if tests pass.

---

## General Guidelines
- [ ] Use `git` for version control.
- [ ] Save work to a public GitHub repository.
- [ ] Ensure secure coding practices (no secrets in the repository).
