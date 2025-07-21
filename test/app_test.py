import json

from langchain import hub
from langchain.agents import create_structured_chat_agent, AgentExecutor
from langchain.globals import set_debug
from langchain_core.agents import AgentAction
from langchain_openai import ChatOpenAI

from AppAutoFrameworkTools import tools

set_debug(True)

#从 LangChain 的 hub 中拉取一个预定义的聊天代理提示模板
prompt = hub.pull("hwchase17/structured-chat-agent")
llm=ChatOpenAI( model_name="deepseek-r1:7b",
            base_url="http://localhost:11434/v1",  # Ollama API 地址
            api_key="ollama",  # Ollama 默认无需真实 API Key，填任意值即可
            temperature=0)

# 结构化聊天代理（Structured Chat Agent），其作用是将 LLM 与工具结合，使代理能够根据用户的输入决定调用哪个工具并处理响应
app_agent = create_structured_chat_agent(llm, tools, prompt)
#用于执行由代理生成的动作。它的主要职责是运行代理、调用工具，并返回结果
app_agent_executor = AgentExecutor(
    agent=app_agent, tools=tools,
    verbose=True,
    return_intermediate_steps=True,
    handle_parsing_errors=True)
query = """
你是一个自动化测试工程师，请根据以下步骤执行测试用例，
每一步如果定位都是根据上一步的返回的html操作完成
执行对应的测试用例，测试步骤如下
1.  打开  app activity ".Settings" , app package "com.android.settings"
2. 点击 Battery
3. 获取 Battery 的电量之后返回上一级页面
"""

def execute_result(_):
    # 获取执行结果
    r = app_agent_executor.invoke({"input": query})
    # 获取执行记录
    steps = r["intermediate_steps"]
    steps_info = []
    # 遍历执行步骤，获取每一步的执行步骤以及输入的信息。
    for step in steps:
        action = step[0]
        if isinstance(action, AgentAction):
            steps_info.append({'tool': action.tool, 'input': action.tool_input})
    return json.dumps(steps_info)
if __name__ == '__main__':
    print(execute_result(""))