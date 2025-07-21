from langchain_core.messages import SystemMessage
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate

# 定义一个包含两个变量的提示模板
prompt = PromptTemplate.from_template(
    "给出一个{topic} 的广告, 它的价格是 {price} ￥，广告需要能够引起用户的兴趣")
# 格式化并传入参数
print(prompt.format(topic='冰淇淋', price=3))
# 给出一个冰淇淋的广告, 它的价格是 3 ￥，广告需要是能够引起用户兴趣的
from langchain_core.prompts import PromptTemplate
# 定义一个包含两个变量的提示模板
prompt2 = PromptTemplate.from_template("告诉我一个广告")
# 格式化并传入参数
print(prompt2.format())
# 告诉我一个广告
# invoke 调用
prompt_val = prompt.invoke({"topic": "冰淇淋", "price": "3"})
print(prompt_val)
# text='给出一个冰淇淋的广告, 它的价格是 3 ￥，广告需要是能够引起用户兴趣的'


# 制定模板
chat_prompt = ChatPromptTemplate.from_messages(
    [("system", "你是一个游戏的 npc，有三个任务让玩家完成，需要给出玩家三个任务，并且规定出完成的标准。"),
     ("human", "你好，我是这个游戏的玩家"),
     ("ai", "{user} 玩家你好，欢迎来到这个游戏"),
     ("human", "{user_input}"),
     ])
# 格式化消息列表，并且传入参数
messages = chat_prompt.format_messages(user="ling", user_input="你好，我需要做什么")
print(messages)
# [SystemMessage(content='你是一个游戏的 npc，有三个任务让玩家完成，需要给出玩家三个任务，并且规定出完成的标准。'), HumanMessage(content='你好，我是这个游戏的玩家'), AIMessage(content='ling 玩家你好，欢迎来到这个游戏'), HumanMessage(content='你好，我需要做什么')]

# 传入 SystemMessage HumanMessagePromptTemplate 实例
chat_template = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=(
            "你是一个擅长制定计划的助手"
            "计划需要贴合用户需求，给出详细的时间节点和任务指标"
        )),
        HumanMessagePromptTemplate.from_template("{user_req}")
    ]
)
messages_o = chat_template.format_messages(user_req="我想要一个旅行计划")
print(messages_o)
# [SystemMessage(content='你是一个擅长制定计划的助手计划需要贴合用户需求，给出详细的时间节点和任务指标'), HumanMessage(content='我想要一个旅行计划')]
# 使用 invoke 方式调用
chat_val = chat_prompt.invoke({"user": "ling", "user_input": "你好，我需要做什么"})
print(chat_val)
# messages=[SystemMessage(content='你是一个游戏的 npc，有三个任务让玩家完成，需要给出玩家三个任务，并且规定出完成的标准。'), HumanMessage(content='你好，我是这个游戏的玩家'), AIMessage(content='ling 玩家你好，欢迎来到这个游戏'), HumanMessage(content='你好，我需要做什么')]
# 转换为消息列表
chat_val_mes = chat_val.to_messages()
print(chat_val_mes)
# [SystemMessage(content='你是一个游戏的 npc，有三个任务让玩家完成，需要给出玩家三个任务，并且规定出完成的标准。'), HumanMessage(content='你好，我是这个游戏的玩家'), AIMessage(content='ling 玩家你好，欢迎来到这个游戏'), HumanMessage(content='你好，我需要做什么')]
