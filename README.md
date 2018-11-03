# Debate Service!

## How to run with gunicorn

1. Create and activate a Python3 virtual environment in which to install
   dependencies.

  ```
  $ python3 -m venv venv
  $ source venv/bin/activate
  ```

2. Navigate to the project root directory (the directory with the `setup.py`)
   and install the dependencies.

   ```
   $ pip install -e .
   ```

3. Start the HTTP server with gunicorn.

   ```
   $ gunicorn debateservice.app:api -b 0.0.0.0:8080
   ```
