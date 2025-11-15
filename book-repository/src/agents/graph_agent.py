''' react_agent.py '''
import os
import asyncio
from typing import Literal
from dotenv import load_dotenv
from langgraph.prebuilt import ToolNode
from langgraph.graph import MessagesState, StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.tools import StructuredTool
from langchain_core.messages import ToolMessage, AIMessage
#from IPython.display import Image, display
from sqlalchemy import text
from src.postgres.pg_client import PgClient



class ReActAgent:
    generate_query_system_prompt = """
        You are an agent designed to interact with a SQL database.
        Given an input question, create a syntactically correct {dialect} query to run,
        then look at the results of the query and return the answer. Unless the user
        specifies a specific number of examples they wish to obtain, always limit your
        query to at most {top_k} results.

        You can order the results by a relevant column to return the most interesting
        examples in the database. Never query for all the columns from a specific table,
        only ask for the relevant columns given the question.

        DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.
        """.format(
            dialect="sql",
            top_k=5,
        )
    
    check_query_system_prompt = """
        You are a SQL expert with a strong attention to detail.
        Double check the {dialect} query for common mistakes, including:
        - Using NOT IN with NULL values
        - Using UNION when UNION ALL should have been used
        - Using BETWEEN for exclusive ranges
        - Data type mismatch in predicates
        - Properly quoting identifiers
        - Using the correct number of arguments for functions
        - Casting to the correct data type
        - Using the proper columns for joins

        If there are any of the above mistakes, rewrite the query. If there are no mistakes,
        just reproduce the original query.

        You will call the appropriate tool to execute the query after running this check.
        """.format(dialect="sql")
    
    def __init__(self, llm):
        self.llm = llm
        #memory = MemorySaver()
        # Build the tools for graph to use
        self.table_tool = StructuredTool.from_function(
            name='get_table_name',
            func= self.get_table_name,
            description="Useful for finding the name of table in database."
        )
        self.schema_tool = StructuredTool.from_function(
            name='get_table_schema',
            func= self.get_table_schema,
            description="Useful for finding the name of the table columns."
        )
        self.query_tool = StructuredTool.from_function(
            name='execute_sql_query',
            func=self.execute_sql_query,
            coroutine=self.execute_sql_query,
            description="Sends Sql query to database for execution"
        )
        self.tools = [self.table_tool, self.schema_tool, self.query_tool]
        get_schema_node_tool = ToolNode([self.schema_tool], name="get_schema")
        run_query_node_tool = ToolNode([self.query_tool], name="run_query")

        # Build the graph for querying the database
        builder = StateGraph(MessagesState)
        builder.add_node(self.get_table)
        builder.add_node(self.call_get_schema)
        builder.add_node(get_schema_node_tool, "get_schema")
        builder.add_node(self.generate_query)
        builder.add_node(self.check_query)
        builder.add_node(run_query_node_tool, "run_query")

        builder.add_edge(START, "get_table")
        builder.add_edge("get_table", "call_get_schema")
        builder.add_edge("call_get_schema", "get_schema")
        builder.add_edge("get_schema", "generate_query")
        builder.add_conditional_edges(
            "generate_query",
            self.should_continue,
        )
        builder.add_edge("check_query", "run_query")
        builder.add_edge("run_query", "generate_query")
        self.agent = builder.compile()
        

    def call_get_schema(self, state: MessagesState):
        ''' Get table columns names '''
        print("====> get schemas")
        get_schema_tool = next(tool for tool in self.tools if tool.name == "get_table_schema")
        llm_with_tools = self.llm.bind_tools([get_schema_tool])
        response = llm_with_tools.invoke(state["messages"])
        return {"messages": [response]}
    
    def get_table(self, state: MessagesState):
        ''' Get table name'''
        print("====> Call table tool returns name")
        tool_call = {
            "name": "get_table_name",
            "args": {"name": "books"},
            "id": "call_id_abc123"
        }
        tool_call_message = AIMessage(content="", tool_calls=[tool_call])
        list_tables_tool = next(tool for tool in self.tools if tool.name == "get_table_name")
        tool_message = list_tables_tool.invoke(tool_call)
        response = AIMessage(f"Available tables: {tool_message.content}")
        return {"messages": [tool_call_message, tool_message, response]}
        
    async def generate_query(self, state: MessagesState):
        system_message = {
            "role": "system",
            "content": self.generate_query_system_prompt,
        }
        llm_with_tools = self.llm.bind_tools([self.query_tool])
        response = await llm_with_tools.ainvoke([system_message] + state["messages"])
        return {"messages": [response]}
    
    async def check_query(self, state: MessagesState):
        system_message = {
            "role": "system",
            "content": self.check_query_system_prompt,
        }
        # Generate an artificial user message to check
        tool_call = state["messages"][-1].tool_calls[0]
        user_message = {"role": "user", "content": tool_call["args"]["query"]}
        llm_with_tools = self.llm.bind_tools([self.query_tool])
        response = await llm_with_tools.ainvoke([system_message, user_message])
        response.id = state["messages"][-1].id
        return {"messages": [response]}
    
    def should_continue(self, state: MessagesState) -> Literal[END, "check_query"]:
        messages = state["messages"]
        last_message = messages[-1]
        if not last_message.tool_calls:
            return END
        else:
            return "check_query"
        
    def get_table_name(self, name: str) -> str:
        """ Returns the table name """
        print(f" ====> Get table name tool {name}")
        toolmsg = ToolMessage(content='[{"name":"bdf_bookstore"}]', tool_call_id="call_id_abc123")
        return toolmsg

    def get_table_schema(self) -> list:
        """ Get the table schema """
        print(" ====> Get table schema tool")
        schemas = PgClient().get_table_schema()
        return schemas

    async def execute_sql_query(self, query: str) -> str:
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
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        api_key=os.getenv("OPENAI_LLM_API_KEY"),
        temperature=0,  # Adjust temperature for desired creativity/determinism
        max_tokens=100,  # Limit the response length if needed
        timeout=30,       # Set a timeout for the API call
    )
    question = "get the number of books of category fiction."
    agent = ReActAgent(llm).agent
    async for step in agent.astream(
        {"messages": [{"role": "user", "content": question}]},
        stream_mode="values",
    ):
        step["messages"][-1].pretty_print()

    #display(Image(agent.get_graph().draw_mermaid_png()))

# Example Usage
if __name__ == "__main__":
    load_dotenv()
    asyncio.run(async_main())