from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from langgraph.graph import MessagesState
from src.models.request import InvokeRequest
from src.agents.graph_agent import ReActAgent


router = APIRouter(
  prefix="/api/v1/search",
  tags=["books"]
)

agent = ReActAgent()

@router.get("/health")
async def health_check():
    ''' For service healthcheck '''
    item = JSONResponse(content={"status": "healthy"}, 
                        status_code=status.HTTP_200_OK, 
                        media_type="application/json")
    return item

@router.post("/invoke")
async def invoke_agent(request: InvokeRequest):
    # Initialize state with the input message
    #initial_state = AgentState(messages=request.input_message)
    print("This is init_state:", request.input_message)
    # Configure the graph for execution.
    # If a thread_id is provided, it can be used for persistent state across calls.
    config = {}
    if request.thread_id:
        config["configurable"] = {"thread_id": request.thread_id}

    # Invoke the LangGraph workflow
    # The output will be the final state after the graph execution
    # final_state = await app_graph.ainvoke(initial_state, config=config)
    # return {"response": final_state}
    async for step in agent.astream(
        {"messages": [{"role": "user", "content": request.input_message}]},
        stream_mode="values",
    ):
        return step["messages"][-1].pretty_print()

@router.get("/")
async def root():
  return {"message": "LangGraph FastAPI Example"}