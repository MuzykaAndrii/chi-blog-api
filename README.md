## How to run

**Clone git repository**:
```bash
git clone https://github.com/MuzykaAndrii/chi-blog-api
```

**Go to repo folder:**
```bash
cd chi-blog-api
```

**Create file with name `.env` in folder `./secrets/` with following content:**
```env
DB_HOST=db
DB_PORT=5432
DB_NAME=chiblog
DB_USER=andrii
DB_PASS=password

AUTH_SECRET=krzyugsckhbsifhekciahelfsiuhaleisuihgufluhszlefuugkucertuyefgapwuiicb
```
All variables except `DB_HOST` can be changed as you wish.

**Run the application**:
```bash
docker compose --env-file ./secrets/.env up --build -d
```
or by command `make up` if you have installed Makefile.

The application can be accessed by url  [http://127.0.0.1:8080/](http://127.0.0.1:8080/)

## Avaliable endpoints

The most endpoints have restricted access, to possess admin account check out clause "Populate database with fake data" below. After populating you can log in with credentials:

Email:
```
admin@example.com
```

Password:
```
password
```
#### **Authentication:**

- `POST /auth/login`: Log in a user and return an authentication token.
#### **Users:**

- `GET /users`: Fetch all users or search by name.
- `GET /users/<user_id>`: Fetch a user by ID.
- `POST /users`: Create a new user.
- `PUT /users/<user_id>`: Update a user.
- `DELETE /users/<user_id>`: Delete a user.

#### **Articles:**

- `GET /articles`: Fetch all articles or search with a query param.
- `GET /users/<user_id>/articles`: Fetch articles by a specific user.
- `GET /articles/<article_id>`: Fetch a single article by ID.
- `POST /articles`: Create a new article.
- `PUT /articles/<article_id>`: Update an article.
- `DELETE /articles/<article_id>`: Delete an article.

#### **Roles:**

- `GET /roles`: Fetch all roles.
- `GET /roles/<role_id>`: Fetch a role by ID.
- `POST /roles`: Create a new role.
- `PUT /roles/<role_id>`: Update a role.
- `DELETE /roles/<role_id>`: Delete a role.
- `GET /roles/<role_id>/permissions`: Get permissions assigned to a role.
- `POST /roles/<role_id>/permissions/<permission_id>`: Assign a permission to a role.
- `DELETE /roles/<role_id>/permissions/<permission_id>`: Remove a permission from a role.

#### **Permissions:**

- `GET /permissions`: List all permissions (requires permission).
- `GET /permissions/<permission_id>`: Fetch a permission by ID.
- `POST /permissions`: Create a new permission (requires permission).
- `PUT /permissions/<permission_id>`: Update a permission (requires permission).
- `DELETE /permissions/<permission_id>`: Delete a permission (requires permission).

#### Swagger docs

- `GET /apidocs` - List documentation (direct [link](http://127.0.0.1:8080/apidocs)) 

## Commands

#### Direct commands

**Start app:**
```bash
docker compose --env-file ./secrets/.env up --build -d
```

**Stop app:**
```bash
docker compose -f docker-compose.yml -f docker-compose-prod.yml --env-file ./secrets/.env down
```

**Run tests:**
```bash
docker exec -t blog-api pytest -s -v
```

**Run tests and coverage:**
```bash
docker exec -t blog-api pytest -s -v --cov
```

**Show backend logs:**
```bash
docker logs --follow blog-api
```

**Populate db with fake data:**
```bash
docker exec -t blog-api python3 fill_db.py
```

#### Makefile commands

**Start app:**
```bash
make up
```

**Stop app:**
```bash
make down
```

**Run tests:**
```bash
make test
```

**Run tests and coverage:**
```bash
make cov
```

**Show backend logs:**
```bash
make logs
```

**Populate db with fake data:**
```bash
make fake
```

## The application architecture

The implemented application conforms following structure:

| Layer                         | Description                                                                                                                  |
| ----------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| Routes                        | The Flask routes, takes care about url's routing and translation the Service layer exceptions to coresponding json responses |
| Data Transfer Objects (DTO's) | The Pydantic schemas, responsible for data exchanging between routes and services. Serialezes and deserializes json data.    |
| Services                      | The service classes, caries out the business logic. Fetches data from DAO's and return those to routes as DTO.               |
| Data Access Objects (DAO's)   | The DAO classes. Makes deal with ORM queries and statements.                                                                 |
| ORM                           | Sqlalchemy models for interaction with PostgreSQL                                                                            |

## Tasks overview

#### Authentication system:
Used JWT access token with cookie transport: [auth app](https://github.com/MuzykaAndrii/chi-blog-api/tree/main/app/auth)
#### Authorization system
Implemented as Role Based Access Control: [rbac](https://github.com/MuzykaAndrii/chi-blog-api/tree/main/app/rbac)
#### User operations (CRUD)
Implemented in package: [users](https://github.com/MuzykaAndrii/chi-blog-api/tree/main/app/users)
#### Articles operations (CRUD)
Implemented in package: [articles](https://github.com/MuzykaAndrii/chi-blog-api/tree/main/app/articles)
#### Database population script
Implementted in file: [fill_db](https://github.com/MuzykaAndrii/chi-blog-api/blob/main/fill_db.py)
#### Unit tests
Implemented in folder: [tests/unit_tests](https://github.com/MuzykaAndrii/chi-blog-api/tree/main/tests/unit_tests)
#### Docker setup
Backend dockerfile: [Dockerfile](https://github.com/MuzykaAndrii/chi-blog-api/blob/main/Dockerfile) 
Dev compose: [docker-compose](https://github.com/MuzykaAndrii/chi-blog-api/blob/main/docker-compose.yml)
Prod compose: [docker-compose-prod](https://github.com/MuzykaAndrii/chi-blog-api/blob/main/docker-compose-prod.yml)
#### Postman collection
Avaliable in: [tests/postman](https://github.com/MuzykaAndrii/chi-blog-api/tree/main/tests/postman)
#### Deploy
Deployed in AWS EC2 with Postgres in AWS RDS: [http://ec2-3-68-77-134.eu-central-1.compute.amazonaws.com](http://ec2-3-68-77-134.eu-central-1.compute.amazonaws.com/apidocs)

#### Continuous Integration
Implemented with GitHub Actions in file: [workflows/ci](https://github.com/MuzykaAndrii/chi-blog-api/blob/main/.github/workflows/ci.yml)

## Possible improvements

There are some imprrovements what good to carry out:
- Use name field in Role and Permission models as natural Primary Key instead of Id
- Split swagger docs to separate files
- Decouple permission and roles in rbac package
- Use db indexes for searching articles by body field.
- Provide logging
- Move `_get_or_raise` method to some `BaseService` class (maybe a good idea to implement `get_or_raise` in BaseDAO)