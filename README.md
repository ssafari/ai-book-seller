# BOOK SELLER APP

## Summary

Simulating SOA online book selling market. Developing microservice providing APIs and automated services powered by AI agents.


### database-agent:

A LangGraph react agent for creating SQL query, based on user search query.  This service will connect to MCP server for getting book information
from the bookstore database. It will reasoning to create a sql query and send that to database for getting the result a user looking for.


### mcp-server:

A service for providing tools for connecting to the postgres database and executing the sql queries.


### book-repository

This service builds the book table database by loading CSV file from Kaggle and cleaning the data.  It creates embedding information for using
as pgvector database for providing a vector-store for performing similarity search for no sql queries.




