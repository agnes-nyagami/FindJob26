from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters
import os

mcp_server_adapter = MCPServerAdapter(server_params)

def start_mcp_adapter():
    try:
        mcp_server_adapter.start()
        print("MCP Server Adapter started successfully.")
    except Exception as e:
        print(f"Failed to start MCP Server Adapter: {e}")

def stop_mcp_adapter():
    if mcp_server_adapter and getattr(mcp_server_adapter, 'is_running', False):
        print("Stopping MCP Server Adapter...")
        mcp_server_adapter.stop()
    elif mcp_server_adapter:
        print("MCP Server Adapter is not running.")
        
server_params=StdioServerParameters(
    command="python", 
    args=["Data/database_mcpserver.py"],
    env={**os.environ},
)

with MCPServerAdapter(server_params) as sponsorship_mcp:
    print(f"Available tools from Stdio MCP server: {[tool.name for tool in sponsorship_mcp]}")


server_par=StdioServerParameters(
    command="python", 
    args=["C:/Users/alems/job26/job_mcp.py"],
    env={**os.environ},
)

with MCPServerAdapter(server_par) as job_mcp:
    print(f"Available tools from Stdio MCP server: {[tool.name for tool in job_mcp]}")
