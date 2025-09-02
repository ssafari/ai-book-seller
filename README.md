# Book Seller Automation

## Summary

Simulating a cloud based online book selling market with an agentic AI as customer service for sales and support. Running codes locally using docker images and docker desktop. For AI programming using local Ollama models. For messaging using Confluent Kafka running locally using Docker Desktop. For datastorage using MongoDB locally as well.

### Guideline

In this simulation following techniques will be used:
- microservice design using Python FastAPI.
- Event-driven architecure using Kafka messaging.
- Database storage using MongoDB.
- LLM and Agentic AI for handling sales and orders.

Book selling tasks are devided into these service:

- book-repository
- book-order
- book-shipping
- crew-agents
- data-pipline

This project is under development...

#### book-repository service

Handling book database operations. Connecting to a MongoDB 

