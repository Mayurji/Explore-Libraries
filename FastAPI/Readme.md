### What is FastAPI?

FastAPI is a modern, high-performance web framework for building APIs with Python 3.7+ based on standard Python type hints. 

*Key benefits:*

It's designed for speed, easy coding, and robustness.

### Why is it Fast?

*ASGI (Asynchronous Server Gateway Interface):*

- FastAPI is built on top of Starlette, an ASGI framework. 
- Unlike the older WSGI standard used by frameworks like standard Flask, ASGI allows for asynchronous programming using Python's `async` and `await` keywords. 
- This is crucial for I/O-bound tasks—like waiting for a database query or an external API call. Instead of one thread being blocked and sitting idle, the server can switch to handle other requests concurrently, leading to incredibly high performance and concurrency.

*Pydantic:*

- FastAPI uses Pydantic for data validation and serialization. 
- Pydantic uses those Python type hints to automatically validate the structure and type of data coming into your API (the request body or parameters) and the data going out (the response).
- This validation is done extremely efficiently and cuts down on developer errors by automatically giving clear, helpful error messages to the client.

### Compare FastAPI against Flask and Django

Django is your go-to if you need a large, feature-rich web application—something with an admin panel, a user system, and an ORM right out of the box.

Flask is perfect for small, simple projects or when you want total control and prefer to choose all your components yourself.

FastAPI shines for building high-performance, modern APIs and microservices. If your primary goal is a fast, robust RESTful API that needs to handle high traffic and leverages modern Python, FastAPI is the clear winner in terms of performance and development speed. Plus, the automatic interactive API documentation using Swagger UI and ReDoc is a massive time-saver!

## *Common Problem: Bad data in your API, missing fields, wrong type, or just garbage in.*

## Pydantic

### It defines the structure of the data it accepts (requests) and the data it sends back (response).

### It is used for Data validation and serialization.

### **Request and Response Model**

**Request Model: Request Models ensure the data coming into your API is correct.**

Task: 
    
    Create a simple Item model for a hypothetical e-commerce API.

    Implementation: Show how to use it in a POST endpoint.

**Response Model: Response Models ensure the data going out of your API is exactly what you promised and nothing more. This is crucial for Security and Consistency.**

### **"Imagine you fetch a user object from a database. It might contain a sensitive field like hashed_password or private_api_key. You MUST NOT send that back!"**


Task:

    Define two models: a database model and a public response model.

**Key takeaways:**

Request Models: For Validation and enforcing a schema on incoming data.

Response Models: For Serialization, Consistency, and crucial Security (data filtering).

## CRUD Operation With FastAPI

CRUD refers to create, read, update, and delete - using a simple, in-memory database.**

**Task**

*Create a simple API for managing a list of items (like products)*

**Steps**

1. Create a Data model: We'll use Pydantic for data validation and enforce a schema.

2. In-memory database and app initialization.

3. Write post, get, put, delete request to perform CURD operation.




