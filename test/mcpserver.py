from mcp.server import FastMCP

mcp=FastMCP("Demo",port=8003)

# Add an addition tool
@mcp.tool()
def add(a: int,b: int)->int:
    """
    Add two numbers
    """
    return a+b

@mcp.tool()
def weather(city:str)-> str:
    """
    Add two numbers
    """
    return f'{city} sunny 20度'

# Add a dynamic greeting resource# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personal greeting"""



if __name__ == '__main__':
    mcp.run(transport='sse')