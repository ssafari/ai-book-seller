''' book_store.py '''
import asyncio
import pandas as pd
import kagglehub
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine
from pgvector.sqlalchemy import Vector
from langchain_postgres import PGVectorStore, Column
from langchain_ollama import OllamaEmbeddings
from src.postgres.pg_client import PgClient


class BookStore:
    ''' It reads data from Kaggle dataset cvs file and cache 
        it as dataframe in order to prepare data for storing
        into the postgres database 
    '''
    def __init__(self, table_name: str, vsize: int):
        self.table_name = table_name
        self.vector_size = vsize

    def load_dataset_local(self, path: str, docname: str) -> pd.DataFrame:
        ''' Load dataset from local direcotry'''
        df = pd.read_csv(path + docname)
        print("dataset shape:", df.shape)
        return df

    def load_dataset_kaggle(self, dataset: str, doc: str) -> pd.DataFrame:
        ''' For dataset needs to be loaded from Kaggle website'''
        path = kagglehub.dataset_download(dataset)
        print("Path to dataset files:", path)
        df = pd.read_csv(path + doc, encoding='latin1')
        print("dataset shape:", df.shape)
        df.drop(
            ['isbn10', 'subtitle', 'thumbnail', 'published_year',	'num_pages',	'ratings_count'],
            axis=1,
            inplace=True
        )
        df.rename(columns={'isbn13': 'isbn'}, inplace=True)
        return df

    def create_metadata(self, df):
        ''' Create metadata as content creating embeddingsfor vector database'''
        df["content"] = str(df.apply(lambda row: {
            "title": row["title"],
            "authors": row["authors"],
            "categories": row["categories"],
            "description": row["description"]
        }, axis = 1))

    def create_embeddings(self, row):
        ''' start create embeddings of the text '''
        combined_text = f'''{row["title"]} {row["authors"]}
                        {row["categories"]} {row["description"]}'''
        return self.get_ollama_embeddings(combined_text)
    
    async def add_vector_column(self, engine: AsyncEngine, table_name):
        ''' call this if need to add embedding column '''
        async with engine.begin() as con:
            await con.execute(text(f"ALTER TABLE {table_name} ADD COLUMN embedding VECTOR(768);"))
            await con.commit()

    async def store_dataframe(self, table_name:str, engine: AsyncEngine, df: pd.DataFrame):
        ''' 
        Define the data type mapping for the 'embedding' column
        Store processed clean dataset to database 
        '''
        self.create_metadata(df)
        print(" --- Start adding embeddings to dataframe ---\n")
        df["embedding"] = df.apply(self.create_embeddings, axis = 1)
        print("\n --- Start inserting dataframe to the database ---")
        dtype_mapping = {
            'embedding': Vector(768)  
        }
        async with engine.begin() as conn:
            await conn.run_sync(lambda sync_conn: df.to_sql(table_name, 
                                                            sync_conn, 
                                                            if_exists='append', 
                                                            index=False, 
                                                            dtype=dtype_mapping))
        print("\n --- Completed inserting of dataframe ---")

    def read_table_to_dataframe(self, table_name, engine):
        '''Verify the table creation by reading it back into a DataFrame '''
        df_from_sql = pd.read_sql_table(table_name, con=engine)
        print(f"\nData read from SQL table: '{table_name}'")
        print(df_from_sql.shape())

    def get_ollama_embeddings(self, doc: str):
        ''' Helper function: get embeddings for a text '''
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        document_vectors = embeddings.embed_documents(doc.replace('\n',''))
        return document_vectors[0]
        
    def create_pg_vectorestore(self, engine, table_name):
        ''' 
        This will create a vector store from an existing
        SQL table. It appends embeddings into allocated
        vector embedding column.
        '''
        embeddings = OllamaEmbeddings(model="llama3.2:latest")
        vector_store = PGVectorStore.create(
            engine=engine,
            table_name=table_name,               #"your_existing_table",
            content_column="content",            # Column with text content
            embedding_column="embedding",        # Column to store embeddings
            embedding_service=embeddings,
        )
        return vector_store

    async def create_vectorestore(self, pg_engine):
        ''' 
            This langchain_postgres will create a table
            with its default columns. It's good when we
            have unstrucuted data to save into pg table
            with embedding vectore codes.
        '''
        METADATA_COLUMNS = [
            Column("author", "varchar(50)", True),
            Column("year", "integer", False)
            #{"name": "category", "type": "text"} # Alternative way to define a column
        ]
        print("Using engine create vectorestore")
        await pg_engine.ainit_vectorstore_table(
                    table_name=self.table_name,
                    vector_size=self.vector_size,
                    metadata_columns=METADATA_COLUMNS
              )
        
async def async_main():
    ''' main function for running async methods '''
    store = BookStore('books', 768)
    books = store.load_dataset_local('csv/','output_np_chunk_1.csv')
    print("\n Start PGClient ... \n")
    pgclient = PgClient()
    #await store.add_vector_column(pgclient.engine, pgclient.TABLE_NAME)
    await store.store_dataframe(pgclient.TABLE_NAME, pgclient.engine, books)


    # Example Usage
if __name__ == "__main__":
    asyncio.run(async_main())
