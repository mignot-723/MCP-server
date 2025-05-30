# Mock implementation of MCPServer base class
class MCPServer:
    def __init__(self, host='0.0.0.0', port=8080):
        self.host = host
        self.port = port

    def start(self):
        print(f"MCP Server running on {self.host}:{self.port}")
        # Here would be the server loop handling requests

    def invoke_method(self, method, params):
        # This method should be overridden by subclasses
        raise NotImplementedError("invoke_method must be implemented by subclass")


# Mock implementation of TaskAPI with necessary methods
class TaskAPI:
    def create_task(self, params):
        # Simulate task creation logic
        return {"status": "success", "task_id": 123, "details": params}

    def get_task(self, task_id):
        # Simulate task retrieval logic
        return {"task_id": task_id, "title": "Example Task", "status": "open"}


# MCP Server wrapping the TaskAPI
class TaskMCPServer(MCPServer):
    def __init__(self, host='0.0.0.0', port=8080):
        super().__init__(host, port)
        self.task_api = TaskAPI()

    def invoke_method(self, method, params):
        if method == "create_task":
            return self.task_api.create_task(params)
        elif method == "get_task":
            task_id = params.get("task_id")
            return self.task_api.get_task(task_id)
        else:
            raise NotImplementedError(f"Method {method} not implemented")


# Run the server if this file is executed directly
if __name__ == "__main__":
    server = TaskMCPServer()
    server.start()
