# Backend Technical Test FastAPI + PostgreSQL + RabbitMQ + Docker

This repository contains the development of the technical test for the Backend Engineer position at ZeBrands.  

- [Instructions](./INSTRUCTIONS.md)  

---

## Getting Started

1. Clone this repository and navigate into it:

    ```bash
    git clone https://github.com/sfaurel/ZebrandsBack.git
    cd ZebrandsBack
    ```

2. Copy and complete the `.env` files, then run the services with Docker Compose:  
    `important`: start the services in the indicated order, as some depend on others.

    Run the commands from the root of the project, in separate terminals for debugging or in detached mode.

    1. DB
    ```bash
    cd db
    cp .env.example .env
    nano .env  # Fill the variables with your own values
    docker compose up
    ```

    2. Event broker
    ```bash
    cd event-broker
    cp .env.example .env
    nano .env  # Fill the variables with your own values
    docker compose up
    ```

    3. Accounts service
    ```bash
    cd accounts_service
    cp .env.example .env
    nano .env  # Fill the variables with your own values
    docker compose up
    ```

    4. Products service
    ```bash
    cd products_service
    cp .env.example .env
    nano .env  # Fill the variables with your own values
    docker compose up
    ```

    5. Notification service
    ```bash
    cd notification_service
    cp .env.example .env
    nano .env  # Fill the variables with your own values, require a resend api key
    docker compose up
    ```

    sign in to [https://resend.com/signup](https://resend.com/signup) and get a free api key for test this service.

3. From the browser, access the following services:
    - Accounts service API: [http://localhost:8000](http://localhost:8000)
    - Accounts service Docs (Swagger): [http://localhost:8000/docs](http://localhost:8000/docs)
    - Products service API: [http://localhost:8001](http://localhost:8001)
    - Products service Docs (Swagger): [http://localhost:8001/docs](http://localhost:8001/docs)

    `important`: When testing accounts endpoint, use real email or notifications may fail.

---

## Tests
1. To run the tests, ensure that only the other services are running (db, event-broker, accounts_service, products_service, notification_service).
2. Then, modify the host environment variables to localhost in the `.env` files of the service being tested.
3. Finally, navigate to the service directory and run the tests with pytest from virtual environment: 

```bash
cd <dir>
python3 -m venv venv
source venv/bin/activate
pytest
```

---

## Tech decisions and notes
- FastAPI was chosen for its ease of use, and automatic generation of API documentation
- Docker images based on Alpine Linux were used due to their small size.
- Gitflow was followed as the branching strategy, although in a less granular way than usual to avoid overcomplicating the development process.
- The possibility of separating the authentication service into an independent microservice was evaluated, but it was decided to keep it within the accounts service to simplify the architecture.
- Accounts are created with the anonymous role by default, ensuring that no account is accidentally granted higher privileges.
- Comments were kept to a minimum, aiming for code that is self-explanatory.
- Delete operations are implemented as soft deletes (is_active = False for accounts or is_discontinued = True for products) to maintain traceability and avoid inconsistencies.
- An event-based notification system using RabbitMQ was implemented to decouple services and improve scalability.
- docker compose files in each folder were created to facilitate independent service testing and decoupling.

---

## Further work
- [ ] Implement pagination for listing endpoints.
- [ ] Decouple the database into separate instances for each service.
- [ ] Expand test coverage and fix failing tests.
- [ ] Fix request counting in products (currently counts even those made by admin users; it should only count requests from anonymous or unauthenticated users).
- [ ] Implement an API gateway to unify the services.
- [ ] Change JWT token signing to public/private key for stronger security.  
  For simplicity and to allow testing, a shared secret key between services was used. With this approach, services can authenticate themselves, but it is less secure and increases the risk of key exposure. Switching to public/private key signing allows only the auth service to issue tokens while enabling any other service to validate them. However, this also requires implementing another method for services to authenticate themselves (e.g., when requesting a list of accounts).
- [ ] Fix error message when attempting a request with an expired token.
- [ ] Use a more concurent aproach for analytics.
- [ ] Fix sending email notifications (currently fails with fake email address).

---

## Extramile
- [x] Add tests for your code
- [x] Containerize the app
- [ ] Deploy the API to a real environment
- [ ] Use AWS SES or another 3rd party API to implement the notification system
- [x] Provide API documentation (ideally, auto generated from code)
- [ ] Propose an architecture design and give an explanation about how it should scale in the future

---

## Folder Structure

### Accounts Service

```
accounts_service/
├── app/                     
│   ├── db/                  # Database utilities
│   ├── dependencies/        # Dependency injection for FastAPI endpoints
│   ├── models/              # SQLModel ORM models
│   ├── routers/             # FastAPI route definitions
│   ├── schemas/             # Pydantic models
│   ├── services/            # Business logic and service layer
│   ├── utils/               # Security helpers
│   └── main.py              
├── tests/                   # Unit and integration tests
├── .env                     # Environment variables for local dev
├── .env.example             # Template for .env file
├── .gitignore               
├── docker-compose.yaml      
├── Dockerfile               
├── populate.py              # Seed script for accounts tables
├── pytest.ini               
└── requirements.txt         
```

### Products Service
```
products_service/
├── app/
│   ├── db/                  # Database utilities
│   ├── dependencies/        # Dependency injection for FastAPI endpoints
│   ├── events/              # Event publishing/subscribing logic
│   ├── models/              # SQLModel ORM models
│   ├── routers/             # FastAPI route definitions
│   ├── schemas/             # Pydantic models
│   ├── services/            # Business logic and service layer
│   ├── utils/               # Security helpers
│   └── main.py              
├── tests/                   # Unit and integration tests
├── .env                     # Environment variables for local dev
├── .env.example             # Template for .env file
├── .gitignore               
├── docker-compose.yaml      
├── Dockerfile               
├── populate.py              # Seed script for products tables
├── pytest.ini               
├── requirements.txt         
```

### Notification Service
```
notification_service/
├── app/                     
│   ├── routers/             # FastAPI route definitions for notifications
│   ├── schemas/             # Pydantic models
│   ├── services/            # Business logic and service layer
│   ├── templates/           # Jinja2 templates for emails
│   ├── utils/               # Helper functions
│   └── main.py              
├── tests/                   # Unit and integration tests
├── .env                     # Environment variables for local dev
├── .env.example             # Template for .env file
├── .gitignore               
├── docker-compose.yaml      
├── Dockerfile               
├── pytest.ini               
└── requirements.txt    
```

### Database
```
db/
├── .env                     # Database-specific environment variables
├── .env.example             # Template for db .env
├── .gitignore               
├── docker-compose.yml       
└── init-services-dbs.sh     # Initialization script for project databases
```

### Event Broker
```
event-broker/
├── .env                     # Environment variables for RabbitMQ or event broker
├── .env.example             # Template for .env
├── .gitignore               
└── docker-compose.yaml      
```

---

## Project Diagram

[![](https://mermaid.ink/img/pako:eNp9kllr4zAUhf-KEBQ6kAbXTrw9DCTxDBQmbZaGgbH7IMs3sYktBS3dQv77yEtCOhOiJ51zPx1dLXtMeQY4xOuSv9GcCIWeo4QhM1bxSoJ4SVgrpU43guxyNKKUa6aWIF4LCnEnUadfWroeo8nkVB3NHroKsOy_yJngmaanyE5eiJwtolP1emQ0jiOiSErkl5aMfTvjUm0ELOe_vl0J-PEKTI0F34KIFyRNCzWdnyVN5_Ht0UYtdi3tkatiXVCiCs6Oxzz3Lpz18en54edX6DcX2-ZJ_tnm5gYtoCTUMCC710N3d9_rJziX5vpaafy2Ho1bw1QuGWin07KQOYL6NmSDTOctYc5tAMqZ1BWcA03jLdNMa0yabhFUpChbZoV7uAJhjMx8vn1NJ1jlUEGCQzPNiNgmOGEHwxGt-PKDURwqoaGHBdebHIdrUkqj9C4jCqKCmIuuTu6OsD-cV8clG1Hv0y03rYCY1N8Sh-7Ab2Ac7vE7DgO7f29brusOLSewXHvYwx8GcvqeE7i2ZVu-N7BsZ3Do4c8m3up7fjAM7j3PHvqe49n-4S8DKgXO?type=png)](https://mermaid.live/edit#pako:eNp9kllr4zAUhf-KEBQ6kAbXTrw9DCTxDBQmbZaGgbH7IMs3sYktBS3dQv77yEtCOhOiJ51zPx1dLXtMeQY4xOuSv9GcCIWeo4QhM1bxSoJ4SVgrpU43guxyNKKUa6aWIF4LCnEnUadfWroeo8nkVB3NHroKsOy_yJngmaanyE5eiJwtolP1emQ0jiOiSErkl5aMfTvjUm0ELOe_vl0J-PEKTI0F34KIFyRNCzWdnyVN5_Ht0UYtdi3tkatiXVCiCs6Oxzz3Lpz18en54edX6DcX2-ZJ_tnm5gYtoCTUMCC710N3d9_rJziX5vpaafy2Ho1bw1QuGWin07KQOYL6NmSDTOctYc5tAMqZ1BWcA03jLdNMa0yabhFUpChbZoV7uAJhjMx8vn1NJ1jlUEGCQzPNiNgmOGEHwxGt-PKDURwqoaGHBdebHIdrUkqj9C4jCqKCmIuuTu6OsD-cV8clG1Hv0y03rYCY1N8Sh-7Ab2Ac7vE7DgO7f29brusOLSewXHvYwx8GcvqeE7i2ZVu-N7BsZ3Do4c8m3up7fjAM7j3PHvqe49n-4S8DKgXO)