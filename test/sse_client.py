import asyncio

from langchain import hub
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

from langchain_openai import ChatOpenAI
from mcp import ClientSession
from mcp.client.sse import sse_client
from mcp.client.streamable_http import streamablehttp_client
from langchain_mcp_adapters.tools import load_mcp_tools

llm=ChatOpenAI( model_name="qwen3:8b",
            base_url="http://localhost:11434/v1",  # Ollama API 地址
            api_key="ollama",  # Ollama 默认无需真实 API Key，填任意值即可
            temperature=0)
async def run():
    client=sse_client('http://127.0.0.1:8003/sse')
    async with client as (read,write):
        async with ClientSession(read,write) as session:
            await session.initialize()

            tools=await load_mcp_tools(session)
            # langgraph.prebuilt 模块 基于图结构，支持中断、恢复、多步执行等高级功能
            agent=create_react_agent(llm, tools)
            agent_response=await agent.ainvoke({"messages": [HumanMessage(content="北京天气如何")]})
            print(agent_response)
def test_run():
    asyncio.run(run())