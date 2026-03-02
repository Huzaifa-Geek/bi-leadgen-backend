# Business Intelligence & Lead Generation Platform 

Production-style FastAPI backend for scraping, scoring, and managing business leads.

##  Features
*   **JWT Authentication**: Secure sessions using **Argon2** password hashing.
*   **Role-based access (RBAC)**: Distinct permissions for Users and Admins.
*   **Asynchronous Processing**: Background scraping via **Celery** & **Redis**.
*   **Job Tracking**: Real-time status updates for lead generation tasks.
*   **Lead Scoring**: Intelligent engine to evaluate and rank lead quality.
*   **External Integration**: Google Maps scraping via **SerpAPI**.
*   **Data Reliability**: Multi-user data isolation and rate limiting (**SlowAPI**).

##  Tech Stack
*   **Framework**: FastAPI (v0.128.0)
*   **Database**: PostgreSQL (SQLAlchemy 2.0 + Alembic)
*   **Task Queue**: Celery 5.6 & Redis
*   **Hashing**: Argon2-cffi
*   **Scraping**: SerpAPI (Google Search Results)
*   **Validation**: Pydantic v2

##  Quick Start (Docker)

1.  **Clone the repository**
    ```bash
    git clone https://github.com
    cd bi-leadgen-backend
    ```

2.  **Configure Environment**
    Create a `.env` file based on `.env.example`:
    ```bash
    cp .env.example .env
    ```
    *Add your `POSTGRES_DB` (use 'leadgen') and `SERPAPI_API_KEY` to the file.*

3.  **Spin up the Containers**
    ```bash
    docker-compose up -d --build
    ```

4.  **Run Database Migrations**
    Sync your database schema:
    ```bash
    docker-compose exec api alembic upgrade head
    ```

5.  **Access the API**
    *   **Interactive Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
    *   **Health Check**: [http://localhost:8000/](http://localhost:8000/)

---
*Developed with ❤️ by [Huzaifa-Geek](https://github.com)*
