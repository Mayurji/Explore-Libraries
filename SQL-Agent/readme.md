### Building a SQL Agent Using Langchain

In this tutorial, you will learn how to build an agent that can answer questions about a SQL database using LangChain agents.

**What happens when a natural language query is passed to the agent?**

1. Fetch the available tables and schemas from the database
2. Decide which tables are relevant to the question
3. Fetch the schemas for the relevant tables
4. Generate a query based on the question and information from the schemas
5. Double-check the query for common mistakes using an LLM
6. Execute the query and return the results
7. Correct mistakes surfaced by the database engine until the query is successful
8. Formulate a response based on the results