from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

# Useful if we want to pass more info to langgraph
class AgentState(TypedDict):
    messages:Annotated[list[BaseMessage], add_messages]
    # input: str
    # chat_history: list[BaseMessage]
    # intermediate_steps: Annotated[list[tuple[AgentAction, str]], operator.add]
    # output: dict[str, Union[str, List[str]]]