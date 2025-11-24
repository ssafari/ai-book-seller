# BOOK SELLER APP

## Summary

Simulating SOA online book selling market. Developing microservice providing APIs and automated services powered by AI agents.


### database-agent:

A LangGraph react agent for creating SQL query, based on user search query.  This service will connect to MCP server for getting book information
from the bookstore database. It starts reasoning to create a sql query.  It sends the query to database by contacting mcp tooling server to send
the query to the datbase for executing.


### mcp-server:

This service provides tools for connecting to the postgres database and executing the sql queries sent by database ai agent.


### book-repository

This service builds the book table in the bookstore database by loading a CSV file from Kaggle. It handles cleaning the data and engineering dataset for saving into
the database.  It creates embedding information for using as pgvector database to create a vector-store for performing similarity search for no sql queries.




