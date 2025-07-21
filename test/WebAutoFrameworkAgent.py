from langchain import hub
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

from WebAutoFramework import WebAutoFramework

web = WebAutoFramework()

@tool
def open(url):
    """
    打开一个网页
    """
    web.open(url)
@tool
def quit_web():
    """
    退出浏览器
    """
    web.quit()
@tool
def get_title():
    """
    获取网页标题
    :return:
    """
    print(web.get_title())


tools = [open, quit_web, get_title]

#从 LangChain Hub 中拉取一个预定义的 Prompt 模板，该模板名为 hwchase17/openai-functions-agent，适用于支持 OpenAI 函数调用（Function Calling）的智能体（Agent）
prompt = hub.pull("hwchase17/openai-functions-agent")

llm  = ChatOpenAI(
    model_name="llama3:8b",
    base_url="http://localhost:11434/v1",  # Ollama API 地址
    api_key="ollama"  # Ollama 默认无需真实 API Key，填任意值即可
)

agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent,
                               tools=tools, verbose=True,
                               return_intermediate_steps =True
                               ,handle_parsing_errors=True)


if __name__ == '__main__':
    agent_executor.invoke({"input": """
                           请打开 https://baidu.com/ 网站
                        返回当前的网页的标题，再退出浏览器。"""})