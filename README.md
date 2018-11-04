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

## How to run with Docker

1. Navigate to the project root directory (the directory with the `Dockerfile`)
   and build an image.

   ```
   $ docker build -t debateservice:latest .
   ```

2. Start a container with debateservice running inside it. Expose port 8080.

   ```
   $ docker run -d -p 8080:8080 debateservice
   ```

3. Post an opinion URL to `/opinions` to get information about the opinion from
   debate.org.

   ```
   $ curl -d '{"url": "http://www.debate.org/opinions/should-drug-users-be-put-in-prison"}' http://localhost:8080/opinions
   ```
