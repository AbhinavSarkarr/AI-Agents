#this is an MCP client to be used with the accounts MCP server

import mcp
from mcp.client.stdio import stdio_client
from mcp import StdioServerParameters
from agents import FunctionTool
import json

params = StdioServerParameters(command="uv", args=["run", "accounts_server.py"], env=None)
#above here we specified the parameteres to be used to run the accounts MCP server

#this could be something configurable, we can make a sort of generic MCP client that takes this configurstion and then spawns a MCP server

async def list_accounts_tools():
    #this is the fucntion to list all the tools, which now the SDK as inbuilt when we create the context manager
    async with stdio_client(params) as streams:
        #context manager to create a session
        async with mcp.ClientSession(*streams) as session:
            #initialized the session
            await session.initialize()
            tools_result = await session.list_tools()
            return tools_result.tools
        
async def call_accounts_tool(tool_name, tool_args):
    async with stdio_client(params) as streams:
        async with mcp.ClientSession(*streams) as session:
            await session.initialize()
            result = await session.call_tool(tool_name, tool_args)
            return result
            
async def read_accounts_resource(name):
    async with stdio_client(params) as streams:
        async with mcp.ClientSession(*streams) as session:
            await session.initialize()
            result = await session.read_resource(f"accounts://accounts_server/{name}")
            return result.contents[0].text
        
async def read_strategy_resource(name):
    async with stdio_client(params) as streams:
        async with mcp.ClientSession(*streams) as session:
            await session.initialize()
            result = await session.read_resource(f"accounts://strategy/{name}")
            return result.contents[0].text

#now the descriptions which used to be probvided by the MCP about a tool used to have a slight difference from the JSON which openai uses

#this function converts all the MCP jsons to the OpenAI jsons 
#all this needs not to be done now 
async def get_accounts_tools_openai():
    openai_tools = []
    for tool in await list_accounts_tools():
        schema = {**tool.inputSchema, "additionalProperties": False}
        openai_tool = FunctionTool(
            name=tool.name,
            description=tool.description,
            params_json_schema=schema,
            on_invoke_tool=lambda ctx, args, toolname=tool.name: call_accounts_tool(toolname, json.loads(args))
                
        )
        openai_tools.append(openai_tool)
    return openai_tools