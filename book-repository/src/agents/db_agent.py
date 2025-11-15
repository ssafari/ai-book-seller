'''  DbAgent.py '''
import os
import asyncio
from dotenv import load_dotenv
from sqlalchemy import text
from langchain.tools import tool
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_classic import hub
from langchain_classic.agents import create_react_agent, AgentExecutor
from src.postgres.pg_client import PgClient
from src.repository.book_store import BookStore


load_dotenv()

class DbAgent:
    ''' An agent load a csv file and create embeddings '''

    prompt = PromptTemplate.from_template("""
        You are a helpful AI assistant that can answer questions about a SQL database.
        Given an input question, find the table and create a syntactically correct PostgreSQL query to run by
        using provided tools.
                                          
        you have access to the following tools: {tools}

        Use the following format:

        Question: the input question you must answer
        Thought: you should always think about what to do
        Action: the action to take, should be one of [{tool_names}]
        Action Input: the input to the action
        Observation: the result of the action
        ... (this Thought/Action/Action Input/Observation can repeat N times)
        Thought: I now know the final answer
        Final Answer: the final answer to the original input question

        Begin!

        Question: {input}
        Thought: {agent_scratchpad}
        """
    )

    def __init__(self):
        ''' Initialize your LLM either using local Ollama or OpenAI '''
        self.llm = ChatOllama(model="mistral:latest")

        # self.llm = ChatOpenAI(
        #     model="gpt-3.5-turbo",
        #     api_key=os.getenv("OPENAI_LLM_API_KEY"),
        #     temperature=0,  # Adjust temperature for desired creativity/determinism
        #     max_tokens=100,  # Limit the response length if needed
        #     timeout=30,       # Set a timeout for the API call
        # )

        self.toolkit = [get_table_name, get_table_schema, execute_sql_query]

        for toolk in self.toolkit:
            print(f"{toolk.name}: {toolk.description}\n")

        self.react_agent = create_react_agent(
            llm=self.llm,
            tools=self.toolkit,
            prompt=self.prompt
        )
        self.agent_executor = AgentExecutor(
            agent=self.react_agent, 
            tools=self.toolkit, 
            handle_parsing_errors=True,
            verbose=True
        )


    async def execute(self, query):
        ''' Invoke the SQL Agent '''
        response = await self.agent_executor.ainvoke({"input": {query}})
        print(f" ===> Agent response: {response['output']}")

    # def create(self):
    #     ''' This is another way to create SQL agent using ReAct agent libraries '''
    #     agent = create_agent(
    #         self.llm,
    #         self.toolkit,
    #         system_prompt=get_dialect_prompt,
    #     )

@tool
def get_table_name(name: str) -> str:
    """ Get the table name """
    # async_session = await PgClient().async_session()
    # async with async_session().begin() as conn:
        #inspect(async_engine).get_table_names()
    return "bdf_bookstore"

@tool
def get_table_schema(name: str) -> list:
    """ Get the table schema """
    return PgClient().get_table_schema()

@tool
async def execute_sql_query(query: str) -> str:
    """Executes a SQL query and returns the results."""
    async with PgClient().async_session() as session:
        try:
            result = await session.execute(text(query))
            # Process result as needed, e.g., fetch all rows
            return str(result.scalars().all())
        except Exception as e:
            return f"Error executing query: {e}"
            
async def async_main() -> None:
    ''' Just for testing functionality of the Agent'''
    agent = DbAgent()
    await agent.execute("how many fiction books do we have?")
    #bookstore = BookStore('bdf_bookstore', 768)
    #await bookstore.search("List of titles written by author 'Agatha Christie'.")

# Example Usage
if __name__ == "__main__":
    asyncio.run(async_main())