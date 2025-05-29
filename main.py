# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
# Mock implementation of MCPServer base class
 #class MCPServer:
#def __init__(self, host='0.0.0.0', port=8080):
        #self.host = host
        #self.port =

    #def start(self):
       # print(f"MCP Server running on {self.host}:{self.port}")
        # Here would be the server loop handling requests

    #def invoke_method(self, method, params):
        # This method should be overridden by subclasses
        #raise NotImplementedError("invoke_method must be implemented by subclass")


# Mock implementation of TaskAPI with necessary methods
#class TaskAPI:
    #def create_task(self, params):
        # Simulate task creation logic
        #return {"status": "success", "task_id": 123, "details": params}

    #def get_task(self, task_id):
        # Simulate task retrieval logic
        #return {"task_id": task_id, "title": "Example Task", "status": "open"}


# MCP Server wrapping the TaskAPI
#class TaskMCPServer(MCPServer):
    #def __init__(self, host='0.0.0.0', port=8080):
        #super().__init__(host, port)
        #self.task_api = TaskAPI()

    #def invoke_method(self, method, params):
        #if method == "create_task":
            #return self.task_api.create_task(params)
        #elif method == "get_task":
            #task_id = params.get("task_id")
            #return self.task_api.get_task(task_id)
        #else:
            #raise NotImplementedError(f"Method {method} not implemented")


# Run the server if this file is executed directly
#if __name__ == "__main__":
    #server = TaskMCPServer()
    #server.start()

from fastapi import FastAPI, HTTPException
import httpx
from pydantic import BaseModel
from typing import Dict

#app = FastAPI()

#MCP_SERVER_MAP = {
    #"github": "http://localhost:8000/mcp",
    #"filesystem": "http://localhost:8010/mcp"
#}


#class MCPRequest(BaseModel):
    #method: str
    #params: Dict


#@app.post("/github/invoke_method")
#async def proxy_request(target: str, request: MCPRequest):
    #if target not in MCP_SERVER_MAP:
        #raise HTTPException(404, detail="Unknown MCP target")
    #async with httpx.AsyncClient() as client:
        #try:
            #response = await client.post(
                #f"{MCP_SERVER_MAP[target]}/invoke_method",
                #json=request.dict(),
                #timeout=30.0
            #)
            #return response.json()
        #except httpx.ConnectError:
            #raise HTTPException(502, detail="Backend server unreachable")


#@app.get("/aggregate_methods")
#async def aggregate_methods():
    #methods = {}
    #async with httpx.AsyncClient() as client:
        #for target, url in MCP_SERVER_MAP.items():
            #try:
                #response = await client.get(f"{url}/get_methods")
                #methods[target] = response.json()
            #except Exception:
                #continue
    #return {"methods": methods}
#from fastapi import FastAPI
#from fastapi_mcp import FastApiMCP

from fastapi import FastAPI, HTTPException
import httpx
from pydantic import BaseModel
from typing import Dict, Any

app = FastAPI()

MCP_SERVER_MAP = {
    "github": "http://localhost:8000/mcp",
    "filesystem": "http://localhost:8010/mcp"
}

class MCPRequest(BaseModel):
    method: str
    params: Dict[str, Any]

@app.post("/{target}/invoke_method")
async def proxy_invoke_method(target: str, request: MCPRequest):
    if target not in MCP_SERVER_MAP:
        raise HTTPException(404, detail=f"Unknown MCP target: {target}")
    backend_url = f"{MCP_SERVER_MAP[target]}/invoke_method"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(backend_url, json=request.dict(), timeout=30)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(502, detail=f"Backend connection error: {str(e)}")
        except httpx.HTTPStatusError as e:
            raise HTTPException(e.response.status_code, detail=f"Backend error: {e.response.text}")

@app.get("/aggregate_methods")
async def aggregate_methods():
    aggregated = {}
    async with httpx.AsyncClient() as client:
        for target, base_url in MCP_SERVER_MAP.items():
            try:
                resp = await client.get(f"{base_url}/get_methods", timeout=10)
                resp.raise_for_status()
                aggregated[target] = resp.json()
            except Exception:
                aggregated[target] = {"error": "Failed to fetch methods"}
    return {"methods": aggregated}
