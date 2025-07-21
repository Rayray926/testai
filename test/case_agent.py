#  注意：需要再原提示词的基础上添加 {code} 变量
# prompt = hub.pull("hwchase17/structured-chat-agent")
from langchain import hub
from langchain.agents import create_structured_chat_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

from case_tools import tools
system='''Respond to the human as helpfully and accurately as possible. You have access to the following tools:

{tools}

Use a json blob to specify a tool by providing an action key (tool name) and an action_input key (tool input).

Valid "action" values: "Final Answer" or {tool_names}

Provide only ONE action per $JSON_BLOB, as shown:

```
{{
  "action": $TOOL_NAME,
  "action_input": $INPUT
}}
```

Follow this format:

Question: input question to answer
Thought: consider previous and subsequent steps
Action:
```
$JSON_BLOB
```
Observation: action result
... (repeat Thought/Action/Observation N times)
Thought: I know what to respond
Action:
```
{{
  "action": "Final Answer",
  "action_input": "Final response to human"
}}

Begin! Reminder to ALWAYS respond with a valid json blob of a single action. Use tools if necessary. Respond directly if appropriate. Format is Action:```$JSON_BLOB```then Observation

'''
human='''{input}
{code}
{agent_scratchpad}
 (reminder to respond in a JSON blob no matter what)'''
# prompt = hub.pull("hwchase17/structured-chat-agent")
prompt=ChatPromptTemplate.from_messages([('system',system),MessagesPlaceholder("chat_history",optional=True),('human',human)])
llm=ChatOpenAI( model_name="gemma3n:e4b",
            base_url="http://localhost:11434/v1",  # Ollama API 地址
            api_key="ollama",  # Ollama 默认无需真实 API Key，填任意值即可
            temperature=0)

agent1 = create_structured_chat_agent(llm, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent1, tools=tools,
    verbose=True,
    return_intermediate_steps=True,
    handle_parsing_errors=True)

if __name__ == '__main__':
    # agent_executor.invoke({"input": "请根据以上源码生成文件", "code": """def test_demo(): return True"""})
    agent_executor.invoke({"input": """
                    
                  请根据以下步骤完成我让你完成操作，没有完成所有步骤不能停止:
                    1. 先根据以上源码生成文件。
                    2. 根据上一步生成的源码文件，进行执行测试用例操作，并返回终的执行结果
                   ""","code": """def test_demo(): return True"""})