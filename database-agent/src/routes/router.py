from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
from fastmcp import Client
from fastmcp.exceptions import ToolError
from src.models.request import InvokeRequest
from src.agents.graph_agent import ReActAgent


router = APIRouter(
  prefix="/api/v1/search",
  tags=["books-agent"]
)

@router.get("/health")
async def health_check():
    ''' For service healthcheck '''
    item = JSONResponse(content={"status": "healthy"},
                        status_code=status.HTTP_200_OK,
                        media_type="application/json")
    return item

@router.post("/invoke")
async def invoke_agent(request: InvokeRequest):
    try:
        client = Client("http://localhost:8003/mcp")
        # Configure the graph for execution.
        # If a thread_id is provided, it can be used
        # for persistent state across calls.
        config = {}
        if request.thread_id:
            config["configurable"] = {"thread_id": request.thread_id}

        # Invoke the LangGraph workflow
        result = await ReActAgent(client).agent.ainvoke({
                      "messages": [
                      {
                          "role": "user", 
                          "content": request.input_message
                      }]
                  }, config=config)
        return {"response": result["messages"][-1].content}
    except ToolError as e:
        print("ERROR calling 'divide' tool:")
        print(f"{type(e).__name__}: {e}")
        #traceback.print_exc()
    except TimeoutError:
        print("ERROR calling 'divide' tool: Call timed out.")
    except Exception as e:
        print("An unexpected error occurred during tool call:")
        print(f"{type(e).__name__}: {e}")
    raise HTTPException(status_code=503, detail="Internal Server Error")


@router.get("/")
async def root():
    return {"message": "LangGraph FastAPI Example"}