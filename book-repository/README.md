# BOOKSTORE 

It is a PostGreSQL database containing books information. Running as FastAPI server and provides
APIs for accessing database CRUD operations. 

## Bookstore Features:

### PG Client

It handles books table creation and provides async database connection for other features to use.
It creates "bdf_bookstore" table with a column reserved for saving vector database embeddings for 
similarity search.

### Repository

It buils the bookstore table by using Kaggle dataset and cleaning and processing dataset for storing 
into database. It handles meta-data creation for building vector embedding column. It provides
access to vectorstore for searching.

 
