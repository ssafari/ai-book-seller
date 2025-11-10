''' book_store.py '''
import asyncio
import pandas as pd
import numpy as np
import kagglehub
from sqlalchemy.ext.asyncio import AsyncEngine
from pgvector.sqlalchemy import Vector
from langchain_postgres import PGVectorStore, PGEngine, Column
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
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")

    def __load_dataset_local(self, path: str, docname: str) -> pd.DataFrame:
        ''' Load dataset from local direcotry'''
        df = pd.read_csv(path + docname)
        print("dataset shape:", df.shape)
        return df

    def __load_dataset_kaggle(self, dataset: str, doc: str) -> pd.DataFrame:
        ''' For dataset needs to be loaded from Kaggle website'''
        path = kagglehub.dataset_download(dataset)
        print("Path to dataset files:", path)
        df = pd.read_csv(path + doc, encoding='latin1')
        print("dataset shape:", df.shape)
        df.drop(['isbn10', 
                 'subtitle', 
                 'thumbnail', 
                 'published_year',	
                 'num_pages',	
                 'ratings_count'],
            axis=1,
            inplace=True
        )
        df.rename(columns={'isbn13': 'isbn', 
                           'authors': 'author', 
                           'categories': 'genre', 
                           'average_rating': 'rating'}, 
                           inplace=True)
        df = df.dropna(subset=['author', 'genre', 'description'])
        print(f"final dataframe shape: {df.shape}")
        df["meta_data"] = df.apply(lambda row: {
            "title": row["title"],
            "author": row["author"],
            "genre": row["genre"],
            "description": row["description"]
        }, axis = 1)
        df['meta_data'] = df['meta_data'].apply(str)
        self.__chunk_data(df, 1000)
        return df

    def __chunk_data(self, df, chunk_size):
        ''' Create multiple CSV files '''
        num_chunks = int(np.ceil(len(df) / chunk_size))
        chunks = np.array_split(df, num_chunks)
        cnt = 0
        for idx, chunk in enumerate(chunks):
            file_name = f'csv/df_chunk_{idx}.csv'
            chunk.to_csv(file_name, index=False)
            cnt += 1
        print(f"DataFrame successfully chunked into {cnt} CSV files.")

    def create_embeddings(self, row):
        ''' start create embeddings of the text '''
        combined_text = f'''{row["title"]} {row["author"]}
                        {row["genre"]} {row["description"]}'''
        return self.__get_document_embeddings(combined_text)

    async def __store_dataframe(self, table_name:str, engine: AsyncEngine, df: pd.DataFrame):
        ''' 
        Define the data type mapping for the 'embedding' column
        Store processed clean dataset to database 
        '''
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
            #conn.aclose()
        print("\n --- Completed inserting of dataframe ---")

    def read_table_to_dataframe(self, table_name, engine):
        '''Verify the table creation by reading it back into a DataFrame '''
        df_from_sql = pd.read_sql_table(table_name, con=engine)
        print(f"\nData read from SQL table: '{table_name}'")
        print(df_from_sql.shape())

    def __get_document_embeddings(self, doc: str):
        ''' Helper function: get embeddings for a text '''
        document_vectors = self.embeddings.embed_documents(doc.replace('\n',''))
        return document_vectors[0]
        
    async def __create_pg_vectorestore(self, engine: PGEngine):
        ''' 
        This will create a vector store from an existing
        SQL table. It appends embeddings into allocated
        vector embedding column.
        '''
        print("Get vectorstore embeddings")
        vector_store = await PGVectorStore.create(
            engine=engine,
            table_name=self.table_name,               #"your_existing_table",
            id_column="isbn",
            content_column="description",            # Column with text content
            embedding_column="embedding",        # Column to store embeddings
            embedding_service=self.embeddings,
            metadata_columns=["title", "author", "genre", "description"]
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

    async def save(self, path:str, doc:str):
        #self.__load_dataset_kaggle('dylanjcastillo/7k-books-with-metadata', '/books.csv')
        df_books = self.__load_dataset_local(path,doc)
        pgclient = PgClient()
        await self.__store_dataframe(pgclient.TABLE_NAME, pgclient.engine, df_books)


    async def search(self, query='a children story'):
        pgclient = PgClient()
        v_store = await self.__create_pg_vectorestore(pgclient.pg_engine)
        print("Start similarity search")
        results = await v_store.asimilarity_search(query, k=2)
        for doc in results:
            print(doc.metadata['title'])
            print(doc.page_content)


async def async_main():
    ''' main function for running async methods '''
    bookstore = BookStore('bookstore', 768)
    await bookstore.search('fiction book')
    #await bookstore.save('csv/','df_chunk_1.csv')


    # Example Usage
if __name__ == "__main__":
    asyncio.run(async_main())
