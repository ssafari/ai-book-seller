'''  DbAgent.py '''
from langchain.agents import create_agent
from langchain_classic.agents import AgentType
from langchain_community.agent_toolkits import SQLDatabaseToolkit, create_sql_agent
from langchain_community.chat_models import ChatOllama

class DbAgent:
    ''' An agent load a csv file and create embeddings '''

    def __init__(self, pgsql):
        ''' Initialize your LLM (e.g., OpenAI)'''
        self.llm = OpenAI(temperature=0, openai_api_key="YOUR_OPENAI_API_KEY")
        self.toolkit = SQLDatabaseToolkit(db=pgsql, llm=self.llm)
        for tool in self.toolkit.get_tools():
            print(f"{tool.name}: {tool.description}\n")

    def execute(self, query):
        ''' Create the SQL Agent '''
        agent_executor = create_sql_agent(
            llm=self.llm,
            toolkit=self.toolkit,
            verbose=True,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        )
        question = "List the names of all employees."
        agent_executor.run(question)

    def create(self):
        ''' This is another way to create SQL agent using ReAct agent libraries '''
        agent = create_agent(
            self.llm,
            self.toolkit.get_tools(),
            system_prompt=system_prompt,
        )



# Example Usage
if __name__ == "__main__":
    