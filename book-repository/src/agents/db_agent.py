'''  DbAgent.py '''
import asyncio
from sqlalchemy import text
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_classic.agents import create_react_agent, AgentExecutor
from src.agents.db_prompt import get_dialect_prompt
from src.postgres.pg_client import PgClient

class DbAgent:
    ''' An agent load a csv file and create embeddings '''

    prompt = PromptTemplate.from_template("""
        You are a helpful AI assistant that can answer questions about a SQL database of
        booksore table storing books information. You will help users to find the books 
        or information about the bookstore.                               
        You have access to the following tools: {tools}

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
        ''' Initialize your LLM (e.g., OpenAI)'''
        self.llm = ChatOllama(model="llama3.2:latest")
        self.toolkit = [get_table_names_async, execute_sql_query_async]

        for toolk in self.toolkit:
            print(f"{toolk.name}: {toolk.description}\n")

        self.react_agent = create_react_agent(
            llm=self.llm,
            tools=self.toolkit,
            prompt=self.prompt
        )
        self.agent_executor = AgentExecutor(agent=self.react_agent, tools=self.toolkit, verbose=True)


    async def execute(self, query):
        ''' Create the SQL Agent '''
        response = await self.agent_executor.ainvoke({"input": {query}})
        print(f" ===> Agent response: {response['output']}")

    def create(self):
        ''' This is another way to create SQL agent using ReAct agent libraries '''
        agent = create_agent(
            self.llm,
            self.toolkit,
            system_prompt=get_dialect_prompt,
        )

@tool
async def get_table_names_async() -> list[str]:
    """Returns a list of all table names in the database."""
    async_session = await PgClient().async_session()
    async with async_session() as session:
        # Implement your async logic to fetch table names
        #inspect(async_engine).get_table_names()
        return ["bookstore"]

@tool
async def execute_sql_query_async(query: str) -> str:
    """Executes a SQL query and returns the results."""
    #print(f"SQL query: {query}")
    async_session = await PgClient().async_session()
    async with async_session() as session:
        try:
            result = await session.execute(text(query))
            # Process result as needed, e.g., fetch all rows
            return str(result.fetchall()) # Replace with appropriate result handling
        except Exception as e:
            return f"Error executing query: {e}"
            
async def async_main() -> None:
    agent = DbAgent()
    await agent.execute("how many books of genre Fiction do we have?")

# Example Usage
if __name__ == "__main__":
    asyncio.run(async_main())