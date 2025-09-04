# Book Seller Automation

## Summary

Simulating a cloud based online book selling market with an agentic AI as customer service for sales and support. Services run locally using docker images and docker desktop. 
For our LLM we use local Ollama models. For messaging we use Confluent Kafka running locally using Docker Desktop. For datastorage using MongoDB locally as well.

### Guideline

In this simulation following techniques will be used:
- microservice design using Python FastAPI.
- Event-driven architecure using Kafka messaging.
- Database storage using MongoDB.
- LLM and Agentic AI for handling sales and orders.

I want to use multiple ai agents as customer service. One agent will help the customer to find and to buy books. Another agent will take care of payment and send the order to a Kakfa network. Another agent will use KG (Neo4j) to make suggestion to customer finding similar book or from same author.  We need a service to extract data
from web and save them into database. Gradually this guideline will be updated with project progress.

Book selling tasks are devided into these service:

- **book-repository**
- **book-order**
- **book-shipping**
- **crew-agents**
- **data-pipline**

This project is under development...

### book-repository service

Handling book database operations. Connecting to a MongoDB and saving books information, kind of books inventory.
(in progress...)

### book-order

A kafka producer service when the customer payment is cleared.
(in progress...)

### book-shipping

TODO: A kafka listener will read the order and contact inventory to ship the book.

### crew-agents

TODO: AI agents for customer service

### data-pipeline

TODO: Searching web for finding books. 


