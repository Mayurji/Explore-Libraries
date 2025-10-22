#!pip install locust

from locust import HttpUser, task, between
# Imports core Locust components: HttpUser (the simulated user), task (the endpoint to hit), 
# and between (for controlling user pause time).

# IMPORTANT: Ensure your FastAPI apps are running on these ports
# Defines the ports where the two separate FastAPI servers are expected to be running.
ASYNC_PORT = 8000
SYNC_PORT = 8001

# Defines a class of virtual users who will specifically target the Async API.
class AsyncAPIUser(HttpUser):
    """
    User class for testing the ASYNC FastAPI application.
    This simulates non-blocking I/O.
    """
    # Instructs the user to wait a random amount of time (0.1 to 0.5 seconds) 
    # between executing tasks, simulating realistic user behavior.
    wait_time = between(0.1, 0.5)

    # Sets the base URL for this group of users to target the application running on port 8000.
    host = f"http://localhost:{ASYNC_PORT}"

    # Decorator indicating that the following method is a task to be executed by the user. 
    # The (1) is a weight (higher number = more frequent execution).
    @task(1)
    def read_async_heroes(self):
        # This task hits the /async/heroes/ endpoint. This is the non-blocking API endpoint we expect to perform well.
        # We hit the ASYNC endpoint
        self.client.get("/async/heroes/")

class SyncAPIUser(HttpUser):
    # Defines a class of virtual users who will target the Sync API.
    """
    User class for testing the SYNC FastAPI application.
    This simulates blocking I/O, which will exhaust the Uvicorn worker threads faster.
    """
    wait_time = between(0.1, 0.5)
    # Sets the base URL for this group of users to target the application running on port 8001.
    host = f"http://localhost:{SYNC_PORT}"

    @task(1)
    def read_sync_heroes(self):
        # This task hits the /sync/heroes/ endpoint. This is the blocking API endpoint 
        # we expect to see performance degradation and request failures on when the worker count is low.
        # We hit the SYNC endpoint
        self.client.get("/sync/heroes/")
