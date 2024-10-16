## Project Setup

**1. Clone the repo:**
  ```
  $ git clone <https url>
  ```

**2. Initialize and activate a virtualenv:**
  ```
  $ virtualenv venv
  $ source venv/bin/activate
  ```

**3. Install the dependencies:**
  ```
  $ pip install -r requirements.txt
  ```

**4. Install the dependencies:**
  ```
  $ Create .env file like .env.example Or set environment variables of chat server
  ```

**4-A. Run following Alembic commands to Migrate your Schema(Tables/Models) into the Database.:**
  ```
  $ alembic revision --autogenerate -m "Auto migrations"
  $ alembic upgrade head
  ```

**5. Run the development server:**
  ```
  $ python run.py
  ```

**6. Navigate to [http://localhost:8000](http://localhost:8000)**

**OR**

**Navigate to open Swagger Docs[http://0.0.0.0:8000/docs](http://0.0.0.0:8000/docs)**

